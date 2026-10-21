from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module04_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)

BASE = "04-Automation/automacao-profissional"
ROUTE = [
    "04-Automation/README.md",
    f"{BASE}/README.md",
    f"{BASE}/00-o-que-automatizar.md",
    f"{BASE}/01-contratos-idempotencia-dry-run.md",
    f"{BASE}/02-arquivos-caminhos-seguros.md",
    f"{BASE}/exemplos/README.md",
    f"{BASE}/laboratorios/README.md",
    f"{BASE}/laboratorios/lab-01-contrato-plan-apply.md",
    f"{BASE}/03-pipelines-dados.md",
    f"{BASE}/04-integracoes-http-webhooks.md",
    f"{BASE}/05-jobs-agendamento-checkpoints.md",
    f"{BASE}/laboratorios/lab-02-pipeline-job-checkpoint.md",
    f"{BASE}/06-retry-backoff-rate-limit.md",
    f"{BASE}/07-lotes-paralelismo.md",
    f"{BASE}/08-navegador-documentos.md",
    f"{BASE}/laboratorios/lab-03-resiliencia-concorrencia-documentos.md",
    f"{BASE}/09-seguranca-segredos.md",
    f"{BASE}/10-observabilidade-auditoria.md",
    f"{BASE}/11-testes-automacao.md",
    f"{BASE}/12-cicd-orquestracao.md",
    f"{BASE}/GUIA-DIAGNOSTICO.md",
    f"{BASE}/laboratorios/lab-04-seguranca-observabilidade-ci.md",
    f"{BASE}/13-distribuicao-operacao.md",
    f"{BASE}/CADERNO-PRATICAS.md",
    f"{BASE}/14-projetos-avaliacao.md",
    f"{BASE}/projetos/fileflow/README.md",
    f"{BASE}/laboratorios/lab-05-capstone-fileflow.md",
]

LAB_REQUIREMENTS = {
    f"{BASE}/laboratorios/lab-01-contrato-plan-apply.md": [
        f"{BASE}/00-o-que-automatizar.md",
        f"{BASE}/01-contratos-idempotencia-dry-run.md",
        f"{BASE}/02-arquivos-caminhos-seguros.md",
        f"{BASE}/exemplos/README.md",
    ],
    f"{BASE}/laboratorios/lab-02-pipeline-job-checkpoint.md": [
        f"{BASE}/laboratorios/lab-01-contrato-plan-apply.md",
        f"{BASE}/03-pipelines-dados.md",
        f"{BASE}/04-integracoes-http-webhooks.md",
        f"{BASE}/05-jobs-agendamento-checkpoints.md",
    ],
    f"{BASE}/laboratorios/lab-03-resiliencia-concorrencia-documentos.md": [
        f"{BASE}/laboratorios/lab-02-pipeline-job-checkpoint.md",
        f"{BASE}/06-retry-backoff-rate-limit.md",
        f"{BASE}/07-lotes-paralelismo.md",
        f"{BASE}/08-navegador-documentos.md",
    ],
    f"{BASE}/laboratorios/lab-04-seguranca-observabilidade-ci.md": [
        f"{BASE}/laboratorios/lab-03-resiliencia-concorrencia-documentos.md",
        f"{BASE}/09-seguranca-segredos.md",
        f"{BASE}/10-observabilidade-auditoria.md",
        f"{BASE}/11-testes-automacao.md",
        f"{BASE}/12-cicd-orquestracao.md",
        f"{BASE}/GUIA-DIAGNOSTICO.md",
    ],
    f"{BASE}/laboratorios/lab-05-capstone-fileflow.md": [
        f"{BASE}/laboratorios/lab-01-contrato-plan-apply.md",
        f"{BASE}/laboratorios/lab-02-pipeline-job-checkpoint.md",
        f"{BASE}/laboratorios/lab-03-resiliencia-concorrencia-documentos.md",
        f"{BASE}/laboratorios/lab-04-seguranca-observabilidade-ci.md",
        f"{BASE}/GUIA-DIAGNOSTICO.md",
        f"{BASE}/CADERNO-PRATICAS.md",
        f"{BASE}/13-distribuicao-operacao.md",
        f"{BASE}/14-projetos-avaliacao.md",
        f"{BASE}/projetos/fileflow/README.md",
    ],
}


class Module04CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "04" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_route_interleaves_theory_labs_and_capstone(self) -> None:
        self.assertEqual([item["sourcePath"] for item in self.documents[: len(ROUTE)]], ROUTE)
        self.assertEqual([item["order"] for item in self.documents], list(range(len(self.documents))))
        for path in ROUTE:
            self.assertEqual(self.by_path[path]["id"], builder._document_id(path))

    def test_required_support_and_project_are_explicit(self) -> None:
        for path in (
            f"{BASE}/GUIA-DIAGNOSTICO.md",
            f"{BASE}/CADERNO-PRATICAS.md",
            f"{BASE}/exemplos/README.md",
            f"{BASE}/projetos/fileflow/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        self.assertEqual(self.by_path[f"{BASE}/projetos/fileflow/README.md"]["role"], "project_readme")

    def test_five_required_labs_have_exact_prerequisites(self) -> None:
        required_labs = {
            document["sourcePath"]: document
            for document in self.documents
            if document["required"] and document["sourcePath"] in LAB_REQUIREMENTS
        }
        self.assertEqual(set(required_labs), set(LAB_REQUIREMENTS))
        for path, expected in LAB_REQUIREMENTS.items():
            actual = [self.path_by_id[item] for item in required_labs[path]["prerequisites"]]
            self.assertEqual(actual, expected, path)

    def test_fifteen_chapters_are_substantive_and_structured(self) -> None:
        chapters = sorted((ROOT / BASE).glob("[0-1][0-9]-*.md"))
        self.assertEqual(len(chapters), 15)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            self.assertGreaterEqual(len(re.findall(r"\b\w+\b", text, re.UNICODE)), 850, chapter.name)
            self.assertIn("## Objetivos", text, chapter.name)
            self.assertIn("## Checklist", text, chapter.name)
            self.assertTrue("## Exercícios" in text or "## 10. Rubrica" in text, chapter.name)

    def test_fileflow_demonstrates_course_controls(self) -> None:
        project = ROOT / BASE / "projetos/fileflow"
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((project / "src/fileflow").glob("*.py"))
        )
        tests = (project / "tests/test_fileflow.py").read_text(encoding="utf-8")
        for marker in (
            "planDigest",
            "operationId",
            "max_total_bytes",
            "fonte mudou depois do planejamento",
            "os.link",
        ):
            self.assertIn(marker, combined)
        for test_name in (
            "test_manifest_is_deterministic",
            "test_source_changed_after_plan",
            "test_audit_failure_reports_confirmed_effect",
        ):
            self.assertIn(test_name, tests)

    def test_base_course_has_no_relocated_offensive_material(self) -> None:
        forbidden = re.compile(
            r"\b(BloodHound|Kerberoast(?:ing)?|EternalBlue|Mimikatz|Cobalt Strike|"
            r"subdomain enumeration|port scanner|credential dumping)\b",
            re.IGNORECASE,
        )
        for path in (ROOT / BASE).rglob("*.md"):
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), path)
        self.assertTrue((ROOT / "28-Engenharia-Ferramentas-Seguranca").is_dir())


if __name__ == "__main__":
    unittest.main()
