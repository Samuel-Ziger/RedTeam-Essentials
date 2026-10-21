from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module06_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BASE = "06-Cheatsheets/linux-do-zero-ao-avancado"
CHAPTERS = [
    "00-como-estudar-laboratorio",
    "01-distribuicoes",
    "02-instalacao",
    "03-arquitetura-linux",
    "04-terminal-ajuda",
    "05-sistema-arquivos",
    "06-manipulacao-arquivos",
    "07-texto-fluxos-editores",
    "08-permissoes",
    "09-usuarios-autenticacao",
    "10-pacotes-software",
    "11-processos-sinais",
    "12-memoria",
    "13-armazenamento",
    "14-lvm-raid-criptografia",
    "15-boot",
    "16-systemd",
    "17-redes-linux",
    "18-ssh-remoto",
    "19-bash-automacao",
    "20-observabilidade",
    "21-backup-recuperacao",
    "22-hardening",
    "23-isolamento-containers",
    "24-kernel",
    "25-modulos-dispositivos",
    "26-kernel-build-debug",
    "27-desempenho",
    "28-desktop",
    "29-servicos",
    "30-projeto-final",
]

ROUTE = [
    "06-Cheatsheets/README.md",
    f"{BASE}/README.md",
    *[f"{BASE}/{name}.md" for name in CHAPTERS[:9]],
    f"{BASE}/exemplos/README.md",
    f"{BASE}/laboratorios/README.md",
    f"{BASE}/laboratorios/lab-01-shell-arquivos-permissoes.md",
    *[f"{BASE}/{name}.md" for name in CHAPTERS[9:13]],
    f"{BASE}/laboratorios/lab-02-identidades-processos-memoria.md",
    *[f"{BASE}/{name}.md" for name in CHAPTERS[13:17]],
    f"{BASE}/laboratorios/lab-03-armazenamento-boot-systemd.md",
    *[f"{BASE}/{name}.md" for name in CHAPTERS[17:24]],
    f"{BASE}/GUIA-DIAGNOSTICO.md",
    f"{BASE}/laboratorios/lab-04-operacao-hardening-isolamento.md",
    *[f"{BASE}/{name}.md" for name in CHAPTERS[24:30]],
    f"{BASE}/laboratorios/lab-05-kernel-desempenho-servicos.md",
    f"{BASE}/CADERNO-PRATICAS.md",
    f"{BASE}/30-projeto-final.md",
    f"{BASE}/projetos/host-observer/README.md",
    f"{BASE}/laboratorios/lab-06-capstone-linux.md",
    f"{BASE}/CHEATSHEET.md",
    f"{BASE}/GLOSSARIO.md",
    f"{BASE}/REFERENCIAS.md",
    f"{BASE}/RESPOSTAS.md",
    f"{BASE}/laboratorios/armazenamento-loop.md",
    f"{BASE}/laboratorios/boot-recovery.md",
    f"{BASE}/laboratorios/kernel.md",
    f"{BASE}/laboratorios/projeto.md",
]

LAB_REQUIREMENTS = {
    f"{BASE}/laboratorios/lab-01-shell-arquivos-permissoes.md": [
        *[f"{BASE}/{name}.md" for name in CHAPTERS[:9]],
        f"{BASE}/exemplos/README.md",
    ],
    f"{BASE}/laboratorios/lab-02-identidades-processos-memoria.md": [
        f"{BASE}/laboratorios/lab-01-shell-arquivos-permissoes.md",
        *[f"{BASE}/{name}.md" for name in CHAPTERS[9:13]],
    ],
    f"{BASE}/laboratorios/lab-03-armazenamento-boot-systemd.md": [
        f"{BASE}/laboratorios/lab-02-identidades-processos-memoria.md",
        *[f"{BASE}/{name}.md" for name in CHAPTERS[13:17]],
    ],
    f"{BASE}/laboratorios/lab-04-operacao-hardening-isolamento.md": [
        f"{BASE}/laboratorios/lab-03-armazenamento-boot-systemd.md",
        *[f"{BASE}/{name}.md" for name in CHAPTERS[17:24]],
        f"{BASE}/GUIA-DIAGNOSTICO.md",
    ],
    f"{BASE}/laboratorios/lab-05-kernel-desempenho-servicos.md": [
        f"{BASE}/laboratorios/lab-04-operacao-hardening-isolamento.md",
        *[f"{BASE}/{name}.md" for name in CHAPTERS[24:30]],
    ],
    f"{BASE}/laboratorios/lab-06-capstone-linux.md": [
        *[
            f"{BASE}/laboratorios/lab-0{number}-{name}.md"
            for number, name in (
                (1, "shell-arquivos-permissoes"),
                (2, "identidades-processos-memoria"),
                (3, "armazenamento-boot-systemd"),
                (4, "operacao-hardening-isolamento"),
                (5, "kernel-desempenho-servicos"),
            )
        ],
        f"{BASE}/GUIA-DIAGNOSTICO.md",
        f"{BASE}/CADERNO-PRATICAS.md",
        f"{BASE}/30-projeto-final.md",
        f"{BASE}/projetos/host-observer/README.md",
    ],
}


class Module06CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "06" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_route_is_complete_and_interleaves_six_gates(self) -> None:
        self.assertEqual(
            [document["sourcePath"] for document in self.documents],
            ROUTE,
        )
        self.assertEqual(
            [document["order"] for document in self.documents],
            list(range(len(self.documents))),
        )

    def test_support_documents_are_required_and_risk_guides_optional(self) -> None:
        for path in (
            f"{BASE}/exemplos/README.md",
            f"{BASE}/laboratorios/README.md",
            f"{BASE}/GUIA-DIAGNOSTICO.md",
            f"{BASE}/CADERNO-PRATICAS.md",
            f"{BASE}/projetos/host-observer/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        self.assertEqual(
            self.by_path[f"{BASE}/projetos/host-observer/README.md"]["role"],
            "project_readme",
        )
        for name in ("armazenamento-loop.md", "boot-recovery.md", "kernel.md", "projeto.md"):
            path = f"{BASE}/laboratorios/{name}"
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

    def test_thirty_one_chapters_are_substantive_and_structured(self) -> None:
        chapters = sorted((ROOT / BASE).glob("[0-3][0-9]-*.md"))
        self.assertEqual(len(chapters), 31)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 600, chapter.name)
            self.assertRegex(text, r"(?im)^## Objetivos", chapter.name)
            self.assertRegex(text, r"(?im)^## Exercícios", chapter.name)
            self.assertRegex(text, r"(?im)^## Checklist", chapter.name)

    def test_executable_examples_cover_baseline_and_kernel_boundaries(self) -> None:
        comparator = (ROOT / BASE / "exemplos/comparar_diagnosticos.py").read_text(
            encoding="utf-8"
        )
        shell_tests = (ROOT / BASE / "exemplos/tests/test_examples.sh").read_text(
            encoding="utf-8"
        )
        syscalls = (ROOT / BASE / "exemplos/c/syscalls.c").read_text(encoding="utf-8")
        runner = (ROOT / BASE / "testar-curso.sh").read_text(encoding="utf-8")
        for marker in (
            "MAX_INPUT_BYTES",
            "chave duplicada",
            "--fail-on-change",
            "DEFAULT_IGNORED",
        ):
            self.assertIn(marker, comparator)
        self.assertIn("test_diagnostic_comparator", shell_tests)
        self.assertIn("EINTR", syscalls)
        self.assertNotIn("sudo ", runner)
        self.assertIn("links Markdown locais", runner)

    def test_linux_scope_excludes_relocated_offensive_and_network_curricula(self) -> None:
        offensive = re.compile(
            r"\b(BloodHound|Kerberoast(?:ing)?|EternalBlue|Mimikatz|"
            r"Cobalt Strike|credential dumping|lateral movement)\b",
            re.IGNORECASE,
        )
        deferred_network_commands = re.compile(
            r"(?m)^\s*(?:sudo\s+)?(?:tcpdump|nft|nstat|iperf3|"
            r"ip\s+(?:route|rule|neigh))\b"
        )
        for path in (ROOT / BASE).rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(offensive.search(text), path)
            self.assertIsNone(deferred_network_commands.search(text), path)
        boundary = (ROOT / BASE / "17-redes-linux.md").read_text(encoding="utf-8")
        self.assertIn("módulos 14 a 18", boundary)


if __name__ == "__main__":
    unittest.main()
