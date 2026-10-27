#!/usr/bin/env python3
"""Thin wrapper: run theme/tools/build_versioned_site.py against this project."""
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("AGILE_DOCS_ROOT", str(ROOT))
sys.argv[0] = str(ROOT / "theme" / "tools" / "build_versioned_site.py")
runpy.run_path(sys.argv[0], run_name="__main__")
