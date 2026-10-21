from pathlib import Path

import yaml
from contract_lab.api import create_app
from openapi_spec_validator import validate

CONTRACT = Path(__file__).parents[1] / "contract" / "openapi.yaml"


def test_contract_has_required_operations_and_components() -> None:
    document = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    validate(document)
    assert document["openapi"] == "3.1.0"
    assert set(document["paths"]) == {
        "/health",
        "/v1/items",
        "/v1/items/{item_id}",
        "/v1/events",
    }
    operations = [
        operation
        for path in document["paths"].values()
        for method, operation in path.items()
        if method in {"get", "post", "patch"}
    ]
    identifiers = [operation["operationId"] for operation in operations]
    assert len(identifiers) == len(set(identifiers))
    assert "Problem" in document["components"]["schemas"]


def test_contract_documents_lab_identity_warning() -> None:
    content = CONTRACT.read_text(encoding="utf-8")
    assert "não representa autenticação de produção" in content


def test_contract_and_runtime_expose_same_operations() -> None:
    source = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    runtime = create_app().openapi()
    methods = {"get", "post", "put", "patch", "delete"}

    def operations(document):
        return {
            (path, method): operation["operationId"]
            for path, path_item in document["paths"].items()
            for method, operation in path_item.items()
            if method in methods
        }

    assert operations(runtime) == operations(source)


def test_problem_contract_has_stable_machine_fields() -> None:
    document = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    problem = document["components"]["schemas"]["Problem"]
    assert {"code", "requestId"} <= set(problem["required"])
    get_item = document["paths"]["/v1/items/{item_id}"]["get"]
    assert "304" in get_item["responses"]
