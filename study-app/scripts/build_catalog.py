#!/usr/bin/env python3
"""Gera o catálogo estático consumido pela aplicação local de estudos.

O script usa apenas a biblioteca padrão. Ele trata os Markdown do repositório
como fonte da verdade, copia o conteúdo sem alterações e produz metadados
determinísticos para navegação, progresso e desbloqueio de laboratórios.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import re
import shutil
import sys
import unicodedata
from collections import deque
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import quote, unquote, urlsplit

SCHEMA_VERSION = 2
WORDS_PER_MINUTE = 200
STUDY_MANIFEST = "STUDY-CONTENT.json"
GENERATED_MARKER = ".study-catalog-generated"
MARKER_CONTENT = "redteam-essentials-study-catalog-v1\n"
MAX_ASSET_BYTES = 2 * 1024 * 1024
MAX_TOTAL_ASSET_BYTES = 64 * 1024 * 1024
MAX_ASSET_FILES = 10_000

FORMATION_COLLECTION = "formacao-principal"
LEGACY_COLLECTION = "acervo-seguranca"
PRACTICE_COLLECTION = "laboratorios-projetos"
RESOURCE_COLLECTION = "ferramentas-codigo"
DOCUMENTATION_COLLECTION = "documentacao-global"
REQUIRED_COLLECTION_IDS = {
    FORMATION_COLLECTION,
    LEGACY_COLLECTION,
    PRACTICE_COLLECTION,
    RESOURCE_COLLECTION,
    DOCUMENTATION_COLLECTION,
}

TRACKS = (
    {
        "id": "programacao",
        "order": 0,
        "title": "Programação",
        "description": "Do primeiro algoritmo à engenharia de aplicações e APIs.",
        "first": 0,
        "last": 5,
    },
    {
        "id": "sistemas-operacionais",
        "order": 1,
        "title": "Sistemas operacionais",
        "description": "Linux, Windows e macOS do uso cotidiano à administração avançada.",
        "first": 6,
        "last": 13,
    },
    {
        "id": "redes",
        "order": 2,
        "title": "Redes",
        "description": "Fundamentos, redes domésticas, switching, roteamento e infraestrutura empresarial.",
        "first": 14,
        "last": 18,
    },
    {
        "id": "criptografia",
        "order": 3,
        "title": "Criptografia",
        "description": "Primitivas, protocolos, PKI e engenharia criptográfica aplicada.",
        "first": 19,
        "last": 22,
    },
    {
        "id": "privacidade",
        "order": 4,
        "title": "Privacidade",
        "description": "Modelos de ameaça, VPN própria e atribuição defensiva.",
        "first": 23,
        "last": 25,
    },
    {
        "id": "purple-team",
        "order": 5,
        "title": "Purple Team",
        "description": "Validação ofensiva autorizada e defesa de perímetro, aplicações e identidade.",
        "first": 26,
        "last": 26,
    },
    {
        "id": "especializacao-seguranca",
        "order": 6,
        "title": "Especialização em segurança",
        "description": "Da autoridade e engenharia de ferramentas ao capstone Purple Team integrado.",
        "first": 27,
        "last": 40,
    },
)

NUMBERED_FILE_RE = re.compile(r"^(\d{1,3})[-_].+\.md$", re.IGNORECASE)
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$")
WORD_RE = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*", re.UNICODE)
LINK_RE = re.compile(r"!?\[([^]]*)\]\([^)]+\)")
INLINE_TARGET_RE = re.compile(r"!?\[[^]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
REFERENCE_TARGET_RE = re.compile(
    r"^\s{0,3}\[[^]]+\]:\s*(?:<([^>]+)>|([^\s]+))",
    re.MULTILINE,
)
HTML_TARGET_RE = re.compile(r"\b(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
HTML_RE = re.compile(r"<[^>]+>")
LAB_DIRECTORIES = {"lab", "labs", "laboratorio", "laboratorios"}
ANSWER_DIRECTORIES = {"answer", "answers", "resposta", "respostas", "solucao", "solucoes"}
REFERENCE_STEMS = {
    "bibliografia",
    "cheatsheet",
    "fontes",
    "glossario",
    "recursos",
    "referencias",
    "references",
    "respostas",
}
TYPE_ORDER = {"overview": 0, "chapter": 1, "lab": 2, "reference": 3, "supplement": 4}
FORBIDDEN_ASSET_DIRECTORIES = {
    ".agents",
    ".aws",
    ".codex",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "generated",
    "node_modules",
    "out",
    "target",
    "venv",
}
TEXT_ASSET_EXTENSIONS = {
    ".awk",
    ".asm",
    ".bash",
    ".bat",
    ".c",
    ".cc",
    ".cfg",
    ".cjs",
    ".conf",
    ".cpp",
    ".cs",
    ".csproj",
    ".css",
    ".csv",
    ".dockerfile",
    ".env.example",
    ".fs",
    ".go",
    ".gql",
    ".graphql",
    ".h",
    ".hpp",
    ".htm",
    ".html",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsonl",
    ".jsx",
    ".kt",
    ".kts",
    ".lock",
    ".markdown",
    ".md",
    ".mobileconfig",
    ".mjs",
    ".properties",
    ".proto",
    ".ps1",
    ".psd1",
    ".psm1",
    ".py",
    ".pyi",
    ".rb",
    ".rs",
    ".rst",
    ".scala",
    ".scss",
    ".service",
    ".sh",
    ".sql",
    ".timer",
    ".toml",
    ".ts",
    ".tsv",
    ".tsx",
    ".txt",
    ".xml",
    ".xsd",
    ".yaml",
    ".yml",
    ".zsh",
}
IMAGE_ASSET_EXTENSIONS = {".avif", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
SAFE_EXTENSIONLESS_NAMES = {
    ".dockerignore",
    ".editorconfig",
    ".gitignore",
    "cmakelists.txt",
    "dockerfile",
    "makefile",
}

LANGUAGE_BY_SUFFIX = {
    ".asm": "assembly",
    ".awk": "awk",
    ".bash": "bash",
    ".bat": "batch",
    ".c": "c",
    ".cc": "cpp",
    ".cjs": "javascript",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".css": "css",
    ".fs": "fsharp",
    ".go": "go",
    ".gql": "graphql",
    ".graphql": "graphql",
    ".h": "c",
    ".hpp": "cpp",
    ".htm": "html",
    ".html": "html",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".mjs": "javascript",
    ".ps1": "powershell",
    ".psd1": "powershell",
    ".psm1": "powershell",
    ".py": "python",
    ".pyi": "python",
    ".rb": "ruby",
    ".rs": "rust",
    ".scala": "scala",
    ".scss": "scss",
    ".sh": "bash",
    ".sql": "sql",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".zsh": "zsh",
}

LAB_PATH_PARTS = LAB_DIRECTORIES | {"docker-lab"}
PROJECT_DIRECTORIES = {"project", "projects", "projeto", "projetos"}
EXAMPLE_DIRECTORIES = {"example", "examples", "exemplo", "exemplos"}
TEST_DIRECTORIES = {"test", "tests", "teste", "testes"}
FIXTURE_DIRECTORIES = {"fixture", "fixtures", "dataset", "datasets", "dados"}
REFERENCE_NAMES = REFERENCE_STEMS | {
    "image-pins",
    "video",
    "videos",
    "links",
    "roadmap",
}
ROLE_ORDER = {
    "module_overview": 0,
    "course_overview": 1,
    "lesson": 2,
    "lab_index": 3,
    "lab_instruction": 4,
    "project_readme": 5,
    "project_document": 6,
    "reference": 7,
    "solution": 8,
    "legacy_document": 9,
    "global_document": 10,
}
SECRET_NAME_RE = re.compile(
    r"(?:^|[._-])(?:credential|credentials|id_ed25519|id_rsa|private[-_]?key|secret|secrets)(?:[._-]|$)",
    re.IGNORECASE,
)
PRIVATE_KEY_RE = re.compile(rb"-----BEGIN (?:EC |OPENSSH |PGP |RSA )?PRIVATE KEY-----")


class CatalogError(ValueError):
    """Erro de entrada ou de segurança que impede uma geração confiável."""


def _normalized(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(character for character in decomposed if not unicodedata.combining(character)).lower()


def _validate_relative_path(raw_path: object, *, label: str) -> PurePosixPath:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise CatalogError(f"{label} deve ser um caminho relativo não vazio")
    if "\x00" in raw_path or "\\" in raw_path:
        raise CatalogError(f"{label} contém separador ou caractere proibido: {raw_path!r}")
    if raw_path != raw_path.strip():
        raise CatalogError(f"{label} não pode começar ou terminar com espaços")

    parts = raw_path.split("/")
    posix_path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if (
        posix_path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or any(part in {"", ".", ".."} for part in parts)
    ):
        raise CatalogError(f"{label} tenta sair da raiz permitida: {raw_path!r}")
    return posix_path


def _safe_join(base: Path, relative: PurePosixPath, *, label: str) -> Path:
    candidate = base.joinpath(*relative.parts)
    base_absolute = base.absolute()
    candidate_absolute = candidate.absolute()
    try:
        candidate_absolute.relative_to(base_absolute)
    except ValueError as exc:
        raise CatalogError(f"{label} saiu da raiz permitida: {relative}") from exc
    return candidate


def _assert_no_symlink_ancestors(path: Path, *, label: str) -> None:
    absolute = path.absolute()
    chain = (absolute, *absolute.parents)
    for candidate in chain:
        if candidate.is_symlink():
            raise CatalogError(f"{label} não pode atravessar link simbólico: {candidate}")


def _iter_markdown_files(module_root: Path) -> list[Path]:
    if module_root.is_symlink():
        raise CatalogError(f"módulo não pode ser link simbólico: {module_root}")

    markdown_files: list[Path] = []
    for current, directory_names, file_names in os.walk(module_root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for directory_name in sorted(directory_names):
            directory = current_path / directory_name
            if _normalized(directory_name) in FORBIDDEN_ASSET_DIRECTORIES:
                continue
            if directory.is_symlink():
                raise CatalogError(f"diretório simbólico recusado: {directory}")
            retained_directories.append(directory_name)
        directory_names[:] = retained_directories
        file_names.sort()

        for file_name in file_names:
            if not file_name.lower().endswith((".md", ".markdown")):
                continue
            document = current_path / file_name
            if document.is_symlink():
                raise CatalogError(f"Markdown simbólico recusado: {document}")
            if not document.is_file():
                raise CatalogError(f"Markdown não é arquivo regular: {document}")
            markdown_files.append(document)

    return sorted(markdown_files, key=lambda path: path.as_posix().casefold())


def _relative_is_under(relative: PurePosixPath, root: PurePosixPath) -> bool:
    return relative == root or root in relative.parents


def _is_manifest_excluded(
    relative: PurePosixPath,
    exclusion_roots: tuple[PurePosixPath, ...],
    exclusion_paths: set[PurePosixPath],
    included_paths: set[PurePosixPath],
) -> bool:
    if relative in included_paths or any(relative in included.parents for included in included_paths):
        return False
    return relative in exclusion_paths or any(_relative_is_under(relative, root) for root in exclusion_roots)


def _iter_repository_files(
    repo_root: Path,
    manifest: dict[str, object],
) -> tuple[list[Path], dict[str, object]]:
    """Lista fontes elegíveis sem atravessar infraestrutura ou links simbólicos."""
    exclusion_roots = tuple(PurePosixPath(value) for value in manifest["exclusionRoots"])
    exclusion_paths = {PurePosixPath(value) for value in manifest["exclusionPaths"]}
    included_document_paths = {PurePosixPath(value) for value in manifest["includedDocumentPaths"]}
    included_resource_paths = {PurePosixPath(value) for value in manifest["includedResourcePaths"]}
    included_paths = included_document_paths | included_resource_paths
    files: list[Path] = []
    explicitly_excluded_paths: set[str] = set()

    for current, directory_names, file_names in os.walk(repo_root, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for directory_name in sorted(directory_names):
            directory = current_path / directory_name
            relative = PurePosixPath(directory.relative_to(repo_root).as_posix())
            if _normalized(directory_name) in FORBIDDEN_ASSET_DIRECTORIES:
                continue
            if _is_manifest_excluded(relative, exclusion_roots, exclusion_paths, included_paths):
                explicitly_excluded_paths.add(relative.as_posix())
                continue
            if directory.is_symlink():
                raise CatalogError(f"diretório simbólico recusado: {directory}")
            retained_directories.append(directory_name)
        directory_names[:] = retained_directories

        for file_name in sorted(file_names):
            candidate = current_path / file_name
            relative = PurePosixPath(candidate.relative_to(repo_root).as_posix())
            if _is_manifest_excluded(relative, exclusion_roots, exclusion_paths, included_paths):
                explicitly_excluded_paths.add(relative.as_posix())
                continue
            if candidate.is_symlink():
                raise CatalogError(f"arquivo simbólico recusado: {candidate}")
            if candidate.is_file():
                files.append(candidate)

    return sorted(files, key=lambda path: path.relative_to(repo_root).as_posix().casefold()), {
        "roots": list(manifest["exclusionRoots"]),
        "paths": list(manifest["exclusionPaths"]),
        "includedExceptions": sorted(value.as_posix() for value in included_paths),
        "includedDocumentExceptions": list(manifest["includedDocumentPaths"]),
        "includedResourceExceptions": list(manifest["includedResourcePaths"]),
        "matched": sorted(explicitly_excluded_paths),
        "reason": manifest["exclusionReason"],
    }


def _markdown_link_targets(text: str) -> list[str]:
    """Extrai destinos de links sem interpretar exemplos dentro de code fences."""
    visible_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            visible_lines.append("")
            continue
        visible_lines.append("" if in_fence else line)
    visible = "\n".join(visible_lines)

    targets: list[str] = []
    for pattern in (INLINE_TARGET_RE, REFERENCE_TARGET_RE):
        for match in pattern.finditer(visible):
            target = match.group(1) or match.group(2)
            if target:
                targets.append(target)
    targets.extend(match.group(1) for match in HTML_TARGET_RE.finditer(visible))
    return targets


def _assert_path_components_are_not_symlinks(repo_root: Path, target: Path) -> None:
    try:
        relative = target.relative_to(repo_root)
    except ValueError as exc:
        raise CatalogError(f"asset tenta sair do repositório: {target}") from exc

    current = repo_root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise CatalogError(f"asset ou diretório simbólico recusado: {current}")


def _resolve_local_link(repo_root: Path, source_file: Path, raw_target: str) -> Path | None:
    target = html.unescape(raw_target.strip())
    if not target or target.startswith("#"):
        return None
    if "\x00" in target or "\\" in target:
        raise CatalogError(f"link local contém caractere proibido em {source_file}: {raw_target!r}")

    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return None
    posix_path = PurePosixPath(decoded_path)
    windows_path = PureWindowsPath(decoded_path)
    if posix_path.is_absolute() or windows_path.is_absolute() or windows_path.drive:
        raise CatalogError(f"link local absoluto recusado em {source_file}: {raw_target!r}")

    candidate = Path(os.path.abspath(source_file.parent.joinpath(*posix_path.parts)))
    try:
        candidate.relative_to(repo_root)
    except ValueError as exc:
        raise CatalogError(f"path traversal em link de {source_file}: {raw_target!r}") from exc
    _assert_path_components_are_not_symlinks(repo_root, candidate)
    return candidate


def _asset_suffix(path: Path) -> str:
    lowered = path.name.casefold()
    if lowered.endswith(".env.example"):
        return ".env.example"
    if lowered.startswith("dockerfile"):
        return ".dockerfile"
    return path.suffix.casefold()


def _valid_image_asset(suffix: str, content: bytes) -> bool:
    if suffix == ".png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return content.startswith(b"\xff\xd8\xff")
    if suffix == ".gif":
        return content.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".webp":
        return len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP"
    if suffix == ".ico":
        return content.startswith(b"\x00\x00\x01\x00")
    if suffix == ".avif":
        return len(content) >= 12 and content[4:8] == b"ftyp" and content[8:12] in {b"avif", b"avis"}
    if suffix == ".svg":
        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError:
            return False
        lowered = decoded.casefold()
        has_svg_root = "<svg" in lowered[:2048]
        has_active_content = bool(re.search(r"<\s*script\b|\bon\w+\s*=|(?:javascript|data)\s*:", lowered))
        return has_svg_root and not has_active_content
    return False


def _asset_path_is_forbidden(repo_root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(repo_root)
    except ValueError:
        return True
    normalized_parts = {_normalized(part) for part in relative.parts}
    return bool(normalized_parts.intersection(FORBIDDEN_ASSET_DIRECTORIES))


def _asset_kind(path: Path, content: bytes) -> str | None:
    if SECRET_NAME_RE.search(path.name):
        return None

    suffix = _asset_suffix(path)
    if suffix in IMAGE_ASSET_EXTENSIONS:
        return "image" if _valid_image_asset(suffix, content) else None
    if suffix not in TEXT_ASSET_EXTENSIONS and path.name.casefold() not in SAFE_EXTENSIONLESS_NAMES:
        if suffix or path.name.startswith("."):
            return None
    if b"\x00" in content or PRIVATE_KEY_RE.search(content):
        return None
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        return None

    if suffix in {".md", ".markdown", ".rst"}:
        return "markdown"
    if suffix in {".csv", ".json", ".jsonl", ".sql", ".tsv"}:
        return "data"
    if (
        suffix
        in {
            ".cfg",
            ".conf",
            ".csproj",
            ".dockerfile",
            ".env.example",
            ".ini",
            ".lock",
            ".properties",
            ".service",
            ".toml",
            ".xml",
            ".xsd",
            ".yaml",
            ".yml",
        }
        or path.name.casefold() in SAFE_EXTENSIONLESS_NAMES
    ):
        return "config"
    if suffix in {".txt", ""}:
        return "text"
    return "code"


def _read_safe_asset(path: Path) -> tuple[str, bytes] | None:
    if path.is_symlink():
        raise CatalogError(f"asset simbólico recusado: {path}")
    if not path.is_file():
        return None
    size = path.stat().st_size
    if size > MAX_ASSET_BYTES:
        return None
    content = path.read_bytes()
    if len(content) > MAX_ASSET_BYTES:
        return None
    kind = _asset_kind(path, content)
    return (kind, content) if kind is not None else None


def _read_explicit_text_resource(path: Path) -> tuple[str, bytes] | None:
    """Aceita uma extensão incomum somente quando o manifesto nomeia o arquivo.

    A exceção é deliberadamente mais estreita que ``_read_safe_asset``: ela
    continua recusando nomes de segredo, binários, chaves privadas e arquivos
    grandes. Assim, um fixture textual ``.bin`` pode ser estudado sem tornar a
    extensão inteira confiável.
    """
    if path.is_symlink():
        raise CatalogError(f"recurso explícito simbólico recusado: {path}")
    if not path.is_file():
        return None
    size = path.stat().st_size
    if size > MAX_ASSET_BYTES or SECRET_NAME_RE.search(path.name):
        return None
    content = path.read_bytes()
    if len(content) > MAX_ASSET_BYTES or b"\x00" in content or PRIVATE_KEY_RE.search(content):
        return None
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return "text", content


def _iter_directory_assets(directory: Path) -> list[Path]:
    candidates: list[Path] = []
    for current, directory_names, file_names in os.walk(directory, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in sorted(directory_names):
            candidate = current_path / name
            if _normalized(name) in FORBIDDEN_ASSET_DIRECTORIES:
                continue
            if candidate.is_symlink():
                raise CatalogError(f"diretório simbólico recusado em assets: {candidate}")
            retained_directories.append(name)
        directory_names[:] = retained_directories

        for name in sorted(file_names):
            candidate = current_path / name
            if candidate.is_symlink():
                raise CatalogError(f"arquivo simbólico recusado em assets: {candidate}")
            if candidate.is_file():
                candidates.append(candidate)
                if len(candidates) > MAX_ASSET_FILES:
                    raise CatalogError(f"diretório de assets excede o limite de arquivos: {directory}")
    return candidates


def _asset_id(source_path: str) -> str:
    digest = hashlib.sha256(source_path.encode("utf-8")).hexdigest()[:20]
    return f"asset-{digest}"


def _discover_linked_assets(
    repo_root: Path,
    documents: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    source_documents = {str(document["sourcePath"]): document for document in documents}
    documents_by_id = {str(document["id"]): document for document in documents}
    queue: deque[tuple[Path, str]] = deque((document["_sourceFile"], str(document["id"])) for document in documents)
    scanned_pairs: set[tuple[str, str]] = set()
    assets_by_path: dict[str, dict[str, object]] = {}
    unresolved_links: set[tuple[str, str]] = set()
    skipped_links: set[tuple[str, str]] = set()
    total_bytes = 0

    while queue:
        source_file, root_document_id = queue.popleft()
        source_key = source_file.relative_to(repo_root).as_posix()
        scan_key = (source_key, root_document_id)
        if scan_key in scanned_pairs:
            continue
        scanned_pairs.add(scan_key)
        try:
            markdown = source_file.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise CatalogError(f"Markdown de asset não está em UTF-8: {source_key}") from exc

        root_document = documents_by_id[root_document_id]
        document_assets = root_document["assetIds"]
        assert isinstance(document_assets, list)

        for raw_target in _markdown_link_targets(markdown):
            target = _resolve_local_link(repo_root, source_file, raw_target)
            if target is None:
                continue
            if _asset_path_is_forbidden(repo_root, target):
                skipped_links.add((source_key, raw_target))
                continue
            if not target.exists():
                unresolved_links.add((source_key, raw_target))
                continue
            if target == repo_root and target.is_dir():
                raise CatalogError(f"link para a raiz inteira do repositório recusado em {source_key}")
            if target.is_dir():
                linked_files = _iter_directory_assets(target)
            elif target.is_file():
                linked_files = [target]
            else:
                skipped_links.add((source_key, raw_target))
                continue

            accepted_from_link = False
            for linked_file in linked_files:
                _assert_path_components_are_not_symlinks(repo_root, linked_file)
                linked_source_path = linked_file.relative_to(repo_root).as_posix()
                if linked_source_path in source_documents:
                    accepted_from_link = True
                    continue
                safe_asset = _read_safe_asset(linked_file)
                if safe_asset is None:
                    continue
                kind, content = safe_asset
                accepted_from_link = True
                asset = assets_by_path.get(linked_source_path)
                if asset is None:
                    total_bytes += len(content)
                    if len(assets_by_path) + 1 > MAX_ASSET_FILES or total_bytes > MAX_TOTAL_ASSET_BYTES:
                        raise CatalogError("limite de quantidade ou tamanho total de assets excedido")
                    asset = {
                        "id": _asset_id(linked_source_path),
                        "order": 0,
                        "sourcePath": linked_source_path,
                        "contentUrl": f"/generated/content/{quote(linked_source_path, safe='/-._~')}",
                        "kind": kind,
                        "bytes": len(content),
                        "referencedBy": [],
                    }
                    assets_by_path[linked_source_path] = asset
                referenced_by = asset["referencedBy"]
                assert isinstance(referenced_by, list)
                if root_document_id not in referenced_by:
                    referenced_by.append(root_document_id)
                if asset["id"] not in document_assets:
                    document_assets.append(asset["id"])
                if kind == "markdown":
                    queue.append((linked_file, root_document_id))

            if not accepted_from_link and target.is_file():
                skipped_links.add((source_key, raw_target))

    assets = sorted(assets_by_path.values(), key=lambda asset: str(asset["sourcePath"]).casefold())
    for order, asset in enumerate(assets):
        asset["order"] = order
        asset["referencedBy"] = sorted(asset["referencedBy"])
    for document in documents:
        document["assetIds"] = sorted(document["assetIds"])
    return assets, {
        "unresolvedLocalLinks": len(unresolved_links),
        "skippedAssetLinks": len(skipped_links),
    }


def _course_adopts_path(relative_path: PurePosixPath, course: dict[str, object]) -> bool:
    return any(
        relative_path == content_path or _relative_is_under(relative_path, content_path)
        for raw_path in course.get("contentPaths", [])
        for content_path in (PurePosixPath(str(raw_path)),)
    )


def _course_context_for_path(
    relative_path: PurePosixPath,
    module_sources: list[dict[str, object]],
    courses_by_module: dict[str, dict[str, object]],
) -> tuple[str | None, dict[str, object] | None, str]:
    for course in courses_by_module.values():
        if _course_adopts_path(relative_path, course):
            return str(course["moduleId"]), course, "formation"
    for module in module_sources:
        module_root = PurePosixPath(str(module["path"]))
        if not _relative_is_under(relative_path, module_root):
            continue
        module_id = str(module["id"])
        course = courses_by_module[module_id]
        course_root = PurePosixPath(str(course["courseRoot"]))
        origin = "formation" if _relative_is_under(relative_path, course_root) else "legacy"
        return module_id, course, origin
    return None, None, "global"


def _resource_language(path: Path, kind: str) -> str:
    suffix = _asset_suffix(path)
    if suffix == ".dockerfile":
        return "dockerfile"
    if suffix in LANGUAGE_BY_SUFFIX:
        return LANGUAGE_BY_SUFFIX[suffix]
    if suffix in {".json", ".jsonl"}:
        return "json"
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix:
        return suffix.removeprefix(".")
    if path.name.casefold() in {"makefile", "cmakelists.txt"}:
        return path.name.casefold().removesuffix(".txt")
    return "text" if kind == "text" else kind


def _resource_category(relative_path: PurePosixPath, kind: str) -> str:
    normalized_parts = {_normalized(part) for part in relative_path.parts[:-1]}
    normalized_stem = _normalized(relative_path.stem)
    if normalized_parts.intersection(TEST_DIRECTORIES) or normalized_stem.startswith("test_"):
        return "test"
    if normalized_parts.intersection(FIXTURE_DIRECTORIES):
        return "fixture"
    return {
        "code": "source-code",
        "config": "configuration",
        "data": "dataset",
        "image": "image",
        "text": "text",
    }.get(kind, kind)


def _discover_all_resources(
    repo_root: Path,
    repository_files: list[Path],
    documents: list[dict[str, object]],
    module_sources: list[dict[str, object]],
    courses_by_module: dict[str, dict[str, object]],
    explicit_resource_paths: set[str],
) -> tuple[list[dict[str, object]], dict[str, int], dict[str, object]]:
    """Cataloga cada arquivo textual/imagem seguro e associa links Markdown."""
    document_paths = {str(document["sourcePath"]): document for document in documents}
    resources_by_path: dict[str, dict[str, object]] = {}
    unsafe_by_kind: dict[str, int] = {}
    unsafe_paths: list[str] = []
    total_bytes = 0

    for source in repository_files:
        source_path = source.relative_to(repo_root).as_posix()
        if source_path in document_paths:
            continue
        safe_asset = _read_safe_asset(source)
        explicitly_allowed = source_path in explicit_resource_paths
        if safe_asset is None and explicitly_allowed:
            safe_asset = _read_explicit_text_resource(source)
        if safe_asset is None:
            suffix = _asset_suffix(source) or "extensionless"
            unsafe_by_kind[suffix] = unsafe_by_kind.get(suffix, 0) + 1
            unsafe_paths.append(source_path)
            continue
        kind, content = safe_asset
        total_bytes += len(content)
        if len(resources_by_path) + 1 > MAX_ASSET_FILES or total_bytes > MAX_TOTAL_ASSET_BYTES:
            raise CatalogError("limite de quantidade ou tamanho total de recursos excedido")

        relative = PurePosixPath(source_path)
        module_id, course, origin = _course_context_for_path(relative, module_sources, courses_by_module)
        project_root = _project_root(relative)
        lab_root = _lab_root(relative)
        course_id = str(course["id"]) if course is not None and origin == "formation" else None
        legacy_section_id = f"legacy-{course['legacyId']}" if course is not None and origin == "legacy" else None
        project_id = (
            f"project-{hashlib.sha256(project_root.as_posix().encode('utf-8')).hexdigest()[:20]}"
            if project_root is not None
            else None
        )
        memberships = [_membership(RESOURCE_COLLECTION, module_id=module_id)]
        if origin == "formation":
            memberships.append(_membership(FORMATION_COLLECTION, module_id=module_id, course_id=course_id))
        elif origin == "legacy":
            memberships.append(_membership(LEGACY_COLLECTION, module_id=module_id, section_id=legacy_section_id))
        if project_root is not None or lab_root is not None:
            memberships.append(
                _membership(
                    PRACTICE_COLLECTION,
                    module_id=module_id,
                    course_id=course_id,
                    section_id=legacy_section_id,
                )
            )

        resource: dict[str, object] = {
            "id": _asset_id(source_path),
            "order": 0,
            "title": source.name,
            "sourcePath": source_path,
            "contentUrl": f"/generated/content/{quote(source_path, safe='/-._~')}",
            "kind": kind,
            "category": _resource_category(relative, kind),
            "language": _resource_language(source, kind),
            "bytes": len(content),
            "module": module_id,
            "moduleId": module_id,
            "origin": origin,
            "courseId": course_id,
            "legacySectionId": legacy_section_id,
            "projectId": project_id,
            "memberships": memberships,
            "referencedBy": [],
        }
        if explicitly_allowed:
            resource["explicitlyAllowed"] = True
        resources_by_path[source_path] = resource

    # Markdown globais eram assets linkados no schema v1. Mantemos aliases
    # explícitos para que assetIds e IDs antigos continuem válidos, enquanto o
    # mesmo arquivo passa a ser também um documento navegável de primeira classe.
    for document in documents:
        if document.get("origin") != "global":
            continue
        source = document["_sourceFile"]
        assert isinstance(source, Path)
        source_path = str(document["sourcePath"])
        content = source.read_bytes()
        total_bytes += len(content)
        if len(resources_by_path) + 1 > MAX_ASSET_FILES or total_bytes > MAX_TOTAL_ASSET_BYTES:
            raise CatalogError("limite de quantidade ou tamanho total de recursos excedido")
        resources_by_path[source_path] = {
            "id": _asset_id(source_path),
            "order": 0,
            "title": str(document["title"]),
            "sourcePath": source_path,
            "contentUrl": document["contentUrl"],
            "kind": "markdown",
            "category": "documentation",
            "language": "markdown",
            "bytes": len(content),
            "module": None,
            "moduleId": None,
            "origin": "global",
            "courseId": None,
            "legacySectionId": None,
            "projectId": None,
            "memberships": [_membership(DOCUMENTATION_COLLECTION)],
            "referencedBy": [],
            "aliasOfDocumentId": document["id"],
        }

    unresolved_links: set[tuple[str, str]] = set()
    skipped_links: set[tuple[str, str]] = set()
    resources = list(resources_by_path.values())
    documents_by_path = {str(document["sourcePath"]): document for document in documents}

    for document in documents:
        source_file = document["_sourceFile"]
        assert isinstance(source_file, Path)
        source_key = str(document["sourcePath"])
        markdown = source_file.read_text(encoding="utf-8")
        document_assets = document["assetIds"]
        related_documents = document["relatedDocumentIds"]
        assert isinstance(document_assets, list)
        assert isinstance(related_documents, list)

        for raw_target in _markdown_link_targets(markdown):
            target = _resolve_local_link(repo_root, source_file, raw_target)
            if target is None:
                continue
            if not target.exists():
                unresolved_links.add((source_key, raw_target))
                continue
            if target == repo_root and target.is_dir():
                raise CatalogError(f"link para a raiz inteira do repositório recusado em {source_key}")

            target_key = target.relative_to(repo_root).as_posix()
            matched_resources: list[dict[str, object]] = []
            matched_documents: list[dict[str, object]] = []
            if target.is_dir():
                target_relative = PurePosixPath(target_key)
                matched_resources = [
                    resource
                    for path, resource in resources_by_path.items()
                    if _relative_is_under(PurePosixPath(path), target_relative)
                ]
                matched_documents = [
                    candidate
                    for path, candidate in documents_by_path.items()
                    if _relative_is_under(PurePosixPath(path), target_relative)
                ]
            else:
                if target_key in resources_by_path:
                    matched_resources = [resources_by_path[target_key]]
                if target_key in documents_by_path:
                    matched_documents = [documents_by_path[target_key]]

            if not matched_resources and not matched_documents:
                skipped_links.add((source_key, raw_target))
                continue
            for resource in matched_resources:
                resource_id = str(resource["id"])
                if resource_id not in document_assets:
                    document_assets.append(resource_id)
                referenced_by = resource["referencedBy"]
                assert isinstance(referenced_by, list)
                if document["id"] not in referenced_by:
                    referenced_by.append(document["id"])
            for related in matched_documents:
                if related["id"] != document["id"] and related["id"] not in related_documents:
                    related_documents.append(related["id"])

    # No v1, um Markdown global linkado era tratado como asset e seus próprios
    # links eram percorridos em nome do documento de origem. Propagamos apenas
    # essa cadeia global para manter os assetIds antigos sem misturar recursos
    # de aulas que hoje são documentos relacionados.
    documents_by_id = {str(document["id"]): document for document in documents}

    def inherited_global_assets(document: dict[str, object], seen: set[str]) -> set[str]:
        inherited: set[str] = set()
        for related_id in document["relatedDocumentIds"]:
            related_key = str(related_id)
            related = documents_by_id.get(related_key)
            if related is None or related.get("origin") != "global" or related_key in seen:
                continue
            inherited.update(str(asset_id) for asset_id in related["assetIds"])
            inherited.update(inherited_global_assets(related, seen | {related_key}))
        return inherited

    resources_by_id = {str(resource["id"]): resource for resource in resources_by_path.values()}
    for document in documents:
        inherited = inherited_global_assets(document, {str(document["id"])})
        document["assetIds"] = sorted({*document["assetIds"], *inherited})
        for asset_id in inherited:
            resource = resources_by_id.get(asset_id)
            if resource is None:
                continue
            referenced_by = resource["referencedBy"]
            assert isinstance(referenced_by, list)
            if document["id"] not in referenced_by:
                referenced_by.append(document["id"])

    resources.sort(key=lambda resource: str(resource["sourcePath"]).casefold())
    for order, resource in enumerate(resources):
        resource["order"] = order
        resource["referencedBy"] = sorted(resource["referencedBy"])
    for document in documents:
        document["assetIds"] = sorted(document["assetIds"])
        document["relatedDocumentIds"] = sorted(document["relatedDocumentIds"])
    return (
        resources,
        {
            "unresolvedLocalLinks": len(unresolved_links),
            "skippedAssetLinks": len(skipped_links),
        },
        {
            "byExtension": dict(sorted(unsafe_by_kind.items())),
            "paths": sorted(unsafe_paths),
        },
    )


def _strip_inline_markdown(value: str) -> str:
    value = LINK_RE.sub(lambda match: match.group(1), value)
    value = HTML_RE.sub(" ", value)
    value = re.sub(r"^[>\s]+", "", value)
    value = re.sub(r"^[-*+]\s+", "", value)
    value = value.replace("`", "").replace("**", "").replace("__", "")
    value = value.replace("*", "").replace("_", "")
    return " ".join(value.split()).strip()


def _markdown_title(text: str, fallback: str) -> str:
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(stripped)
        if match:
            title = _strip_inline_markdown(match.group(1))
            if title:
                return title
    return fallback.replace("-", " ").replace("_", " ").strip().title()


def _markdown_description(text: str, *, fallback: str, limit: int = 280) -> str:
    lines = text.splitlines()
    saw_title = False
    in_fence = False
    paragraph: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not saw_title:
            if HEADING_RE.match(stripped):
                saw_title = True
            continue
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith("#"):
            if paragraph:
                break
            continue
        if stripped.startswith("![") or stripped.startswith("<"):
            continue
        if stripped.startswith("|") or re.match(r"^[-:| ]{3,}$", stripped):
            if paragraph:
                break
            continue
        if re.match(r"^(?:[-*+] |\d+[.)] )", stripped) and not stripped.startswith(">"):
            if paragraph:
                break
            continue
        cleaned = _strip_inline_markdown(stripped)
        if cleaned:
            paragraph.append(cleaned)

    description = " ".join(paragraph) or fallback
    if len(description) <= limit:
        return description
    shortened = description[: limit + 1].rsplit(" ", 1)[0].rstrip(" .,;:")
    return f"{shortened}…"


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def _document_id(source_path: str) -> str:
    digest = hashlib.sha256(source_path.encode("utf-8")).hexdigest()[:20]
    return f"document-{digest}"


def _document_type(relative_path: PurePosixPath) -> str:
    normalized_parts = {_normalized(part) for part in relative_path.parts[:-1]}
    stem = _normalized(relative_path.stem)
    name = relative_path.name.casefold()

    if stem in REFERENCE_STEMS or normalized_parts.intersection(ANSWER_DIRECTORIES):
        return "reference"
    if name == "readme.md":
        return "overview"
    if normalized_parts.intersection(LAB_DIRECTORIES) or stem.startswith("lab-"):
        return "lab"
    if NUMBERED_FILE_RE.match(relative_path.name):
        return "chapter"
    if stem.startswith("laboratorio-"):
        return "lab"
    return "supplement"


def _project_root(relative_path: PurePosixPath) -> PurePosixPath | None:
    normalized_parts = [_normalized(part) for part in relative_path.parts]
    for index, part in enumerate(normalized_parts[:-1]):
        if part in PROJECT_DIRECTORIES and index + 1 < len(relative_path.parts) - 1:
            return PurePosixPath(*relative_path.parts[: index + 2])
    return None


def _lab_root(relative_path: PurePosixPath) -> PurePosixPath | None:
    for index, part in enumerate(relative_path.parts[:-1]):
        if _normalized(part) in LAB_PATH_PARTS:
            return PurePosixPath(*relative_path.parts[: index + 1])
    return None


def _membership(
    collection_id: str,
    *,
    module_id: str | None = None,
    course_id: str | None = None,
    section_id: str | None = None,
) -> dict[str, str]:
    result = {"collectionId": collection_id}
    if module_id:
        result["moduleId"] = module_id
    if course_id:
        result["courseId"] = course_id
    if section_id:
        result["sectionId"] = section_id
    return result


def _classify_document(
    document: dict[str, object],
    course: dict[str, object] | None,
) -> None:
    relative_path = document["_relativePath"]
    assert isinstance(relative_path, PurePosixPath)
    module_id = str(document["module"]) if document.get("module") else ""

    if course is None:
        document.update(
            {
                "type": "reference",
                "role": "global_document",
                "origin": "global",
                "required": False,
                "memberships": [_membership(DOCUMENTATION_COLLECTION)],
                "language": "markdown",
                "category": "documentation",
                "courseId": None,
                "legacySectionId": None,
                "projectId": None,
                "relatedDocumentIds": [],
            }
        )
        return

    course_root = PurePosixPath(str(course["courseRoot"]))
    overview_path = PurePosixPath(str(course["overviewPath"]))
    course_id = str(course["id"])
    legacy_section_id = f"legacy-{course['legacyId']}"
    is_adopted = _course_adopts_path(relative_path, course)
    is_formation = (
        relative_path == overview_path
        or _relative_is_under(relative_path, course_root)
        or is_adopted
    )
    origin = "formation" if is_formation else "legacy"
    normalized_parent_parts = {_normalized(part) for part in relative_path.parts[:-1]}
    stem = _normalized(relative_path.stem)
    project_root = _project_root(relative_path)
    lab_root = _lab_root(relative_path)
    is_solution = bool(normalized_parent_parts.intersection(ANSWER_DIRECTORIES))
    is_reference = stem in REFERENCE_NAMES or "referencias" in normalized_parent_parts

    if is_solution:
        role = "solution"
        document_type = "reference"
    elif project_root is not None:
        role = "project_readme" if relative_path.name.casefold() == "readme.md" else "project_document"
        document_type = "overview" if role == "project_readme" else _document_type(relative_path)
    elif lab_root is not None or stem.startswith(("lab-", "laboratorio-")):
        if (
            origin == "formation"
            and not _course_adopts_path(relative_path, course)
            and relative_path.name.casefold() == "readme.md"
            and lab_root is not None
            and relative_path.parent == lab_root
        ):
            role = "lab_index"
            document_type = "overview"
        elif is_reference:
            role = "reference"
            document_type = "reference"
        else:
            role = "lab_instruction"
            document_type = "lab"
    elif relative_path == overview_path:
        role = "module_overview"
        document_type = "overview"
    elif relative_path == course_root / "README.md":
        role = "course_overview"
        document_type = "overview"
    elif is_reference or normalized_parent_parts.intersection(EXAMPLE_DIRECTORIES):
        role = "reference"
        document_type = "reference"
    elif origin == "formation":
        role = "lesson"
        document_type = _document_type(relative_path)
    else:
        role = "legacy_document"
        document_type = _document_type(relative_path)

    required = origin == "formation" and role not in {
        "lab_index",
        "project_readme",
        "project_document",
        "reference",
        "solution",
    }
    memberships = [
        _membership(
            FORMATION_COLLECTION if origin == "formation" else LEGACY_COLLECTION,
            module_id=module_id,
            course_id=course_id if origin == "formation" else None,
            section_id=legacy_section_id if origin == "legacy" else None,
        )
    ]
    if role in {"lab_index", "lab_instruction", "solution", "project_readme", "project_document"}:
        memberships.append(
            _membership(
                PRACTICE_COLLECTION,
                module_id=module_id,
                course_id=course_id if origin == "formation" else None,
                section_id=legacy_section_id if origin == "legacy" else None,
            )
        )

    if role in {"lab_index", "lab_instruction"}:
        category = "laboratory"
    elif role == "solution":
        category = "solution"
    elif role.startswith("project_"):
        category = "project"
    elif role == "reference":
        category = "reference"
    elif origin == "legacy":
        category = "security-archive"
    else:
        category = "course"

    project_id = (
        f"project-{hashlib.sha256(project_root.as_posix().encode('utf-8')).hexdigest()[:20]}" if project_root else None
    )
    document.update(
        {
            "type": document_type,
            "role": role,
            "origin": origin,
            "required": required,
            "memberships": memberships,
            "language": "markdown",
            "category": category,
            "courseId": course_id if origin == "formation" else None,
            "legacySectionId": legacy_section_id if origin == "legacy" else None,
            "projectId": project_id,
            "relatedDocumentIds": [],
            "_adopted": is_adopted,
        }
    )
    document["chapterNumber"] = _number_from_name(relative_path.name) if document_type == "chapter" else None
    document["labNumber"] = _number_from_name(relative_path.name) if document_type == "lab" else None
    if origin == "formation":
        document["coursePath"] = course_root.as_posix()
    elif lab_root is not None:
        document["coursePath"] = lab_root.as_posix()


def _number_from_name(name: str) -> int | None:
    match = NUMBERED_FILE_RE.match(name)
    return int(match.group(1)) if match else None


def _track_for_module(module_id: str) -> dict[str, object]:
    module_number = int(module_id)
    for track in TRACKS:
        if int(track["first"]) <= module_number <= int(track["last"]):
            return track
    raise CatalogError(f"módulo fora das trilhas conhecidas: {module_id}")


def _read_source_document(repo_root: Path, module_id: str | None, source_file: Path) -> dict[str, object]:
    try:
        source_path = source_file.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise CatalogError(f"Markdown fora do repositório: {source_file}") from exc

    relative_path = _validate_relative_path(source_path, label="sourcePath")
    raw_content = source_file.read_bytes()
    try:
        text = raw_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CatalogError(f"Markdown não está em UTF-8: {source_path}") from exc

    document_type = _document_type(relative_path)
    title = _markdown_title(text, relative_path.stem)
    words = _word_count(text)
    chapter_number = _number_from_name(relative_path.name) if document_type == "chapter" else None
    lab_number = _number_from_name(relative_path.name) if document_type == "lab" else None
    track = _track_for_module(module_id) if module_id is not None else None

    return {
        "id": _document_id(source_path),
        "order": 0,
        "globalOrder": 0,
        "module": module_id or "",
        "trackId": track["id"] if track is not None else "",
        "type": document_type,
        "title": title,
        "description": _markdown_description(text, fallback=title),
        "sourcePath": source_path,
        "contentUrl": f"/generated/content/{quote(source_path, safe='/-._~')}",
        "words": words,
        "readingMinutes": max(1, math.ceil(words / WORDS_PER_MINUTE)),
        "prerequisites": [],
        "assetIds": [],
        "chapterNumber": chapter_number,
        "labNumber": lab_number,
        "coursePath": None,
        "_relativePath": relative_path,
        "_sourceFile": source_file,
        "_content": raw_content,
    }


def _document_sort_key(document: dict[str, object]) -> tuple[object, ...]:
    document_type = str(document["type"])
    number = document["chapterNumber"] if document_type == "chapter" else document["labNumber"]
    numeric_order = int(number) if isinstance(number, int) else 10_000
    relative_path = document["_relativePath"]
    assert isinstance(relative_path, PurePosixPath)
    curriculum_order = document.get("_curriculumOrder")
    has_curriculum_order = isinstance(curriculum_order, int) and not isinstance(curriculum_order, bool)
    return (
        0 if document.get("origin") == "formation" else 1 if document.get("origin") == "legacy" else 2,
        0 if has_curriculum_order else 1,
        int(curriculum_order) if has_curriculum_order else 10_000,
        ROLE_ORDER.get(str(document.get("role")), 99),
        TYPE_ORDER[document_type],
        numeric_order,
        len(relative_path.parts),
        relative_path.as_posix().casefold(),
    )


def _nearest_course_root(
    lab_path: PurePosixPath,
    course_roots: list[PurePosixPath],
) -> PurePosixPath | None:
    lab_directory = lab_path.parent
    ancestors = [root for root in course_roots if root == lab_directory or root in lab_directory.parents]
    if ancestors:
        return max(ancestors, key=lambda root: len(root.parts))
    return None


def _nearest_ancestor_overview(
    lab_path: PurePosixPath,
    overviews: list[dict[str, object]],
) -> dict[str, object] | None:
    lab_directory = lab_path.parent
    ancestors: list[dict[str, object]] = []
    for overview in overviews:
        overview_path = overview["_relativePath"]
        assert isinstance(overview_path, PurePosixPath)
        if overview_path.parent == lab_directory or overview_path.parent in lab_directory.parents:
            ancestors.append(overview)
    if not ancestors:
        return None
    return min(
        ancestors,
        key=lambda overview: (
            -len(overview["_relativePath"].parent.parts),
            str(overview["sourcePath"]).casefold(),
        ),
    )


def _assign_lab_prerequisites(documents: list[dict[str, object]]) -> None:
    chapters_by_root: dict[PurePosixPath, list[dict[str, object]]] = {}
    overviews = [
        document for document in documents if document["type"] == "overview" and document.get("origin") == "formation"
    ]
    for document in documents:
        if document["type"] != "chapter" or document.get("origin") != "formation":
            continue
        relative_path = document["_relativePath"]
        assert isinstance(relative_path, PurePosixPath)
        chapters_by_root.setdefault(relative_path.parent, []).append(document)

    for chapters in chapters_by_root.values():
        chapters.sort(
            key=lambda document: (
                int(document["chapterNumber"]),
                str(document["sourcePath"]).casefold(),
            )
        )

    roots = sorted(chapters_by_root, key=lambda root: root.as_posix().casefold())
    labs_by_root: dict[PurePosixPath, list[dict[str, object]]] = {}
    for document in documents:
        if document["type"] != "lab" or document.get("origin") != "formation":
            continue
        relative_path = document["_relativePath"]
        assert isinstance(relative_path, PurePosixPath)
        root = _nearest_course_root(relative_path, roots)
        if root is None:
            if document.get("_adopted"):
                logical_prerequisites = sorted(
                    (
                        candidate
                        for candidate in documents
                        if candidate.get("origin") == "formation"
                        and candidate.get("required")
                        and candidate.get("role") != "lab_instruction"
                    ),
                    key=_document_sort_key,
                )
                document["prerequisites"] = [candidate["id"] for candidate in logical_prerequisites]
                continue
            overview = _nearest_ancestor_overview(relative_path, overviews)
            if overview is not None:
                document["coursePath"] = str(overview["_relativePath"].parent)
                document["prerequisites"] = [overview["id"]]
            continue
        document["coursePath"] = root.as_posix()
        labs_by_root.setdefault(root, []).append(document)

    for root, labs in labs_by_root.items():
        chapters = chapters_by_root[root]
        labs.sort(
            key=lambda document: (
                int(document["labNumber"]) if isinstance(document["labNumber"], int) else 10_000,
                str(document["sourcePath"]).casefold(),
            )
        )
        for rank, lab in enumerate(labs, start=1):
            if lab.get("_prerequisitesOverridden"):
                continue
            unlocked_count = max(1, math.ceil(rank * len(chapters) / len(labs)))
            lab["prerequisites"] = [chapter["id"] for chapter in chapters[:unlocked_count]]

    for root, chapters in chapters_by_root.items():
        for chapter in chapters:
            chapter["coursePath"] = root.as_posix()


def _apply_document_overrides(
    documents: list[dict[str, object]],
    course: dict[str, object],
) -> None:
    """Aplica metadados curriculares explícitos sem alterar IDs baseados no caminho."""
    by_path = {str(document["sourcePath"]): document for document in documents}
    for override in course.get("documentOverrides", []):
        source_path = str(override["sourcePath"])
        document = by_path.get(source_path)
        if document is None:
            raise CatalogError(
                f"documentOverride do módulo {course['moduleId']} não pertence ao catálogo: {source_path}"
            )
        if "order" in override:
            document["_curriculumOrder"] = int(override["order"])
        if "required" in override:
            document["required"] = bool(override["required"])
        if "prerequisitePaths" in override:
            prerequisite_paths = list(override["prerequisitePaths"])
            unknown = [path for path in prerequisite_paths if path not in by_path]
            if unknown:
                raise CatalogError(
                    f"documentOverride de {source_path} referencia documentos fora do módulo: "
                    + ", ".join(unknown)
                )
            if source_path in prerequisite_paths:
                raise CatalogError(f"documentOverride não pode depender de si mesmo: {source_path}")
            document["prerequisites"] = [by_path[path]["id"] for path in prerequisite_paths]
            document["_prerequisitesOverridden"] = True


def _module_description(documents: list[dict[str, object]], fallback: str) -> str:
    root_overviews = [
        document
        for document in documents
        if document["type"] == "overview" and isinstance(document["_relativePath"], PurePosixPath)
    ]
    if root_overviews:
        overview = min(
            root_overviews,
            key=lambda document: (
                len(document["_relativePath"].parts),
                str(document["sourcePath"]).casefold(),
            ),
        )
        return str(overview["description"])
    return fallback


def _validate_module_entry(entry: object, known_ids: set[str]) -> dict[str, object]:
    if not isinstance(entry, dict):
        raise CatalogError("cada entrada de módulo deve ser um objeto JSON")

    module_id = entry.get("id")
    if not isinstance(module_id, str) or not re.fullmatch(r"\d{2}", module_id):
        raise CatalogError(f"id de módulo inválido: {module_id!r}")
    if module_id in known_ids:
        raise CatalogError(f"id de módulo duplicado: {module_id}")

    module_path = _validate_relative_path(entry.get("path"), label=f"path do módulo {module_id}")
    if not module_path.name.startswith(f"{module_id}-"):
        raise CatalogError(f"path do módulo {module_id} não possui o prefixo esperado")

    title = entry.get("title")
    if not isinstance(title, str) or not title.strip():
        raise CatalogError(f"título ausente no módulo {module_id}")

    prerequisites = entry.get("prerequisites", [])
    if not isinstance(prerequisites, list) or not all(isinstance(item, str) for item in prerequisites):
        raise CatalogError(f"pré-requisitos inválidos no módulo {module_id}")

    known_ids.add(module_id)
    validated = dict(entry)
    validated["id"] = module_id
    validated["path"] = module_path.as_posix()
    validated["title"] = title.strip()
    validated["prerequisites"] = prerequisites
    return validated


def _load_module_catalog(repo_root: Path) -> list[dict[str, object]]:
    catalog_file = repo_root / "MODULE-CATALOG.json"
    if catalog_file.is_symlink():
        raise CatalogError("MODULE-CATALOG.json não pode ser link simbólico")
    if not catalog_file.is_file():
        raise CatalogError(f"catálogo de módulos ausente: {catalog_file}")

    try:
        raw_catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CatalogError(f"MODULE-CATALOG.json inválido: {exc}") from exc
    if not isinstance(raw_catalog, dict) or not isinstance(raw_catalog.get("modules"), list):
        raise CatalogError("MODULE-CATALOG.json deve possuir uma lista 'modules'")

    known_ids: set[str] = set()
    modules = [_validate_module_entry(entry, known_ids) for entry in raw_catalog["modules"]]
    if not known_ids:
        raise CatalogError("o catálogo deve declarar ao menos um módulo")
    highest_module = max(int(module_id) for module_id in known_ids)
    expected = {f"{number:02d}" for number in range(highest_module + 1)}
    if known_ids != expected:
        missing = ", ".join(sorted(expected - known_ids)) or "nenhum"
        extra = ", ".join(sorted(known_ids - expected)) or "nenhum"
        raise CatalogError(
            "o catálogo deve conter uma sequência contígua a partir de 00; "
            f"ausentes={missing}; extras={extra}"
        )

    for module in modules:
        invalid = set(module["prerequisites"]) - known_ids
        if invalid:
            raise CatalogError(
                f"módulo {module['id']} referencia pré-requisitos inexistentes: {', '.join(sorted(invalid))}"
            )
    return sorted(modules, key=lambda module: int(str(module["id"])))


def _required_string(entry: dict[str, object], key: str, *, label: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{label} deve possuir {key} não vazio")
    return value.strip()


def _load_study_manifest(
    repo_root: Path,
    modules: list[dict[str, object]],
) -> dict[str, object]:
    manifest_path = repo_root / STUDY_MANIFEST
    if manifest_path.is_symlink():
        raise CatalogError(f"{STUDY_MANIFEST} não pode ser link simbólico")
    if not manifest_path.is_file():
        raise CatalogError(f"manifesto de estudos ausente: {manifest_path}")
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CatalogError(f"{STUDY_MANIFEST} inválido: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schemaVersion") != SCHEMA_VERSION:
        raise CatalogError(f"{STUDY_MANIFEST} deve declarar schemaVersion={SCHEMA_VERSION}")

    raw_collections = raw.get("collections")
    if not isinstance(raw_collections, list) or not raw_collections:
        raise CatalogError(f"{STUDY_MANIFEST} deve possuir collections")
    collection_ids: set[str] = set()
    collections: list[dict[str, object]] = []
    for index, value in enumerate(raw_collections):
        if not isinstance(value, dict):
            raise CatalogError("cada collection deve ser um objeto")
        collection_id = _required_string(value, "id", label=f"collection {index}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", collection_id):
            raise CatalogError(f"id de collection inválido: {collection_id}")
        if collection_id in collection_ids:
            raise CatalogError(f"collection duplicada: {collection_id}")
        collection_ids.add(collection_id)
        collections.append(
            {
                "id": collection_id,
                "order": int(value.get("order", index)),
                "kind": _required_string(value, "kind", label=f"collection {collection_id}"),
                "title": _required_string(value, "title", label=f"collection {collection_id}"),
                "description": str(value.get("description", "")).strip(),
            }
        )
    missing_collections = REQUIRED_COLLECTION_IDS - collection_ids
    if missing_collections:
        raise CatalogError("collections obrigatórias ausentes: " + ", ".join(sorted(missing_collections)))

    raw_courses = raw.get("courses")
    if not isinstance(raw_courses, list):
        raise CatalogError(f"{STUDY_MANIFEST} deve possuir courses")
    modules_by_id = {str(module["id"]): module for module in modules}
    courses: list[dict[str, object]] = []
    course_module_ids: set[str] = set()
    legacy_ids: set[str] = set()
    for value in raw_courses:
        if not isinstance(value, dict):
            raise CatalogError("cada course deve ser um objeto")
        module_id = _required_string(value, "moduleId", label="course")
        if module_id not in modules_by_id:
            raise CatalogError(f"course referencia módulo inexistente: {module_id}")
        if module_id in course_module_ids:
            raise CatalogError(f"course duplicado para o módulo {module_id}")
        course_module_ids.add(module_id)

        course_root = _validate_relative_path(
            value.get("courseRoot"),
            label=f"courseRoot do módulo {module_id}",
        )
        overview_path = _validate_relative_path(
            value.get("overviewPath"),
            label=f"overviewPath do módulo {module_id}",
        )
        module_root = PurePosixPath(str(modules_by_id[module_id]["path"]))
        if module_root not in course_root.parents:
            raise CatalogError(f"courseRoot do módulo {module_id} deve ficar dentro de {module_root}")
        if overview_path.parent != module_root:
            raise CatalogError(f"overviewPath do módulo {module_id} deve ficar na raiz de {module_root}")

        course_root_path = _safe_join(repo_root, course_root, label=f"courseRoot do módulo {module_id}")
        overview_file = _safe_join(repo_root, overview_path, label=f"overviewPath do módulo {module_id}")
        _assert_path_components_are_not_symlinks(repo_root, course_root_path)
        _assert_path_components_are_not_symlinks(repo_root, overview_file)
        if not course_root_path.is_dir():
            raise CatalogError(f"courseRoot do módulo {module_id} ausente: {course_root}")
        if not overview_file.is_file():
            raise CatalogError(f"overviewPath do módulo {module_id} ausente: {overview_path}")

        raw_content_paths = value.get("contentPaths", [])
        if not isinstance(raw_content_paths, list) or any(not isinstance(item, str) for item in raw_content_paths):
            raise CatalogError(f"contentPaths do módulo {module_id} deve ser uma lista de caminhos")
        content_paths = [
            _validate_relative_path(item, label=f"contentPath do módulo {module_id}")
            for item in raw_content_paths
        ]
        if len(content_paths) != len(set(content_paths)):
            raise CatalogError(f"contentPaths duplicados no módulo {module_id}")
        for content_path in content_paths:
            resolved_content = _safe_join(
                repo_root,
                content_path,
                label=f"contentPath do módulo {module_id}",
            )
            _assert_path_components_are_not_symlinks(repo_root, resolved_content)
            if not resolved_content.exists():
                raise CatalogError(f"contentPath do módulo {module_id} ausente: {content_path}")

        legacy_id = _required_string(value, "legacyId", label=f"course {module_id}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", legacy_id):
            raise CatalogError(f"legacyId inválido no módulo {module_id}: {legacy_id}")
        if legacy_id in legacy_ids:
            raise CatalogError(f"legacyId duplicado: {legacy_id}")
        legacy_ids.add(legacy_id)
        raw_overrides = value.get("documentOverrides", [])
        if not isinstance(raw_overrides, list):
            raise CatalogError(f"documentOverrides do módulo {module_id} deve ser uma lista")
        document_overrides: list[dict[str, object]] = []
        overridden_paths: set[PurePosixPath] = set()
        overridden_orders: set[int] = set()

        def belongs_to_course(path: PurePosixPath) -> bool:
            return (
                path == overview_path
                or _relative_is_under(path, course_root)
                or any(_relative_is_under(path, adopted) for adopted in content_paths)
            )

        for index, raw_override in enumerate(raw_overrides):
            label = f"documentOverride {index} do módulo {module_id}"
            if not isinstance(raw_override, dict):
                raise CatalogError(f"{label} deve ser um objeto")
            source_path = _validate_relative_path(raw_override.get("sourcePath"), label=f"sourcePath de {label}")
            if source_path in overridden_paths:
                raise CatalogError(f"documentOverrides do módulo {module_id} duplica {source_path}")
            if not belongs_to_course(source_path):
                raise CatalogError(f"{label} aponta para fora da formação: {source_path}")
            if source_path.suffix.casefold() not in {".md", ".markdown"}:
                raise CatalogError(f"{label} deve apontar para Markdown: {source_path}")
            source_file = _safe_join(repo_root, source_path, label=f"sourcePath de {label}")
            _assert_path_components_are_not_symlinks(repo_root, source_file)
            if not source_file.is_file():
                raise CatalogError(f"{label} ausente: {source_path}")

            validated_override: dict[str, object] = {"sourcePath": source_path.as_posix()}
            if "order" in raw_override:
                order = raw_override["order"]
                if isinstance(order, bool) or not isinstance(order, int) or order < 0:
                    raise CatalogError(f"order de {label} deve ser inteiro não negativo")
                if order in overridden_orders:
                    raise CatalogError(f"documentOverrides do módulo {module_id} duplica order={order}")
                overridden_orders.add(order)
                validated_override["order"] = order
            if "required" in raw_override:
                required = raw_override["required"]
                if not isinstance(required, bool):
                    raise CatalogError(f"required de {label} deve ser booleano")
                validated_override["required"] = required
            if "prerequisitePaths" in raw_override:
                raw_prerequisites = raw_override["prerequisitePaths"]
                if not isinstance(raw_prerequisites, list) or any(
                    not isinstance(path, str) for path in raw_prerequisites
                ):
                    raise CatalogError(f"prerequisitePaths de {label} deve ser uma lista de caminhos")
                prerequisite_paths = [
                    _validate_relative_path(path, label=f"pré-requisito de {label}")
                    for path in raw_prerequisites
                ]
                if len(prerequisite_paths) != len(set(prerequisite_paths)):
                    raise CatalogError(f"prerequisitePaths de {label} contém duplicatas")
                for prerequisite_path in prerequisite_paths:
                    if not belongs_to_course(prerequisite_path):
                        raise CatalogError(
                            f"pré-requisito de {label} aponta para fora da formação: {prerequisite_path}"
                        )
                    prerequisite_file = _safe_join(
                        repo_root,
                        prerequisite_path,
                        label=f"pré-requisito de {label}",
                    )
                    _assert_path_components_are_not_symlinks(repo_root, prerequisite_file)
                    if not prerequisite_file.is_file():
                        raise CatalogError(f"pré-requisito de {label} ausente: {prerequisite_path}")
                validated_override["prerequisitePaths"] = [path.as_posix() for path in prerequisite_paths]
            if len(validated_override) == 1:
                raise CatalogError(f"{label} precisa alterar order, required ou prerequisitePaths")
            overridden_paths.add(source_path)
            document_overrides.append(validated_override)

        courses.append(
            {
                "id": f"course-{module_id}",
                "moduleId": module_id,
                "courseRoot": course_root.as_posix(),
                "overviewPath": overview_path.as_posix(),
                "contentPaths": [item.as_posix() for item in content_paths],
                "documentOverrides": document_overrides,
                "legacyId": legacy_id,
                "legacyTitle": _required_string(value, "legacyTitle", label=f"course {module_id}"),
            }
        )
    expected_module_ids = set(modules_by_id)
    if course_module_ids != expected_module_ids:
        missing = expected_module_ids - course_module_ids
        extra = course_module_ids - expected_module_ids
        raise CatalogError(
            "courses deve cobrir todos os módulos declarados; "
            f"ausentes={', '.join(sorted(missing)) or 'nenhum'}; "
            f"extras={', '.join(sorted(extra)) or 'nenhum'}"
        )

    claimed_paths: list[tuple[str, PurePosixPath]] = []
    course_roots = [PurePosixPath(str(course["courseRoot"])) for course in courses]
    overview_paths = [PurePosixPath(str(course["overviewPath"])) for course in courses]
    for course in courses:
        module_id = str(course["moduleId"])
        for raw_path in course["contentPaths"]:
            content_path = PurePosixPath(str(raw_path))
            for owner_id, claimed in claimed_paths:
                if (
                    content_path == claimed
                    or _relative_is_under(content_path, claimed)
                    or _relative_is_under(claimed, content_path)
                ):
                    raise CatalogError(
                        f"contentPaths sobrepostos entre os módulos {owner_id} e {module_id}: "
                        f"{claimed} / {content_path}"
                    )
            if any(
                content_path == root
                or _relative_is_under(content_path, root)
                or _relative_is_under(root, content_path)
                for root in course_roots
            ):
                raise CatalogError(f"contentPath adotado sobrepõe courseRoot: {content_path}")
            if any(content_path == overview for overview in overview_paths):
                raise CatalogError(f"contentPath adotado não pode ser overviewPath: {content_path}")
            claimed_paths.append((module_id, content_path))

    global_documents = raw.get("globalDocuments")
    resources = raw.get("resources")
    if not isinstance(global_documents, dict) or global_documents.get("includeAllOutsideModules") is not True:
        raise CatalogError("globalDocuments.includeAllOutsideModules deve ser true")
    if global_documents.get("collectionId") != DOCUMENTATION_COLLECTION:
        raise CatalogError(f"globalDocuments.collectionId deve ser {DOCUMENTATION_COLLECTION}")
    included_document_paths = global_documents.get("includePaths", [])
    if not isinstance(included_document_paths, list):
        raise CatalogError("globalDocuments.includePaths deve ser uma lista")
    validated_included_paths = [
        _validate_relative_path(value, label="documento global incluído").as_posix()
        for value in included_document_paths
    ]
    if len(validated_included_paths) != len(set(validated_included_paths)):
        raise CatalogError("globalDocuments.includePaths contém caminhos duplicados")
    module_roots = [PurePosixPath(str(module["path"])) for module in modules]
    for included_value in validated_included_paths:
        included = PurePosixPath(included_value)
        if included.suffix.casefold() not in {".md", ".markdown"}:
            raise CatalogError(f"documento global incluído deve ser Markdown: {included}")
        if any(_relative_is_under(included, module_root) for module_root in module_roots):
            raise CatalogError(f"documento global incluído não pode duplicar um módulo: {included}")
        included_file = _safe_join(repo_root, included, label="documento global incluído")
        _assert_path_components_are_not_symlinks(repo_root, included_file)
        if not included_file.is_file():
            raise CatalogError(f"documento global incluído ausente: {included}")
    if not isinstance(resources, dict) or resources.get("includeAllSafeFiles") is not True:
        raise CatalogError("resources.includeAllSafeFiles deve ser true")
    if resources.get("collectionId") != RESOURCE_COLLECTION:
        raise CatalogError(f"resources.collectionId deve ser {RESOURCE_COLLECTION}")
    included_resource_paths = resources.get("includePaths", [])
    if not isinstance(included_resource_paths, list):
        raise CatalogError("resources.includePaths deve ser uma lista")
    validated_resource_paths = [
        _validate_relative_path(value, label="recurso explícito incluído").as_posix()
        for value in included_resource_paths
    ]
    if len(validated_resource_paths) != len(set(validated_resource_paths)):
        raise CatalogError("resources.includePaths contém caminhos duplicados")
    if set(validated_resource_paths).intersection(validated_included_paths):
        raise CatalogError("um includePath não pode ser documento e recurso ao mesmo tempo")
    for included_value in validated_resource_paths:
        included = PurePosixPath(included_value)
        if included.suffix.casefold() in {".md", ".markdown"}:
            raise CatalogError(f"recurso explícito Markdown deve estar em globalDocuments: {included}")
        included_file = _safe_join(repo_root, included, label="recurso explícito incluído")
        _assert_path_components_are_not_symlinks(repo_root, included_file)
        if not included_file.is_file():
            raise CatalogError(f"recurso explícito incluído ausente: {included}")

    exclusions = raw.get("exclusions", {})
    if not isinstance(exclusions, dict):
        raise CatalogError("exclusions deve ser um objeto")
    exclusion_roots = exclusions.get("roots", [])
    exclusion_paths = exclusions.get("paths", [])
    if not isinstance(exclusion_roots, list) or not isinstance(exclusion_paths, list):
        raise CatalogError("exclusions.roots e exclusions.paths devem ser listas")
    validated_roots = [_validate_relative_path(value, label="raiz excluída").as_posix() for value in exclusion_roots]
    validated_paths = [_validate_relative_path(value, label="arquivo excluído").as_posix() for value in exclusion_paths]
    if len(validated_roots) != len(set(validated_roots)) or len(validated_paths) != len(set(validated_paths)):
        raise CatalogError("exclusions contém caminhos duplicados")
    included_exceptions = set(validated_included_paths) | set(validated_resource_paths)
    conflicts = included_exceptions.intersection(validated_paths)
    if conflicts:
        raise CatalogError("includePaths também foram excluídos: " + ", ".join(sorted(conflicts)))

    return {
        "schemaVersion": SCHEMA_VERSION,
        "collections": sorted(collections, key=lambda item: (int(item["order"]), str(item["id"]))),
        "courses": sorted(courses, key=lambda item: int(str(item["moduleId"]))),
        "exclusionRoots": sorted(validated_roots),
        "exclusionPaths": sorted(validated_paths),
        "includedDocumentPaths": sorted(validated_included_paths),
        "includedResourcePaths": sorted(validated_resource_paths),
        "exclusionReason": str(exclusions.get("reason", "")).strip(),
    }


def _public_document(document: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in document.items() if not key.startswith("_")}


def _entity_has_membership(entity: dict[str, object], collection_id: str) -> bool:
    memberships = entity.get("memberships", [])
    return isinstance(memberships, list) and any(
        isinstance(membership, dict) and membership.get("collectionId") == collection_id for membership in memberships
    )


def _build_labs(
    documents: list[dict[str, object]],
    resources: list[dict[str, object]],
) -> list[dict[str, object]]:
    solutions = [document for document in documents if document.get("role") == "solution"]
    labs: list[dict[str, object]] = []
    for document in documents:
        if document.get("role") != "lab_instruction":
            continue
        relative = document["_relativePath"]
        assert isinstance(relative, PurePosixPath)
        lab_root = _lab_root(relative)
        solution_ids = []
        if lab_root is not None:
            solution_ids = sorted(
                str(solution["id"])
                for solution in solutions
                if solution.get("module") == document.get("module") and _lab_root(solution["_relativePath"]) == lab_root
            )
        resource_ids = set(document.get("assetIds", []))
        if lab_root is not None:
            resource_ids.update(
                str(resource["id"])
                for resource in resources
                if _relative_is_under(PurePosixPath(str(resource["sourcePath"])), lab_root)
            )
        document["solutionIds"] = solution_ids
        document["labId"] = document["id"]
        labs.append(
            {
                "id": document["id"],
                "order": len(labs),
                "title": document["title"],
                "description": document["description"],
                "instructionDocumentId": document["id"],
                "prerequisiteDocumentIds": list(document["prerequisites"]),
                "resourceIds": sorted(resource_ids),
                "solutionDocumentIds": solution_ids,
                "moduleId": document.get("module") or None,
                "courseId": document.get("courseId"),
                "legacySectionId": document.get("legacySectionId"),
                "origin": document["origin"],
                "required": bool(document["required"]),
                "memberships": list(document["memberships"]),
                "safety": "Execute somente no laboratório local e autorizado descrito no material.",
            }
        )
    return labs


def _build_projects(
    documents: list[dict[str, object]],
    resources: list[dict[str, object]],
    module_sources: list[dict[str, object]],
    courses_by_module: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    roots: set[PurePosixPath] = set()
    for document in documents:
        relative = document["_relativePath"]
        assert isinstance(relative, PurePosixPath)
        root = _project_root(relative)
        if root is not None:
            roots.add(root)
    for resource in resources:
        root = _project_root(PurePosixPath(str(resource["sourcePath"])))
        if root is not None:
            roots.add(root)

    projects: list[dict[str, object]] = []
    for order, root in enumerate(sorted(roots, key=lambda value: value.as_posix().casefold())):
        project_id = f"project-{hashlib.sha256(root.as_posix().encode('utf-8')).hexdigest()[:20]}"
        project_documents = [document for document in documents if _project_root(document["_relativePath"]) == root]
        project_resources = [
            resource for resource in resources if _project_root(PurePosixPath(str(resource["sourcePath"]))) == root
        ]
        module_id, course, origin = _course_context_for_path(root, module_sources, courses_by_module)
        course_id = str(course["id"]) if course is not None and origin == "formation" else None
        legacy_section_id = f"legacy-{course['legacyId']}" if course is not None and origin == "legacy" else None
        readme = next(
            (document for document in project_documents if document.get("role") == "project_readme"),
            None,
        )
        memberships = [_membership(PRACTICE_COLLECTION, module_id=module_id, course_id=course_id)]
        projects.append(
            {
                "id": project_id,
                "order": order,
                "title": str(readme["title"]) if readme else root.name.replace("-", " ").title(),
                "rootPath": root.as_posix(),
                "readmeDocumentId": readme["id"] if readme else None,
                "documentIds": sorted(str(document["id"]) for document in project_documents),
                "resourceIds": sorted(str(resource["id"]) for resource in project_resources),
                "moduleId": module_id,
                "courseId": course_id,
                "legacySectionId": legacy_section_id,
                "origin": origin,
                "memberships": memberships,
            }
        )
    return projects


def _build_courses_and_legacy_sections(
    manifest: dict[str, object],
    module_results: list[dict[str, object]],
    documents: list[dict[str, object]],
    resources: list[dict[str, object]],
    labs: list[dict[str, object]],
    projects: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    modules_by_id = {str(module["id"]): module for module in module_results}
    courses: list[dict[str, object]] = []
    legacy_sections: list[dict[str, object]] = []
    for order, source in enumerate(manifest["courses"]):
        module_id = str(source["moduleId"])
        module = modules_by_id[module_id]
        course_documents = [
            document
            for document in documents
            if document.get("module") == module_id and document.get("origin") == "formation"
        ]
        legacy_documents = [
            document
            for document in documents
            if document.get("module") == module_id and document.get("origin") == "legacy"
        ]
        course_resources = [
            resource
            for resource in resources
            if resource.get("moduleId") == module_id and resource.get("origin") == "formation"
        ]
        legacy_resources = [
            resource
            for resource in resources
            if resource.get("moduleId") == module_id and resource.get("origin") == "legacy"
        ]
        course_id = str(source["id"])
        legacy_section_id = f"legacy-{source['legacyId']}"
        course_labs = [lab for lab in labs if lab.get("courseId") == course_id]
        legacy_labs = [lab for lab in labs if lab.get("legacySectionId") == legacy_section_id]
        course_projects = [project for project in projects if project.get("courseId") == course_id]
        legacy_projects = [project for project in projects if project.get("legacySectionId") == legacy_section_id]
        courses.append(
            {
                "id": course_id,
                "order": order,
                "moduleId": module_id,
                "trackId": module["trackId"],
                "title": module["title"],
                "description": module["description"],
                "rootPath": source["courseRoot"],
                "contentPaths": list(source.get("contentPaths", [])),
                "overviewDocumentIds": [
                    document["id"]
                    for document in course_documents
                    if document["role"] in {"module_overview", "course_overview"}
                ],
                "documentIds": [document["id"] for document in course_documents],
                "requiredDocumentIds": [document["id"] for document in course_documents if document["required"]],
                "optionalDocumentIds": [document["id"] for document in course_documents if not document["required"]],
                "resourceIds": [resource["id"] for resource in course_resources],
                "labIds": [lab["id"] for lab in course_labs],
                "projectIds": [project["id"] for project in course_projects],
            }
        )
        if legacy_documents or legacy_resources or legacy_labs or legacy_projects:
            legacy_sections.append(
                {
                    "id": legacy_section_id,
                    "order": order,
                    "moduleId": module_id,
                    "title": source["legacyTitle"],
                    "containerPath": module["path"],
                    "excludedCourseRoot": source["courseRoot"],
                    "documentIds": [document["id"] for document in legacy_documents],
                    "resourceIds": [resource["id"] for resource in legacy_resources],
                    "labIds": [lab["id"] for lab in legacy_labs],
                    "projectIds": [project["id"] for project in legacy_projects],
                    "requiredDocumentIds": [],
                }
            )
    return courses, legacy_sections


def _build_collections(
    manifest: dict[str, object],
    tracks: list[dict[str, object]],
    courses: list[dict[str, object]],
    legacy_sections: list[dict[str, object]],
    documents: list[dict[str, object]],
    resources: list[dict[str, object]],
    labs: list[dict[str, object]],
    projects: list[dict[str, object]],
) -> list[dict[str, object]]:
    collections: list[dict[str, object]] = []
    for source in manifest["collections"]:
        collection_id = str(source["id"])
        collections.append(
            {
                **source,
                "trackIds": [track["id"] for track in tracks] if collection_id == FORMATION_COLLECTION else [],
                "courseIds": [course["id"] for course in courses] if collection_id == FORMATION_COLLECTION else [],
                "sectionIds": [section["id"] for section in legacy_sections]
                if collection_id == LEGACY_COLLECTION
                else [],
                "documentIds": [
                    document["id"] for document in documents if _entity_has_membership(document, collection_id)
                ],
                "resourceIds": [
                    resource["id"] for resource in resources if _entity_has_membership(resource, collection_id)
                ],
                "labIds": [lab["id"] for lab in labs] if collection_id == PRACTICE_COLLECTION else [],
                "projectIds": [project["id"] for project in projects] if collection_id == PRACTICE_COLLECTION else [],
            }
        )
    return collections


def assemble_catalog(repo_root: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Monta o catálogo em memória e retorna também os documentos internos."""
    if repo_root.is_symlink():
        raise CatalogError(f"a raiz do repositório não pode ser link simbólico: {repo_root}")
    repo_root = repo_root.resolve(strict=True)
    modules_from_source = _load_module_catalog(repo_root)
    manifest = _load_study_manifest(repo_root, modules_from_source)
    courses_by_module = {str(course["moduleId"]): course for course in manifest["courses"]}
    repository_files, explicit_exclusions = _iter_repository_files(repo_root, manifest)
    markdown_files = [path for path in repository_files if path.suffix.casefold() in {".md", ".markdown"}]

    module_results: list[dict[str, object]] = []
    all_documents: list[dict[str, object]] = []
    source_paths: set[str] = set()
    document_ids: set[str] = set()
    module_roots: list[PurePosixPath] = []

    for module_source in modules_from_source:
        module_id = str(module_source["id"])
        module_relative = _validate_relative_path(module_source["path"], label=f"path do módulo {module_id}")
        module_root = _safe_join(repo_root, module_relative, label=f"módulo {module_id}")
        if module_root.is_symlink() or not module_root.is_dir():
            raise CatalogError(f"diretório do módulo {module_id} ausente ou simbólico: {module_root}")
        module_roots.append(module_relative)

        module_documents = []
        for source_file in markdown_files:
            relative_source = PurePosixPath(source_file.relative_to(repo_root).as_posix())
            owner_module_id, _owner_course, _owner_origin = _course_context_for_path(
                relative_source,
                modules_from_source,
                courses_by_module,
            )
            if owner_module_id == module_id:
                module_documents.append(_read_source_document(repo_root, module_id, source_file))
        if not module_documents:
            raise CatalogError(f"módulo {module_id} não contém Markdown")

        course = courses_by_module[module_id]
        for document in module_documents:
            _classify_document(document, course)

        _apply_document_overrides(module_documents, course)
        _assign_lab_prerequisites(module_documents)
        module_documents.sort(key=_document_sort_key)
        for order, document in enumerate(module_documents):
            document["order"] = order
            source_path = str(document["sourcePath"])
            document_id = str(document["id"])
            if source_path in source_paths:
                raise CatalogError(f"sourcePath duplicado: {source_path}")
            if document_id in document_ids:
                raise CatalogError(f"colisão de id de documento: {document_id}")
            source_paths.add(source_path)
            document_ids.add(document_id)

        track = _track_for_module(module_id)
        type_counts = {
            document_type: sum(document["type"] == document_type for document in module_documents)
            for document_type in TYPE_ORDER
        }
        module_result = {
            "id": module_id,
            "order": int(module_id),
            "trackId": track["id"],
            "path": module_source["path"],
            "title": module_source["title"],
            "description": _module_description(module_documents, str(module_source["title"])),
            "status": module_source.get("status", "unknown"),
            "maturity": module_source.get("maturity", "unknown"),
            "estimatedHours": module_source.get("estimatedHours", {}),
            "prerequisiteModuleIds": list(module_source["prerequisites"]),
            "courseId": course["id"],
            "legacySectionId": f"legacy-{course['legacyId']}",
            "documentIds": [document["id"] for document in module_documents],
            "requiredDocumentIds": [document["id"] for document in module_documents if document["required"]],
            "optionalDocumentIds": [document["id"] for document in module_documents if not document["required"]],
            "chapterIds": [document["id"] for document in module_documents if document["type"] == "chapter"],
            "labIds": [document["id"] for document in module_documents if document["role"] == "lab_instruction"],
            "referenceIds": [document["id"] for document in module_documents if document["type"] == "reference"],
            "stats": {
                "documents": len(module_documents),
                "requiredDocuments": sum(bool(document["required"]) for document in module_documents),
                "words": sum(int(document["words"]) for document in module_documents),
                "readingMinutes": sum(int(document["readingMinutes"]) for document in module_documents),
                "byType": type_counts,
                "byRole": {role: sum(document["role"] == role for document in module_documents) for role in ROLE_ORDER},
            },
        }
        module_results.append(module_result)
        all_documents.extend(module_documents)

    global_markdown = []
    for source in markdown_files:
        relative_source = PurePosixPath(source.relative_to(repo_root).as_posix())
        owner_module_id, _owner_course, _owner_origin = _course_context_for_path(
            relative_source,
            modules_from_source,
            courses_by_module,
        )
        if owner_module_id is None:
            global_markdown.append(source)
    global_documents = [_read_source_document(repo_root, None, source) for source in global_markdown]
    for document in global_documents:
        _classify_document(document, None)
    global_documents.sort(key=_document_sort_key)
    for order, document in enumerate(global_documents):
        document["order"] = order
        source_path = str(document["sourcePath"])
        document_id = str(document["id"])
        if source_path in source_paths:
            raise CatalogError(f"sourcePath duplicado: {source_path}")
        if document_id in document_ids:
            raise CatalogError(f"colisão de id de documento: {document_id}")
        source_paths.add(source_path)
        document_ids.add(document_id)
    all_documents.extend(global_documents)

    for global_order, document in enumerate(all_documents):
        document["globalOrder"] = global_order

    assets, asset_link_stats, unsafe_resources = _discover_all_resources(
        repo_root,
        repository_files,
        all_documents,
        modules_from_source,
        courses_by_module,
        set(manifest["includedResourcePaths"]),
    )
    resources = [asset for asset in assets if "aliasOfDocumentId" not in asset]
    assets_by_id = {str(asset["id"]): asset for asset in assets}
    documents_by_id = {str(document["id"]): document for document in all_documents}
    for module in module_results:
        module_asset_ids = sorted(
            {
                str(asset_id)
                for document_id in module["documentIds"]
                for asset_id in documents_by_id[str(document_id)]["assetIds"]
            }
        )
        module["assetIds"] = module_asset_ids
        module["resourceIds"] = [resource["id"] for resource in resources if resource.get("moduleId") == module["id"]]
        module["stats"]["assets"] = len(module_asset_ids)
        module["stats"]["assetBytes"] = sum(int(assets_by_id[asset_id]["bytes"]) for asset_id in module_asset_ids)
        module["stats"]["resources"] = len(module["resourceIds"])

    track_results: list[dict[str, object]] = []
    for track in TRACKS:
        module_ids = [module["id"] for module in module_results if module["trackId"] == track["id"]]
        if not module_ids:
            continue
        track_results.append(
            {
                "id": track["id"],
                "order": track["order"],
                "title": track["title"],
                "description": track["description"],
                "moduleIds": module_ids,
                "courseIds": [f"course-{module_id}" for module_id in module_ids],
                "collectionId": FORMATION_COLLECTION,
            }
        )

    labs = _build_labs(all_documents, resources)
    projects = _build_projects(all_documents, resources, modules_from_source, courses_by_module)
    courses, legacy_sections = _build_courses_and_legacy_sections(
        manifest,
        module_results,
        all_documents,
        resources,
        labs,
        projects,
    )
    available_legacy_sections = {str(section["id"]) for section in legacy_sections}
    for module in module_results:
        if module.get("legacySectionId") not in available_legacy_sections:
            module["legacySectionId"] = None
    collections = _build_collections(
        manifest,
        track_results,
        courses,
        legacy_sections,
        all_documents,
        resources,
        labs,
        projects,
    )

    unassigned_documents = [document for document in all_documents if not document.get("memberships")]
    unassigned_resources = [resource for resource in resources if not resource.get("memberships")]
    if unassigned_documents or unassigned_resources:
        raise CatalogError(
            "cobertura incompleta: "
            f"{len(unassigned_documents)} documentos e {len(unassigned_resources)} recursos sem coleção"
        )

    public_documents = [_public_document(document) for document in all_documents]
    category_counts: dict[str, int] = {}
    for entity in (*public_documents, *resources):
        category = str(entity["category"])
        category_counts[category] = category_counts.get(category, 0) + 1
    unsafe_by_kind = unsafe_resources["byExtension"]
    assert isinstance(unsafe_by_kind, dict)
    unsafe_count = sum(int(value) for value in unsafe_by_kind.values())
    coverage = {
        "eligible": len(public_documents) + len(resources),
        "assigned": len(public_documents) + len(resources),
        "excluded": unsafe_count,
        "unassigned": 0,
        "markdown": {
            "eligible": len(public_documents),
            "assigned": len(public_documents),
            "excluded": 0,
            "unassigned": 0,
        },
        "resources": {
            "eligible": len(resources),
            "assigned": len(resources),
            "excluded": unsafe_count,
            "unassigned": 0,
        },
        "byCategory": {
            category: {
                "eligible": count,
                "assigned": count,
                "excluded": 0,
                "unassigned": 0,
            }
            for category, count in sorted(category_counts.items())
        },
        "unsafeExcludedByExtension": unsafe_by_kind,
        "unsafeExcludedPaths": unsafe_resources["paths"],
        "explicitExclusions": explicit_exclusions,
    }
    catalog = {
        "schemaVersion": SCHEMA_VERSION,
        "collections": collections,
        "tracks": track_results,
        "modules": module_results,
        "courses": courses,
        "legacySections": legacy_sections,
        "documents": public_documents,
        "globalDocumentIds": [document["id"] for document in global_documents],
        "labs": labs,
        "projects": projects,
        "resources": resources,
        "assets": assets,
        "stats": {
            "tracks": len(track_results),
            "modules": len(module_results),
            "courses": len(courses),
            "legacySections": len(legacy_sections),
            "collections": len(collections),
            "documents": len(public_documents),
            "requiredDocuments": sum(bool(document["required"]) for document in public_documents),
            "legacyDocuments": sum(document["origin"] == "legacy" for document in public_documents),
            "globalDocuments": len(global_documents),
            "chapters": sum(document["type"] == "chapter" for document in public_documents),
            "labs": len(labs),
            "projects": len(projects),
            "references": sum(document["type"] == "reference" for document in public_documents),
            "words": sum(int(document["words"]) for document in public_documents),
            "readingMinutes": sum(int(document["readingMinutes"]) for document in public_documents),
            "resources": len(resources),
            "resourceAliases": len(assets) - len(resources),
            "assets": len(assets),
            "assetBytes": sum(int(asset["bytes"]) for asset in assets),
            "coverage": coverage,
            **asset_link_stats,
        },
    }
    return catalog, all_documents


def _validate_output_location(repo_root: Path, output_directory: Path, module_paths: list[str]) -> Path:
    output_absolute = output_directory.absolute()
    _assert_no_symlink_ancestors(output_absolute, label="diretório de saída")
    output_resolved = output_absolute.resolve(strict=False)

    if output_resolved == Path(output_resolved.anchor):
        raise CatalogError("a raiz do sistema não pode ser usada como diretório de saída")
    for module_path in module_paths:
        module_root = (repo_root / module_path).resolve(strict=True)
        if output_resolved == module_root or module_root in output_resolved.parents:
            raise CatalogError(f"a saída não pode ficar dentro de um módulo: {module_path}")
    if output_absolute.exists() and not output_absolute.is_dir():
        raise CatalogError(f"a saída existe e não é diretório: {output_absolute}")
    return output_absolute


def _verify_generated_tree(tree: Path) -> None:
    if tree.is_symlink():
        raise CatalogError(f"diretório gerado não pode ser link simbólico: {tree}")
    for current, directory_names, file_names in os.walk(tree, followlinks=False):
        current_path = Path(current)
        for name in (*directory_names, *file_names):
            candidate = current_path / name
            if candidate.is_symlink():
                raise CatalogError(f"link simbólico encontrado na saída gerada: {candidate}")


def _prepare_output(output_directory: Path) -> None:
    marker = output_directory / GENERATED_MARKER
    content_directory = output_directory / "content"
    catalog_file = output_directory / "catalog.json"

    if output_directory.exists():
        if marker.is_symlink() or content_directory.is_symlink() or catalog_file.is_symlink():
            raise CatalogError("a saída gerada não pode conter links simbólicos")
        has_managed_files = content_directory.exists() or catalog_file.exists()
        if has_managed_files and not marker.is_file():
            raise CatalogError(f"recusado sobrescrever saída sem marcador de propriedade: {output_directory}")
        if marker.is_file() and marker.read_text(encoding="utf-8") != MARKER_CONTENT:
            raise CatalogError(f"marcador de saída desconhecido: {marker}")

    output_directory.mkdir(parents=True, exist_ok=True)
    if content_directory.exists():
        if not content_directory.is_dir():
            raise CatalogError(f"content existe e não é diretório: {content_directory}")
        _verify_generated_tree(content_directory)
        shutil.rmtree(content_directory)
    content_directory.mkdir()


def _atomic_write_text(target: Path, content: str) -> None:
    temporary = target.with_name(f".{target.name}.tmp")
    if temporary.is_symlink() or target.is_symlink():
        raise CatalogError(f"arquivo de saída simbólico recusado: {target}")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    os.replace(temporary, target)


def write_catalog(
    repo_root: Path,
    output_directory: Path,
    catalog: dict[str, object],
    internal_documents: list[dict[str, object]],
) -> Path:
    """Copia os Markdown e grava ``catalog.json`` de forma determinística."""
    raw_modules = catalog.get("modules")
    if not isinstance(raw_modules, list) or not all(isinstance(module, dict) for module in raw_modules):
        raise CatalogError("catálogo interno possui módulos inválidos")
    module_paths = [str(module["path"]) for module in raw_modules]
    output_directory = _validate_output_location(repo_root, output_directory, module_paths)
    _prepare_output(output_directory)
    content_root = output_directory / "content"

    for document in internal_documents:
        relative = _validate_relative_path(document["sourcePath"], label="sourcePath de saída")
        destination = _safe_join(content_root, relative, label="cópia de Markdown")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink():
            raise CatalogError(f"destino simbólico recusado: {destination}")
        content = document["_content"]
        assert isinstance(content, bytes)
        destination.write_bytes(content)

    raw_assets = catalog.get("assets")
    if not isinstance(raw_assets, list) or not all(isinstance(asset, dict) for asset in raw_assets):
        raise CatalogError("catálogo interno possui assets inválidos")
    for asset in raw_assets:
        relative = _validate_relative_path(asset.get("sourcePath"), label="sourcePath de asset")
        source = _safe_join(repo_root, relative, label="asset de origem")
        _assert_path_components_are_not_symlinks(repo_root, source)
        if _asset_path_is_forbidden(repo_root, source):
            raise CatalogError(f"asset aponta para diretório proibido: {relative}")
        safe_asset = _read_safe_asset(source)
        if safe_asset is None and asset.get("explicitlyAllowed") is True:
            safe_asset = _read_explicit_text_resource(source)
        if safe_asset is None:
            raise CatalogError(f"asset deixou de ser seguro durante a geração: {relative}")
        kind, content = safe_asset
        if kind != asset.get("kind") or len(content) != asset.get("bytes"):
            raise CatalogError(f"asset mudou durante a geração: {relative}")
        destination = _safe_join(content_root, relative, label="cópia de asset")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink():
            raise CatalogError(f"destino simbólico recusado: {destination}")
        destination.write_bytes(content)

    serialized = json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    catalog_path = output_directory / "catalog.json"
    _atomic_write_text(catalog_path, serialized)
    _atomic_write_text(output_directory / GENERATED_MARKER, MARKER_CONTENT)
    return catalog_path


def build_catalog(repo_root: Path, output_directory: Path) -> Path:
    """Monta, valida e grava o catálogo; retorna o caminho de ``catalog.json``."""
    catalog, internal_documents = assemble_catalog(repo_root)
    resolved_root = repo_root.resolve(strict=True)
    return write_catalog(resolved_root, output_directory, catalog, internal_documents)


def _argument_parser() -> argparse.ArgumentParser:
    default_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_root,
        help="raiz que contém MODULE-CATALOG.json (padrão: detectada pelo script)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="diretório gerado (padrão: study-app/public/generated)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _argument_parser().parse_args(argv)
    repo_root = args.repo_root
    output_directory = args.output or repo_root / "study-app/public/generated"
    try:
        catalog_path = build_catalog(repo_root, output_directory)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (CatalogError, OSError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 1

    stats = catalog["stats"]
    print(
        "[OK] catálogo gerado em "
        f"{catalog_path}: {stats['modules']} módulos, "
        f"{stats['documents']} documentos, {stats['labs']} laboratórios "
        f"e {stats['assets']} assets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
