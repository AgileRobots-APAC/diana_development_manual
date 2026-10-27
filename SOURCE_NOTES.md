# Content Source Notes

[English](SOURCE_NOTES.md) | [中文](SOURCE_NOTES.cn.md)

This file records the source baseline and evidence boundaries used by the Diana developer documentation.

## C++ SDK Primary Source

Industrial API Manual for C/C++:

- Software version: V3.4.0
- Document version: V3.4.0
- File date: 2026-05-28
- Original function entries: 1-234
- Appendix A: DianaApi error codes
- Appendix B: ensuring inverse-kinematics solution uniqueness
- Appendix C: additional notes for realtime commands

The C++ example guides are also checked against the matching SDK headers, release information, and current `diana-api-examples-cpp` source.

## Python SDK Primary Sources

- Diana Industrial API Manual for Python V3.4.0, dated 2026-05-28
- Python SDK version `industry-v3.4.0.260605`
- `lib/DianaApi.py` and the `version` file in the Python SDK submodule
- Current `diana-api-examples-python` source and accompanying documentation

Python function prototypes follow the matching SDK wrapper. Parameter meanings, units, ranges, and return values are checked against the Python API manual. Example flows, constants, and call snippets follow the current example repository source.

## FCI Primary Sources

- Current Diana FCI example source
- Official `libfranka 0.18.2` API Reference
- `libfranka 0.18.2` type definitions and control-interface documentation

FCI prototypes, overloads, control types, return values, and exceptions are checked specifically against version 0.18.2. Material for another `libfranka` version is not applied implicitly.

## Web-Oriented Reorganization

Function-level API Reference is maintained on a separate site. This repository retains the structured data required to generate the error-code tables and reorganizes source material into:

- Shared concepts, units, safety boundaries, I/O, and troubleshooting
- Development preparation and quick starts for C++, Python, and FCI
- Runnable example overviews and per-example explanations
- API prototypes, return descriptions, and focused call examples used by each example
- Web versions of the error-code table and selected manual appendices

`data/api_v3_3_0.json` is initial structured data derived from the C/C++ V3.3.0 manual. It is currently used only to generate the Chinese and English error-code tables.

## Content Not Inferred

When the matching manuals, SDK packages, release notes, and example repositories do not fully specify a topic, this repository does not infer:

- Robot dimensions, rated payload, or reach
- Complete controller-terminal, network-port, or electrical wiring details
- Behavior or compatibility of unreleased SDK versions
- Operating-system or Python-version compatibility that has not been tested
- Realtime or safety performance that has not been validated at the deployment site
- Physical-robot run output that has not actually been collected

Use the product user manual, safety documentation, SDK release notes, equipment configuration, and site validation results for these topics.
