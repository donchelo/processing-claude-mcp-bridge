"""Pruebas de regresión: `sketch_name` no puede escapar de PROCESSING_SKETCH_DIR.

Todo se ejecuta contra directorios temporales; nunca se escribe fuera de ellos.
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import processing_server as ps  # noqa: E402

MALICIOUS = ["../evil", "../../evil", "..", ".", "", "a/b", "a\\b", "..\\evil",
             "/etc/evil", "C:\\evil", "evil\x00", "con espacio", "a.b", "-", "é"]


@pytest.fixture
def dirs(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        base = root / "sketches"
        base.mkdir()
        monkeypatch.setattr(ps, "PROCESSING_SKETCH_DIR", str(base))
        yield root, base


def snapshot(root):
    return sorted(str(p.relative_to(root)) for p in root.rglob("*"))


def run(coro):
    return asyncio.run(coro)


@pytest.mark.parametrize("name", MALICIOUS)
def test_create_sketch_rechaza_nombres_maliciosos(dirs, name):
    root, base = dirs
    before = snapshot(root)
    result = run(ps.create_sketch(name, "void setup(){}"))
    assert result.startswith("Error"), result
    assert snapshot(root) == before  # nada escrito, ni dentro ni fuera


@pytest.mark.parametrize("name", MALICIOUS)
def test_update_sketch_rechaza_nombres_maliciosos(dirs, name):
    root, base = dirs
    (root / "evil").mkdir()
    (root / "evil" / "evil.pde").write_text("original")
    (root / "evil.pde").write_text("original")
    before = snapshot(root)
    result = run(ps.update_sketch(name, "pwned"))
    assert result.startswith("Error"), result
    assert snapshot(root) == before
    assert (root / "evil" / "evil.pde").read_text() == "original"


@pytest.mark.parametrize("name", MALICIOUS)
def test_run_sketch_rechaza_nombres_maliciosos(dirs, monkeypatch, name):
    root, base = dirs
    (root / "evil").mkdir()
    cli = root / "cli"
    cli.write_text("")
    monkeypatch.setattr(ps, "PROCESSING_CLI_PATH", str(cli))
    called = []
    monkeypatch.setattr(ps.subprocess, "Popen", lambda *a, **k: called.append(a))
    result = run(ps.run_sketch(name))
    assert result.startswith("Error"), result
    assert not called


@pytest.mark.skipif(os.name == "nt", reason="symlinks requieren privilegios en Windows")
def test_symlink_que_apunta_fuera_es_rechazado(dirs):
    root, base = dirs
    outside = root / "fuera"
    outside.mkdir()
    (base / "link").symlink_to(outside, target_is_directory=True)
    result = run(ps.create_sketch("link", "pwned"))
    assert result.startswith("Error"), result
    assert not list(outside.iterdir())
    (outside / "link.pde").write_text("original")
    result = run(ps.update_sketch("link", "pwned"))
    assert result.startswith("Error"), result
    assert (outside / "link.pde").read_text() == "original"


def test_flujo_normal_sigue_funcionando(dirs):
    root, base = dirs
    assert "creado" in run(ps.create_sketch("mi_Sketch-01", "v1"))
    assert (base / "mi_Sketch-01" / "mi_Sketch-01.pde").read_text() == "v1"
    assert "actualizado" in run(ps.update_sketch("mi_Sketch-01", "v2"))
    assert (base / "mi_Sketch-01" / "mi_Sketch-01.pde").read_text() == "v2"
    assert (base / "mi_Sketch-01" / "mi_Sketch-01.pde.bak").read_text() == "v1"
    assert "mi_Sketch-01" in run(ps.list_sketches())
    assert run(ps.update_sketch("noexiste", "x")).startswith("Error")
