#!/usr/bin/env python3
"""Render the release-baseline diagram of the Versions and Updates page.

Requires Graphviz (`dot`) and the Noto Sans CJK SC font. Writes two PNG files
(Chinese and English) to docs/_static/images/.

Usage: scripts/build_release_baseline.py
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "_static" / "images"
FONT = "Noto Sans CJK SC"

BLUE = 'fillcolor="#EAF2FD" color="#2F6DB5"'
GREEN = 'fillcolor="#EAF6EA" color="#3A8A3A"'
AMBER = 'fillcolor="#FFF6E5" color="#B7791F"'
PURPLE = 'fillcolor="#F0EBFA" color="#7C5CBF"'

TEXT = {
    "zh": {
        "tag": "diana-docs tag",
        "ctrl": "控制器软件版本",
        "sdk": "C++ / Python SDK",
        "sdk1": "Example 版本 tag\\n(固定 SDK 子模块)",
        "sdk2": "SDK 版本 tag\\n与 version 文件",
        "fci": "FCI",
        "fci1": "Diana FCI Example 源码",
        "fci2": "libfranka 0.18.2",
        "ros": "ROS 2 Humble",
        "ros1": "diana_ros2 源码版本",
        "ros2": "dependency.repos\\n(固定 libfranka 与 diana_description)",
    },
    "en": {
        "tag": "diana-docs tag",
        "ctrl": "Controller software version",
        "sdk": "C++ / Python SDK",
        "sdk1": "Example version tag\\n(pins the SDK submodule)",
        "sdk2": "SDK version tag\\nand version file",
        "fci": "FCI",
        "fci1": "Diana FCI example source",
        "fci2": "libfranka 0.18.2",
        "ros": "ROS 2 Humble",
        "ros1": "diana_ros2 source version",
        "ros2": "dependency.repos\\n(pins libfranka and diana_description)",
    },
}


def dot(t: dict) -> str:
    return f"""
digraph G {{
  bgcolor="white"; pad=0.3; dpi=160; fontname="{FONT}";
  node [shape=box style="rounded,filled" fontname="{FONT}" fontsize=15 margin="0.3,0.16" penwidth=1.6];
  edge [color="#4B5563" penwidth=1.4 arrowsize=0.8];
  rankdir=TB; nodesep=0.5; ranksep=0.45;
  tag  [label="{t['tag']}" {BLUE}];
  ctrl [label="{t['ctrl']}" {GREEN}];
  tag -> ctrl;
  subgraph cluster_sdk {{
    label="{t['sdk']}"; fontname="{FONT}"; fontsize=14; fontcolor="#B7791F"; labelloc=b;
    style="rounded,dashed"; color="#B7791F"; margin=14;
    s1 [label="{t['sdk1']}" {AMBER}];
    s2 [label="{t['sdk2']}" {PURPLE}];
    s1 -> s2;
  }}
  subgraph cluster_fci {{
    label="{t['fci']}"; fontname="{FONT}"; fontsize=14; fontcolor="#B7791F"; labelloc=b;
    style="rounded,dashed"; color="#B7791F"; margin=14;
    f1 [label="{t['fci1']}" {AMBER}];
    f2 [label="{t['fci2']}" {PURPLE}];
    f1 -> f2;
  }}
  subgraph cluster_ros {{
    label="{t['ros']}"; fontname="{FONT}"; fontsize=14; fontcolor="#B7791F"; labelloc=b;
    style="rounded,dashed"; color="#B7791F"; margin=14;
    r1 [label="{t['ros1']}" {AMBER}];
    r2 [label="{t['ros2']}" {PURPLE}];
    r1 -> r2;
  }}
  ctrl -> s1; ctrl -> f1; ctrl -> r1;
}}
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, t in TEXT.items():
        target = OUT / f"release-baseline-{lang}.png"
        subprocess.run(["dot", "-Tpng", "-o", str(target)], input=dot(t).encode("utf-8"), check=True)
        print(f"[baseline] wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
