from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module08_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BASE = "08-Cloud-RedTeam/windows-domestico-fundamentos"
CHAPTERS = [
    "00-metodo-laboratorio",
    "01-familia-edicoes-ciclo",
    "02-hardware-firmware",
    "03-instalacao-oobe",
    "04-interface-configuracoes",
    "05-arquivos-caminhos",
    "06-discos-volumes-bitlocker",
    "07-contas-permissoes-uac",
    "08-processos-servicos",
    "09-aplicativos-pacotes",
    "10-windows-update",
    "11-registro",
    "12-eventos-confiabilidade",
    "13-backup-recuperacao",
    "14-defender-seguranca",
    "15-terminal-powershell",
    "16-diagnostico-reparo",
    "17-projeto-final",
]
LABS = [
    "01-instalacao-inventario",
    "02-arquivos-permissoes",
    "03-disco-recuperacao",
    "04-eventos-diagnostico",
    "05-defender-integridade",
    "06-projeto-recuperacao",
]

CHAPTER_PATHS = [f"{BASE}/{name}.md" for name in CHAPTERS]
LAB_PATHS = [f"{BASE}/laboratorios/{name}.md" for name in LABS]
GUIDE = f"{BASE}/GUIA-DIAGNOSTICO-RECUPERACAO.md"
NOTEBOOK = f"{BASE}/CADERNO-PRATICAS.md"
PROJECT = f"{BASE}/projetos/computador-recuperavel/README.md"

ROUTE = [
    "08-Cloud-RedTeam/README.md",
    f"{BASE}/README.md",
    *CHAPTER_PATHS[:5],
    f"{BASE}/exemplos/README.md",
    f"{BASE}/laboratorios/README.md",
    LAB_PATHS[0],
    *CHAPTER_PATHS[5:8],
    LAB_PATHS[1],
    *CHAPTER_PATHS[8:14],
    GUIDE,
    LAB_PATHS[2],
    LAB_PATHS[3],
    *CHAPTER_PATHS[14:17],
    LAB_PATHS[4],
    NOTEBOOK,
    CHAPTER_PATHS[17],
    PROJECT,
    LAB_PATHS[5],
    f"{BASE}/CHEATSHEET.md",
    f"{BASE}/GLOSSARIO.md",
    f"{BASE}/REFERENCIAS.md",
    f"{BASE}/RESPOSTAS.md",
]

LAB_REQUIREMENTS = {
    LAB_PATHS[0]: [*CHAPTER_PATHS[:5], f"{BASE}/exemplos/README.md"],
    LAB_PATHS[1]: [LAB_PATHS[0], *CHAPTER_PATHS[5:8]],
    LAB_PATHS[2]: [LAB_PATHS[1], *CHAPTER_PATHS[8:14], GUIDE],
    LAB_PATHS[3]: [LAB_PATHS[2]],
    LAB_PATHS[4]: [LAB_PATHS[3], *CHAPTER_PATHS[14:17]],
    LAB_PATHS[5]: [
        *LAB_PATHS[:5],
        GUIDE,
        NOTEBOOK,
        CHAPTER_PATHS[17],
        PROJECT,
    ],
}


class Module08CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "08" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {
            document["id"]: document["sourcePath"] for document in cls.documents
        }

    def test_route_is_complete_and_interleaves_six_gates(self) -> None:
        self.assertEqual(
            [document["sourcePath"] for document in self.documents], ROUTE
        )
        self.assertEqual(
            [document["order"] for document in self.documents],
            list(range(len(self.documents))),
        )

    def test_support_documents_are_required_and_references_optional(self) -> None:
        for path in (
            f"{BASE}/exemplos/README.md",
            f"{BASE}/laboratorios/README.md",
            GUIDE,
            NOTEBOOK,
            PROJECT,
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        self.assertEqual(self.by_path[PROJECT]["role"], "project_readme")
        for name in ("CHEATSHEET.md", "GLOSSARIO.md", "REFERENCIAS.md", "RESPOSTAS.md"):
            path = f"{BASE}/{name}"
            self.assertFalse(self.by_path[path]["required"], path)

    def test_six_labs_have_exact_semantic_prerequisites(self) -> None:
        required_labs = {
            document["sourcePath"]
            for document in self.documents
            if document["role"] == "lab_instruction" and document["required"]
        }
        self.assertEqual(required_labs, set(LAB_REQUIREMENTS))
        for lab_path, expected in LAB_REQUIREMENTS.items():
            actual = [
                self.path_by_id[document_id]
                for document_id in self.by_path[lab_path]["prerequisites"]
            ]
            self.assertEqual(actual, expected, lab_path)

    def test_eighteen_chapters_are_substantive_and_structured(self) -> None:
        chapters = sorted((ROOT / BASE).glob("[0-1][0-9]-*.md"))
        self.assertEqual(len(chapters), 18)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 600, chapter.name)
            self.assertRegex(text, r"(?im)^## Objetivos", chapter.name)
            self.assertRegex(text, r"(?im)^## Exercícios", chapter.name)
            self.assertRegex(text, r"(?im)^## Checklist", chapter.name)

    def test_labs_and_transversal_material_are_substantive(self) -> None:
        for lab_path in LAB_PATHS:
            text = (ROOT / lab_path).read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 400, lab_path)
            self.assertIn("Classe:", text, lab_path)
        guide = (ROOT / GUIDE).read_text(encoding="utf-8")
        self.assertGreaterEqual(
            len(re.findall(r"\b[\wÀ-ÿ]+\b", guide, flags=re.UNICODE)), 800
        )
        notebook = (ROOT / NOTEBOOK).read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^### P\d{2}\b", notebook)), 48)

    def test_real_powershell_examples_have_safety_boundaries(self) -> None:
        examples = ROOT / BASE / "exemplos"
        inventory = (examples / "Get-RteLocalInventory.ps1").read_text(encoding="utf-8")
        backup = (examples / "Backup-RteFixture.ps1").read_text(encoding="utf-8")
        comparator = (examples / "Compare-RteManifest.ps1").read_text(encoding="utf-8")
        tests = (examples / "tests/WindowsDomesticFundamentals.Tests.ps1").read_text(
            encoding="utf-8"
        )
        for marker in ("QueryStatus", "rte.windows.local-inventory/v1"):
            self.assertIn(marker, inventory)
        for marker in ("SupportsShouldProcess", "ReparsePoint", "destino já existe"):
            self.assertIn(marker, backup)
        for marker in ("IsPathRooted", "Caminho duplicado", "Unexpected", "Changed"):
            self.assertIn(marker, comparator)
        self.assertIn("reprova conteúdo alterado", tests)
        self.assertIn("rejeita travessia", tests)

    def test_scope_stays_local_domestic_and_non_offensive(self) -> None:
        offensive = re.compile(
            r"\b(BloodHound|Kerberoast(?:ing)?|EternalBlue|Mimikatz|"
            r"Cobalt Strike|credential dumping|lateral movement)\b",
            re.IGNORECASE,
        )
        deferred_commands = re.compile(
            r"(?im)^\s*(?:New-NetIPAddress|Set-DnsClientServerAddress|"
            r"New-NetFirewallRule|Enable-PSRemoting|New-SmbShare|"
            r"Install-ADDSForest)\b"
        )
        for path in (ROOT / BASE).rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(offensive.search(text), path)
            self.assertIsNone(deferred_commands.search(text), path)
        overview = (ROOT / "08-Cloud-RedTeam/README.md").read_text(encoding="utf-8")
        self.assertIn("módulos 14–18", overview)
        self.assertIn("módulos 10–11", overview)


if __name__ == "__main__":
    unittest.main()
