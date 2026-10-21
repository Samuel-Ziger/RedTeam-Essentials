#!/usr/bin/env python3
"""Valida, sem rede, a integracao da aplicacao local de estudos."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "study-app"
LAUNCHER = ROOT / "estudo.sh"
STUDY_MANIFEST = ROOT / "STUDY-CONTENT.json"
MODULE_CATALOG = ROOT / "MODULE-CATALOG.json"

REQUIRED_FILES = (
    LAUNCHER,
    STUDY_MANIFEST,
    MODULE_CATALOG,
    APP / "README.md",
    APP / "index.html",
    APP / "package.json",
    APP / "package-lock.json",
    APP / "vite.config.js",
    APP / "scripts/build_catalog.py",
    APP / "src/App.jsx",
    APP / "src/main.jsx",
    APP / "src/styles.css",
)
REQUIRED_PACKAGE_SCRIPTS = {"dev", "test", "build"}
REQUIRED_DEPENDENCIES = {"react", "react-dom", "react-markdown", "rehype-sanitize"}
REQUIRED_COLLECTIONS = {
    "formacao-principal",
    "acervo-seguranca",
    "laboratorios-projetos",
    "ferramentas-codigo",
    "documentacao-global",
}
IGNORED_RUNTIME_PATHS = (
    "study-app/node_modules/",
    "study-app/dist/",
    "study-app/public/generated/",
)
SECRET_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
}
SECRET_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
)


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"JSON invalido em {path.relative_to(ROOT)}: {exc}")
        return None


def validate_package(errors: list[str]) -> None:
    package = load_json(APP / "package.json", errors)
    lock = load_json(APP / "package-lock.json", errors)
    if not isinstance(package, dict):
        return

    if package.get("private") is not True:
        errors.append("study-app/package.json deve declarar private=true")
    scripts = package.get("scripts")
    if not isinstance(scripts, dict):
        errors.append("study-app/package.json nao possui scripts validos")
    else:
        missing_scripts = REQUIRED_PACKAGE_SCRIPTS - scripts.keys()
        if missing_scripts:
            errors.append(f"scripts npm ausentes: {', '.join(sorted(missing_scripts))}")
        lifecycle = {"preinstall", "install", "postinstall"} & scripts.keys()
        if lifecycle:
            errors.append(f"scripts npm de instalacao nao permitidos: {', '.join(sorted(lifecycle))}")

    dependencies = package.get("dependencies")
    if not isinstance(dependencies, dict):
        errors.append("study-app/package.json nao possui dependencies validas")
    else:
        missing_dependencies = REQUIRED_DEPENDENCIES - dependencies.keys()
        if missing_dependencies:
            errors.append("dependencias essenciais ausentes: " + ", ".join(sorted(missing_dependencies)))

    engines = package.get("engines")
    node_engine = engines.get("node", "") if isinstance(engines, dict) else ""
    if node_engine != ">=22.12.0":
        errors.append("engines.node deve ser '>=22.12.0'")

    if not isinstance(lock, dict):
        return
    if lock.get("lockfileVersion") not in {2, 3}:
        errors.append("package-lock.json deve usar lockfileVersion 2 ou 3")
    if lock.get("name") != package.get("name"):
        errors.append("package-lock.json diverge do nome em package.json")
    locked_packages = lock.get("packages")
    locked_root = locked_packages.get("") if isinstance(locked_packages, dict) else None
    if not isinstance(locked_root, dict):
        errors.append("package-lock.json nao possui a entrada raiz packages['']")
        return
    for field in ("dependencies", "devDependencies", "engines"):
        if locked_root.get(field, {}) != package.get(field, {}):
            errors.append(f"package-lock.json diverge de package.json em {field}")


def validate_study_manifest(errors: list[str]) -> None:
    manifest = load_json(STUDY_MANIFEST, errors)
    module_catalog = load_json(MODULE_CATALOG, errors)
    if not isinstance(manifest, dict):
        return
    if manifest.get("schemaVersion") != 2:
        errors.append("STUDY-CONTENT.json deve declarar schemaVersion=2")

    collections = manifest.get("collections")
    if not isinstance(collections, list):
        errors.append("STUDY-CONTENT.json nao possui collections validas")
    else:
        collection_ids = {
            value.get("id") for value in collections if isinstance(value, dict) and isinstance(value.get("id"), str)
        }
        missing = REQUIRED_COLLECTIONS - collection_ids
        if missing:
            errors.append("colecoes essenciais ausentes: " + ", ".join(sorted(missing)))

    courses = manifest.get("courses")
    catalog_modules = module_catalog.get("modules", []) if isinstance(module_catalog, dict) else []
    expected_module_ids = {
        value.get("id")
        for value in catalog_modules
        if isinstance(value, dict) and isinstance(value.get("id"), str)
    }
    if not isinstance(courses, list):
        errors.append("STUDY-CONTENT.json nao possui courses validos")
    else:
        module_ids = {
            value.get("moduleId")
            for value in courses
            if isinstance(value, dict) and isinstance(value.get("moduleId"), str)
        }
        if module_ids != expected_module_ids or len(courses) != len(expected_module_ids):
            missing = expected_module_ids - module_ids
            extra = module_ids - expected_module_ids
            errors.append(
                "courses deve mapear exatamente os modulos do catalogo; "
                f"ausentes={','.join(sorted(missing)) or 'nenhum'}; "
                f"extras={','.join(sorted(extra)) or 'nenhum'}"
            )
        for course in courses:
            if not isinstance(course, dict):
                errors.append("cada course deve ser um objeto")
                continue
            for field in ("courseRoot", "overviewPath", "legacyId", "legacyTitle"):
                if not isinstance(course.get(field), str) or not course[field].strip():
                    errors.append(f"course {course.get('moduleId', '?')} nao possui {field}")
            content_paths = course.get("contentPaths", [])
            if not isinstance(content_paths, list) or any(not isinstance(item, str) for item in content_paths):
                errors.append(f"course {course.get('moduleId', '?')} possui contentPaths invalido")
            overrides = course.get("documentOverrides", [])
            if not isinstance(overrides, list):
                errors.append(f"course {course.get('moduleId', '?')} possui documentOverrides invalido")
                continue
            seen_paths: set[str] = set()
            seen_orders: set[int] = set()
            for override in overrides:
                if not isinstance(override, dict):
                    errors.append(f"course {course.get('moduleId', '?')} possui documentOverride nao-objeto")
                    continue
                source_path = override.get("sourcePath")
                if not isinstance(source_path, str) or not source_path.strip():
                    errors.append(f"course {course.get('moduleId', '?')} possui override sem sourcePath")
                elif source_path in seen_paths:
                    errors.append(f"course {course.get('moduleId', '?')} duplica override de {source_path}")
                else:
                    seen_paths.add(source_path)
                if "order" in override:
                    order = override["order"]
                    if isinstance(order, bool) or not isinstance(order, int) or order < 0:
                        errors.append(f"course {course.get('moduleId', '?')} possui order de override invalido")
                    elif order in seen_orders:
                        errors.append(f"course {course.get('moduleId', '?')} duplica order de override {order}")
                    else:
                        seen_orders.add(order)
                if "required" in override and not isinstance(override["required"], bool):
                    errors.append(f"course {course.get('moduleId', '?')} possui required de override invalido")
                prerequisites = override.get("prerequisitePaths", [])
                if not isinstance(prerequisites, list) or any(not isinstance(item, str) for item in prerequisites):
                    errors.append(
                        f"course {course.get('moduleId', '?')} possui prerequisitePaths de override invalido"
                    )

    global_documents = manifest.get("globalDocuments")
    resources = manifest.get("resources")
    if not isinstance(global_documents, dict) or global_documents.get("includeAllOutsideModules") is not True:
        errors.append("o manifesto deve incluir toda a documentacao global")
    if not isinstance(resources, dict) or resources.get("includeAllSafeFiles") is not True:
        errors.append("o manifesto deve incluir todos os recursos seguros")

    exclusions = manifest.get("exclusions")
    if not isinstance(exclusions, dict) or not str(exclusions.get("reason", "")).strip():
        errors.append("exclusoes do manifesto precisam de justificativa explicita")


def validate_shell(errors: list[str]) -> None:
    result = subprocess.run(
        ["bash", "-n", str(LAUNCHER)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        errors.append(f"estudo.sh possui sintaxe invalida: {result.stderr.strip()}")
        return

    content = LAUNCHER.read_text(encoding="utf-8")
    required_fragments = (
        "127.0.0.1",
        "npm ci --ignore-scripts",
        "build_catalog.py",
        "--no-open",
        "--check",
        "trap cleanup EXIT",
    )
    for fragment in required_fragments:
        if fragment not in content:
            errors.append(f"estudo.sh nao implementa o contrato: {fragment}")
    if "0.0.0.0" in content:
        errors.append("estudo.sh nao pode expor o Vite em 0.0.0.0")
    if not LAUNCHER.stat().st_mode & 0o100:
        errors.append("estudo.sh deve ser executavel")


def validate_vite_binding(errors: list[str]) -> None:
    path = APP / "vite.config.js"
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8")
    if "127.0.0.1" not in content:
        errors.append("vite.config.js deve limitar server e preview ao loopback")
    if "0.0.0.0" in content or re.search(r"host\s*:\s*true", content):
        errors.append("vite.config.js contem binding de rede publica")


def tracked_runtime_paths(errors: list[str]) -> None:
    if shutil.which("git") is None:
        errors.append("git nao encontrado; impossivel verificar artefatos versionados")
        return
    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--",
            "study-app/node_modules",
            "study-app/dist",
            "study-app/public/generated",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        errors.append(f"git ls-files falhou: {result.stderr.strip()}")
    elif result.stdout.strip():
        tracked = ", ".join(result.stdout.splitlines())
        errors.append(f"artefatos gerados estao versionados: {tracked}")


def validate_ignored_paths(errors: list[str]) -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    entries = {line.strip() for line in gitignore if line.strip() and not line.startswith("#")}
    for runtime_path in IGNORED_RUNTIME_PATHS:
        if runtime_path not in entries:
            errors.append(f".gitignore nao cobre {runtime_path}")


def validate_sources(errors: list[str]) -> None:
    excluded_parts = {"node_modules", "dist", "generated", "__pycache__"}
    for path in APP.rglob("*"):
        if not path.is_file() or excluded_parts.intersection(path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.name in SECRET_FILENAMES or path.suffix.lower() in SECRET_SUFFIXES:
            errors.append(f"arquivo sensivel presente: {relative}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"arquivo binario inesperado: {relative}")
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"possivel segredo em {relative}: {pattern.pattern}")
        if path.suffix == ".py":
            try:
                compile(content, str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python invalido em {relative}: {exc}")


def validate() -> list[str]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"arquivo obrigatorio ausente: {path.relative_to(ROOT)}")
    if errors:
        return errors
    validate_package(errors)
    validate_study_manifest(errors)
    validate_shell(errors)
    validate_vite_binding(errors)
    validate_ignored_paths(errors)
    tracked_runtime_paths(errors)
    validate_sources(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("[PASS] aplicacao de estudos validada sem acesso a rede")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
