#!/usr/bin/env python3
"""Analisador de notas: domínio, validação, coleções e CLI sem dependências.

O arquivo foi mantido autocontido para que possa ser executado diretamente e
também importado pela suíte de testes. A camada de domínio não imprime nem lê
entrada: isso torna suas funções reutilizáveis em uma CLI, API ou interface.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType


FAIXAS = ("A", "B", "C", "D")


@dataclass(frozen=True, slots=True)
class ResumoNotas:
    """Resultado imutável da análise de um conjunto não vazio de notas."""

    quantidade: int
    media: float
    menor: float
    maior: float
    conceitos: Mapping[str, int]

    def como_dict(self) -> dict[str, object]:
        """Converte o resultado para uma estrutura serializável como JSON."""
        return {
            "quantidade": self.quantidade,
            "media": self.media,
            "menor": self.menor,
            "maior": self.maior,
            "conceitos": dict(self.conceitos),
        }

    def como_resumo(self) -> dict[str, object]:
        """Expõe o contrato público mínimo, sem as estatísticas opcionais."""
        return {
            "quantidade": self.quantidade,
            "media": self.media,
            "conceitos": dict(self.conceitos),
        }


def validar_nota(nota: object) -> float:
    """Valida e normaliza uma nota.

    ``bool`` é rejeitado explicitamente porque, embora seja subtipo de ``int``
    em Python, não representa uma nota válida neste domínio.
    """
    if isinstance(nota, bool) or not isinstance(nota, (int, float)):
        raise TypeError("nota deve ser numérica")

    valor = float(nota)
    if not math.isfinite(valor) or not 0 <= valor <= 10:
        raise ValueError("nota deve estar entre 0 e 10")
    return valor


def conceito(nota: float) -> str:
    """Converte uma nota válida em conceito A, B, C ou D."""
    valor = validar_nota(nota)
    if valor >= 9:
        return "A"
    if valor >= 7:
        return "B"
    if valor >= 5:
        return "C"
    return "D"


def analisar(notas: Iterable[float]) -> ResumoNotas:
    """Consome ``notas`` uma vez e devolve estatísticas do conjunto.

    Aceitar ``Iterable`` permite receber listas, tuplas ou geradores. Os dados
    são materializados em uma tupla porque precisamos fazer mais de uma
    operação sobre eles. ``math.fsum`` reduz erro acumulado da soma de floats.
    """
    valores = tuple(validar_nota(nota) for nota in notas)
    if not valores:
        raise ValueError("informe ao menos uma nota")

    frequencias = dict.fromkeys(FAIXAS, 0)
    for nota in valores:
        faixa = conceito(nota)
        frequencias[faixa] += 1

    return ResumoNotas(
        quantidade=len(valores),
        media=round(math.fsum(valores) / len(valores), 2),
        menor=min(valores),
        maior=max(valores),
        conceitos=MappingProxyType(frequencias.copy()),
    )


def resumir(notas: Iterable[float]) -> dict[str, object]:
    """API compatível do exemplo: devolve apenas o resumo essencial."""
    return analisar(notas).como_resumo()


def converter_argumentos(textos: Iterable[str]) -> list[float]:
    """Converte a fronteira textual da CLI e acrescenta contexto aos erros."""
    notas: list[float] = []
    for posicao, texto in enumerate(textos, start=1):
        try:
            nota = float(texto)
            notas.append(validar_nota(nota))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"argumento {posicao} inválido ({texto!r}): {exc}") from exc
    return notas


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notas", nargs="+", help="notas entre 0 e 10")
    parser.add_argument(
        "--detalhado",
        action="store_true",
        help="inclui menor e maior nota no JSON",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        notas = converter_argumentos(args.notas)
        resultado = analisar(notas)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    payload = resultado.como_dict() if args.detalhado else resultado.como_resumo()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
