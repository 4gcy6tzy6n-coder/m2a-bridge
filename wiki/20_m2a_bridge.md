# M2A-BRIDGE：Nature 主刊级双向机制研究

> 来源：[M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md](../M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md)（v1.0，立项候选；SHA-256 `2a9422480fc1a65e9961f7199a77505ac7d7f197a0cdf18f3ba32f817fdf146e`）。原件曾位于 `~/Downloads/`，内容未改动。
> 状态：`PROPOSED_NOT_PREREGISTERED`；未开始确认性实验；不是投稿就绪。

## 1 一句话科学问题

**一个系统在自主运动造成的感觉信号、外部运动扰动与目标驱动的行动要求之间，如何计算“哪些视觉变化应当被抵消、哪些变化应当驱动行动”？**

这是一个真正的 Motion-to-Action 问题，不是光流分类。

## 2 必须同时完成的三个证据环节

1. **Biology → AI**：由连接组、神经响应和行为约束提出可精确定义的计算机制与结构约束；在受控 AI 系统中做机制特异迁移。
2. **AI → Biology**：由模型分歧、控制理论与反事实分析生成**未用于模型选择**的神经元、刺激、时序与行为预测，经独立生物观测 / 干预验证。
3. **Cross-system bridge**：说明两端共同依赖的是什么计算关系，而不只是统计相关或网络图相似；并说明何种情况下不成立。

## 3 候选发现与反命题

**候选发现（有条件，不是已知事实）**：自运动与外部扰动的分离依赖一种具备特定可观测性、时延和反馈耦合条件的计算机制；该机制的生物学扰动后果与人工控制策略的迁移收益都可事前预测，且不能由通用网络容量、普通反馈或已有竞争性去抑制机制解释。

**反命题同等合法**：如果无法给出跨系统机制特异预测，或通用 GRU / 状态估计器及公平重连网络完全解释结果，就停止“发现新共同机制”的叙事；负结果归档，不把标签转为证据。

## 4 旗舰分支：果蝇自运动视觉反馈与行动

**为什么选它**：视觉光流中外部扰动、身体自运动（reafference）和目标相关行动相互纠缠；果蝇有连接组、视觉生理、感受-运动行为、定向干预和模拟平台。

**解剖边界（必须先登记）**：flyvis 视叶模型、FlyWire / optic-lobe 连接组、2026 brain-and-cord connectome、2025 视觉去抑制回路与 FlyGym 具身仿真**不是同一份整合数据集**。必须记录每个轴的物种、雌雄、成虫 / 幼虫、脑区、细胞身份映射、记录环境、采样频率与采集 / 处理过程。若无法建立输出细胞到行动命令回路的可信跨数据映射，只能声称 `visual computation module + behavioural decoder`，不能声称完整 connectome-to-action 因果链。

## 5 已覆盖的先例与可竞争新增点

已经覆盖、不能称为创新的部分：

- Lappalainen et al., *Nature* 2024：flyvis 连接组约束模型预测细胞响应，含任务优化、结构消融与神经数据比较。
- Wang-Chen et al., *Nature Methods* 2024：NeuroMechFly v2 / FlyGym 的视觉、运动与具身闭环。
- Westeinde et al., *Nature* 2024：PFL 类群把方向 / 目标信号变成转向命令。
- Erginkaya et al., *Nature Neuroscience* 2025：竞争性去抑制提高旋转光流选择性。
- Bates et al., *Nature* 2026：脑-神经索完整连接组与分布式局部感觉运动反馈。
- FlyHack、Topological Sensitivity、FlyGM、ConnectomeX / FlyVision（2026 预印本）：已示范 flyvis 消融、拓扑对照、全脑连接组控制和连接组启发视觉网络。

**可竞争新增点**：*同一个事前定义的计算变量 / 干预，对先前不可见的生物-行动结果和独立 AI 行为结果，形成联合而且能排除替代模型的预测。* 这必须由独立证据证明，不能靠概念宣称。

## 6 三个事前竞争机制

| ID | 机制 | 核心主张 | 关键可识别操纵 |
| --- | --- | --- | --- |
| **H-F** | 通用反馈控制 | 无需机制特异生物回路；容量、可观测性和时延决定结果 | 匹配容量 / 时延的 GRU、PID、Kalman 对照 |
| **H-D** | 视觉竞争性去抑制 / 运动 opponency | 对称平移与差分旋转通过竞争或抑制分离；不要求行动拷贝 | 对称性操纵；与 C3（结构化 opponency）比较 |
| **H-P** | 动作条件预测 / 感觉反馈误差 | 内部状态与过去动作产生自运动感觉预测，残差驱动行动 | 自运动预测有效 / 失效 × 外部扰动有 / 无 × 时延 × 对称性 |

**H-P 的生物学识别门**：能否在真实神经回路中定位动作相关信息。仅观察运动相关活动不能把 *efference copy* 当作已证实机制。

**工作近似（假说模型，非生物事实）**：

- 观测生成：`v_t = R(a_{<t}, h_t) + d_t + eps_t`（实际视觉信号是非线性图像变换）。
- H-F：`a_t = pi_theta(v_<=t, a_<t, g_t)`。
- H-D：`z_t = Opp(v_<=t)`，`a_t = pi_theta(z_t, g_t)`。
- H-P：`rhat_t = P_theta(a_<t, h_t)`，`z_t = phi(v_t − rhat_t)`，`a_t = pi_theta(z_t, g_t)`。

关键比较是同时操纵 `(自运动预测有效/失效) × (外部扰动有/无) × (视觉-动作时延) × (视觉对称性)`，产生三种模型不同的神经响应、行为转向或闭环稳定性预测。仅拟合已有开环转向曲线不能识别 H-P。

## 7 工作包

| WP | 问题 | 主要产出 | 关键门 |
| --- | --- | --- | --- |
| **WP0** | 生物实验是否真的可做 | `BIO_DATA_ELIGIBILITY.csv`、字段级审计、`G0_G1_FEASIBILITY_DECISION.md` | G0-A/B/C/D |
| **WP1** | AI → Biology 的可区分预测 | 三模型冻结预测表、揭盲分析、B0–B3 验证 | G2 |
| **WP2** | Biology → AI 的机制迁移 | Task-A/B/C、C0–C6 对照、匹配审计 | G3 |
| **WP3** | 共同可识别性（旗舰关键） | `Delta_B` / `Delta_A`、映射 `M`、未见扰动挑战 | G4 |
| **WP4** | 独立系统推广与 Route A 合同 | 第二回路 / 行为状态、T1–T5 证据台账 | G5 |

### WP0 硬门（第一优先、低成本）

- **G0-A**：至少一条完整 `stimulus → neural response` 路径，和一条完整 `stimulus → action/behaviour` 路径；不同动物 / 来源必须明确不伪称配对。
- **G0-B**：有独立样本、独立干预或新合作方可采集的**前瞻生物验证**路径，能区分至少两个竞争机制；否则只授权 `COMPUTATIONAL_PILOT`。
- **G0-C**：合法、科学可辩护的细胞类型 / 连接来源 / 神经区域对应；不满足则缩小机制主张。
- **G0-D**：完成 2024–2026+ 文献逐项排重，不存在完全等价的刺激 × 机制 × 结果主实验。

### WP2 公平对照

`C0` 经典状态估计 + 反馈；`C1` GRU/LSTM；`C2` LTC/CfC；`C3` 结构化视觉 opponency；`C4` 生物约束候选机制；`C5` 重连 / 符号翻转 / 时序错位 / 无反馈 null；`C6` 同参数量、同 token/steps、同输入信息量的通用替代器。至少 5 个独立训练 seed 只算模型随机性，不是生物重复。

### WP3 主张层级

`qualitative analogy` → `quantitative correspondence` → `interventional correspondence` → `jointly predictive mechanism`。不能因为两端都出现“改善 / 下降”就判机制相同。

## 8 成功与失败的写法

- 生物成功 / AI 失败：机制或许解释神经活动，但不说明有人工迁移价值。
- AI 成功 / 生物失败：是有效人工技巧，**不是**新生物机制发现。
- 两者成功 / 映射失败：两个独立结果，**不是**已证实同一计算机制。
- 都失败：预注册假说被否证，完整公开。

只有联合结果与替代机制区分同时成立，才可讨论 general computational principle。

## 9 P0 结果（2026-10-27）

**决策：`GO_PILOT`**，不是 `GO_CONFIRMATORY_PENDING_LAB`，也不是 `NO_GO`。

| 门 | 判定 | 依据 |
| --- | --- | --- |
| G0-A 数据 | `PASS_WITH_CAVEAT` | Erginkaya 有视觉光流→HS/H2 神经响应；Rayshubskiy 有同动物 stimulus→neural→behavior，但刺激是光遗传/嗅觉，不是视觉；Turner/Dryad 最理想但下载被 401/403 拦截 |
| G0-B 旗舰资格 | `FAIL_NO_LAB` | 没有独立生物干预或合作实验室路径 |
| G0-C 解剖 | `PARTIAL` | HS/H2、DNp15、DNa01/02、LT52 可查；视叶→行动命令的跨数据集映射未建立 |
| G0-D 近邻 | `CONDITIONAL_PASS` | 无完全等价主实验；但 2026 年近邻很强（Zenodo 23018266、arXiv 2610.33881、FlyHack、Digital Sphinx） |
| G1 新颖性 | `CONDITIONAL_PASS_NARROW` | H-P 已有生物学证据；新意只能是同套操纵下的跨系统联合预测与替代模型排除 |

**关键修正**：

1. **H-P 不是新发现**。Kim et al. 2015 已给出 sign/latency 合适的 motor-related input；Hartman et al. 2025 的 LT52 给出肢体运动反馈。
2. **DNa01 运动消融的跨系统对应已被占据**。Zenodo 23018266 在 FlyGym 中做单侧 DNa01 消融，并与 Rayshubskiy 2025 在体光遗传结果对照，20 个 degree-matched null 中 0 个复现。
3. **全脑/连接组具身行为已有先例**。arXiv 2610.33881 的未训练 brain-VNC 连接组、FlyGM 的全脑图控制、Digital Sphinx 的行为逼真≠生物逼真。

**可辩护的窄缺口**：没有研究把 H-P 与 H-D、H-F 放在同一套事前操纵下，同时检验它能否解释果蝇视觉/行为数据，并在匹配容量、时延、信息和训练预算的人工系统中预测未见扰动。

详见 [G0_G1_FEASIBILITY_DECISION.md](../M2A-BRIDGE/G0_G1_FEASIBILITY_DECISION.md)、[DATA_ACCESS_REPORT.md](../M2A-BRIDGE/02_DATA_FEASIBILITY/DATA_ACCESS_REPORT.md)、[COMPETING_MECHANISMS_v0.md](../M2A-BRIDGE/03_THEORY/COMPETING_MECHANISMS_v0.md)。

## 10 状态块

```text
M2A_ORIGINAL                         = FROZEN_HISTORICAL_EVIDENCE
ROUTE_A_ORIGINAL                     = FROZEN_HISTORICAL_AUDIT
M2A_BRIDGE                           = PROPOSED_NOT_PREREGISTERED
BIO_DATA_FIELD_LEVEL_ELIGIBILITY     = NOT_VERIFIED
BIO_INTERVENTIONAL_CONFIRMATION      = NOT_STARTED
AI_MATCHED_OOD_CONFIRMATION          = NOT_STARTED
JOINT_MECHANISM_TEST                 = NOT_STARTED
NATURE_ARTICLE_SCIENTIFIC_GATE       = NOT_PASSED
NATURE_SUBMISSION_READY              = FALSE
```
