# Diana Developer Documentation · 1.0.0

[English](README.md) | [中文](README.cn.md)

Bilingual **Sphinx + MyST + sphinx-rtd-theme** developer documentation for the Diana and Thor robot SDKs, published with GitHub Pages or GitLab Pages.

Documentation baseline:

- Industrial API Manual for C/C++ V3.3.0
- Diana Python SDK and API Manual V3.3.0
- Diana FCI examples using `libfranka 0.18.2`
- Documentation version: 1.0.0 (based on SDK 3.3.0)
- Structured API records: 230

## Current Coverage

- Chinese and English sites are built and published together.
- Navigation is organized into Overview, Programming Guides, and Reference.
- Programming guides cover the C++ SDK, Python SDK, and FCI.
- C++ and Python include overview, development preparation, quick start, example overview, and per-example API usage.
- FCI covers realtime preparation, control modes, and examples against `libfranka 0.18.2`.
- Appendix A is a searchable table containing 176 error codes.
- Appendix B inverse-kinematics uniqueness and Appendix C realtime commands are published as focused guides.
- GitHub Pages and GitLab Pages CI builds are configured.
- The version selector supports the development build and future immutable Git tags. No formal release tag has been created yet.

Function-level API Reference is maintained separately. This repository keeps only the structured data required to generate the error-code table.

## Local Preview

On Ubuntu 22.04:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make html
python3 -m http.server 8000 -d build/html
```

Open `http://127.0.0.1:8000`. The Chinese site is generated at the site root and the English site at `/en/`.

## Live Preview

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make live
```

Open `http://127.0.0.1:8000` locally. Devices on the same network can use `http://<control-pc-ip>:8000`; allow TCP port 8000 through the firewall. Changes under `docs/` are rebuilt and refreshed automatically.

`make html` and `make live` prefer the repository-local `.venv`. Each build removes old HTML so disabled languages or modules cannot leave stale pages behind. Chinese full-text search uses `jieba`, included in `requirements.txt`.

Optional guide modules are enabled by default. Set `DIANA_BUILD_CPP`, `DIANA_BUILD_PYTHON`, `DIANA_BUILD_FCI`, or `DIANA_BUILD_ROS2` to `0` to exclude that module from both language sites. For example:

```bash
DIANA_BUILD_ROS2=0 make html
```

The two ROS 2 distributions can also be switched individually with `DIANA_BUILD_ROS2_HUMBLE` and `DIANA_BUILD_ROS2_JAZZY`, for example to hide Jazzy while its pages are still being written:

```bash
DIANA_BUILD_ROS2_JAZZY=0 make html
```

## Publish to GitHub Pages

Push commits to `main`; the workflow builds and deploys the bilingual site automatically.

In repository **Settings → Pages**, set **Source** to **GitHub Actions**. After the `main` workflow succeeds, the published URL is shown in the workflow's deployment summary.

## Publish to GitLab Pages

Push the same commit to the GitLab project's default branch. `.gitlab-ci.yml` builds the bilingual site, then publishes `public/` through GitLab Pages. Ensure a GitLab Runner is enabled; after the pipeline succeeds, find the URL under **Deploy → Pages**.

The GitHub and GitLab CI files coexist safely: each platform reads only its own configuration.

## Repository Layout

```text
docs/
├── conf_common.py        # shared Sphinx configuration and build hooks
├── navigation.py         # sidebar tree shared by both languages
├── _static/              # content assets (images, diagrams, module icons) and project.js
├── zh_CN/                # Chinese site source (conf.py + pages) -> build/html/
└── en/                   # English site source (conf.py + pages) -> build/html/en/
data/                     # structured manual data and the version registry
scripts/                  # build, generation and consistency-check scripts
theme/                    # agile-docs-theme submodule: theme, templates, styles, build tools
```

`docs/zh_CN/` and `docs/en/` have identical page paths, for example `zh_CN/cpp/quick_start.md` and `en/cpp/quick_start.md`. The page tree is organized into Overview (`about/`, `guide/`), Programming Guides (`programming/`, `cpp/`, `python/`, `fci/`, `ros2/`) and Reference (`reference/`).

## Generation Flow

```text
data/api_v3_3_0.json
        └─ scripts/generate_error_codes.py
                ├─ docs/zh_CN/reference/error_codes.md
                └─ docs/en/reference/error_codes.md

docs/zh_CN + docs/en -> Sphinx -> build/html/ and build/html/en/ -> GitHub Pages or GitLab Pages
```

## Maintenance Rules

- **Add, rename or remove a page in both languages at once**, then update the toctree and `docs/navigation.py`. The build fails if a page is missing from the sidebar or the sidebar points to a missing page. Sidebar labels default to the page H1; set a label only when the sidebar should be shorter.
- **Run `make check` before committing.** It fails when a page exists in only one language, when a page pair has a different number of H2/H3 headings, when a code block swallows another fence opener, or when a type such as `std::shared_ptr<Robot>` is written outside inline code (MyST would hide `<Robot>` as HTML); admonition differences are reported as warnings. CI runs the same check.
- **Do not edit `reference/error_codes.md` by hand.** It is regenerated from `data/api_v3_3_0.json` on every build.
- The home-page button and toctree entry of a module disabled with `DIANA_BUILD_*=0` are removed by link target (`href="cpp/index.html"`, `cpp/index`), so button labels can be changed freely.

## Versioned Releases

The default branch represents the development build of version 1.0.0, based on SDK 3.3.0. After validation, create an immutable release tag and add it to `data/versions.json`:

```json
{
  "id": "v1.0.0",
  "label": "1.0.0",
  "ref": "v1.0.0",
  "path": "v1.0.0",
  "status": "stable",
  "published": true
}
```

The Pages pipeline publishes development content at the site root and registered tags under paths such as `/v1.0.0/`. Run `make versions` for the same complete local build. Never move a published tag; create a patch release such as `v1.0.1` for corrections.

## Important Note

`data/api_v3_3_0.json` is initial structured data derived from the V3.3.0 manual. It is currently used only to generate the error-code tables.
