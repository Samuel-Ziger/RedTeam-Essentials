from __future__ import annotations

from contract_lab.api import create_app
from fastapi.testclient import TestClient

WRITER = {"X-Lab-Actor": "ana", "X-Lab-Tenant": "escola", "X-Lab-Role": "writer"}
READER = {"X-Lab-Actor": "bia", "X-Lab-Tenant": "escola", "X-Lab-Role": "reader"}


def new_client() -> TestClient:
    return TestClient(create_app())


def create_item(client: TestClient, title: str = "Primeiro item", key: str = "create-001"):
    return client.post(
        "/v1/items",
        headers={**WRITER, "Idempotency-Key": key},
        json={"title": title},
    )


def test_health_is_public_and_has_request_id() -> None:
    response = new_client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["X-Request-ID"].startswith("req_")


def test_identity_is_required() -> None:
    response = new_client().get("/v1/items")
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["code"] == "unauthorized"
    assert response.json()["requestId"] == response.headers["X-Request-ID"]


def test_create_returns_location_and_etag() -> None:
    response = create_item(new_client())
    assert response.status_code == 201
    assert response.headers["Location"].endswith(response.json()["item_id"])
    assert response.headers["ETag"].endswith('-v1"')
    assert response.headers["Idempotency-Replayed"] == "false"
    assert response.headers["Cache-Control"] == "no-store"


def test_validation_rejects_unknown_field_as_problem() -> None:
    client = new_client()
    response = client.post(
        "/v1/items",
        headers={**WRITER, "Idempotency-Key": "create-001"},
        json={"title": "Item seguro", "admin": True},
    )
    assert response.status_code == 422
    assert response.json()["type"].endswith("/validation")


def test_idempotency_replays_and_rejects_changed_body() -> None:
    client = new_client()
    first = create_item(client)
    replay = create_item(client)
    conflict = create_item(client, title="Conteudo diferente")
    assert replay.json() == first.json()
    assert replay.headers["Idempotency-Replayed"] == "true"
    assert conflict.status_code == 409


def test_reader_cannot_create_or_read_events() -> None:
    client = new_client()
    denied_create = client.post(
        "/v1/items",
        headers={**READER, "Idempotency-Key": "create-001"},
        json={"title": "Item seguro"},
    )
    denied_events = client.get("/v1/events", headers=READER)
    assert denied_create.status_code == 403
    assert denied_events.status_code == 403


def test_tenant_isolation_returns_not_found() -> None:
    client = new_client()
    created = create_item(client).json()
    outsider = {**WRITER, "X-Lab-Tenant": "outra-escola"}
    response = client.get(f"/v1/items/{created['item_id']}", headers=outsider)
    assert response.status_code == 404


def test_pagination_uses_cursor() -> None:
    client = new_client()
    for number in range(3):
        create_item(client, title=f"Item numero {number}", key=f"create-00{number}")
    first = client.get("/v1/items?limit=2", headers=READER).json()
    second = client.get(f"/v1/items?limit=2&after={first['page']['next']}", headers=READER).json()
    assert len(first["items"]) == 2
    assert len(second["items"]) == 1
    assert second["page"]["next"] is None


def test_patch_requires_current_etag() -> None:
    client = new_client()
    created = create_item(client)
    item_id = created.json()["item_id"]
    etag = created.headers["ETag"]
    updated = client.patch(
        f"/v1/items/{item_id}",
        headers={**WRITER, "If-Match": etag},
        json={"status": "archived"},
    )
    stale = client.patch(
        f"/v1/items/{item_id}",
        headers={**WRITER, "If-Match": etag},
        json={"title": "Outro titulo"},
    )
    assert updated.status_code == 200
    assert updated.json()["version"] == 2
    assert stale.status_code == 412


def test_get_supports_conditional_cache_validation() -> None:
    client = new_client()
    created = create_item(client)
    item_id = created.json()["item_id"]
    etag = created.headers["ETag"]
    cached = client.get(
        f"/v1/items/{item_id}",
        headers={**READER, "If-None-Match": etag},
    )
    assert cached.status_code == 304
    assert cached.content == b""
    assert cached.headers["ETag"] == etag
    assert cached.headers["Cache-Control"] == "private, no-cache"


def test_invalid_path_identifier_is_rejected_before_lookup() -> None:
    response = new_client().get("/v1/items/not-valid", headers=READER)
    assert response.status_code == 422
    assert response.json()["code"] == "validation"


def test_archived_item_cannot_be_reactivated() -> None:
    client = new_client()
    created = create_item(client)
    item_id = created.json()["item_id"]
    archived = client.patch(
        f"/v1/items/{item_id}",
        headers={**WRITER, "If-Match": created.headers["ETag"]},
        json={"status": "archived"},
    )
    reactivated = client.patch(
        f"/v1/items/{item_id}",
        headers={**WRITER, "If-Match": archived.headers["ETag"]},
        json={"status": "active"},
    )
    assert reactivated.status_code == 409
    assert reactivated.json()["code"] == "invalid-transition"


def test_generated_openapi_contains_public_operations() -> None:
    document = new_client().get("/openapi.json").json()
    assert document["openapi"].startswith("3.1.")
    assert set(document["paths"]) >= {"/health", "/v1/items", "/v1/items/{item_id}"}
    assert "não são autenticação" in document["info"]["description"]
