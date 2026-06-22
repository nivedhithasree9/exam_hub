"""Run pytest with a fresh workspace-local temp directory."""

from __future__ import annotations

import shutil
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path


def main() -> int:
    temp_root = Path(".pytest-tmp")
    temp_root.mkdir(exist_ok=True)
    base_temp = Path(tempfile.mkdtemp(prefix="run-", dir=temp_root))
    try:
        return subprocess.call([sys.executable, "-m", "pytest", f"--basetemp={base_temp}"])  # nosec B603
    finally:
        shutil.rmtree(base_temp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
