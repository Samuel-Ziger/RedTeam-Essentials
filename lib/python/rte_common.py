"""
RTE Common - utilidades compartilhadas pelos scripts Python do RedTeam-Essentials.

Logging colorido com niveis, validacao etica, helpers de export
e checagens reutilizaveis. Mantemos o codigo deliberadamente pequeno
(stdlib + opcionalmente colorama/rich nao sao obrigatorios) para que
qualquer Python 3.9+ rode sem dependencias.

Autor:    Samuel Ziger - RedTeam Essentials
Versao:   2.0.0
Licenca:  MIT
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

__all__ = [
    "get_logger",
    "RTEContext",
    "is_valid_domain",
    "is_valid_ipv4",
    "confirm_authorization",
    "export_json",
    "ETHICAL_DISCLAIMER",
]

ETHICAL_DISCLAIMER = (
    "RedTeam Essentials - Uso EXCLUSIVAMENTE educacional. "
    "Voce e responsavel por garantir autorizacao escrita antes de qualquer teste."
)


# --- ANSI logging -----------------------------------------------------------
class _ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG:    "\033[0;90m",  # gray
        logging.INFO:     "\033[0;36m",  # cyan
        logging.WARNING:  "\033[1;33m",  # yellow
        logging.ERROR:    "\033[0;31m",  # red
        logging.CRITICAL: "\033[1;31m",  # bright red
    }
    GLYPHS = {
        logging.DEBUG:    "[~]",
        logging.INFO:     "[*]",
        logging.WARNING:  "[!]",
        logging.ERROR:    "[x]",
        logging.CRITICAL: "[X]",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        glyph = self.GLYPHS.get(record.levelno, "[?]")
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if record.levelno == logging.INFO and getattr(record, "rte_success", False):
            color = "\033[0;32m"
            glyph = "[+]"
        return f"{color}{stamp} {glyph} {record.getMessage()}{self.RESET}"


def get_logger(name: str = "rte", level: str | int = "INFO") -> logging.Logger:
    """Retorna um logger configurado uma unica vez."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_ColorFormatter())
    logger.addHandler(handler)
    logger.setLevel(level if isinstance(level, int) else getattr(logging, str(level).upper(), logging.INFO))
    logger.propagate = False
    return logger


# --- Sucesso "helper" -------------------------------------------------------
def log_success(logger: logging.Logger, msg: str) -> None:
    record = logger.makeRecord(logger.name, logging.INFO, __file__, 0, msg, (), None)
    record.rte_success = True  # type: ignore[attr-defined]
    logger.handle(record)


# --- Contexto / sessao ------------------------------------------------------
@dataclass
class RTEContext:
    """Contexto de execucao basico para scripts."""
    tool: str
    version: str = "2.0.0"
    output_dir: Path = Path("./output")

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def banner(self) -> None:
        bar = "=" * 64
        sys.stderr.write(
            f"\n\033[0;36m{bar}\n"
            f" RedTeam Essentials :: {self.tool:<40} v{self.version}\n"
            f"{bar}\n"
            f" AVISO: Uso apenas educacional/autorizado.\n"
            f"{bar}\033[0m\n\n"
        )


# --- Validacoes -------------------------------------------------------------
_DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)([a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)
_IPV4_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d)$")


def is_valid_domain(value: str) -> bool:
    return bool(value and _DOMAIN_RE.match(value))


def is_valid_ipv4(value: str) -> bool:
    return bool(value and _IPV4_RE.match(value))


# --- Autorizacao ------------------------------------------------------------
def confirm_authorization(force: bool = False) -> None:
    """Bloqueia ate o usuario digitar AUTORIZADO."""
    if force or os.environ.get("RTE_SKIP_AUTH") == "1":
        return
    sys.stderr.write(
        "\033[1;33m"
        "Voce tem autorizacao por escrito para testar este alvo?\n"
        "Digite AUTORIZADO para prosseguir: \033[0m"
    )
    answer = sys.stdin.readline().strip()
    if answer != "AUTORIZADO":
        sys.stderr.write("\033[0;31m[x] Autorizacao nao confirmada. Abortando.\033[0m\n")
        sys.exit(2)


# --- Export -----------------------------------------------------------------
def export_json(data: Any, output_dir: Path | str, basename: str) -> Path:
    """Salva `data` como JSON com timestamp em `output_dir`."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out / f"{basename}_{stamp}.json"
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, default=str)
    return path


# --- Iter helper ------------------------------------------------------------
def chunks(iterable: Iterable[Any], size: int) -> Iterable[list[Any]]:
    bucket: list[Any] = []
    for item in iterable:
        bucket.append(item)
        if len(bucket) == size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket
