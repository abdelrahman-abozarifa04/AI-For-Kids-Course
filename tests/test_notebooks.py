"""Execute every notebook top to bottom, then run each hidden solution in the same kernel.

Solutions live in markdown cells as:
    <details><summary>...</summary> ```python ... ``` </details>
so this test also guarantees the published solutions actually work.

Run:  pytest tests/test_notebooks.py -v
"""
from __future__ import annotations

import re
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = sorted((ROOT / "notebooks").rglob("*.ipynb"))
SOLUTION_RE = re.compile(r"<details>.*?```python\n(.*?)```.*?</details>", re.S)

# Lines that only make sense interactively or would slow CI down.
SKIP_SOLUTION_MARKERS = ("input(",)


def extract_solutions(nb: nbformat.NotebookNode) -> list[str]:
    solutions = []
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for block in SOLUTION_RE.findall(cell.source):
            if not any(marker in block for marker in SKIP_SOLUTION_MARKERS):
                solutions.append(block)
    return solutions


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[p.stem for p in NOTEBOOKS])
def test_notebook_and_solutions_run(path: Path, tmp_path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    for code in extract_solutions(nb):
        nb.cells.append(nbformat.v4.new_code_cell(code))
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(tmp_path)}})
    client.execute()


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[p.stem for p in NOTEBOOKS])
def test_notebook_is_clean(path: Path) -> None:
    """Committed notebooks must not contain outputs, so diffs stay readable."""
    nb = nbformat.read(path, as_version=4)
    dirty = [i for i, c in enumerate(nb.cells)
             if c.cell_type == "code" and (c.get("outputs") or c.get("execution_count"))]
    assert not dirty, f"cells with outputs: {dirty}. Clear outputs before committing."


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[p.stem for p in NOTEBOOKS])
def test_colab_badge_points_to_this_file(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    rel = path.relative_to(ROOT).as_posix()
    first = nb.cells[0].source
    assert "colab.research.google.com" in first, "first cell needs an Open-in-Colab badge"
    assert rel in first, f"Colab badge should link to {rel}"
