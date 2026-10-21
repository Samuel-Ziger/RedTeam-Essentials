from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "build_catalog.py"
SPEC = importlib.util.spec_from_file_location("study_catalog_builder", SCRIPT)
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _fixture_repo(root: Path) -> None:
    modules = []
    courses = []
    _write(root / "study-app/README.md", "# Aplicação de estudos\n\nGuia local.\n")
    for number in range(27):
        module_id = f"{number:02d}"
        module_path = f"{module_id}-Modulo-{module_id}"
        prerequisites = [f"{number - 1:02d}"] if number else []
        modules.append(
            {
                "id": module_id,
                "path": module_path,
                "title": f"Módulo {module_id}",
                "maturity": "established",
                "status": "active",
                "prerequisites": prerequisites,
                "estimatedHours": {"min": 1, "max": 2},
            }
        )
        courses.append(
            {
                "moduleId": module_id,
                "courseRoot": f"{module_path}/curso",
                "overviewPath": f"{module_path}/README.md",
                "legacyId": f"tema-{module_id}",
                "legacyTitle": f"Tema legado {module_id}",
            }
        )
        _write(
            root / module_path / "README.md",
            f"# Visão geral {module_id}\n\nDescrição objetiva do módulo {module_id}.\n",
        )
        chapter_count = 4 if number == 0 else 2
        lab_count = 2 if number == 0 else 1
        for chapter in range(chapter_count):
            _write(
                root / module_path / "curso" / f"{chapter:02d}-capitulo.md",
                (
                    f"# Capítulo {chapter}\n\n"
                    f"Texto introdutório do capítulo {chapter}, com palavras suficientes para leitura.\n"
                ),
            )
        for lab in range(1, lab_count + 1):
            _write(
                root / module_path / "curso" / "laboratorios" / f"{lab:02d}-pratica.md",
                f"# Laboratório {lab}\n\nPrática local e determinística {lab}.\n",
            )
        _write(
            root / module_path / "curso" / "REFERENCIAS.md",
            "# Referências\n\nDocumentação complementar.\n",
        )
        _write(
            root / module_path / "nota-extra.md",
            "# Nota extra\n\nMaterial suplementar.\n",
        )

    (root / "MODULE-CATALOG.json").write_text(
        json.dumps({"schemaVersion": 1, "modules": modules}, ensure_ascii=False),
        encoding="utf-8",
    )
    (root / "STUDY-CONTENT.json").write_text(
        json.dumps(
            {
                "schemaVersion": 2,
                "collections": [
                    {
                        "id": "formacao-principal",
                        "order": 0,
                        "kind": "curriculum",
                        "title": "Formação principal",
                    },
                    {
                        "id": "acervo-seguranca",
                        "order": 1,
                        "kind": "library",
                        "title": "Acervo de segurança",
                    },
                    {
                        "id": "laboratorios-projetos",
                        "order": 2,
                        "kind": "practice",
                        "title": "Laboratórios e projetos",
                    },
                    {
                        "id": "ferramentas-codigo",
                        "order": 3,
                        "kind": "resources",
                        "title": "Ferramentas e código",
                    },
                    {
                        "id": "documentacao-global",
                        "order": 4,
                        "kind": "documentation",
                        "title": "Documentação global",
                    },
                ],
                "courses": courses,
                "globalDocuments": {
                    "includeAllOutsideModules": True,
                    "collectionId": "documentacao-global",
                    "includePaths": ["study-app/README.md"],
                },
                "resources": {
                    "includeAllSafeFiles": True,
                    "collectionId": "ferramentas-codigo",
                    "includePaths": [],
                },
                "exclusions": {
                    "roots": [".git", "study-app"],
                    "paths": ["MODULE-CATALOG.json", "STUDY-CONTENT.json"],
                    "reason": "Infraestrutura de teste.",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


class BuildCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        _fixture_repo(self.root)
        self.output = Path(self.temporary.name) / "generated"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_tracks_modules_and_ids_have_stable_order(self) -> None:
        catalog, _ = builder.assemble_catalog(self.root)

        self.assertEqual(catalog["schemaVersion"], 2)
        self.assertEqual(
            [track["id"] for track in catalog["tracks"]],
            [
                "programacao",
                "sistemas-operacionais",
                "redes",
                "criptografia",
                "privacidade",
                "purple-team",
            ],
        )
        self.assertEqual(catalog["tracks"][0]["moduleIds"], ["00", "01", "02", "03", "04", "05"])
        self.assertEqual(catalog["tracks"][-1]["moduleIds"], ["26"])
        self.assertEqual([module["order"] for module in catalog["modules"]], list(range(27)))
        self.assertEqual(catalog["modules"][1]["prerequisiteModuleIds"], ["00"])
        self.assertNotIn("generatedAt", catalog)

        ids = [document["id"] for document in catalog["documents"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(document_id.startswith("document-") for document_id in ids))

    def test_catalog_can_extend_beyond_foundational_modules(self) -> None:
        module_catalog_path = self.root / "MODULE-CATALOG.json"
        module_catalog = json.loads(module_catalog_path.read_text(encoding="utf-8"))
        module_catalog["modules"].append(
            {
                "id": "27",
                "path": "27-Modulo-27",
                "title": "Especialização",
                "maturity": "established",
                "status": "active",
                "prerequisites": ["26"],
                "estimatedHours": {"min": 1, "max": 2},
            }
        )
        module_catalog_path.write_text(
            json.dumps(module_catalog, ensure_ascii=False),
            encoding="utf-8",
        )

        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["courses"].append(
            {
                "moduleId": "27",
                "courseRoot": "27-Modulo-27/curso",
                "overviewPath": "27-Modulo-27/README.md",
                "legacyId": "especializacao",
                "legacyTitle": "Complementos da especialização",
            }
        )
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        _write(self.root / "27-Modulo-27/README.md", "# Especialização\n\nVisão geral.\n")
        _write(self.root / "27-Modulo-27/curso/00-capitulo.md", "# Capítulo avançado\n\nConteúdo.\n")

        catalog, _ = builder.assemble_catalog(self.root)

        self.assertEqual(len(catalog["modules"]), 28)
        self.assertEqual(catalog["modules"][-1]["id"], "27")
        self.assertEqual(catalog["tracks"][-1]["id"], "especializacao-seguranca")
        self.assertEqual(catalog["tracks"][-1]["moduleIds"], ["27"])

    def test_schema_v2_exposes_collections_courses_legacy_and_complete_coverage(self) -> None:
        catalog, _ = builder.assemble_catalog(self.root)

        self.assertEqual(
            [collection["id"] for collection in catalog["collections"]],
            [
                "formacao-principal",
                "acervo-seguranca",
                "laboratorios-projetos",
                "ferramentas-codigo",
                "documentacao-global",
            ],
        )
        self.assertEqual(len(catalog["courses"]), 27)
        self.assertEqual(len(catalog["legacySections"]), 27)
        self.assertEqual(catalog["courses"][0]["rootPath"], "00-Modulo-00/curso")
        self.assertEqual(catalog["legacySections"][0]["title"], "Tema legado 00")
        self.assertEqual(catalog["modules"][0]["courseId"], "course-00")
        self.assertEqual(catalog["tracks"][0]["collectionId"], "formacao-principal")

        coverage = catalog["stats"]["coverage"]
        self.assertEqual(coverage["unassigned"], 0)
        self.assertEqual(coverage["markdown"]["unassigned"], 0)
        self.assertEqual(coverage["resources"]["unassigned"], 0)
        self.assertTrue(coverage["byCategory"])
        self.assertTrue(all(item["unassigned"] == 0 for item in coverage["byCategory"].values()))
        self.assertEqual(coverage["eligible"], coverage["assigned"])

    def test_classifies_documents_and_copies_exact_markdown(self) -> None:
        catalog_path = builder.build_catalog(self.root, self.output)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        module = catalog["modules"][0]
        documents = [document for document in catalog["documents"] if document["module"] == "00"]

        self.assertEqual(module["stats"]["byType"]["overview"], 1)
        self.assertEqual(module["stats"]["byType"]["chapter"], 4)
        self.assertEqual(module["stats"]["byType"]["lab"], 2)
        self.assertEqual(module["stats"]["byType"]["reference"], 1)
        self.assertEqual(module["stats"]["byType"]["supplement"], 1)

        chapter = next(document for document in documents if document["type"] == "chapter")
        self.assertEqual(chapter["title"], "Capítulo 0")
        self.assertTrue(chapter["description"].startswith("Texto introdutório"))
        self.assertGreater(chapter["words"], 0)
        self.assertGreaterEqual(chapter["readingMinutes"], 1)
        self.assertEqual(chapter["module"], "00")
        self.assertEqual(chapter["contentUrl"], f"/generated/content/{chapter['sourcePath']}")

        source = self.root / chapter["sourcePath"]
        copied = self.output / "content" / chapter["sourcePath"]
        self.assertEqual(copied.read_bytes(), source.read_bytes())

        self.assertEqual(chapter["role"], "lesson")
        self.assertEqual(chapter["origin"], "formation")
        self.assertTrue(chapter["required"])
        self.assertEqual(chapter["language"], "markdown")
        self.assertEqual(chapter["category"], "course")
        self.assertEqual(chapter["courseId"], "course-00")
        self.assertEqual(chapter["memberships"][0]["collectionId"], "formacao-principal")

        reference = next(document for document in documents if document["role"] == "reference")
        legacy = next(document for document in documents if document["sourcePath"].endswith("nota-extra.md"))
        self.assertFalse(reference["required"])
        self.assertEqual(legacy["origin"], "legacy")
        self.assertEqual(legacy["role"], "legacy_document")
        self.assertFalse(legacy["required"])

    def test_content_paths_adopt_existing_material_without_changing_source_path(self) -> None:
        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["courses"][1]["contentPaths"] = ["00-Modulo-00/nota-extra.md"]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

        catalog, _ = builder.assemble_catalog(self.root)
        adopted = next(
            document
            for document in catalog["documents"]
            if document["sourcePath"] == "00-Modulo-00/nota-extra.md"
        )

        self.assertEqual(adopted["module"], "01")
        self.assertEqual(adopted["origin"], "formation")
        self.assertEqual(adopted["courseId"], "course-01")
        self.assertEqual(adopted["role"], "lesson")
        self.assertTrue(adopted["required"])
        self.assertIn(adopted["id"], catalog["courses"][1]["documentIds"])
        self.assertFalse(
            any(section["moduleId"] == "00" for section in catalog["legacySections"]),
            "uma seção legada vazia não deve permanecer no catálogo",
        )

    def test_adopted_lab_readme_keeps_its_existing_practice_semantics(self) -> None:
        adopted_path = "00-Modulo-00/labs"
        _write(
            self.root / adopted_path / "README.md",
            "# Laboratório adotado\n\n## Procedimento\n\n1. Analise a fixture local.\n",
        )
        _write(self.root / adopted_path / "fixture.json", '{"ok": true}\n')
        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["courses"][1]["contentPaths"] = [adopted_path]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

        catalog, _ = builder.assemble_catalog(self.root)
        adopted = next(
            document
            for document in catalog["documents"]
            if document["sourcePath"] == f"{adopted_path}/README.md"
        )

        self.assertEqual(adopted["module"], "01")
        self.assertEqual(adopted["origin"], "formation")
        self.assertEqual(adopted["role"], "lab_instruction")
        self.assertEqual(adopted["type"], "lab")
        expected_prerequisites = {
            document["id"]
            for document in catalog["documents"]
            if document["module"] == "01" and document["required"] and document["type"] != "lab"
        }
        self.assertEqual(set(adopted["prerequisites"]), expected_prerequisites)
        self.assertTrue(any(lab["id"] == adopted["id"] for lab in catalog["labs"]))

    def test_global_markdown_is_navigable_and_keeps_v1_asset_alias(self) -> None:
        _write(self.root / "LICENSE", "Licença de teste.\n")
        _write(self.root / "GUIDE.md", "# Guia global\n\nDocumento global navegável.\n\n[Licença](LICENSE)\n")
        chapter = self.root / "00-Modulo-00/curso/00-capitulo.md"
        chapter.write_text(
            chapter.read_text(encoding="utf-8") + "\n[Guia](../../GUIDE.md)\n",
            encoding="utf-8",
        )

        catalog_path = builder.build_catalog(self.root, self.output)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        guide = next(document for document in catalog["documents"] if document["sourcePath"] == "GUIDE.md")
        alias = next(resource for resource in catalog["assets"] if resource["sourcePath"] == "GUIDE.md")
        linked_chapter = next(
            document
            for document in catalog["documents"]
            if document["sourcePath"] == "00-Modulo-00/curso/00-capitulo.md"
        )

        self.assertEqual(guide["role"], "global_document")
        self.assertEqual(guide["origin"], "global")
        self.assertFalse(guide["required"])
        self.assertEqual(guide["memberships"][0]["collectionId"], "documentacao-global")
        self.assertIn(guide["id"], catalog["globalDocumentIds"])
        self.assertEqual(alias["id"], builder._asset_id("GUIDE.md"))
        self.assertEqual(alias["aliasOfDocumentId"], guide["id"])
        self.assertIn(alias["id"], linked_chapter["assetIds"])
        self.assertIn(builder._asset_id("LICENSE"), linked_chapter["assetIds"])
        self.assertIn(guide["id"], linked_chapter["relatedDocumentIds"])
        self.assertEqual((self.output / "content/GUIDE.md").read_bytes(), (self.root / "GUIDE.md").read_bytes())

    def test_labs_unlock_progressively_from_nearest_course(self) -> None:
        catalog, _ = builder.assemble_catalog(self.root)
        module_documents = [document for document in catalog["documents"] if document["module"] == "00"]
        chapters = sorted(
            (document for document in module_documents if document["type"] == "chapter"),
            key=lambda document: document["chapterNumber"],
        )
        labs = sorted(
            (document for document in module_documents if document["type"] == "lab"),
            key=lambda document: document["labNumber"],
        )

        self.assertEqual(labs[0]["prerequisites"], [chapter["id"] for chapter in chapters[:2]])
        self.assertEqual(labs[1]["prerequisites"], [chapter["id"] for chapter in chapters])
        self.assertEqual(labs[0]["coursePath"], "00-Modulo-00/curso")
        document_ids = {document["id"] for document in catalog["documents"]}
        self.assertTrue(
            all(
                prerequisite in document_ids
                for document in catalog["documents"]
                for prerequisite in document["prerequisites"]
            )
        )

    def test_document_overrides_define_order_required_and_exact_prerequisites(self) -> None:
        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        course = manifest["courses"][0]
        root = "00-Modulo-00/curso"
        chapter_zero = f"{root}/00-capitulo.md"
        chapter_two = f"{root}/02-capitulo.md"
        lab_one = f"{root}/laboratorios/01-pratica.md"
        course["documentOverrides"] = [
            {"sourcePath": chapter_two, "order": 0, "required": True},
            {"sourcePath": chapter_zero, "order": 1, "required": True},
            {
                "sourcePath": lab_one,
                "order": 2,
                "required": True,
                "prerequisitePaths": [chapter_two, chapter_zero],
            },
        ]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

        catalog, _ = builder.assemble_catalog(self.root)
        documents = [document for document in catalog["documents"] if document["module"] == "00"]
        by_path = {document["sourcePath"]: document for document in documents}

        self.assertEqual([document["sourcePath"] for document in documents[:3]], [chapter_two, chapter_zero, lab_one])
        self.assertEqual(
            by_path[lab_one]["prerequisites"],
            [by_path[chapter_two]["id"], by_path[chapter_zero]["id"]],
        )
        self.assertTrue(by_path[lab_one]["required"])
        self.assertEqual(by_path[chapter_two]["id"], builder._document_id(chapter_two))

    def test_legacy_labs_are_optional_and_do_not_inherit_formation_prerequisites(self) -> None:
        module = self.root / "00-Modulo-00"
        _write(
            module / "legado" / "labs" / "README.md",
            "# Laboratórios legados\n\nLeia estas regras antes da prática.\n",
        )
        _write(
            module / "legado" / "labs" / "01-antigo.md",
            "# Laboratório legado\n\nPrática isolada.\n",
        )

        catalog, _ = builder.assemble_catalog(self.root)
        orphan = next(
            document for document in catalog["documents"] if document["sourcePath"].endswith("legado/labs/01-antigo.md")
        )
        lab_overview = next(
            document for document in catalog["documents"] if document["sourcePath"].endswith("legado/labs/README.md")
        )
        sibling_chapter_ids = {
            document["id"]
            for document in catalog["documents"]
            if document["module"] == "00" and document["type"] == "chapter"
        }

        self.assertEqual(orphan["prerequisites"], [])
        self.assertEqual(orphan["coursePath"], "00-Modulo-00/legado/labs")
        self.assertEqual(orphan["role"], "lab_instruction")
        self.assertEqual(orphan["origin"], "legacy")
        self.assertFalse(orphan["required"])
        self.assertEqual(lab_overview["role"], "lab_instruction")
        self.assertTrue(sibling_chapter_ids.isdisjoint(orphan["prerequisites"]))

    def test_lab_indexes_solutions_and_projects_have_distinct_roles(self) -> None:
        course = self.root / "00-Modulo-00/curso"
        _write(course / "laboratorios/README.md", "# Índice de laboratórios\n")
        _write(course / "laboratorios/api/README.md", "# Laboratório de API\n\nPrática guiada.\n")
        _write(course / "laboratorios/answers/api.md", "# Solução\n\nResposta controlada.\n")
        _write(course / "laboratorios/api/fixture.json", '{"ok": true}\n')
        _write(course / "projetos/demo/README.md", "# Projeto demo\n\nProjeto integrador.\n")
        _write(course / "projetos/demo/docs/001-decisao.md", "# Decisão\n\nRegistro do projeto.\n")
        _write(course / "projetos/demo/app.py", "print('demo')\n")

        catalog, _ = builder.assemble_catalog(self.root)
        by_path = {document["sourcePath"]: document for document in catalog["documents"]}
        lab_index = by_path["00-Modulo-00/curso/laboratorios/README.md"]
        lab_document = by_path["00-Modulo-00/curso/laboratorios/api/README.md"]
        solution = by_path["00-Modulo-00/curso/laboratorios/answers/api.md"]
        project_readme = by_path["00-Modulo-00/curso/projetos/demo/README.md"]
        project_document = by_path["00-Modulo-00/curso/projetos/demo/docs/001-decisao.md"]

        self.assertEqual(lab_index["role"], "lab_index")
        self.assertFalse(lab_index["required"])
        self.assertEqual(lab_document["role"], "lab_instruction")
        self.assertEqual(lab_document["type"], "lab")
        self.assertTrue(lab_document["required"])
        self.assertEqual(solution["role"], "solution")
        self.assertFalse(solution["required"])
        self.assertEqual(project_readme["role"], "project_readme")
        self.assertEqual(project_document["role"], "project_document")
        self.assertFalse(project_readme["required"])

        lab = next(item for item in catalog["labs"] if item["instructionDocumentId"] == lab_document["id"])
        self.assertIn(solution["id"], lab["solutionDocumentIds"])
        self.assertTrue(lab["resourceIds"])
        project = next(item for item in catalog["projects"] if item["readmeDocumentId"] == project_readme["id"])
        self.assertIn(project_document["id"], project["documentIds"])
        self.assertTrue(project["resourceIds"])
        self.assertIn(lab["id"], catalog["collections"][2]["labIds"])
        self.assertIn(project["id"], catalog["collections"][2]["projectIds"])

    def test_legacy_docker_lab_is_optional_practice_with_its_resources(self) -> None:
        module = self.root / "01-Modulo-01/docker-lab"
        _write(module / "README.md", "# Docker lab\n\nAmbiente local isolado.\n")
        _write(module / "docker-compose.yml", "services: {}\n")
        _write(module / "Dockerfile.attacker", "FROM scratch\n")

        catalog, _ = builder.assemble_catalog(self.root)
        document = next(
            item for item in catalog["documents"] if item["sourcePath"] == "01-Modulo-01/docker-lab/README.md"
        )
        lab = next(item for item in catalog["labs"] if item["instructionDocumentId"] == document["id"])
        resources = {
            item["sourcePath"]: item
            for item in catalog["resources"]
            if item["sourcePath"].startswith("01-Modulo-01/docker-lab/")
        }

        self.assertEqual(document["role"], "lab_instruction")
        self.assertEqual(document["origin"], "legacy")
        self.assertFalse(document["required"])
        self.assertTrue(
            any(membership["collectionId"] == "laboratorios-projetos" for membership in document["memberships"])
        )
        self.assertEqual(resources["01-Modulo-01/docker-lab/docker-compose.yml"]["category"], "configuration")
        self.assertTrue(
            any(
                membership["collectionId"] == "laboratorios-projetos"
                for membership in resources["01-Modulo-01/docker-lab/docker-compose.yml"]["memberships"]
            )
        )
        self.assertTrue(lab["resourceIds"])

    def test_generation_is_deterministic_and_prunes_stale_content(self) -> None:
        first_path = builder.build_catalog(self.root, self.output)
        first = first_path.read_bytes()
        stale = self.output / "content" / "arquivo-obsoleto.md"
        stale.write_text("obsoleto", encoding="utf-8")

        second_path = builder.build_catalog(self.root, self.output)
        second = second_path.read_bytes()

        self.assertEqual(first, second)
        self.assertFalse(stale.exists())
        self.assertEqual(
            (self.output / builder.GENERATED_MARKER).read_text(encoding="utf-8"),
            builder.MARKER_CONTENT,
        )

    def test_copies_all_safe_resources_and_preserves_linked_asset_ids(self) -> None:
        module = self.root / "00-Modulo-00"
        chapter = module / "curso" / "00-capitulo.md"
        chapter.write_text(
            chapter.read_text(encoding="utf-8")
            + "\n[Código](../exemplos/demo.py)\n"
            + "[Configuração](../exemplos/config.yaml)\n"
            + "![Diagrama](../imagens/diagrama.png)\n"
            + "[Anexos](../anexos/)\n"
            + "[Binário recusado](../exemplos/programa.exe)\n",
            encoding="utf-8",
        )
        _write(module / "exemplos" / "demo.py", "print('exemplo seguro')\n")
        _write(module / "exemplos" / "config.yaml", "modo: laboratorio\n")
        _write(module / "exemplos" / "programa.exe", "MZ-nao-copiar\n")
        _write(module / "anexos" / "consulta.sql", "SELECT 1;\n")
        _write(module / "curso" / "exemplos" / "nao-linkado.py", "print('também catalogado')\n")
        _write(module / "curso" / "tests" / "test_exemplo.py", "def test_ok():\n    assert True\n")
        _write(module / "legado.py", "print('ferramenta legada')\n")
        _write(module / "anexos" / "node_modules" / "dependencia.js", "nao copiar\n")
        image = b"\x89PNG\r\n\x1a\nconteudo-de-teste"
        image_path = module / "imagens" / "diagrama.png"
        image_path.parent.mkdir(parents=True)
        image_path.write_bytes(image)

        catalog_path = builder.build_catalog(self.root, self.output)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        assets = {asset["sourcePath"]: asset for asset in catalog["assets"]}
        expected = {
            "00-Modulo-00/exemplos/demo.py": "code",
            "00-Modulo-00/exemplos/config.yaml": "config",
            "00-Modulo-00/imagens/diagrama.png": "image",
            "00-Modulo-00/anexos/consulta.sql": "data",
            "00-Modulo-00/curso/exemplos/nao-linkado.py": "code",
            "00-Modulo-00/curso/tests/test_exemplo.py": "code",
            "00-Modulo-00/legado.py": "code",
        }

        for source_path, kind in expected.items():
            with self.subTest(source_path=source_path):
                self.assertIn(source_path, assets)
                self.assertEqual(assets[source_path]["kind"], kind)
                self.assertEqual(
                    (self.output / "content" / source_path).read_bytes(),
                    (self.root / source_path).read_bytes(),
                )
        self.assertNotIn("00-Modulo-00/exemplos/programa.exe", assets)
        self.assertNotIn("00-Modulo-00/anexos/node_modules/dependencia.js", assets)
        self.assertFalse((self.output / "content/00-Modulo-00/exemplos/programa.exe").exists())

        document = next(
            document
            for document in catalog["documents"]
            if document["sourcePath"] == "00-Modulo-00/curso/00-capitulo.md"
        )
        linked_paths = {
            "00-Modulo-00/exemplos/demo.py",
            "00-Modulo-00/exemplos/config.yaml",
            "00-Modulo-00/imagens/diagrama.png",
            "00-Modulo-00/anexos/consulta.sql",
        }
        expected_ids = {assets[source_path]["id"] for source_path in linked_paths}
        self.assertTrue(expected_ids.issubset(document["assetIds"]))
        self.assertEqual(catalog["stats"]["assets"], len(assets))
        self.assertEqual(catalog["stats"]["skippedAssetLinks"], 1)

        unlinked = assets["00-Modulo-00/curso/exemplos/nao-linkado.py"]
        course_test = assets["00-Modulo-00/curso/tests/test_exemplo.py"]
        legacy_tool = assets["00-Modulo-00/legado.py"]
        self.assertEqual(unlinked["language"], "python")
        self.assertEqual(unlinked["category"], "source-code")
        self.assertEqual(unlinked["moduleId"], "00")
        self.assertEqual(unlinked["origin"], "formation")
        self.assertEqual(course_test["category"], "test")
        self.assertEqual(legacy_tool["origin"], "legacy")
        self.assertEqual(legacy_tool["legacySectionId"], "legacy-tema-00")
        resource_ids = {resource["id"] for resource in catalog["resources"]}
        asset_ids = {asset["id"] for asset in catalog["assets"]}
        self.assertTrue(resource_ids.issubset(asset_ids))
        self.assertTrue(all("aliasOfDocumentId" not in resource for resource in catalog["resources"]))

    def test_explicit_infrastructure_exclusions_do_not_hide_course_tests(self) -> None:
        _write(self.root / "study-app/src/internal.jsx", "export default null\n")
        _write(self.root / "study-app/README.md", "# Interno\n")
        _write(self.root / "PROJECT.md", "# Projeto\n\n[Aplicação](study-app/README.md)\n")
        _write(self.root / ".git/config", "[core]\n")
        _write(self.root / "00-Modulo-00/curso/tests/test_course.py", "def test_course():\n    assert True\n")

        catalog, _ = builder.assemble_catalog(self.root)
        source_paths = {entity["sourcePath"] for key in ("documents", "resources") for entity in catalog[key]}

        self.assertNotIn("study-app/src/internal.jsx", source_paths)
        self.assertIn("study-app/README.md", source_paths)
        self.assertNotIn(".git/config", source_paths)
        self.assertIn("00-Modulo-00/curso/tests/test_course.py", source_paths)
        study_readme = next(
            document for document in catalog["documents"] if document["sourcePath"] == "study-app/README.md"
        )
        self.assertEqual(study_readme["role"], "global_document")
        self.assertEqual(study_readme["memberships"][0]["collectionId"], "documentacao-global")
        self.assertEqual(catalog["stats"]["skippedAssetLinks"], 0)
        exclusions = catalog["stats"]["coverage"]["explicitExclusions"]
        self.assertIn("study-app", exclusions["roots"])
        self.assertIn("study-app/README.md", exclusions["includedExceptions"])
        self.assertTrue(exclusions["reason"])

    def test_exact_resource_allowlist_includes_only_safe_textual_binary_fixture(self) -> None:
        allowed_path = "00-Modulo-00/curso/fixtures/inbox/ignored.bin"
        unlisted_path = "00-Modulo-00/curso/fixtures/inbox/unlisted.bin"
        unsafe_path = "00-Modulo-00/curso/fixtures/inbox/unsafe.bin"
        allowed_content = b"fixture textual ignorado pelo processamento\n"
        allowed = self.root / allowed_path
        allowed.parent.mkdir(parents=True, exist_ok=True)
        allowed.write_bytes(allowed_content)
        (self.root / unlisted_path).write_bytes(b"tambem textual, mas nao autorizado\n")
        (self.root / unsafe_path).write_bytes(bytes((0, 1, 2, 3)))

        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["resources"]["includePaths"] = [allowed_path, unsafe_path]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        catalog_path = builder.build_catalog(self.root, self.output)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        resources = {resource["sourcePath"]: resource for resource in catalog["resources"]}

        self.assertIn(allowed_path, resources)
        self.assertNotIn(unlisted_path, resources)
        self.assertNotIn(unsafe_path, resources)
        self.assertEqual(resources[allowed_path]["kind"], "text")
        self.assertEqual(resources[allowed_path]["category"], "fixture")
        self.assertEqual(resources[allowed_path]["language"], "bin")
        self.assertTrue(resources[allowed_path]["explicitlyAllowed"])
        self.assertEqual((self.output / "content" / allowed_path).read_bytes(), allowed_content)

        coverage = catalog["stats"]["coverage"]
        self.assertIn(unlisted_path, coverage["unsafeExcludedPaths"])
        self.assertIn(unsafe_path, coverage["unsafeExcludedPaths"])
        self.assertEqual(
            coverage["explicitExclusions"]["includedResourceExceptions"],
            [allowed_path, unsafe_path],
        )

    def test_secret_named_private_key_and_oversized_files_are_excluded(self) -> None:
        module = self.root / "00-Modulo-00/curso"
        _write(module / "credential.txt", "token de exemplo\n")
        private_key_marker = "-----BEGIN " + "PRIVATE KEY-----"
        _write(module / "private.pem", f"{private_key_marker}\nnao-copiar\n")
        oversized = module / "grande.txt"
        oversized.write_bytes(b"a" * (builder.MAX_ASSET_BYTES + 1))

        catalog_path = builder.build_catalog(self.root, self.output)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        paths = {resource["sourcePath"] for resource in catalog["resources"]}

        self.assertNotIn("00-Modulo-00/curso/credential.txt", paths)
        self.assertNotIn("00-Modulo-00/curso/private.pem", paths)
        self.assertNotIn("00-Modulo-00/curso/grande.txt", paths)
        self.assertFalse((self.output / "content/00-Modulo-00/curso/credential.txt").exists())
        self.assertGreaterEqual(catalog["stats"]["coverage"]["resources"]["excluded"], 3)

    def test_existing_v1_document_and_asset_ids_are_unchanged(self) -> None:
        _write(self.root / "00-Modulo-00/curso/exemplo.py", "print('id estável')\n")
        catalog, _ = builder.assemble_catalog(self.root)
        document = next(
            item for item in catalog["documents"] if item["sourcePath"] == "00-Modulo-00/curso/00-capitulo.md"
        )
        resource = next(item for item in catalog["resources"] if item["sourcePath"] == "00-Modulo-00/curso/exemplo.py")

        self.assertEqual(document["id"], builder._document_id(document["sourcePath"]))
        self.assertEqual(resource["id"], builder._asset_id(resource["sourcePath"]))

    def test_rejects_link_path_traversal_outside_repository(self) -> None:
        outside = Path(self.temporary.name) / "fora.txt"
        outside.write_text("nao copiar", encoding="utf-8")
        chapter = self.root / "00-Modulo-00/curso/00-capitulo.md"
        chapter.write_text(
            chapter.read_text(encoding="utf-8") + "\n[Fora](../../../fora.txt)\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(builder.CatalogError, "path traversal"):
            builder.assemble_catalog(self.root)

    def test_rejects_symlinked_link_asset(self) -> None:
        target = self.root / "asset-real.txt"
        target.write_text("conteudo", encoding="utf-8")
        symlink = self.root / "00-Modulo-00/curso/asset.txt"
        try:
            symlink.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"links simbólicos não suportados: {exc}")
        chapter = self.root / "00-Modulo-00/curso/00-capitulo.md"
        chapter.write_text(
            chapter.read_text(encoding="utf-8") + "\n[Asset](asset.txt)\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(builder.CatalogError, "simbólico"):
            builder.assemble_catalog(self.root)

    def test_rejects_path_traversal_from_module_catalog(self) -> None:
        catalog_path = self.root / "MODULE-CATALOG.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog["modules"][0]["path"] = "../fora"
        catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

        with self.assertRaisesRegex(builder.CatalogError, "sair da raiz"):
            builder.assemble_catalog(self.root)

    def test_rejects_path_traversal_from_study_manifest(self) -> None:
        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["courses"][0]["courseRoot"] = "../fora"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaisesRegex(builder.CatalogError, "sair da raiz"):
            builder.assemble_catalog(self.root)

    def test_requires_one_explicit_course_root_for_every_module(self) -> None:
        manifest_path = self.root / "STUDY-CONTENT.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["courses"].pop()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaisesRegex(builder.CatalogError, "courses deve cobrir"):
            builder.assemble_catalog(self.root)

    def test_rejects_symlinked_markdown(self) -> None:
        target = self.root / "arquivo-externo.md"
        target.write_text("# Externo\n", encoding="utf-8")
        symlink = self.root / "00-Modulo-00" / "curso" / "atalho.md"
        try:
            symlink.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"links simbólicos não suportados: {exc}")

        with self.assertRaisesRegex(builder.CatalogError, "simbólico"):
            builder.assemble_catalog(self.root)

    def test_refuses_to_overwrite_unowned_output(self) -> None:
        (self.output / "content").mkdir(parents=True)
        (self.output / "content" / "do-usuario.md").write_text("preservar", encoding="utf-8")

        with self.assertRaisesRegex(builder.CatalogError, "sem marcador"):
            builder.build_catalog(self.root, self.output)
        self.assertTrue((self.output / "content" / "do-usuario.md").is_file())

    def test_relative_path_validator_rejects_windows_and_posix_escape(self) -> None:
        for unsafe in ("../segredo.md", "/etc/passwd", r"C:\segredo.md", "a//b.md"):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(builder.CatalogError):
                    builder._validate_relative_path(unsafe, label="teste")


if __name__ == "__main__":
    unittest.main()
