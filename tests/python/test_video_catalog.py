import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("video_catalog_validator", ROOT / "scripts" / "validate_video_catalog.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def test_repository_video_catalog_is_valid():
    assert validator.validate_catalog(ROOT) == []


def test_catalog_rejects_missing_modules_and_incomplete_section(tmp_path):
    module = tmp_path / "00-Fundamentos"
    module.mkdir()
    (module / "README.md").write_text(
        "## Vídeos em português\n\n1. [Exemplo](https://www.youtube.com/watch?v=RxxCan33CbA) — **Canal**.\n",
        encoding="utf-8",
    )

    errors = validator.validate_catalog(tmp_path)

    assert any("seções esperadas" in error for error in errors)
    assert any("mínimo 5" in error for error in errors)
    assert any("seções esperadas" in error for error in errors)


def test_module_rejects_duplicate_videos(tmp_path):
    for number in range(27):
        module = tmp_path / f"{number:02d}-Test"
        module.mkdir()
        video = "1. [Exemplo](https://www.youtube.com/watch?v=RxxCan33CbA) — **Canal**.\n"
        (module / "README.md").write_text("## Vídeos em português\n\n" + video * 5, encoding="utf-8")

    errors = validator.validate_catalog(tmp_path)

    assert any("duplicados" in error for error in errors)
