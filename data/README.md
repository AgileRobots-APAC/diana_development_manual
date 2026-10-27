# 数据目录

| 文件 | 用途 | 使用者 |
|---|---|---|
| `api_v3_3_0.json` | 从《工业版 API 手册（C&C++版）》V3.3.0 结构化得到的数据：230 条 API 记录、15 个分类和附件 A 的 176 条错误码 | `scripts/generate_error_codes.py`（目前只读取 `error_codes`） |
| `versions.json` | 公开文档版本清单，决定版本下拉菜单和哪些 Git tag 会被构建发布 | `docs/conf_common.py`、`scripts/build_versioned_site.py` |

函数级 API Reference 由独立站点维护。`api_v3_3_0.json` 中的 `apis` 与 `categories` 字段保留为该站点和后续生成工具的数据源；本仓库新增结构化数据时直接放在本目录，不预先建立空的子目录。
