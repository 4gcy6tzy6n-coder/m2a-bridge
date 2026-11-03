# CodeGraph 代码导航

> 安装日期：2026-10-27；版本：v1.6.2；来源：https://github.com/colbymchenry/codegraph （MIT）。
> 索引：`codegraph status` → 408 文件、8,086 节点、16,251 边、25.97 MB（2026-10-27 建立）。
> 遥测：已关闭（`codegraph telemetry off`，安装时同时清除了缓冲数据）。

## 是什么

本地代码知识图谱：tree-sitter 解析 20 种语言 → SQLite（`.codegraph/codegraph.db`，含 FTS5）→ 通过 MCP 工具或 CLI 一次回答“源码 + 调用路径 + 影响面”。文件改动由 daemon 增量同步。安装为自包含 bundle（`~/.codegraph` + `~/.local/bin/codegraph`），无需 Node。

## 已完成的接入

1. CLI 安装（官方 `install.sh`，先下载检查后执行）。
2. `codegraph install --yes`：把 MCP server（`codegraph serve --mcp`）写入 Claude Code、Cursor、Codex、VS Code、Kiro、Copilot CLI 等配置；Claude Code 侧同时写入 `mcp__codegraph__*` 免提示规则与指令标记。**重启代理后生效。**
3. `codegraph init`（工作区根目录）：建立索引；`.gitignore` 排除 `.venv/`、实验输出、code snapshot、debug 日志。
4. 验证：`codegraph status`、`codegraph query simulate`、`codegraph explore "..."` 均通过（见 CLAUDE.md 第 5 节命令）。

## 用法约定（与流程的关系）

- 结构性问题先 `codegraph explore`，不要先开 grep/Read 循环；explore 返回的源码视为已读。
- 改代码前 `codegraph impact <symbol>` 估影响面；改完仍必须走「代码 → debug → 门禁 → 实验」流程（[30 每轮流程](30_process.md)）。
- 大批量改动后 `codegraph index --force`；新机器/新克隆执行 `codegraph init`。
- 数字来源：`codegraph status`（2026-10-27）。

## 与 wiki 的分工

| 需求 | 去处 |
| --- | --- |
| 代码在哪、谁调用谁、改动影响面 | CodeGraph（本页 + CLAUDE.md 第 5 节） |
| 为什么这么做、结论与数字、决策与风险 | `wiki/` |
| 某轮实验的证据 | `runs/<round_id>/` + [33 论文页](33_manuscript_track_c.md) |

## 已知注意点

- `codegraph explore` 的自由文本查询可能混入冻结历史包（`M2A_full_bundle`）的同名符号；在查询里带上路径或符号全名（如 `ec_model simulate`）可收窄。
- 索引在非 git 工作区按 `.gitignore` 文本过滤；改动排除规则后需 `--force` 重建。
- 冻结包被索引为**只读导航**，不改变其 `FROZEN` 边界（[10 冻结历史](10_legacy_projects.md)）。
