from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module05_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BASE = "05-DFIR/engenharia-apis"
ROUTE = [
    "05-DFIR/README.md",
    f"{BASE}/README.md",
    *[f"{BASE}/{number:02d}-{name}.md" for number, name in (
        (0, "mapa-das-apis"),
        (1, "http-semantica"),
        (2, "estilos-e-decisoes"),
        (3, "design-rest"),
        (4, "representacoes-validacao"),
        (5, "erros-problem-details"),
    )],
    f"{BASE}/laboratorios/README.md",
    f"{BASE}/laboratorios/lab-01-contrato-http.md",
    *[f"{BASE}/{number:02d}-{name}.md" for number, name in (
        (6, "colecoes-paginacao"),
        (7, "idempotencia-cache"),
        (8, "versionamento-evolucao"),
        (9, "autenticacao"),
        (10, "autorizacao"),
        (11, "seguranca-owasp"),
        (12, "openapi-contract-first"),
    )],
    f"{BASE}/laboratorios/lab-02-contrato-seguranca.md",
    *[f"{BASE}/{number:02d}-{name}.md" for number, name in (
        (13, "arquitetura-implementacao"),
        (14, "dados-consistencia"),
        (15, "resiliencia-desempenho"),
        (16, "observabilidade"),
        (17, "testes"),
    )],
    f"{BASE}/GUIA-DIAGNOSTICO.md",
    f"{BASE}/laboratorios/lab-03-servico-operavel.md",
    *[f"{BASE}/{number:02d}-{name}.md" for number, name in (
        (18, "webhooks"),
        (19, "apis-assincronas"),
        (20, "graphql"),
        (21, "grpc"),
        (22, "streaming-tempo-real"),
        (23, "clientes-sdks"),
        (24, "governanca-dx"),
    )],
    f"{BASE}/exemplos/README.md",
    f"{BASE}/laboratorios/lab-04-integracoes-clientes.md",
    f"{BASE}/CADERNO-PRATICAS.md",
    f"{BASE}/25-projeto-avaliacao.md",
    f"{BASE}/projetos/contract-lab-api/README.md",
    f"{BASE}/laboratorios/lab-05-capstone-contract-lab.md",
]

LAB_REQUIREMENTS = {
    f"{BASE}/laboratorios/lab-01-contrato-http.md": [
        f"{BASE}/00-mapa-das-apis.md",
        f"{BASE}/01-http-semantica.md",
        f"{BASE}/02-estilos-e-decisoes.md",
        f"{BASE}/03-design-rest.md",
        f"{BASE}/04-representacoes-validacao.md",
        f"{BASE}/05-erros-problem-details.md",
    ],
    f"{BASE}/laboratorios/lab-02-contrato-seguranca.md": [
        f"{BASE}/laboratorios/lab-01-contrato-http.md",
        *[f"{BASE}/{number:02d}-{name}.md" for number, name in (
            (6, "colecoes-paginacao"),
            (7, "idempotencia-cache"),
            (8, "versionamento-evolucao"),
            (9, "autenticacao"),
            (10, "autorizacao"),
            (11, "seguranca-owasp"),
            (12, "openapi-contract-first"),
        )],
    ],
    f"{BASE}/laboratorios/lab-03-servico-operavel.md": [
        f"{BASE}/laboratorios/lab-02-contrato-seguranca.md",
        f"{BASE}/13-arquitetura-implementacao.md",
        f"{BASE}/14-dados-consistencia.md",
        f"{BASE}/15-resiliencia-desempenho.md",
        f"{BASE}/16-observabilidade.md",
        f"{BASE}/17-testes.md",
        f"{BASE}/GUIA-DIAGNOSTICO.md",
    ],
    f"{BASE}/laboratorios/lab-04-integracoes-clientes.md": [
        f"{BASE}/laboratorios/lab-03-servico-operavel.md",
        f"{BASE}/18-webhooks.md",
        f"{BASE}/19-apis-assincronas.md",
        f"{BASE}/20-graphql.md",
        f"{BASE}/21-grpc.md",
        f"{BASE}/22-streaming-tempo-real.md",
        f"{BASE}/23-clientes-sdks.md",
        f"{BASE}/24-governanca-dx.md",
        f"{BASE}/exemplos/README.md",
    ],
    f"{BASE}/laboratorios/lab-05-capstone-contract-lab.md": [
        f"{BASE}/laboratorios/lab-01-contrato-http.md",
        f"{BASE}/laboratorios/lab-02-contrato-seguranca.md",
        f"{BASE}/laboratorios/lab-03-servico-operavel.md",
        f"{BASE}/laboratorios/lab-04-integracoes-clientes.md",
        f"{BASE}/GUIA-DIAGNOSTICO.md",
        f"{BASE}/CADERNO-PRATICAS.md",
        f"{BASE}/25-projeto-avaliacao.md",
        f"{BASE}/projetos/contract-lab-api/README.md",
    ],
}


class Module05CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "05" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_route_interleaves_theory_labs_and_capstone(self) -> None:
        self.assertEqual(
            [document["sourcePath"] for document in self.documents[: len(ROUTE)]],
            ROUTE,
        )
        self.assertEqual(
            [document["order"] for document in self.documents],
            list(range(len(self.documents))),
        )

    def test_support_and_reference_project_are_required(self) -> None:
        for path in (
            f"{BASE}/GUIA-DIAGNOSTICO.md",
            f"{BASE}/CADERNO-PRATICAS.md",
            f"{BASE}/exemplos/README.md",
            f"{BASE}/projetos/contract-lab-api/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        self.assertEqual(
            self.by_path[f"{BASE}/projetos/contract-lab-api/README.md"]["role"],
            "project_readme",
        )

    def test_five_labs_have_exact_semantic_prerequisites(self) -> None:
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

    def test_twenty_six_chapters_are_substantive_and_structured(self) -> None:
        chapters = sorted((ROOT / BASE).glob("[0-2][0-9]-*.md"))
        self.assertEqual(len(chapters), 26)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 600, chapter.name)
            self.assertRegex(text, r"(?im)^## Objetivos", chapter.name)
            self.assertRegex(text, r"(?im)^## Exercícios", chapter.name)
            self.assertRegex(text, r"(?im)^## Checklist", chapter.name)

    def test_contract_lab_demonstrates_the_course_invariants(self) -> None:
        project = ROOT / BASE / "projetos/contract-lab-api"
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((project / "contract_lab").glob("*.py"))
        )
        tests = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((project / "tests").glob("test_*.py"))
        )
        for marker in (
            "hmac.compare_digest",
            "Idempotency-Replayed",
            "If-None-Match",
            "invalid-transition",
            "requestId",
            "ReplayGuard",
        ):
            self.assertIn(marker, source)
        for test_name in (
            "test_cursor_rejects_tampering_and_filter_change",
            "test_contract_and_runtime_expose_same_operations",
            "test_archived_item_cannot_be_reactivated",
        ):
            self.assertIn(test_name, tests)

    def test_module_stays_on_api_engineering_scope(self) -> None:
        forbidden = re.compile(
            r"\b(BloodHound|Kerberoast(?:ing)?|EternalBlue|Mimikatz|"
            r"Cobalt Strike|credential dumping|lateral movement)\b",
            re.IGNORECASE,
        )
        for path in (ROOT / BASE).rglob("*.md"):
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), path)


if __name__ == "__main__":
    unittest.main()
