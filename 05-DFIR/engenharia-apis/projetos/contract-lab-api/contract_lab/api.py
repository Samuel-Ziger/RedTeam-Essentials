"""FastAPI adapter for the framework-independent Contract Lab service."""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, Path, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .domain import Event, Item, Principal, Status
from .errors import AppError, unauthorized
from .service import MAX_CURSOR_LENGTH, ItemService
from .store import InMemoryStore

LOGGER = logging.getLogger("contract_lab")
SAFE_ID = re.compile(r"[A-Za-z0-9_-]{1,64}")
ItemId = Annotated[
    str,
    Path(
        min_length=36,
        max_length=36,
        pattern=r"^itm_[a-f0-9]{32}$",
    ),
]


class CreateItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=3, max_length=80)


class UpdateItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=3, max_length=80)
    status: Literal["active", "archived"] | None = None

    @model_validator(mode="after")
    def at_least_one_change(self) -> UpdateItem:
        if self.title is None and self.status is None:
            raise ValueError("informe title ou status")
        return self


class ItemView(BaseModel):
    item_id: str
    title: str
    status: Status
    version: int
    created_at: datetime
    updated_at: datetime


class Page(BaseModel):
    limit: int
    next: str | None


class ItemCollection(BaseModel):
    items: list[ItemView]
    page: Page


class EventView(BaseModel):
    event_id: str
    event_type: str
    item_id: str
    actor_id: str
    occurred_at: datetime


def item_view(item: Item) -> ItemView:
    return ItemView.model_validate(item, from_attributes=True)


def event_view(event: Event) -> EventView:
    return EventView.model_validate(event, from_attributes=True)


def lab_principal(
    actor: Annotated[str | None, Header(alias="X-Lab-Actor")] = None,
    tenant: Annotated[str | None, Header(alias="X-Lab-Tenant")] = None,
    role: Annotated[str | None, Header(alias="X-Lab-Role")] = None,
) -> Principal:
    if actor is None or tenant is None or role not in {"reader", "writer"}:
        raise unauthorized()
    if not SAFE_ID.fullmatch(actor) or not SAFE_ID.fullmatch(tenant):
        raise unauthorized()
    return Principal(actor_id=actor, tenant_id=tenant, role=role)


def problem(error: AppError, request: Request) -> JSONResponse:
    return JSONResponse(
        status_code=error.status,
        media_type="application/problem+json",
        content={
            "type": f"https://example.test/problems/{error.code}",
            "title": error.title,
            "status": error.status,
            "detail": error.detail,
            "instance": request.url.path,
            "code": error.code,
            "requestId": request.state.request_id,
        },
    )


def create_app(store: InMemoryStore | None = None) -> FastAPI:
    repository = store or InMemoryStore()
    service = ItemService(repository)
    application = FastAPI(
        title="Contract Lab API",
        version="1.1.0",
        description=(
            "API local educacional. Os cabeçalhos X-Lab-* não são autenticação e nunca devem ser usados em produção."
        ),
    )

    @application.middleware("http")
    async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
        started = time.perf_counter()
        supplied = request.headers.get("X-Request-ID")
        request_id = supplied if supplied and SAFE_ID.fullmatch(supplied) else f"req_{uuid4().hex}"
        request.state.request_id = request_id
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            LOGGER.info(
                json.dumps(
                    {
                        "event": "api.request.completed",
                        "request_id": request_id,
                        "method": request.method,
                        "route": request.scope.get("route").path
                        if request.scope.get("route") is not None
                        else "unmatched",
                        "status": status,
                        "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                    },
                    separators=(",", ":"),
                )
            )

    @application.exception_handler(AppError)
    async def handle_app_error(request: Request, error: AppError) -> JSONResponse:
        return problem(error, request)

    @application.exception_handler(RequestValidationError)
    async def handle_validation(request: Request, error: RequestValidationError) -> JSONResponse:
        fields = [".".join(str(part) for part in item["loc"]) for item in error.errors()]
        return JSONResponse(
            status_code=422,
            media_type="application/problem+json",
            content={
                "type": "https://example.test/problems/validation",
                "title": "Requisição inválida",
                "status": 422,
                "detail": "Um ou mais campos são inválidos.",
                "instance": request.url.path,
                "code": "validation",
                "requestId": request.state.request_id,
                "errors": [{"field": field, "code": "invalid"} for field in fields],
            },
        )

    @application.get("/health", tags=["operation"], operation_id="getHealth")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post(
        "/v1/items",
        status_code=201,
        response_model=ItemView,
        tags=["items"],
        operation_id="createItem",
    )
    def create_item(
        command: CreateItem,
        response: Response,
        principal: Annotated[Principal, Depends(lab_principal)],
        idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    ) -> ItemView:
        item, created = service.create(principal, command.title, idempotency_key)
        response.headers["Location"] = f"/v1/items/{item.item_id}"
        response.headers["ETag"] = item.etag
        response.headers["Cache-Control"] = "no-store"
        response.headers["Idempotency-Replayed"] = "false" if created else "true"
        return item_view(item)

    @application.get(
        "/v1/items",
        response_model=ItemCollection,
        tags=["items"],
        operation_id="listItems",
    )
    def list_items(
        response: Response,
        principal: Annotated[Principal, Depends(lab_principal)],
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        after: Annotated[str | None, Query(max_length=MAX_CURSOR_LENGTH)] = None,
        status: Literal["active", "archived"] | None = None,
    ) -> ItemCollection:
        items, next_cursor = service.list_items(principal, after=after, limit=limit, status=status)
        response.headers["Cache-Control"] = "private, no-store"
        return ItemCollection(items=[item_view(item) for item in items], page=Page(limit=limit, next=next_cursor))

    @application.get(
        "/v1/items/{item_id}",
        response_model=ItemView,
        tags=["items"],
        operation_id="getItem",
    )
    def get_item(
        item_id: ItemId,
        response: Response,
        principal: Annotated[Principal, Depends(lab_principal)],
        if_none_match: Annotated[str | None, Header(alias="If-None-Match")] = None,
    ) -> ItemView | Response:
        item = service.get(principal, item_id)
        headers = {"ETag": item.etag, "Cache-Control": "private, no-cache"}
        if if_none_match == item.etag:
            return Response(status_code=304, headers=headers)
        response.headers["ETag"] = item.etag
        response.headers["Cache-Control"] = "private, no-cache"
        return item_view(item)

    @application.patch(
        "/v1/items/{item_id}",
        response_model=ItemView,
        tags=["items"],
        operation_id="updateItem",
    )
    def update_item(
        item_id: ItemId,
        command: UpdateItem,
        response: Response,
        principal: Annotated[Principal, Depends(lab_principal)],
        if_match: Annotated[str, Header(alias="If-Match")],
    ) -> ItemView:
        item = service.update(
            principal,
            item_id,
            if_match,
            title=command.title,
            status=command.status,
        )
        response.headers["ETag"] = item.etag
        response.headers["Cache-Control"] = "no-store"
        return item_view(item)

    @application.get(
        "/v1/events",
        response_model=list[EventView],
        tags=["events"],
        operation_id="listEvents",
    )
    def list_events(
        response: Response,
        principal: Annotated[Principal, Depends(lab_principal)],
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
    ) -> list[EventView]:
        response.headers["Cache-Control"] = "private, no-store"
        return [event_view(event) for event in service.events(principal, limit=limit)]

    return application


app = create_app()
