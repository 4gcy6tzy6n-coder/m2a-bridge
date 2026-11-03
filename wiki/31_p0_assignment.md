# P0：资格与先导可行性任务

> 来源：master protocol §11.1、§11.2。
> 状态：**等待 owner 批准**。批准 P0 不等于批准 WP1–WP4 的确认性实验。

## 1 目标

识别可独立检验的生物机制预测；**不得训练确认模型，不得宣布新自然规律**。

## 2 六项任务

| # | 任务 | 产出 | 状态 |
| --- | --- | --- | --- |
| P0-1 | 阅读 M2A 与 Route A 冻结权威记录，分别做 evidence boundary 表；不改两个原项目 | `M2A-BRIDGE/07_AUDIT/LEGACY_EVIDENCE_BOUNDARY.md` | `DONE` |
| P0-2 | 核对近邻论文与代码发布日期；记录论文 DOI、code commit、数据 DOI、文件大小、许可证；只记已核实信息 | `M2A-BRIDGE/01_PRIOR_ART_AND_NOVELTY_MATRIX.csv` | `DONE` |
| P0-3 | 为 flyvis、FlyGym 2.x、Erginkaya 2025、BANC 2026 及一个可用小型行为数据集做身份 / 时基 / 刺激 / 行为 / 干预匹配审计 | `BIO_DATA_ELIGIBILITY.csv`、`CROSS_SOURCE_IDENTITY_MAP.csv`、`DATA_ACCESS_REPORT.md` | `PARTIAL`（Dryad 登录拦截；两套数据已实测） |
| P0-4 | 为 H-F / H-D / H-P 各写至少三条互相不同、可通过公开数据或未来生物实验判别的预测；含测量单位、符号、时间尺度、null | `COMPETING_PREDICTIONS_v0.csv`、`COMPETING_MECHANISMS_v0.md` | `DONE（v0，未冻结）` |
| P0-5 | 运行**一次**最小 flyvis / FlyGym smoke test；保留版本、运行时、显存、CPU/RAM、断言结果；即使 API 不兼容也记 `FAIL` | `runs/P0-SMOKE-01/experiment/outputs/smoke.json`、`experiment_log.md` | `DONE（PASS；全驱动模型 BLOCKED_BY_ASSET_HOST）` |
| P0-6 | 形成 `G0_G1_FEASIBILITY_DECISION.md`，唯一允许状态 `GO_PILOT / GO_CONFIRMATORY_PENDING_LAB / NO_GO`，列出 owner 必须补齐的人类实验资源 | `G0_G1_FEASIBILITY_DECISION.md` | `DONE → GO_PILOT` |

## 2.1 P0 结果（2026-10-27）

- **G0-A `PASS_WITH_CAVEAT`**：Erginkaya 提供 `visual flow → HS/H2`；Rayshubskiy 提供同动物 `stimulus → neural → behavior`（刺激非视觉光流）；Turner/Dryad 最理想但下载被拦截。
- **G0-B `FAIL_NO_LAB`**：没有独立生物干预或合作实验室路径，不能承诺 Nature 旗舰确认。
- **G1 `CONDITIONAL_PASS_NARROW`**：H-P 已被 Kim 2015 / Hartman 2025 支持；Zenodo 23018266 已占运动消融跨系统对应；剩余缺口是视觉 reafference 的 H-F/H-D/H-P 联合跨系统预测。
- **决策**：`GO_PILOT`，只做计算 pilot；不启动确认性生物实验。
- **Smoke test（P0-SMOKE-01）**：flyvis 1.2.0 连接组 45,669 nodes / 1,513,231 edges；FlyGym 2.1.1 自由体 50 步，qpos/positions finite；RSS ~1.0 GB；全驱动 FlyBody/MusculoskeletalFly 因 `datasets.epfl.ch` TLS 失败未验证。

详见 [G0_G1_FEASIBILITY_DECISION.md](../M2A-BRIDGE/G0_G1_FEASIBILITY_DECISION.md)。

## 3 禁止

- 把“可下载”当成“同动物配对”；
- 把公开既有机制重述称为新发现；
- 因先导结果强行更换主机制；
- 更改历史结果或复制未获授权的第三方全文；
- 擅自标 `NATURE_READY`；
- 训练确认模型或运行确认性实验。

## 4 首轮交付验收

- 至少两种竞争机制已经写出**不会因任务成功与否而自动成立**的可证伪预测。
- 至少一个生物数据源字段实际可读；记录具体 key、shape、物种 / 动物 / 刺激 / 神经读数、时间单位、缺失和许可证。
- 一份明确的 `NEURAL_ACTIVITY_PRESENT` 与 `BEHAVIOR_PRESENT` 状态表，不能默认两者同动物。
- 一份生物合作需求表：最少的基因 / 细胞类群、干预方法、动物数功效前置参数、实验时间窗与盲法。
- 对比文献写出**我们比各前例多验证什么**，每项必须是可实验检验的差异。
- 如 G0 失败，保持 `NO_GO_FOR_NATURE_CONFIRMATORY`，不把模拟输出当成功。

## 5 允许的最终状态

| 状态 | 含义 | 下一步 |
| --- | --- | --- |
| `GO_PILOT` | 字段级可行，但确认性生物路径未定 | 进入低成本计算 pilot；不同时承诺确认实验 |
| `GO_CONFIRMATORY_PENDING_LAB` | 有明确合作实验室 / 干预路径，等资源与审批 | 冻结预测、启动伦理 / 遗传线 / 刺激校准 |
| `NO_GO` | 没有独立生物结局或可辩护的解剖映射 | 停 Nature 旗舰确认；保留计算 / 方法论文路线 |

## 6 执行前需要 owner 确认

1. 批准 P0 的低成本核验（不包含 WP1–WP4 确认实验）；
2. 是否已有果蝇神经生理 / 行为合作方；
3. 可接受的下载 / 算力预算上限；
4. P0 产出的存放位置与是否需要新仓库。

> 在这些确认之前，本页所有任务保持 `PENDING`，不启动下载、不训练模型。
