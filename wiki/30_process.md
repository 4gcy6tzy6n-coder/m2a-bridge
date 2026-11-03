# 每轮流程：代码 → debug → 实验

> 详细规程：[PROCESS/ROUND_PROTOCOL.md](../PROCESS/ROUND_PROTOCOL.md)。
> 可执行门禁：[PROCESS/round_gate.py](../PROCESS/round_gate.py)。
> 本页是给 wiki 读者的一页版。

## 1 一轮的六步

```text
定义本轮 → 代码工作 → Debug（7 项）→ 门禁 → 实验 → 结果核验 → wiki 更新
```

每轮一个目录 `runs/<round_id>/`，由门禁脚本初始化：

```bash
python3 PROCESS/round_gate.py --init runs/R001
```

## 2 Debug 七项

| # | 检查 | 最低要求 |
| --- | --- | --- |
| D1 | 语法 / 导入 | `compileall` 或等价；所有新模块可导入 |
| D2 | 单元测试 / 自测 | `pytest -q` 或 `--selftest`；新增函数有测试 |
| D3 | 契约 | schema、ID 唯一、单位、时间基、缺失值 |
| D4 | 小样本 smoke | 1 个 animal / session / task / seed，真实读一次输入 |
| D5 | dry-run | 打印将执行的步骤、命令、输出路径 |
| D6 | 资源预检 | 数据路径、版本、磁盘 / RAM / GPU |
| D7 | 确定性 | seed、排序、浮点容差、缓存 |

## 3 门禁

```bash
python3 PROCESS/round_gate.py --round runs/R001
```

- 退出码 0：允许运行 `experiment_command`；
- 退出码 2：blocked，按列出的原因修复，**不得启动实验**；
- 门禁生成 `code_hashes.json` 与 `GATE_RESULT.json`，作为本轮代码版本的证据。

门禁检查：manifest 必需字段；代码哈希；`debug/debug_result.json` 为 pass 且至少 4 项检查；`debug/debug_report.md` 六节齐全；确认性轮次的预注册文件存在。

## 4 省时间硬规则

1. **15 分钟 / 1 GPU-hour 规则**：超过任一上限，先 smoke + dry-run。
2. **先字段、后下载**：先确认数据字段存在，再下载大包。
3. **先小样本、后全量**：全量前必须有 1 个样本的可运行证据。
4. **先断言、后计算**：入口处 fail fast。
5. **缓存可复用且可失效**：预训练权重、特征、解码结果记录版本。
6. **同一错误不重跑三次以上**：第二次停下来写最小复现。
7. **实验中途不改代码**：改代码 = 新一轮。
8. **看到结果后不改主终点**。

## 5 结果核验

实验结束后先核验：输出齐全、schema、行数 / 单位 / 时间基、独立单位计数、缺失 / 重复 / 越界、预算未超。**没有核验的结果不得进入 wiki 的“结果”段。**

## 6 Wiki 更新

每轮结束：

1. 追加 [90 变更日志](90_changelog.md)；
2. 更新受影响的工作包 / 门禁页；
3. 重大决策写 [40 决策与风险](40_decisions_and_risks.md)；
4. 失败和负结果保留，附 `experiment_log.md` 指针。

wiki 是派生视图，不是证据；冻结工件与预注册优先。
