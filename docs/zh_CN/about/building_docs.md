# 构建与发布本手册

本页面向维护本手册的人员，说明如何在本地构建网页、打印当前页 PDF，以及如何发布到 GitHub Pages 或 GitLab Pages。

## 准备环境

需要 Python 3.12 或兼容版本、Git。

```bash
git clone --recurse-submodules <仓库地址>
cd <仓库目录>
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 构建网页

执行：

```bash
make html
```

网页输出到 `build/html/`，中英文入口分别为 `build/html/index.html` 与 `build/html/en/index.html`。可用以下命令本地预览：

```bash
python3 -m http.server --directory build/html 8000
```

然后访问 `http://127.0.0.1:8000`。

### 只构建部分模块

各指南模块默认启用。将 `DIANA_BUILD_CPP`、`DIANA_BUILD_PYTHON`、`DIANA_BUILD_FCI` 或 `DIANA_BUILD_ROS2` 设为 `0`，即可同时从中英文站点排除对应模块；两个 ROS 2 发行版还可以用 `DIANA_BUILD_ROS2_HUMBLE` 和 `DIANA_BUILD_ROS2_JAZZY` 分别开关。例如在 Jazzy 页面还没写完时先隐藏它：

```bash
DIANA_BUILD_ROS2_JAZZY=0 make html
```

每次构建都会清理旧的 HTML，不会残留已关闭模块的页面。

## 源文件结构与维护约定

中文源文件位于 `docs/zh_CN/`，英文源文件位于 `docs/en/`，两者页面路径一一对应；`docs/_static/`、`docs/_templates/`、`docs/conf_common.py` 和侧边栏目录 `docs/navigation.py` 由两个站点共用。

- 新增、改名或删除页面时，中英文同时修改，并同步更新 toctree 与 `docs/navigation.py`；页面未加入侧边栏时构建会失败。
- 提交前执行 `make check`，检查中英文页面是否成对、标题结构是否一致。
- `reference/error_codes.md` 由 `scripts/generate_error_codes.py` 生成，不要手工编辑。
- ROS 2 Humble 的结构图和“版本与更新”页的发布基线图由 `scripts/build_ros2_diagrams.py` 与 `scripts/build_release_baseline.py` 用 Graphviz 生成；需要修改时改脚本并重新运行，不要直接编辑 PNG。

## 主题与构建工具

网页的外观（模板、配色与暗色模式、侧栏、提示框、表格、图片查看、版本选择和语言切换等）以及版本站点构建、静态资源去重、双语一致性检查这几个工具，都来自独立的主题仓库 `agile-docs-theme`，它作为子模块放在 `theme/` 目录。本仓库只保留与内容有关的部分：导航结构 `docs/navigation.py`、侧栏图标配置 `docs/_static/project.js`、图片和图示。

- 已克隆但 `theme/` 为空时，执行 `git submodule update --init`。
- 不要直接修改 `theme/` 里的文件；外观上的改动请在主题仓库中完成，再更新子模块指向的提交。
- 主题的使用方法和配置项见 `theme/README.md`；其他文档项目也可以用同样的方式引入。

## 打印当前页 PDF

网页工具栏中的打印按钮会调用浏览器打印当前页面。需要 PDF 时，在浏览器打印界面选择“另存为 PDF”即可。该功能不依赖 CI 预先生成文件，也不会构建或下载整本手册。

## 构建版本站点与发布

版本清单由 `data/versions.json` 管理。构建当前版本及清单中已发布版本：

```bash
python3 scripts/build_versioned_site.py
```

最终发布目录为 `public/`：开发中版本位于站点根目录，已登记的正式版本位于 `/v1.0.0/` 这样的独立子目录。推送到默认分支后，所在平台的 CI 会自动：

1. 构建中英文网页；
2. 校验两个语言入口；
3. 在 GitHub 上由 `.github/workflows/deploy-pages.yml` 发布到 GitHub Pages，或在 GitLab 上由 `.gitlab-ci.yml` 发布到 GitLab Pages。

两套配置可以同时保留。GitHub 不会执行 `.gitlab-ci.yml`，GitLab 也不会执行 `.github/workflows/`，因此同一份提交可安全推送到两个平台。

发布正式版本的步骤：

1. 内容验证完成后，创建以 `v` 开头的 Git tag，例如 `v1.0.0`。已发布的 tag 不要移动；内容修订时创建 `v1.0.1` 这样的补丁版本。
2. 在 `data/versions.json` 中新增条目，`ref` 填该 tag，`path` 为站点子目录，`published` 设为 `true`，`status` 不能是 `development`。只有登记的 tag 才会被发布，不会自动发现 tag。
3. 推送到默认分支，CI 会构建开发中版本和所有登记的 tag。

发布前请确认版本清单、各模块的发布基线（C++ / Python SDK、FCI、ROS 2，见[版本与更新](versions.md)）和本手册内容一致。
