from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module02_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


ROUTE = [
    "02-OSINT/README.md",
    "02-OSINT/engenharia-software/README.md",
    "02-OSINT/engenharia-software/00-como-pensar-problemas.md",
    "02-OSINT/engenharia-software/01-complexidade.md",
    "02-OSINT/engenharia-software/laboratorios/README.md",
    "02-OSINT/engenharia-software/laboratorios/lab-01-contrato-complexidade.md",
    "02-OSINT/engenharia-software/02-estruturas-lineares.md",
    "02-OSINT/engenharia-software/03-arvores-heaps-tries.md",
    "02-OSINT/engenharia-software/04-grafos.md",
    "02-OSINT/engenharia-software/05-busca-ordenacao.md",
    "02-OSINT/engenharia-software/exemplos/README.md",
    "02-OSINT/engenharia-software/laboratorios/lab-02-estruturas-grafos.md",
    "02-OSINT/engenharia-software/06-recursao-backtracking.md",
    "02-OSINT/engenharia-software/07-programacao-dinamica-gulosa.md",
    "02-OSINT/engenharia-software/08-paradigmas-tipos.md",
    "02-OSINT/engenharia-software/09-design-modular.md",
    "02-OSINT/engenharia-software/10-solid-patterns.md",
    "02-OSINT/engenharia-software/projetos/dependency-planner/README.md",
    "02-OSINT/engenharia-software/laboratorios/lab-03-estrategias-design.md",
    "02-OSINT/engenharia-software/11-refatoracao-legado.md",
    "02-OSINT/engenharia-software/12-requisitos-modelagem.md",
    "02-OSINT/engenharia-software/13-arquitetura.md",
    "02-OSINT/engenharia-software/14-testes-qualidade.md",
    "02-OSINT/engenharia-software/15-colaboracao-documentacao.md",
    "02-OSINT/engenharia-software/GUIA-DIAGNOSTICO.md",
    "02-OSINT/engenharia-software/laboratorios/lab-04-evolucao-arquitetura-testes.md",
    "02-OSINT/engenharia-software/CADERNO-PRATICAS.md",
    "02-OSINT/engenharia-software/16-projetos-avaliacao.md",
    "02-OSINT/engenharia-software/laboratorios/lab-05-dependency-planner.md",
]


LAB_REQUIREMENTS = {
    "02-OSINT/engenharia-software/laboratorios/lab-01-contrato-complexidade.md": [
        "02-OSINT/engenharia-software/00-como-pensar-problemas.md",
        "02-OSINT/engenharia-software/01-complexidade.md",
    ],
    "02-OSINT/engenharia-software/laboratorios/lab-02-estruturas-grafos.md": [
        "02-OSINT/engenharia-software/laboratorios/lab-01-contrato-complexidade.md",
        "02-OSINT/engenharia-software/02-estruturas-lineares.md",
        "02-OSINT/engenharia-software/03-arvores-heaps-tries.md",
        "02-OSINT/engenharia-software/04-grafos.md",
        "02-OSINT/engenharia-software/05-busca-ordenacao.md",
        "02-OSINT/engenharia-software/exemplos/README.md",
    ],
    "02-OSINT/engenharia-software/laboratorios/lab-03-estrategias-design.md": [
        "02-OSINT/engenharia-software/laboratorios/lab-02-estruturas-grafos.md",
        "02-OSINT/engenharia-software/06-recursao-backtracking.md",
        "02-OSINT/engenharia-software/07-programacao-dinamica-gulosa.md",
        "02-OSINT/engenharia-software/08-paradigmas-tipos.md",
        "02-OSINT/engenharia-software/09-design-modular.md",
        "02-OSINT/engenharia-software/10-solid-patterns.md",
        "02-OSINT/engenharia-software/projetos/dependency-planner/README.md",
    ],
    "02-OSINT/engenharia-software/laboratorios/lab-04-evolucao-arquitetura-testes.md": [
        "02-OSINT/engenharia-software/laboratorios/lab-03-estrategias-design.md",
        "02-OSINT/engenharia-software/11-refatoracao-legado.md",
        "02-OSINT/engenharia-software/12-requisitos-modelagem.md",
        "02-OSINT/engenharia-software/13-arquitetura.md",
        "02-OSINT/engenharia-software/14-testes-qualidade.md",
        "02-OSINT/engenharia-software/15-colaboracao-documentacao.md",
        "02-OSINT/engenharia-software/GUIA-DIAGNOSTICO.md",
    ],
    "02-OSINT/engenharia-software/laboratorios/lab-05-dependency-planner.md": [
        "02-OSINT/engenharia-software/laboratorios/lab-01-contrato-complexidade.md",
        "02-OSINT/engenharia-software/laboratorios/lab-02-estruturas-grafos.md",
        "02-OSINT/engenharia-software/laboratorios/lab-03-estrategias-design.md",
        "02-OSINT/engenharia-software/laboratorios/lab-04-evolucao-arquitetura-testes.md",
        "02-OSINT/engenharia-software/GUIA-DIAGNOSTICO.md",
        "02-OSINT/engenharia-software/CADERNO-PRATICAS.md",
        "02-OSINT/engenharia-software/projetos/dependency-planner/README.md",
        "02-OSINT/engenharia-software/16-projetos-avaliacao.md",
    ],
}


class Module02CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "02" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_route_interleaves_theory_practice_and_capstone(self) -> None:
        self.assertEqual([document["sourcePath"] for document in self.documents[: len(ROUTE)]], ROUTE)
        self.assertEqual([document["order"] for document in self.documents], list(range(len(self.documents))))
        for path in ROUTE:
            self.assertEqual(self.by_path[path]["id"], builder._document_id(path))

    def test_required_support_and_project_documents_are_explicit(self) -> None:
        for path in (
            "02-OSINT/engenharia-software/GUIA-DIAGNOSTICO.md",
            "02-OSINT/engenharia-software/CADERNO-PRATICAS.md",
            "02-OSINT/engenharia-software/exemplos/README.md",
            "02-OSINT/engenharia-software/projetos/dependency-planner/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        project = self.by_path[
            "02-OSINT/engenharia-software/projetos/dependency-planner/README.md"
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
        course_root = ROOT / "02-OSINT/engenharia-software"
        chapters = sorted(course_root.glob("[0-1][0-9]-*.md"))
        self.assertEqual(len(chapters), 17)
        for chapter in chapters:
            text = chapter.read_text(encoding="utf-8")
            words = re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)
            self.assertGreaterEqual(len(words), 1_200, chapter.name)
            self.assertRegex(text, r"(?im)^## .*objetiv", chapter.name)
            self.assertRegex(text, r"(?im)^## .*?(exerc|laborat)", chapter.name)
            self.assertRegex(text, r"(?im)^## .*checklist|^## .*domínio", chapter.name)


if __name__ == "__main__":
    unittest.main()
