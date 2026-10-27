"""Shared Sphinx configuration for the independent Chinese and English sites.

The look and the generic navigation machinery come from the ``theme`` submodule
(``agile_docs_theme``); this file keeps what is specific to this project.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "theme"))

from agile_docs_theme import get_enabled_modules as _get_enabled_modules  # noqa: E402
from agile_docs_theme import get_module_excludes  # noqa: E402,F401

from navigation import NAVIGATION  # noqa: E402

OPTIONAL_MODULES = {
    "cpp": "DIANA_BUILD_CPP",
    "python": "DIANA_BUILD_PYTHON",
    "fci": "DIANA_BUILD_FCI",
    "ros2": "DIANA_BUILD_ROS2",
    "ros2_humble": "DIANA_BUILD_ROS2_HUMBLE",
    "ros2_jazzy": "DIANA_BUILD_ROS2_JAZZY",
}
# Source directory of each optional module when it differs from the module name.
MODULE_DIRS = {
    "ros2_humble": "ros2/humble",
    "ros2_jazzy": "ros2/jazzy",
}


def get_enabled_modules() -> dict[str, bool]:
    return _get_enabled_modules(OPTIONAL_MODULES)


def get_optional_module_excludes() -> list[str]:
    return get_module_excludes(OPTIONAL_MODULES, MODULE_DIRS)


def _filter_distribution_links(source: str, enabled_modules: dict[str, bool]) -> str:
    """Drop lines of the ROS 2 selector pages that point into a disabled distribution."""
    disabled = [
        MODULE_DIRS[module] + "/"
        for module in ("ros2_humble", "ros2_jazzy")
        if not enabled_modules[module]
    ]
    return "\n".join(
        line for line in source.splitlines() if not any(path[len("ros2/"):] in line for path in disabled)
    ) + "\n"


def filter_distribution_pages(app, docname, source):
    """Drop the ROS 2 selector links that point into a disabled distribution."""
    if docname in ("ros2/index", "ros2/overview"):
        source[0] = _filter_distribution_links(source[0], app.config.html_context["enabled_modules"])


def setup(app):
    app.connect("source-read", filter_distribution_pages)


def _load_versions() -> tuple[list[dict], dict]:
    registry = Path(os.getenv("DIANA_VERSIONS_FILE", ROOT / "data" / "versions.json"))
    data = json.loads(registry.read_text(encoding="utf-8"))
    versions = [item for item in data["versions"] if item.get("published", True)]
    current_id = os.getenv("DIANA_DOCS_VERSION", "development")
    current = next((item for item in versions if item.get("id") == current_id), None)
    if current is None:
        raise RuntimeError(f"版本 {current_id!r} 不在公开版本清单中")
    return versions, current


def make_config(*, is_english: bool) -> dict[str, object]:
    versions, current = _load_versions()
    enabled_modules = get_enabled_modules()
    project = "Diana Developer Documentation" if is_english else "Diana 开发者文档"
    author = (
        "Agile Robots SE"
        # "Beijing Agile Robots Technology Co., Ltd."
        # if is_english
        # else "北京思灵机器人科技有限责任公司"
    )
    return {
        "project": project,
        "author": author,
        # The RTD footer supplies the trailing full stop itself.
        "copyright": f"2026, {author.rstrip('.')}",
        "release": current["label"],
        "version": current["label"],
        "language": "en" if is_english else "zh_CN",
        "extensions": [
            "agile_docs_theme",
            "myst_parser",
            "sphinx_copybutton",
            "sphinx_design",
            "sphinx.ext.autosectionlabel",
        ],
        "autosectionlabel_prefix_document": True,
        "myst_enable_extensions": ["colon_fence", "deflist"],
        "source_suffix": {".rst": "restructuredtext", ".md": "markdown"},
        "html_theme": "agile_docs",
        "html_static_path": ["../_static"],
        "html_js_files": ["project.js"],
        "agile_navigation": NAVIGATION,
        "agile_navigation_file": "docs/navigation.py",
        "html_show_sphinx": False,
        "html_title": f"{project} · {current['label']}",
        "html_theme_options": {
            "document_title_en": "Diana Developer Documentation",
            "document_title_zh": "Diana 开发者文档",
            "repository_url": "https://github.com/AgileRobots-APAC/diana_development_manual",
            "repository_api": "https://api.github.com/repos/AgileRobots-APAC/diana_development_manual",
            "logo_only": True,
            "prev_next_buttons_location": "both",
            "style_external_links": True,
            "collapse_navigation": False,
            "sticky_navigation": True,
            "navigation_depth": 4,
            "includehidden": True,
            "titles_only": False,
        },
        "html_context": {
            "display_gitlab": False,
            "doc_versions": versions,
            "current_doc_version": current,
            "is_english": is_english,
            "enable_english": True,
            "language_site_prefix": "en/" if is_english else "",
            "enabled_modules": enabled_modules,
        },
        "copybutton_prompt_text": r"\$ |>>> |\.\.\. ",
        "copybutton_prompt_is_regexp": True,
        "rst_prolog": "\n.. |sdk_version| replace:: %s\n" % current["label"],
        "setup": setup,
    }
