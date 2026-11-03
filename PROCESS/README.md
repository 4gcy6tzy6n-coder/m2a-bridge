# PROCESS

本目录是工作区的执行流程层。

- [ROUND_PROTOCOL.md](ROUND_PROTOCOL.md) — 每轮“代码 → debug → 门禁 → 实验 → 核验 → wiki”的完整规程。
- [round_gate.py](round_gate.py) — 可执行门禁：没有通过的 debug 证据，实验不得启动。
- [templates/](templates/) — manifest、debug 报告、实验日志模板。

## 快速开始

```bash
python3 PROCESS/round_gate.py --init runs/R001
# 填写 runs/R001/round_manifest.json，执行 debug，写 debug/debug_result.json
python3 PROCESS/round_gate.py --round runs/R001
```

门禁返回 0 才允许运行 `experiment_command`；返回 2 时先修复 blocking reasons。

自测：

```bash
python3 PROCESS/round_gate.py --selftest
```
