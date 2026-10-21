from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module07_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BASE = "07-Web-AppSec/linux-avancado"
CHAPTERS = [
    "00-metodo-laboratorio",
    "01-fonte-kernel",
    "02-build-kernel",
    "03-abi-syscalls",
    "04-elf-loader",
    "05-processos-internals",
    "06-namespaces-locais",
    "07-scheduler",
    "08-smp-interrupcoes",
    "09-concorrencia",
    "10-rcu",
    "11-mm-internals",
    "12-numa-pressao",
    "13-vfs-page-cache",
    "14-filesystems",
    "15-block-layer",
    "16-device-mapper",
    "17-io-assincrona",
    "18-drivers-iommu",
    "19-boot-confiavel",
    "20-systemd-avancado",
    "21-cgroups-recursos",
    "22-perf-metodologia",
    "23-tracing",
    "24-ebpf-local",
    "25-debug-userspace",
    "26-debug-kernel",
    "27-kvm-qemu",
    "28-tempo-real",
    "29-embarcado",
    "30-seguranca-internals",
    "31-integridade",
    "32-engenharia-distribuicao",
    "33-contribuicao-kernel",
    "34-projeto-final",
]
LABS = [
    "01-fonte-abi-elf",
    "02-scheduler-memoria",
    "03-filesystems-bloco",
    "04-boot-systemd-cgroups",
    "05-tracing-ebpf",
    "06-debug-kdump",
    "07-kvm-offline",
    "08-distribuicao",
    "09-projeto-final",
]

CHAPTER_PATHS = [f"{BASE}/{name}.md" for name in CHAPTERS]
LAB_PATHS = [f"{BASE}/laboratorios/{name}.md" for name in LABS]
GUIDE = f"{BASE}/GUIA-EXPERIMENTOS-DIAGNOSTICO.md"
NOTEBOOK = f"{BASE}/CADERNO-PRATICAS.md"
PROJECT = f"{BASE}/projetos/offline-appliance/README.md"

ROUTE = [
    "07-Web-AppSec/README.md",
    f"{BASE}/README.md",
    *CHAPTER_PATHS[:7],
    f"{BASE}/exemplos/README.md",
    f"{BASE}/laboratorios/README.md",
    LAB_PATHS[0],
    *CHAPTER_PATHS[7:13],
    LAB_PATHS[1],
    *CHAPTER_PATHS[13:19],
    LAB_PATHS[2],
    *CHAPTER_PATHS[19:22],
    LAB_PATHS[3],
    *CHAPTER_PATHS[22:25],
    GUIDE,
    LAB_PATHS[4],
    *CHAPTER_PATHS[25:27],
    LAB_PATHS[5],
    *CHAPTER_PATHS[27:30],
    LAB_PATHS[6],
    *CHAPTER_PATHS[30:34],
    LAB_PATHS[7],
    NOTEBOOK,
    CHAPTER_PATHS[34],
    PROJECT,
    LAB_PATHS[8],
    f"{BASE}/CHEATSHEET.md",
    f"{BASE}/GLOSSARIO.md",
    f"{BASE}/REFERENCIAS.md",
    f"{BASE}/RESPOSTAS.md",
]

LAB_REQUIREMENTS = {
    LAB_PATHS[0]: [*CHAPTER_PATHS[:7], f"{BASE}/exemplos/README.md"],
    LAB_PATHS[1]: [LAB_PATHS[0], *CHAPTER_PATHS[7:13]],
    LAB_PATHS[2]: [LAB_PATHS[1], *CHAPTER_PATHS[13:19]],
    LAB_PATHS[3]: [LAB_PATHS[2], *CHAPTER_PATHS[19:22]],
    LAB_PATHS[4]: [LAB_PATHS[3], *CHAPTER_PATHS[22:25], GUIDE],
    LAB_PATHS[5]: [LAB_PATHS[4], *CHAPTER_PATHS[25:27]],
    LAB_PATHS[6]: [LAB_PATHS[5], *CHAPTER_PATHS[27:30]],
    LAB_PATHS[7]: [LAB_PATHS[6], *CHAPTER_PATHS[30:34]],
    LAB_PATHS[8]: [
        *LAB_PATHS[:8],
        GUIDE,
        NOTEBOOK,
        CHAPTER_PATHS[34],
        PROJECT,
    ],
}


class Module07CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "07" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {
            document["id"]: document["sourcePath"] for document in cls.documents
        }

    def test_route_is_complete_and_interleaves_nine_gates(self) -> None:
        self.assertEqual(
            [document["sourcePath"] for document in self.documents],
            ROUTE,
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

    def test_nine_labs_have_exact_semantic_prerequisites(self) -> None:
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

    def test_thirty_five_chapters_are_substantive_and_structured(self) -> None:
        chapters = sorted((ROOT / BASE).glob("[0-3][0-9]-*.md"))
        self.assertEqual(len(chapters), 35)
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
            len(re.findall(r"\b[\wÀ-ÿ]+\b", guide, flags=re.UNICODE)),
            800,
        )
        notebook = (ROOT / NOTEBOOK).read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^### P\d{2}\b", notebook)), 72)

    def test_executable_examples_cover_system_boundaries_safely(self) -> None:
        tests = (ROOT / BASE / "exemplos/tests/test_examples.sh").read_text(
            encoding="utf-8"
        )
        runner = (ROOT / BASE / "testar-curso.sh").read_text(encoding="utf-8")
        for marker in (
            "test_c_portable",
            "test_linux_c",
            "test_reproducible_archive",
            "test_static_privileged_sources",
        ):
            self.assertIn(marker, tests)
        self.assertNotIn("sudo ", runner)
        self.assertIn("local Markdown links", runner)

    def test_scope_excludes_offensive_and_network_curricula(self) -> None:
        offensive = re.compile(
            r"\b(BloodHound|Kerberoast(?:ing)?|EternalBlue|Mimikatz|"
            r"Cobalt Strike|credential dumping|lateral movement)\b",
            re.IGNORECASE,
        )
        network_commands = re.compile(
            r"(?m)^\s*(?:sudo\s+)?(?:tcpdump|nft|nstat|iperf3|"
            r"ip\s+(?:route|rule|neigh))\b"
        )
        for path in (ROOT / BASE).rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(offensive.search(text), path)
            self.assertIsNone(network_commands.search(text), path)
        overview = (ROOT / "07-Web-AppSec/README.md").read_text(encoding="utf-8")
        self.assertIn("Redes não fazem parte do módulo 07", overview)


if __name__ == "__main__":
    unittest.main()
