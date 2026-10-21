from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "study-app/scripts/build_catalog.py"
SPEC = importlib.util.spec_from_file_location("module01_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


ROUTE = [
    "01-Recon/README.md",
    "01-Recon/programacao-avancada/README.md",
    "01-Recon/programacao-avancada/00-arquitetura-dados.md",
    "01-Recon/programacao-avancada/01-modelagem-relacional.md",
    "01-Recon/programacao-avancada/02-sql-fundamentos.md",
    "01-Recon/programacao-avancada/laboratorios/lab-01-modelagem-sql.md",
    "01-Recon/programacao-avancada/03-sql-avancado.md",
    "01-Recon/programacao-avancada/04-transacoes-concorrencia.md",
    "01-Recon/programacao-avancada/05-indices-performance.md",
    "01-Recon/programacao-avancada/laboratorios/lab-02-transacoes-indices.md",
    "01-Recon/programacao-avancada/06-nosql-modelos.md",
    "01-Recon/programacao-avancada/07-mongodb.md",
    "01-Recon/programacao-avancada/laboratorios/lab-03-mongodb-documentos.md",
    "01-Recon/programacao-avancada/08-anatomia-api.md",
    "01-Recon/programacao-avancada/09-design-api-http.md",
    "01-Recon/programacao-avancada/10-implementacao-api.md",
    "01-Recon/programacao-avancada/11-seguranca-api.md",
    "01-Recon/programacao-avancada/12-testes-observabilidade.md",
    "01-Recon/programacao-avancada/15-stacks-multilinguagem.md",
    "01-Recon/programacao-avancada/exemplos/README.md",
    "01-Recon/programacao-avancada/laboratorios/lab-04-contrato-api.md",
    "01-Recon/programacao-avancada/13-dados-distribuidos.md",
    "01-Recon/programacao-avancada/GUIA-DIAGNOSTICO.md",
    "01-Recon/programacao-avancada/CADERNO-PRATICAS.md",
    "01-Recon/programacao-avancada/projetos/inventory-api/README.md",
    "01-Recon/programacao-avancada/14-projetos-avaliacao.md",
    "01-Recon/programacao-avancada/laboratorios/lab-05-inventory-capstone.md",
]


LAB_REQUIREMENTS = {
    "01-Recon/programacao-avancada/laboratorios/lab-01-modelagem-sql.md": [
        "01-Recon/programacao-avancada/00-arquitetura-dados.md",
        "01-Recon/programacao-avancada/01-modelagem-relacional.md",
        "01-Recon/programacao-avancada/02-sql-fundamentos.md",
    ],
    "01-Recon/programacao-avancada/laboratorios/lab-02-transacoes-indices.md": [
        "01-Recon/programacao-avancada/03-sql-avancado.md",
        "01-Recon/programacao-avancada/04-transacoes-concorrencia.md",
        "01-Recon/programacao-avancada/05-indices-performance.md",
    ],
    "01-Recon/programacao-avancada/laboratorios/lab-03-mongodb-documentos.md": [
        "01-Recon/programacao-avancada/06-nosql-modelos.md",
        "01-Recon/programacao-avancada/07-mongodb.md",
    ],
    "01-Recon/programacao-avancada/laboratorios/lab-04-contrato-api.md": [
        "01-Recon/programacao-avancada/08-anatomia-api.md",
        "01-Recon/programacao-avancada/09-design-api-http.md",
        "01-Recon/programacao-avancada/10-implementacao-api.md",
        "01-Recon/programacao-avancada/11-seguranca-api.md",
        "01-Recon/programacao-avancada/12-testes-observabilidade.md",
        "01-Recon/programacao-avancada/15-stacks-multilinguagem.md",
        "01-Recon/programacao-avancada/exemplos/README.md",
    ],
    "01-Recon/programacao-avancada/laboratorios/lab-05-inventory-capstone.md": [
        "01-Recon/programacao-avancada/laboratorios/lab-01-modelagem-sql.md",
        "01-Recon/programacao-avancada/laboratorios/lab-02-transacoes-indices.md",
        "01-Recon/programacao-avancada/laboratorios/lab-03-mongodb-documentos.md",
        "01-Recon/programacao-avancada/laboratorios/lab-04-contrato-api.md",
        "01-Recon/programacao-avancada/12-testes-observabilidade.md",
        "01-Recon/programacao-avancada/13-dados-distribuidos.md",
        "01-Recon/programacao-avancada/15-stacks-multilinguagem.md",
        "01-Recon/programacao-avancada/GUIA-DIAGNOSTICO.md",
        "01-Recon/programacao-avancada/projetos/inventory-api/README.md",
        "01-Recon/programacao-avancada/14-projetos-avaliacao.md",
    ],
}


class Module01CurriculumIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, _ = builder.assemble_catalog(ROOT)
        cls.documents = [
            document
            for document in cls.catalog["documents"]
            if document["module"] == "01" and document["origin"] == "formation"
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
            "01-Recon/programacao-avancada/GUIA-DIAGNOSTICO.md",
            "01-Recon/programacao-avancada/CADERNO-PRATICAS.md",
            "01-Recon/programacao-avancada/exemplos/README.md",
            "01-Recon/programacao-avancada/projetos/inventory-api/README.md",
        ):
            self.assertTrue(self.by_path[path]["required"], path)
        self.assertEqual(
            self.by_path["01-Recon/programacao-avancada/projetos/inventory-api/README.md"]["role"],
            "project_readme",
        )

    def test_five_required_labs_use_exact_semantic_prerequisites(self) -> None:
        required_labs = {
            document["sourcePath"]
            for document in self.documents
            if document["role"] == "lab_instruction" and document["required"]
        }
        self.assertEqual(required_labs, set(LAB_REQUIREMENTS))
        for lab_path, expected_paths in LAB_REQUIREMENTS.items():
            lab = self.by_path[lab_path]
            actual_paths = [self.path_by_id[document_id] for document_id in lab["prerequisites"]]
            self.assertEqual(actual_paths, expected_paths, lab_path)

    def test_module01_contains_only_programming_data_and_api_material(self) -> None:
        self.assertEqual(
            {path.name for path in (ROOT / "01-Recon").iterdir()},
            {"README.md", "programacao-avancada"},
        )
        module_documents = [
            document for document in self.catalog["documents"] if document["module"] == "01"
        ]
        self.assertTrue(module_documents)
        self.assertTrue(
            all(
                document["sourcePath"] == "01-Recon/README.md"
                or document["sourcePath"].startswith("01-Recon/programacao-avancada/")
                for document in module_documents
            )
        )
        self.assertFalse(any(document["origin"] == "legacy" for document in module_documents))

    def test_recon_archive_belongs_to_module29(self) -> None:
        legacy = next(
            document
            for document in self.catalog["documents"]
            if document["sourcePath"] == "29-Reconhecimento-OSINT/LEGADO-RECON.md"
        )
        self.assertEqual(legacy["module"], "29")
        self.assertEqual(legacy["origin"], "legacy")
        self.assertFalse(legacy["required"])

    def test_modules_00_to_26_do_not_store_advanced_security_archives(self) -> None:
        manifest = json.loads((ROOT / "STUDY-CONTENT.json").read_text(encoding="utf-8"))
        courses = {
            course["moduleId"]: course
            for course in manifest["courses"]
            if int(course["moduleId"]) <= 26
        }
        self.assertEqual(set(courses), {f"{number:02d}" for number in range(27)})

        for module_id, course in courses.items():
            module_root = ROOT / Path(course["overviewPath"]).parent
            course_root = Path(course["courseRoot"])
            self.assertEqual(
                {path.name for path in module_root.iterdir()},
                {Path(course["overviewPath"]).name, course_root.name},
                module_id,
            )
            self.assertFalse(course.get("contentPaths"), module_id)

            allowed_overview = course["overviewPath"]
            allowed_prefix = f"{course['courseRoot']}/"
            module_documents = [
                document
                for document in self.catalog["documents"]
                if document.get("module") == module_id
            ]
            self.assertTrue(module_documents, module_id)
            self.assertTrue(
                all(
                    document["sourcePath"] == allowed_overview
                    or document["sourcePath"].startswith(allowed_prefix)
                    for document in module_documents
                ),
                module_id,
            )
            self.assertFalse(
                any(document["origin"] == "legacy" for document in module_documents),
                module_id,
            )


if __name__ == "__main__":
    unittest.main()
