# 两个冻结历史项目：M2A 与 Route A

> 这两个项目是 M2A-BRIDGE 的**来源、风险清单和方法资产**，不是新实验的确认证据。
> 原文入口：`M2A_full_bundle_2026-10-26/`、`ROUTE_A_EVIDENCE_PACKAGE_20261026/`。
> 本页只做导航和边界说明；任何数字以包内冻结工件为准。

## 1 M2A（Motion to Action，旧项目）

**原始问题**：跨系统的触发 / 门 / 约束 / 省略能否写成可迁移的定量机制，并从合成模型推到真实系统。

**权威状态**（`M2A_full_bundle_2026-10-26/PROJECT_STATE_2026-10-26.md`）：

- 三条律 L1/L2/L3 只在合成模型族内成立；L1 的“分布无关”已撤回；L3 原式被否证并修正。
- I1（省略 = S ⊕ C）是定义 + 假说；文献编码 17 行中 12 行 NEITHER，21 篇全文双编码全为 NEITHER；真实 OBD 七轮只测得 S-only 效应，C 的决策优势始终未测得。
- 理论延伸 DCAMT / DRBA 被判 `REDUNDANT` / `NO_GO`；没有一条达到 `NEW_AND_NONTRIVIAL`。
- Nature 三盲审：2 reject + 1 major revision，主刊 `NO_GO`；阻断项是“没有真实系统指涉”和“没有被因果抽象覆盖之外的命题”。

**M2A-BRIDGE 可以使用**：

- Motion-to-Action 的状态 / 观测接口、控制目标；
- 预注册、门控、哈希绑定、失败保留的治理模板；
- `S-only measurable / C not identified`、合成律修正、理论 `NO_GO` 作为**已知失败风险**和 SI 审计案例。

**禁止**：

- 把旧 S-only 观察升级为新生物机制；
- 把合成 L1/L2/L3 称为 Nature 级定律；
- 用旧仓库的审计通过数代替新发现。

## 2 Route A（文献证据审计，旧项目）

**原始问题**：bio→AI 迁移论文在自身论文内部，沿推断链每一段提供了什么证据。

**权威状态**（`ROUTE_A_EVIDENCE_PACKAGE_20261026/00_CONCLUSIONS_AND_EVIDENCE.md`）：

- 五段链 T1 结构→计算、T2 计算→对应、T3 对应→效用、T4 效用→普适、T5 任何→宣称范围；证据等级 E0–E4；11 项报告性；哈希绑定评分器；预注册 kill rule 80%。
- 60 条 claim（主 18→16、验证 42），四轮编码；T1 在所有读数中 100% 为 E0（引用外借）。
- 效用证据集中于 T3，对应证据 T2 多为暗示性；但 T2 的两种可辩护操作化在 58 篇中只在 3/19 篇一致，且人类原始读数在主语料反转 T2/T3 对比。
- kill rule 未触发；稿件为 NMI Article 格式，3,439/3,500 词；门禁 `TECHNICAL_CLOSURE_ACCEPTED_WITH_RIGHTS_REVIEW`，**NOT SUBMISSION_READY**（O-5、O-6、导师三问待办）。

**M2A-BRIDGE 可以使用**：

- 证据分层、来源核查、B（生物目标对应）/ A（机制归因）的独立评估；
- T1–T5 作为 WP4 的“可实测验证合同”；
- 失败容纳和权利审查方法。

**禁止**：

- 把旧 58 条当作生物验证或新实验的独立证据；
- 宣称“人类无条件确认了效用 > 对应”的不对称；
- 把旧文献审计与新神经元读数放进同一个统计模型。

## 3 命名陷阱：两个“Route A”

| 名称 | 在哪里 | 是什么 | 状态 |
| --- | --- | --- | --- |
| **Route A（文献审计）** | `ROUTE_A_EVIDENCE_PACKAGE_20261026/` | 五段链 T1–T5 的文献证据审计，目标 NMI | 冻结历史，接近可投稿 |
| **Route A（DRBA）** | `M2A_full_bundle_2026-10-26/theory/M2A-Theory-A/ROUTE_A_*` | description-conditioned action-mechanism transfer 算法设计 | `REDUNDANT` / 理论轨 `NO-GO` |

两者不是同一个项目。看到 `ROUTE_A_G1_VERDICT.md` 的 `NO-GO` 时，不要误读为“文献审计不能投 NMI”。

## 4 两个旧包进入新项目的正确方式

| 旧资产 | 进入位置 | 角色 |
| --- | --- | --- |
| M2A 形式化接口与失败边界 | `03_THEORY/`、SI | provenance / motivation |
| M2A OBD 七轮与合成律修正 | SI、风险登记 | 已知失败风险，不是正结果 |
| Route A T1–T5 与 E 等级 | `07_AUDIT/T1_T5_EVIDENCE_LEDGER.csv`、WP4 | 评估合同 |
| Route A 58 条审计 | SI、Methods | 旧审计，不是新证据 |
| 两包的治理模板 | 新仓库 `07_AUDIT/` | 预注册、哈希、失败保留 |

新项目必须独立立项、独立时间戳、独立 owner 决策日志；旧仓库只读。
