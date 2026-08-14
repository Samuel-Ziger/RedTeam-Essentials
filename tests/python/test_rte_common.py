from __future__ import annotations

import json

import pytest
from rte_common import RTEContext, chunks, confirm_authorization, export_json, is_valid_domain, is_valid_ipv4


@pytest.mark.parametrize("value", ["example.com", "sub.example.com", "a-b.example.org"])
def test_valid_domains(value: str) -> None:
    assert is_valid_domain(value)


@pytest.mark.parametrize("value", ["", "localhost", "-bad.example", "example..com", "example.com/"])
def test_invalid_domains(value: str) -> None:
    assert not is_valid_domain(value)


@pytest.mark.parametrize("value", ["127.0.0.1", "0.0.0.0", "255.255.255.255"])
def test_valid_ipv4(value: str) -> None:
    assert is_valid_ipv4(value)


@pytest.mark.parametrize("value", ["256.1.1.1", "1.2.3", "1.2.3.-1", "01.02.03.999"])
def test_invalid_ipv4(value: str) -> None:
    assert not is_valid_ipv4(value)


def test_export_json_creates_utf8_document(tmp_path) -> None:
    path = export_json({"mensagem": "autorização"}, tmp_path / "nested", "result")
    assert path.parent == tmp_path / "nested"
    assert json.loads(path.read_text(encoding="utf-8")) == {"mensagem": "autorização"}


def test_context_creates_output_directory(tmp_path) -> None:
    output = tmp_path / "new" / "output"
    context = RTEContext(tool="Teste", output_dir=output)
    assert context.output_dir == output
    assert output.is_dir()


def test_authorization_can_be_enabled_by_environment(monkeypatch) -> None:
    monkeypatch.setenv("RTE_SKIP_AUTH", "1")
    confirm_authorization()


def test_authorization_rejects_unconfirmed_input(monkeypatch) -> None:
    monkeypatch.delenv("RTE_SKIP_AUTH", raising=False)
    monkeypatch.setattr("sys.stdin.readline", lambda: "NAO\n")
    with pytest.raises(SystemExit, match="2"):
        confirm_authorization()


def test_chunks_preserves_items() -> None:
    assert list(chunks(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_chunks_rejects_non_positive_size() -> None:
    with pytest.raises(ValueError, match="positivo"):
        list(chunks([1], 0))
