"""Errors shared by the application and HTTP adapter."""

from __future__ import annotations


class AppError(Exception):
    def __init__(self, status: int, code: str, title: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail


def bad_request(code: str, detail: str) -> AppError:
    return AppError(400, code, "Requisição inválida", detail)


def unauthorized(detail: str = "Identidade de laboratório ausente ou inválida.") -> AppError:
    return AppError(401, "unauthorized", "Não autenticado", detail)


def forbidden(detail: str = "A identidade não pode executar esta operação.") -> AppError:
    return AppError(403, "forbidden", "Acesso negado", detail)


def not_found() -> AppError:
    return AppError(404, "not-found", "Recurso não encontrado", "O item solicitado não existe.")


def conflict(code: str, detail: str) -> AppError:
    return AppError(409, code, "Conflito", detail)


def precondition(detail: str) -> AppError:
    return AppError(412, "precondition-failed", "Precondição falhou", detail)
