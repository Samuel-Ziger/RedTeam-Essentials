"""Contrato mínimo de configuração e saída de uma aplicação profissional."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass

PROFILES = ("development", "testing", "production")


@dataclass(frozen=True, slots=True)
class ResolvedProfile:
    profile: str
    source: str


def resolve_profile(cli_value: str | None, environment: Mapping[str, str]) -> ResolvedProfile:
    if cli_value is not None:
        if cli_value not in PROFILES:
            raise ValueError(f"profile invalido: {cli_value!r}")
        return ResolvedProfile(cli_value, "cli")
    if "APP_PROFILE" in environment:
        value = environment["APP_PROFILE"]
        if value not in PROFILES:
            raise ValueError(f"APP_PROFILE invalido: {value!r}")
        return ResolvedProfile(value, "environment")
    return ResolvedProfile("development", "default")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="app-config",
        description="Demonstra precedencia e saida estavel de configuracao.",
    )
    result.add_argument("--profile", choices=PROFILES)
    result.add_argument("--format", choices=("text", "json"), default="text")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        resolved = resolve_profile(arguments.profile, os.environ)
    except ValueError as error:
        parser().error(str(error))

    if arguments.format == "json":
        print(json.dumps(asdict(resolved), separators=(",", ":")))
    else:
        print(f"profile={resolved.profile} source={resolved.source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
