# 每轮研究流程（Round Protocol）

> 目的：把“代码写完直接开跑”改成“代码 → debug 门禁 → 实验”，减少无效算力、无效动物实验和不可追溯的失败。
> 适用范围：本工作区所有代码与实验轮次，包括 M2A-BRIDGE、未来的 Route A 复算和工具开发。
> 门禁脚本：`python3 PROCESS/round_gate.py --round runs/<round_id>`。

---

## 1 一轮的定义

一轮 = 一个可回答的问题 + 一次代码变更 + 一次实验（或明确的“不运行实验”决定）。

每轮必须有：

- 唯一的 `round_id`（建议 `R001`, `R002` … 或 `WP0-P0-01`）；
- 一句 `objective`：本轮要回答什么，不回答什么；
- 一份 `round_manifest.json`；
- 一个 `runs/<round_id>/` 目录；
- 一条 wiki 变更记录。

轮次类型：

| 类型 | 用途 | 额外要求 |
| --- | --- | --- |
| `dev` | 代码、工具、schema、文档 | 可无实验；仍须 debug 记录 |
| `pilot` | 小样本、可行性、方差估计 | 预算上限；不得当确认证据 |
| `confirmatory` | 预注册的确认性检验 | 冻结的预注册文件、主终点、停止规则、owner 批准 |

---

## 2 标准步骤

### 2.1 步骤 0：定义本轮

写 `round_manifest.json`：

```bash
python3 PROCESS/round_gate.py --init runs/R001
```

填清楚：问题、代码路径、debug 命令、实验命令、预算、预期输出、预注册文件（确认性轮次必填）。

**先写“本轮不做什么”**。如果一个问题需要超过一个预算上限，拆轮。

### 2.2 步骤 1：代码工作

- 小步改动；每个改动点能单独回滚。
- 记录代码版本：git 用 commit，非 git 用文件 SHA-256（门禁会自动生成 `code_hashes.json`）。
- 不在这一轮顺手重构无关模块；无关改动另开 `dev` 轮。

### 2.3 步骤 2：Debug（强制）

按下表逐项执行；每项把命令、输出摘要、结论写进 `debug/debug_report.md` 和 `debug/debug_result.json`。

| # | 检查 | 最低要求 | 失败时 |
| --- | --- | --- | --- |
| D1 | 语法 / 导入 | `python3 -m compileall <paths>`；导入所有新模块 | 修复后再继续 |
| D2 | 单元测试 / 自测 | `pytest -q` 或包内 `--selftest`；新增函数必须有测试 | 修复或明确记录豁免理由 |
| D3 | 契约 | 输入 schema、必需字段、ID 唯一性、单位、时间基、缺失值 | 加断言或 schema 校验 |
| D4 | 小样本 smoke | 1 个 animal / session / task / seed，真实读一次输入 | 修复数据 / 接口 |
| D5 | dry-run | `--dry-run` 或打印将执行的步骤、命令、输出路径 | 修复控制流 |
| D6 | 资源预检 | 数据路径存在、版本正确、磁盘 / RAM / GPU 足够 | 调整预算或分批 |
| D7 | 确定性 | 固定 seed；检查排序、浮点容差、缓存是否改变结果 | 固定或记录不稳定来源 |

> Debug 不是“跑一遍没报错”。每一格必须留下可复核的输出或指针。

`debug/debug_result.json` 最小结构：

```json
{
  "status": "pass",
  "timestamp": "2026-10-27T15:00:00+08:00",
  "checks": [
    {"name": "D1 syntax", "status": "pass", "evidence": "compileall: 12 files OK"},
    {"name": "D2 tests", "status": "pass", "evidence": "pytest: 24 passed"},
    {"name": "D3 contract", "status": "pass", "evidence": "schema validation: 1 sample OK"},
    {"name": "D4 smoke", "status": "pass", "evidence": "1 animal, 30 s, exit 0"}
  ],
  "residual_risks": []
}
```

### 2.4 步骤 3：门禁

```bash
python3 PROCESS/round_gate.py --round runs/R001
```

门禁做五件事：

1. 校验 manifest 必需字段；
2. 记录所有 `code_paths` 的 SHA-256；
3. 要求 `debug/debug_result.json` 为 `pass`，且至少 4 项检查、无 fail；
4. 要求 `debug/debug_report.md` 含规定的六节；
5. 确认性轮次要求 `preregistration` 路径存在。

通过才写 `GATE_RESULT.json` 的 `status: pass`；否则退出码 2，并列出 blocking reasons。

### 2.5 步骤 4：实验

- 只运行 manifest 里登记的 `experiment_command`；临时改命令视为新一轮。
- 日志写入 `experiment/stdout.log`、`experiment/stderr.log`，命令写入 `experiment/command.txt`。
- 超过预算上限立即停止；把停止原因写进 `experiment_log.md`。
- 任何异常先归类，再决定是否重跑：`TECHNICAL_FAILURE` 可修复重跑；`BIOLOGICAL_NULL` / `MECHANISM_CONTRADICTED` 是结果，不是错误。

### 2.6 步骤 5：结果核验

实验结束后，先核验再解释：

- 输出文件是否齐全、schema 是否正确；
- 行数、单位、时间基、动物 / session / seed 计数是否与预期一致；
- 是否有缺失、重复、越界、NaN；
- 是否触碰预算或提前停止；
- 结果能否从保存的工件重算。

核验记录写进 `experiment_log.md`。**没有核验的结果不得进入 wiki 的“结果”段。**

### 2.7 步骤 6：记录与 wiki

- 追加 `wiki/90_changelog.md`；
- 更新对应工作包页的状态、门禁状态、待办；
- 重大决策写 `wiki/40_decisions_and_risks.md`；
- 失败和负结果保留，附 `experiment_log.md` 指针。

---

## 3 目录与工件

```text
runs/<round_id>/
  round_manifest.json
  code_hashes.json          # 门禁生成
  GATE_RESULT.json          # 门禁生成
  debug/
    debug_report.md
    debug_result.json
    logs/                   # D1–D7 的原始输出
  experiment/
    command.txt
    stdout.log
    stderr.log
    outputs/
  experiment_log.md
```

---

## 4 省时间的硬规则

1. **15 分钟 / 1 GPU-hour 规则**：超过任一上限，先 smoke + dry-run；没有例外。
2. **先字段、后下载**：数据先读 README、文件清单、小型处理文件；确认字段存在再下载大包。
3. **先小样本、后全量**：任何全量运行前必须有 1 个样本的可运行证据。
4. **先断言、后计算**：ID 唯一、时间基一致、单位正确，在入口处 fail fast。
5. **缓存可复用**：把预训练权重、特征、解码结果放到明确的缓存目录，并在 manifest 记录版本；缓存失效必须可检测。
6. **失败不重跑三次以上**：同一错误连续两次，停下来读日志、写最小复现；第三次仍失败则升级为 blocker。
7. **不在实验中途改代码**：改代码 = 新一轮；中途改动使结果不可归因。
8. **不在看到结果后改主终点**：确认性轮次的主终点、对照、排除规则在 `preregistration` 里冻结。

---

## 5 确认性轮次的附加要求

- `round_manifest.json` 的 `type` 必须是 `confirmatory`；
- `preregistration` 指向冻结文件，文件内必须写明：主终点、竞争假设、对照、样本量 / 功效依据、停止规则、缺失数据处理；
- owner 批准记录写入 `wiki/40_decisions_and_risks.md`；
- 确认与探索物理隔离：探索性分析在新目录、新分支，标注 `EXPLORATORY`；
- 任何偏离登记为 dated amendment，不改原预注册文本。
