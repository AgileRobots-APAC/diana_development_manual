"""Chinese Sphinx build configuration."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conf_common import get_optional_module_excludes, make_config

globals().update(make_config(is_english=False))
root_doc = "index"
exclude_patterns = ["conf.py", *get_optional_module_excludes()]
