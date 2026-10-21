"""Erros esperados e apresentaveis da aplicacao."""


class PlannerError(Exception):
    """Base para falhas de entrada ou regra de negocio."""


class ValidationError(PlannerError):
    """Indica um valor ou uma referencia invalida."""


class CycleError(PlannerError):
    """Indica um ciclo no grafo de dependencias."""

    def __init__(self, path: tuple[str, ...]) -> None:
        self.path = path
        super().__init__(f"ciclo de dependencias: {' -> '.join(path)}")
