from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module03_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


ROUTE = [
    "03-AD-Notes/README.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/README.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/00-do-codigo-ao-produto.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/01-cli-profissional.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/02-configuracao-ambientes-segredos.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/exemplos/README.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/03-validacao-erros-feedback.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/README.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-01-contrato-cli-configuracao.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/04-arquivos-serializacao-dados-locais.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/05-estado-eventos.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/06-gui-desktop.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-02-dados-estado-gui.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/07-interfaces-web.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/08-acessibilidade-responsividade.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/09-clientes-api-offline.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/10-internacionalizacao-tempo-dinheiro.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-03-web-acessivel-offline-i18n.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/11-logs-diagnostico.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/12-plugins-extensibilidade.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/13-empacotamento-distribuicao.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/14-desempenho-profiling.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/15-qualidade-release-suporte.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/GUIA-DIAGNOSTICO.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-04-diagnostico-distribuicao-desempenho.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/CADERNO-PRATICAS.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/16-projetos-avaliacao.md",
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-05-capstone-aplicacao-profissional.md",
]


LAB_REQUIREMENTS = {
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-01-contrato-cli-configuracao.md": [
        "03-AD-Notes/desenvolvimento-aplicacoes/00-do-codigo-ao-produto.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/01-cli-profissional.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/02-configuracao-ambientes-segredos.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/03-validacao-erros-feedback.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/exemplos/README.md",
    ],
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-02-dados-estado-gui.md": [
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-01-contrato-cli-configuracao.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/04-arquivos-serializacao-dados-locais.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/05-estado-eventos.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/06-gui-desktop.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md",
    ],
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-03-web-acessivel-offline-i18n.md": [
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-02-dados-estado-gui.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/07-interfaces-web.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/08-acessibilidade-responsividade.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/09-clientes-api-offline.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/10-internacionalizacao-tempo-dinheiro.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md",
    ],
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-04-diagnostico-distribuicao-desempenho.md": [
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-03-web-acessivel-offline-i18n.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/11-logs-diagnostico.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/12-plugins-extensibilidade.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/13-empacotamento-distribuicao.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/14-desempenho-profiling.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/15-qualidade-release-suporte.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/GUIA-DIAGNOSTICO.md",
    ],
    "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-05-capstone-aplicacao-profissional.md": [
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-01-contrato-cli-configuracao.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-02-dados-estado-gui.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-03-web-acessivel-offline-i18n.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/laboratorios/lab-04-diagnostico-distribuicao-desempenho.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/GUIA-DIAGNOSTICO.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/CADERNO-PRATICAS.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md",
        "03-AD-Notes/desenvolvimento-aplicacoes/16-projetos-avaliacao.md",
    ],
}


class Module03CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "03" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_route_interleaves_theory_practice_and_capstone(self) -> None:
        self.assertEqual([document["sourcePath"] for document in self.documents[: len(ROUTE)]], ROUTE)
        self.assertEqual([document["order"] for document in self.documents], list(range(len(self.documents))))
        for path in ROUTE:
            self.assertEqual(self.by_path[path]["id"], builder._document_id(path))

    def test_required_support_and_reference_project_are_explicit(self) -> None:
        for path in (
            "03-AD-Notes/desenvolvimento-aplicacoes/GUIA-DIAGNOSTICO.md",
            "03-AD-Notes/desenvolvimento-aplicacoes/CADERNO-PRATICAS.md",
            "03-AD-Notes/desenvolvimento-aplicacoes/exemplos/README.md",
            "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        project = self.by_path[
            "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk/README.md"
        ]
        self.assertEqual(project["role"], "project_readme")

    def test_five_required_labs_use_exact_semantic_prerequisites(self) -> None:
        required_labs = {
            document["sourcePath"]
            for document in self.documents
            if document["role"] == "lab_instruction" and document["required"]
        }
        self.assertEqual(required_labs, set(LAB_REQUIREMENTS))
        for lab_path, expected_paths in LAB_REQUIREMENTS.items():
            actual_paths = [
                self.path_by_id[document_id]
                for document_id in self.by_path[lab_path]["prerequisites"]
            ]
            self.assertEqual(actual_paths, expected_paths, lab_path)

    def test_seventeen_chapters_keep_a_minimum_technical_depth(self) -> None:
        course_root = ROOT / "03-AD-Notes/desenvolvimento-aplicacoes"
        chapters = sorted(course_root.glob("[0-1][0-9]-*.md"))
        self.assertEqual(len(chapters), 17)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 1_200, chapter.name)
            self.assertRegex(text, r"(?im)^## .*objetiv", chapter.name)
            self.assertRegex(text, r"(?im)^## .*?(exerc|laborat)", chapter.name)
            self.assertRegex(text, r"(?im)^## .*checklist|^## .*domínio", chapter.name)

    def test_study_desk_keeps_executable_quality_contract(self) -> None:
        project_root = ROOT / "03-AD-Notes/desenvolvimento-aplicacoes/projetos/study-desk"
        tests = "\n".join(
            path.read_text(encoding="utf-8") for path in sorted((project_root / "tests").glob("*.test.mjs"))
        )
        self.assertGreaterEqual(len(re.findall(r"\btest\(", tests)), 30)
        architecture = (project_root / "docs/architecture.md").read_text(encoding="utf-8")
        self.assertIn("## Invariantes", architecture)
        self.assertTrue((project_root / "RUNBOOK.md").is_file())
        self.assertTrue((project_root / "docs/adr/001-local-first-versioned-document.md").is_file())
        self.assertTrue((project_root / "docs/adr/002-state-commit-and-errors.md").is_file())

    def test_historical_active_directory_material_is_not_in_base_module(self) -> None:
        module_root = ROOT / "03-AD-Notes"
        legacy_files = {
            "ad_enum_commands.md",
            "bloodhound_teoria.md",
            "kerberoasting_teoria.md",
            "modern-ad-attacks-2026.md",
        }
        self.assertFalse(legacy_files.intersection(path.name for path in module_root.glob("*.md")))
        self.assertTrue((ROOT / "31-Active-Directory-Identidade/README.md").is_file())


if __name__ == "__main__":
    unittest.main()
