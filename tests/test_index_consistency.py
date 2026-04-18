"""Index audit script consistency."""

import subprocess
import sys
from pathlib import Path


def test_rebuild_index_audit_ok(repo_root: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "rebuild_index.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "OK" in proc.stdout or "OK" in proc.stderr
