# G0/G1 可行性决策（P0）

- 日期：2026-10-27
- 依据：`01_PRIOR_ART_AND_NOVELTY_MATRIX.csv`、`02_DATA_FEASIBILITY/`、`03_THEORY/`、`07_AUDIT/LEGACY_EVIDENCE_BOUNDARY.md`
- 决策：**`GO_PILOT`**（计算 pilot），不是 `GO_CONFIRMATORY_PENDING_LAB`，也不是 `NO_GO`。

---

## 1 决策摘要

| 门 | 判定 | 理由 |
| --- | --- | --- |
| **G0-A 数据** | `PASS_WITH_CAVEAT` | Erginkaya 有完整 `visual flow → HS/H2 neural` 路径；Rayshubskiy 有同动物 `stimulus → neural → behavior` 路径（刺激为光遗传/嗅觉，不是视觉光流）；没有已验证的同动物视觉+神经+行为数据集（Turner/Dryad 被登录拦截）。 |
| **G0-B 旗舰资格** | `FAIL_NO_LAB` | 当前没有独立生物干预或新合作方采集路径。不能承诺新的动物观测/干预。 |
| **G0-C 解剖** | `PARTIAL` | HS/H2、DNp15、DNa01/02、LT52 的细胞身份可查；跨数据集（视叶→行动命令）的同一性映射未建立。 |
| **G0-D 近邻** | `CONDITIONAL_PASS` | 没有完全等价的主实验；但 2026 年已有强近邻（Zenodo 23018266、arXiv 2610.33881、FlyHack、Digital Sphinx）。剩余缺口是“视觉 reafference 的 H-F/H-D/H-P 联合跨系统预测”，不是“发现 efference copy”。 |
| **G1 新颖性** | `CONDITIONAL_PASS_NARROW` | H-P 已在生物学上被 Kim 2015 / Hartman 2025 支持；不能声称新生物机制。可辩护的新意是：同一套事前操纵下，H-P vs H-D vs H-F 的跨系统联合预测与替代模型排除。 |

## 2 关键变化（相对 master protocol）

1. **H-P 不是新发现。** Kim et al. 2015 已给出 sign/latency 合适的 motor-related input；Hartman et al. 2025 给出 LT52 的非视觉自运动反馈。项目必须把 H-P 当作竞争机制之一，而不是待发现的机制。
2. **跨系统运动消融已有先例。** Zenodo 23018266 已在 FlyGym 中对 DNa01 做单侧消融，并与 Rayshubskiy 2025 在体光遗传结果对照，20 个 degree-matched null 中 0 个复现。这占据了一部分 G3/G4 空间。
3. **全脑/连接组具身行为已有先例。** arXiv 2610.33881 用未训练 brain-VNC 连接组驱动身体，rewired twin 失败；FlyGM 用全脑图控制运动；Digital Sphinx 证明行为逼真不等于生物逼真。
4. **因此 G1 必须收窄**：不能做“连接组放进控制器”“消融有差异”“行为像果蝇”这类已被覆盖的命题。必须是**视觉自运动预测的跨系统联合检验**，并且有公平对照与未见扰动。

## 3 当前授权

| 动作 | 允许 | 条件 |
| --- | --- | --- |
| 公开数据字段审计 | 是 | 不下载大包；不伪称配对 |
| 计算 pilot（flyvis / FlyGym / 简单模型） | 是 | 必须过 `PROCESS/round_gate.py` |
| 预注册草案与预测冻结 | 是 | owner 签字前不称确认性 |
| 新生物实验 / 新动物 / 新干预 | 否 | 需要合作实验室与伦理/审批 |
| Nature 旗舰确认结论 | 否 | G0-B 未过 |
| 把模拟写成生物确认 | 否 | 明确区分 B1 与 B3 |

## 4 现在做什么（计算 pilot）

1. **数据管线**：Erginkaya HS 48×78×2 的视觉响应管线；Rayshubskiy 71 MB 文件的 spike/PSTH 与 action→neural 管线。
2. **模型比较**：在同一套操纵下实现 H-F/H-D/H-P；匹配参数量、时延、信息和训练预算。
3. **AI 端**：FlyGym 最小闭环；先做 1 个 task、1 个 seed 的 smoke test，再做多 seed。
4. **跨系统挑战**：预留一个未用于拟合的扰动/刺激族；只在计算端先做。
5. **预注册草案**：把主终点、对照、停止规则、缺失分类写清楚，等待 owner 冻结。

## 5 什么情况下升级/停止

- **升级到 `GO_CONFIRMATORY_PENDING_LAB`**：出现果蝇生理/行为合作方，能提供独立干预数据；G0-B 重新评估。
- **降级到 `NO_GO`**：公开数据无法支持 H-P/H-D/H-F 的可判别比较，且计算 pilot 也无法给出可证伪预测。
- **保持 `GO_PILOT`**：以上两者都不发生；产出计算/方法论文，明确证据等级 B1，不冒充 Nature 旗舰。

## 6 一句话

**有可发表的计算/方法论文路径，没有当前可承诺的 Nature 旗舰确认路径。** 先做计算 pilot，把“H-P 是否必要”变成可证伪的跨系统检验；如果实验室路径出现，再升级。
