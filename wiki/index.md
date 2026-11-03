# M2A-BRIDGE 项目 Wiki

> 最后更新：2026-10-27
> 当前状态：`M2A-BRIDGE = PROPOSED_NOT_PREREGISTERED`；P0 决策 **`GO_PILOT`**（计算 pilot）；G0-B `FAIL_NO_LAB`；确认性实验 `NOT_STARTED`。
> 当前可发表产出：**Track C 计算论文草稿**（PLOS Comp Biol 目标，B0，无需新生物数据）；见 [33](33_manuscript_track_c.md)。

## 一句话

**Motion-to-Action：一个系统如何计算“哪些视觉变化应当被抵消、哪些变化应当驱动行动”？** M2A-BRIDGE 要用同一套事前定义的计算变量与干预，同时在真实果蝇神经/行为数据和独立人工系统中做出可区分、可反证的预测——而不是把两端都出现“改善”当作机制相同。

## 现在在哪

| 项目 | 状态 | 现在能做什么 | 不能做什么 |
| --- | --- | --- | --- |
| M2A（旧） | `FROZEN_HISTORICAL_EVIDENCE` | 作为失败风险、形式化接口、治理模板 | 当作新生物机制的确认证据 |
| Route A（旧） | `FROZEN_HISTORICAL_AUDIT` | 作为证据分层、来源核查、T1–T5 合同 | 把旧 58 条当新实验的独立证据 |
| **M2A-BRIDGE** | `PROPOSED_NOT_PREREGISTERED` → P0 `GO_PILOT` | 计算 pilot、公开数据审计、最小 smoke test | 训练确认模型、宣布新机制、声称 Nature 旗舰确认 |
| Nature 主刊 | `GATE_NOT_PASSED` | 按 G0–G5 逐门推进 | 在 G0 未过时承诺旗舰结论 |

**下一步**：P0 已给出 `GO_PILOT`；执行计算 pilot（Erginkaya HS 视觉管线 + Rayshubskiy action→neural 管线 + FlyGym 最小闭环），不启动确认性生物实验。详见 [31 P0 可行性任务](31_p0_assignment.md) 与 [M2A-BRIDGE/G0_G1_FEASIBILITY_DECISION.md](../M2A-BRIDGE/G0_G1_FEASIBILITY_DECISION.md)。

## 导航

- [10 两个冻结历史项目](10_legacy_projects.md) — M2A 与 Route A 的真实状态、可用/禁用边界、命名陷阱。
- [20 M2A-BRIDGE 总体设计](20_m2a_bridge.md) — 科学问题、三个证据环节、旗舰分支、H-F/H-D/H-P、WP0–WP4。
- [21 门禁、证据等级与统计](21_gates_and_stats.md) — G0–G5、B0–B3、独立单位、功效、缺失分类、不可写的话。
- [22 先例与数据](22_prior_art_and_data.md) — flyvis/FlyGym/Erginkaya/BANC/Dryad、已有覆盖与未知字段。
- [30 每轮流程](30_process.md) — 代码 → debug → 门禁 → 实验 → 核验 → wiki；附可执行门禁。
- [31 P0 可行性任务](31_p0_assignment.md) — 首轮精确任务、验收标准、三个允许状态。
- [32 计算 pilot：EC 类型 × 反馈延迟](32_ec_delay_pilot.md) — 四模型 768 条件；allnone 最稳健、graded_sensory 最脆弱。
- [33 Track C 计算论文草稿](33_manuscript_track_c.md) — 完整稿件、claim-evidence map、图表契约；目标 PLOS Comp Biol。
- [34 CodeGraph 代码导航](34_codegraph.md) — 已安装并索引；先查图再 grep；与 wiki 的分工。
- [36 self-state 命题的已有证据核查](36_selfstate_prior_evidence.md) — 文献中无直接证明；果蝇内定性支撑强（本体感觉定增益、触角稳定延迟视觉）；prediction 6 仍是空白实验。
- [40 决策与风险](40_decisions_and_risks.md) — owner 待决事项、风险登记、决策日志。
- [90 变更日志](90_changelog.md) — 追加式记录。
- [99 术语表](99_glossary.md) — H-F/H-D/H-P、G/B/T/E 等级、reafference 等。

## 真相层级

冲突时从高到低：

1. 冻结工件、SHA-256 清单、预注册文件；
2. 有日期的 decision / amendment ledger；
3. 本 wiki（派生视图，不是证据）；
4. 会话摘要与聊天记录。

本 wiki 的数字必须带来源路径；没有来源的数字不写。
