# Diana 开发者文档 · 1.0.1

[English](README.md) | [中文](README.cn.md)

这是面向 Diana 与 Thor 机器人 SDK 的双语 **Sphinx + MyST + sphinx-rtd-theme** 开发者文档仓库，可通过 GitHub Pages 或 GitLab Pages 发布。

当前文档基线：

- 《工业版 API 手册（C&C++ 版）》V3.4.0
- Diana Python SDK 与 Python API 手册 V3.4.0
- 基于 `libfranka 0.18.2` 的 Diana FCI 示例
- 文档版本：1.0.1（依据 SDK 3.4.0；1.0.0 以 tag `v1.0.0` 保留，依据 SDK 3.3.0）
- 结构化 API 记录：230

## 当前覆盖范围

- 默认同时构建和发布中文、英文站点。
- 顶层导航按接口概述、编程指南和参考组织。
- 编程指南覆盖 C++ SDK、Python SDK 和 FCI。
- C++ 与 Python 均包含概述、开发准备、快速开始、Example 总览和逐例 API 用法。
- FCI 包含实时开发准备、控制模式和基于 `libfranka 0.18.2` 的逐例说明。
- 附件 A 错误码表已转为包含 176 条记录的可搜索网页表格。
- 附录 B 逆解唯一性和附录 C 实时指令说明已整理为专题指南。
- GitHub Pages 与 GitLab Pages CI 构建均已配置。
- 版本下拉支持开发中版本和已登记的不可变 Git tag。

函数级 API Reference 由独立站点维护。本仓库只保留生成错误码表所需的结构化数据。

## 本地预览

Ubuntu 22.04：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make html
python3 -m http.server 8000 -d build/html
```

打开 `http://127.0.0.1:8000`。中文站生成在站点根目录，英文站生成在 `/en/`。

## 本地实时预览

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make live
```

本机打开 `http://127.0.0.1:8000`。局域网设备可使用 `http://<控制PC的局域网IP>:8000` 访问；请确认防火墙允许 TCP 8000。保存 `docs/` 下的文件后，页面会自动重新构建并刷新。

`make html` 和 `make live` 会优先使用仓库内 `.venv`。每次构建都会清理旧 HTML，避免关闭语言或模块后残留旧页面。中文全文检索依赖 `jieba`，已包含在 `requirements.txt` 中。

各指南模块默认启用。将 `DIANA_BUILD_CPP`、`DIANA_BUILD_PYTHON`、`DIANA_BUILD_FCI` 或 `DIANA_BUILD_ROS2` 设为 `0`，即可同时从中英文站点排除对应模块。例如：

```bash
DIANA_BUILD_ROS2=0 make html
```

两个 ROS 2 发行版还可以用 `DIANA_BUILD_ROS2_HUMBLE` 和 `DIANA_BUILD_ROS2_JAZZY` 分别开关，例如在 Jazzy 页面还没写完时先隐藏它：

```bash
DIANA_BUILD_ROS2_JAZZY=0 make html
```

## 发布到 GitHub Pages

向 `main` 推送提交后，工作流会自动构建并部署双语站点。

在仓库的 **Settings → Pages** 中将 **Source** 设为 **GitHub Actions**；`main` 分支工作流成功后，可在部署摘要中查看发布地址。

## 发布到 GitLab Pages

将相同提交推送到 GitLab 项目的默认分支，`.gitlab-ci.yml` 会构建中英文网页，并把 `public/` 发布到 GitLab Pages。请确认项目已启用 GitLab Runner；流水线成功后，可在 **Deploy → Pages** 查看发布地址。

GitHub 与 GitLab 的 CI 文件可以同时保留，两个平台只读取各自的配置，不会相互执行。

## 仓库结构

```text
docs/
├── conf_common.py        # 中英文共用的 Sphinx 配置与构建钩子
├── navigation.py         # 中英文共用的侧边栏目录树
├── _static/              # 内容相关的资源（图片、图示、模块图标）和 project.js
├── zh_CN/                # 中文站源文件（conf.py + 页面）-> build/html/
└── en/                   # 英文站源文件（conf.py + 页面）-> build/html/en/
data/                     # 手册结构化数据与版本清单
scripts/                  # 构建、生成与一致性检查脚本
theme/                    # agile-docs-theme 子模块：主题、模板、样式与构建工具
```

`docs/zh_CN/` 与 `docs/en/` 的页面路径一一对应，例如 `zh_CN/cpp/quick_start.md` 与 `en/cpp/quick_start.md`。页面按接口概述（`about/`、`guide/`）、编程指南（`programming/`、`cpp/`、`python/`、`fci/`、`ros2/`）和参考（`reference/`）组织。

## 文档生成逻辑

```text
data/api_v3_3_0.json
        └─ scripts/generate_error_codes.py
                ├─ docs/zh_CN/reference/error_codes.md
                └─ docs/en/reference/error_codes.md

docs/zh_CN + docs/en -> Sphinx -> build/html/ 和 build/html/en/ -> GitHub Pages 或 GitLab Pages
```

## 维护约定

- **新增、改名或删除页面时，中英文同时修改**，并同步更新 toctree 与 `docs/navigation.py`。页面未加入侧边栏或侧边栏指向不存在的页面时，构建会失败。侧边栏标签默认使用页面 H1，只有需要更短的标签时才单独填写。
- **提交前执行 `make check`。** 页面只存在于一种语言、同一对页面的 H2/H3 数量不一致、代码块里混入了新的围栏开头，或 `std::shared_ptr<Robot>` 这类类型没有写在行内代码里（MyST 会把 `<Robot>` 当作 HTML 隐藏）时会报错；提示块差异以警告列出。CI 会执行同样的检查。
- **不要手工编辑 `reference/error_codes.md`。** 每次构建都会根据 `data/api_v3_3_0.json` 重新生成。
- 通过 `DIANA_BUILD_*=0` 关闭模块时，首页按钮和 toctree 条目按链接目标（`href="cpp/index.html"`、`cpp/index`）删除，按钮文字可以自由修改。

## 文档版本发布

当前默认分支代表 1.0.1 的开发中版本，依据 SDK 3.4.0。验证完成后，创建不可变发布 tag，并在 `data/versions.json` 中新增条目：

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

Pages CI 会把开发中内容发布到站点根目录，把登记的 tag 构建到 `/v1.0.0/` 等独立目录。`make versions` 可在本地生成同样的完整站点。不要移动已发布 tag；技术内容修订时应创建 `v1.0.1` 等补丁版本。

## 重要说明

`data/api_v3_3_0.json` 是从 V3.3.0 手册结构化得到的初始数据，目前只用于生成错误码表。
