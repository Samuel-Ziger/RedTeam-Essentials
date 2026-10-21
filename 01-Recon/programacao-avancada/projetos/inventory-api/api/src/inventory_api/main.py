"""HTTP adapter and application lifecycle for the Inventory API."""

from __future__ import annotations

import json
import logging
import re
import time
from contextlib import asynccontextmanager
from typing import Annotated, Any
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pymongo import MongoClient
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import Settings
from .errors import Problem, dependency_unavailable
from .models import (
    AuditEventView,
    HealthView,
    ProblemView,
    ProductCreate,
    ProductPage,
    ProductPatch,
    ProductView,
    StockAdjustmentCreate,
    StockMovementView,
    parse_etag,
)
from .outbox import OutboxWorker
from .repositories import MongoAuditRepository, PostgresRepository
from .service import InventoryService

LOGGER = logging.getLogger("inventory_api")
REQUEST_ID = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
PROBLEM_RESPONSES = {
    400: {"model": ProblemView},
    404: {"model": ProblemView},
    409: {"model": ProblemView},
    412: {"model": ProblemView},
    422: {"model": ProblemView},
    428: {"model": ProblemView},
    503: {"model": ProblemView},
    500: {"model": ProblemView},
}


def _problem_document(request: Request, problem: Problem, errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    document: dict[str, Any] = {
        "type": problem.problem_type,
        "title": problem.title,
        "status": problem.status,
        "detail": problem.detail,
        "instance": request.url.path,
        "requestId": getattr(request.state, "request_id", "unavailable"),
    }
    if errors:
        document["errors"] = errors
    return document


def _expected_version(value: str | None) -> int:
    try:
        return parse_etag(value)
    except ValueError as exc:
        status = 428 if value is None else 400
        problem_type = "precondition-required" if value is None else "invalid-etag"
        title = "Precondition required" if value is None else "Invalid ETag"
        raise Problem(status, f"https://inventory.example.test/problems/{problem_type}", title, str(exc)) from exc


def get_service(request: Request) -> Any:
    return request.app.state.service


def create_app(service_override: Any | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        if service_override is not None:
            application.state.service = service_override
            yield
            return

        settings = Settings.from_environment()
        pool = ConnectionPool(
            conninfo=settings.postgres_dsn,
            min_size=settings.pool_min,
            max_size=settings.pool_max,
            kwargs={"row_factory": dict_row},
            open=False,
        )
        mongo_client: MongoClient[Any] = MongoClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=5_000,
            connectTimeoutMS=3_000,
            socketTimeoutMS=5_000,
        )
        worker: OutboxWorker | None = None
        try:
            pool.open(wait=True, timeout=10)
            products = PostgresRepository(pool)
            audit = MongoAuditRepository(mongo_client, settings.mongo_database)
            audit.ping()
            audit.ensure_indexes()
            worker = OutboxWorker(products, audit, settings.outbox_interval_seconds)
            application.state.service = InventoryService(products, audit)
            worker.start()
            yield
        finally:
            if worker is not None:
                worker.stop()
            mongo_client.close()
            pool.close()

    application = FastAPI(
        title="Inventory API",
        version="1.0.0",
        summary="API educacional sobre HTTP, PostgreSQL, MongoDB e consistência",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    @application.middleware("http")
    async def request_context(request: Request, call_next: Any) -> Response:
        supplied = request.headers.get("X-Request-ID", "")
        request.state.request_id = supplied if REQUEST_ID.fullmatch(supplied) else uuid4().hex
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        LOGGER.info(
            json.dumps(
                {
                    "event": "request_finished",
                    "requestId": request.state.request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "durationMs": round((time.perf_counter() - started) * 1000, 2),
                },
                separators=(",", ":"),
            )
        )
        return response

    @application.exception_handler(Problem)
    async def handle_problem(request: Request, problem: Problem) -> JSONResponse:
        headers = {"Retry-After": "1"} if problem.status == 503 else None
        return JSONResponse(
            _problem_document(request, problem),
            status_code=problem.status,
            media_type="application/problem+json",
            headers=headers,
        )

    @application.exception_handler(RequestValidationError)
    async def handle_validation(request: Request, error: RequestValidationError) -> JSONResponse:
        fields = [
            {
                "location": "/".join(str(part) for part in item["loc"]),
                "message": item["msg"],
                "code": item["type"],
            }
            for item in error.errors()
        ]
        problem = Problem(
            422,
            "https://inventory.example.test/problems/validation-error",
            "Validation failed",
            "One or more request fields are invalid",
        )
        return JSONResponse(
            _problem_document(request, problem, fields),
            status_code=422,
            media_type="application/problem+json",
        )

    @application.exception_handler(StarletteHTTPException)
    async def handle_http(request: Request, error: StarletteHTTPException) -> JSONResponse:
        problem = Problem(
            error.status_code,
            f"https://inventory.example.test/problems/http-{error.status_code}",
            "HTTP request failed",
            str(error.detail),
        )
        return JSONResponse(
            _problem_document(request, problem),
            status_code=error.status_code,
            media_type="application/problem+json",
            headers=error.headers,
        )

    @application.exception_handler(Exception)
    async def handle_unexpected(request: Request, error: Exception) -> JSONResponse:
        LOGGER.error(
            "unhandled_request_error request_id=%s path=%s error_type=%s",
            getattr(request.state, "request_id", "unavailable"),
            request.url.path,
            type(error).__name__,
        )
        problem = Problem(
            500,
            "https://inventory.example.test/problems/internal-error",
            "Internal server error",
            "The request could not be completed",
        )
        request_id = getattr(request.state, "request_id", "unavailable")
        return JSONResponse(
            _problem_document(request, problem),
            status_code=500,
            media_type="application/problem+json",
            headers={"X-Request-ID": request_id},
        )

    @application.get("/health/live", response_model=HealthView, tags=["health"])
    def live() -> HealthView:
        return HealthView(status="ok")

    @application.get(
        "/health/ready",
        response_model=HealthView,
        responses={503: {"model": ProblemView}},
        tags=["health"],
    )
    def ready(service: Annotated[Any, Depends(get_service)]) -> HealthView:
        try:
            service.ready()
        except Exception as exc:
            raise dependency_unavailable() from exc
        return HealthView(status="ok")

    @application.post(
        "/api/v1/products",
        response_model=ProductView,
        status_code=201,
        responses=PROBLEM_RESPONSES,
        tags=["products"],
    )
    def create_product(
        command: ProductCreate,
        response: Response,
        idempotency_key: Annotated[
            str,
            Header(
                alias="Idempotency-Key",
                min_length=8,
                max_length=128,
                pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{7,127}$",
            ),
        ],
        service: Annotated[Any, Depends(get_service)],
    ) -> ProductView:
        product, replayed = service.create_product(command, idempotency_key)
        response.headers["Location"] = f"/api/v1/products/{product.id}"
        response.headers["ETag"] = f'"{product.version}"'
        if replayed:
            response.headers["Idempotency-Replayed"] = "true"
        return product

    @application.get(
        "/api/v1/products",
        response_model=ProductPage,
        responses=PROBLEM_RESPONSES,
        tags=["products"],
    )
    def list_products(
        service: Annotated[Any, Depends(get_service)],
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
        after: Annotated[str | None, Query(max_length=512)] = None,
        query: Annotated[
            str | None,
            Query(alias="q", min_length=1, max_length=50, pattern=r"^[^\x00]*$"),
        ] = None,
    ) -> ProductPage:
        normalized_query = " ".join(query.split()) if query else None
        return service.list_products(limit=limit, after=after, query=normalized_query or None)

    @application.get(
        "/api/v1/products/{product_id}",
        response_model=ProductView,
        responses=PROBLEM_RESPONSES,
        tags=["products"],
    )
    def get_product(
        product_id: UUID,
        response: Response,
        service: Annotated[Any, Depends(get_service)],
    ) -> ProductView:
        product = service.get_product(product_id)
        response.headers["ETag"] = f'"{product.version}"'
        return product

    @application.patch(
        "/api/v1/products/{product_id}",
        response_model=ProductView,
        responses=PROBLEM_RESPONSES,
        tags=["products"],
    )
    def update_product(
        product_id: UUID,
        command: ProductPatch,
        response: Response,
        service: Annotated[Any, Depends(get_service)],
        if_match: Annotated[str | None, Header(alias="If-Match")] = None,
    ) -> ProductView:
        product = service.update_product(product_id, _expected_version(if_match), command)
        response.headers["ETag"] = f'"{product.version}"'
        return product

    @application.post(
        "/api/v1/products/{product_id}/stock-movements",
        response_model=StockMovementView,
        status_code=201,
        responses=PROBLEM_RESPONSES,
        tags=["stock"],
    )
    def adjust_stock(
        product_id: UUID,
        command: StockAdjustmentCreate,
        response: Response,
        service: Annotated[Any, Depends(get_service)],
        if_match: Annotated[str | None, Header(alias="If-Match")] = None,
    ) -> StockMovementView:
        movement, replayed = service.adjust_stock(product_id, _expected_version(if_match), command)
        response.headers["Location"] = f"/api/v1/products/{product_id}/stock-movements/{movement.id}"
        response.headers["ETag"] = f'"{movement.resulting_version}"'
        if replayed:
            response.headers["Idempotency-Replayed"] = "true"
        return movement

    @application.get(
        "/api/v1/products/{product_id}/events",
        response_model=list[AuditEventView],
        responses=PROBLEM_RESPONSES,
        tags=["audit"],
    )
    def list_events(
        product_id: UUID,
        response: Response,
        service: Annotated[Any, Depends(get_service)],
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
    ) -> list[AuditEventView]:
        response.headers["X-Consistency"] = "eventual"
        return service.list_events(product_id, limit)

    return application


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
app = create_app()
