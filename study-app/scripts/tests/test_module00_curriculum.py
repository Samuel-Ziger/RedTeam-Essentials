from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module00_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


ROUTE = [
    "00-Fundamentos/README.md",
    "00-Fundamentos/programacao/README.md",
    "00-Fundamentos/programacao/00-como-estudar.md",
    "00-Fundamentos/programacao/01-logica-algoritmos.md",
    "00-Fundamentos/programacao/02-ambiente-terminal-git.md",
    "00-Fundamentos/programacao/GUIA-DEPURACAO.md",
    "00-Fundamentos/programacao/03-fundamentos-comuns.md",
    "00-Fundamentos/programacao/linguagens/python.md",
    "00-Fundamentos/programacao/labs/lab-01-logica-controle-fluxo.md",
    "00-Fundamentos/programacao/04-estruturas-dados-algoritmos.md",
    "00-Fundamentos/programacao/linguagens/java.md",
    "00-Fundamentos/programacao/labs/lab-02-cli-git-duas-linguagens.md",
    "00-Fundamentos/programacao/linguagens/csharp.md",
    "00-Fundamentos/programacao/05-engenharia-software.md",
    "00-Fundamentos/programacao/labs/lab-03-agenda-persistencia-testes.md",
    "00-Fundamentos/programacao/linguagens/c.md",
    "00-Fundamentos/programacao/linguagens/javascript.md",
    "00-Fundamentos/programacao/06-web-http-bancos.md",
    "00-Fundamentos/programacao/labs/lab-04-http-api-sqlite.md",
    "00-Fundamentos/programacao/07-sistemas-concorrencia.md",
    "00-Fundamentos/programacao/08-docker-nginx.md",
    "00-Fundamentos/programacao/CADERNO-PRATICAS.md",
    "00-Fundamentos/programacao/09-projetos.md",
    "00-Fundamentos/programacao/projetos/taskboard/README.md",
    "00-Fundamentos/programacao/labs/lab-05-taskboard-docker-nginx.md",
]

LAB_REQUIREMENTS = {
    "00-Fundamentos/programacao/labs/lab-01-logica-controle-fluxo.md": [
        "00-Fundamentos/programacao/00-como-estudar.md",
        "00-Fundamentos/programacao/01-logica-algoritmos.md",
        "00-Fundamentos/programacao/02-ambiente-terminal-git.md",
        "00-Fundamentos/programacao/linguagens/python.md",
    ],
    "00-Fundamentos/programacao/labs/lab-02-cli-git-duas-linguagens.md": [
        "00-Fundamentos/programacao/00-como-estudar.md",
        "00-Fundamentos/programacao/01-logica-algoritmos.md",
        "00-Fundamentos/programacao/02-ambiente-terminal-git.md",
        "00-Fundamentos/programacao/03-fundamentos-comuns.md",
        "00-Fundamentos/programacao/linguagens/python.md",
        "00-Fundamentos/programacao/linguagens/java.md",
    ],
    "00-Fundamentos/programacao/labs/lab-03-agenda-persistencia-testes.md": [
        "00-Fundamentos/programacao/02-ambiente-terminal-git.md",
        "00-Fundamentos/programacao/GUIA-DEPURACAO.md",
        "00-Fundamentos/programacao/03-fundamentos-comuns.md",
        "00-Fundamentos/programacao/linguagens/python.md",
        "00-Fundamentos/programacao/04-estruturas-dados-algoritmos.md",
        "00-Fundamentos/programacao/05-engenharia-software.md",
    ],
    "00-Fundamentos/programacao/labs/lab-04-http-api-sqlite.md": [
        "00-Fundamentos/programacao/GUIA-DEPURACAO.md",
        "00-Fundamentos/programacao/linguagens/python.md",
        "00-Fundamentos/programacao/05-engenharia-software.md",
        "00-Fundamentos/programacao/06-web-http-bancos.md",
    ],
    "00-Fundamentos/programacao/labs/lab-05-taskboard-docker-nginx.md": [
        "00-Fundamentos/programacao/GUIA-DEPURACAO.md",
        "00-Fundamentos/programacao/06-web-http-bancos.md",
        "00-Fundamentos/programacao/07-sistemas-concorrencia.md",
        "00-Fundamentos/programacao/08-docker-nginx.md",
        "00-Fundamentos/programacao/09-projetos.md",
        "00-Fundamentos/programacao/projetos/taskboard/README.md",
    ],
}


class Module00CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "00" and document["origin"] == "formation"
        ]
        cls.by_path = {document["sourcePath"]: document for document in cls.documents}
        cls.path_by_id = {document["id"]: document["sourcePath"] for document in cls.documents}

    def test_real_route_interleaves_chapters_and_language_guides(self) -> None:
        self.assertEqual([document["sourcePath"] for document in self.documents[: len(ROUTE)]], ROUTE)
        self.assertEqual([document["order"] for document in self.documents], list(range(len(self.documents))))
        for path in ROUTE:
            self.assertEqual(self.by_path[path]["id"], builder._document_id(path))

    def test_required_supplements_and_taskboard_are_explicit(self) -> None:
        for path in (
            "00-Fundamentos/programacao/GUIA-DEPURACAO.md",
            "00-Fundamentos/programacao/CADERNO-PRATICAS.md",
            "00-Fundamentos/programacao/projetos/taskboard/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        taskboard = self.by_path["00-Fundamentos/programacao/projetos/taskboard/README.md"]
        self.assertEqual(taskboard["role"], "project_readme")

    def test_five_labs_use_exact_semantic_prerequisites(self) -> None:
        for lab_path, expected_paths in LAB_REQUIREMENTS.items():
            lab = self.by_path[lab_path]
            actual_paths = [self.path_by_id[document_id] for document_id in lab["prerequisites"]]
            self.assertEqual(actual_paths, expected_paths, lab_path)
            self.assertTrue(lab["required"], lab_path)


if __name__ == "__main__":
    unittest.main()
