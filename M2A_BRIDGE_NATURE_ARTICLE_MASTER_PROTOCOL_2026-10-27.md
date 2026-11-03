# M2A-BRIDGE｜Nature 主刊级双向机制发现总研究方案（立项候选 v1.0）

**日期：** 2026-10-27  
**性质：** 可执行研究设计与门禁契约草案；**未预注册、未开始确认性实验、并非投稿就绪**。任何数字型成功阈值、采样量和显著性边界，在先导方差/可用数据核查后由 owner 冻结，不得把本草案当作已经执行。  
**第一目标：** *Nature*（主刊）Article；若跨系统生物学确认不可行，保持 *Nature Machine Intelligence / Nature Neuroscience / Nature Communications* 等与实际贡献相称的投稿选择，不以降刊倒推结果。  
**项目名称：** `M2A-BRIDGE`（暂用，避免混淆已有 M2A 和文献审计 Route A）。

---

## 0. 一句话科学问题与核心承诺

**Motion-to-Action：一个系统在自主运动造成的感觉信号、外部运动扰动与目标驱动的行动要求之间，如何计算“哪些视觉变化应当被抵消、哪些变化应当驱动行动”？**

研究必须同时完成以下三个独立的证据环节：

1. **Biology → AI**：由连接组、神经响应和行为约束，提出可精确定义的计算机制与结构约束；在受控 AI 系统内进行机制特异迁移。
2. **AI → Biology**：由模型分歧、控制理论与反事实分析生成 *未用于模型选择* 的神经元、刺激、时序及行为的前瞻预测，经独立生物观测/干预验证。
3. **Cross-system bridge**：说明两端共同依赖的究竟是何种计算关系，而不只是统计相关或类似网络图；研究何种情况下不成立。

**Nature 级候选科学发现**（有条件的期待，不是已知事实）：自运动与外部扰动的分离依赖一种具备特定可观测性、时延和反馈耦合条件的计算机制；该机制的生物学扰动后果与人工控制策略的迁移收益均可事前预测，且不能由通用网络容量、普通反馈与已有竞争性去抑制机制解释。

**反命题同等合法**：如果无法给出跨系统机制特异预测，或通用 GRU/状态估计器及公平重连网络完全解释结果，就停止“发现新共同机制”的叙事。负结果归档，不将标签转为证据。

---

## 1. 与两个原有项目的关系：不混样本、不追认成功

| 既有资产 | 原研究定位 | 本项目可使用的部分 | 本项目禁止做的事 |
|---|---|---|---|
| **M2A = Motion to Action** | 感知/状态/约束/决策如何产生行动的理论与实验程序；此前合成律、OBD 与省略机制存在明确失败和限制 | 形式化 Motion-to-Action 的状态与观测接口、控制目标、冻结和负结果治理；历史结果用于指出不可识别边界 | 不能把旧的 S-only 观察升级为新生物机制，也不能将合成 L1/L2/L3 称为 Nature 级定律 |
| **NeuroConverge Route A** | bio→AI 文献的 T1–T5 证据审计；原始人类 H 在主语料反转 T2/T3 对比 | 证据分层、来源核查、B（生物目标对应）/A（机制归因）的独立评估与失败容纳 | 不能以旧 58 条作为生物验证或新实验的独立证据，不能宣称人类无条件确认不对称 |
| **本项目 M2A-BRIDGE** | 独立的新跨系统机制研究 | 新生物假说、新真实实验、新 AI 验证、跨系统特异性检验 | 不得以双项目总实验数、代码覆盖率或 Nature 的既有先例代替新发现 |

既有项目的作者贡献、代码与数据权利和发表重叠分别审查。旧仓库只读，新的确认研究独立立项、独立时间戳和 owner 决策日志。

## 2. 首个旗舰分支的选择：自运动视觉反馈与行动

### 2.1 为什么选择它

视觉光流中外部扰动、身体自运动（reafference）和目标相关行动相互纠缠，是真正的 Motion-to-Action，而不仅是光流分类。果蝇具有连接组、视觉生理、感受-运动行为、定向干预和可用的模拟平台；但它们目前不一定来自同一个物种阶段、个体、细胞类型映射或实验设置，**不能直接拼接为一个已经验证的完整回路**。

### 2.2 已经被先例覆盖、不能再称创新的部分

- Lappalainen et al., *Nature* 2024：真实连接组约束的 flyvis 模型在视觉运动任务训练后可预测细胞响应；研究已包含任务优化、结构消融和已有神经数据比较。
- Wang-Chen et al., *Nature Methods* 2024：NeuroMechFly v2/FlyGym 的视觉、运动和具身闭环任务已有实现。
- Westeinde et al., *Nature* 2024：PFL 类群将方向/目标信号变成转向命令，已有电生理、成像和干预。
- Erginkaya et al., *Nature Neuroscience* 2025：竞争性去抑制提高旋转光流选择性，已有解剖、生理、干预和行为证据。
- Bates et al., *Nature* 2026：脑-神经索完整连接组支持分布式局部感觉运动反馈及升降神经元协调。
- *FlyHack* (arXiv 2026) 与 *Topological Sensitivity* (arXiv 2026)：已示范 flyvis 的模型、干预和拓扑对照依赖；不应重复“消融后有差异就是新机制”。
- *FlyGM* (arXiv 2026)：已直接使用全脑连接组图控制具身果蝇；简单“把连接组放进控制器”不新。
- *From the Drosophila Visual Connectome to General-Purpose Computer Vision* (arXiv 2026)：已有连接组启发网络的跨视觉任务应用；仅在分类数据集改善并非独创。

**因此，本项目的可竞争新增点是**：*同一个事前定义的计算变量/干预，对先前不可见的生物-行动结果和独立 AI 行为结果，形成联合而且能排除替代模型的预测*。必须以独立证据证明，不可凭概念宣称。

### 2.3 三个事前竞争机制模型（不得事后只保留成功者）

- **H-F：通用反馈控制**。无需机制特异的生物回路，只根据观测历史和 action history 实现控制；容量、可观测性和时延决定结果。
- **H-D：视觉通路竞争性去抑制/运动 opponency**。对称平移成分与差分旋转成分通过竞争或抑制获得分离；不要求行动拷贝输入。此类机制已有 2025 生物学先例，若再现仅算 baseline reproduction。
- **H-P：动作条件预测/感觉反馈误差**。内部状态和过去动作产生自运动感觉预测，残差决定对外界扰动的行动；是否存在可以定位到真实神经回路的动作相关信息，是其生物学识别门。

也可存在 H-D+H-P 混合模型，但**只有在首次数据解封前冻结独立可识别预测**才可作为确认假说；否则仅探索。所谓 *efference copy* 不得在仅观察运动相关活动时使用为已证实生物机制。

### 2.4 可检验的数学接口（假说模型，非生物事实）

观察视觉信号 `v_t`，动作 `a_t`，目标 `g_t`，隐状态 `h_t`，环境外部扰动 `d_t`；设 

- 观测生成：`v_t = R(a_{<t}, h_t) + d_t + eps_t`（仅为工作近似，实际视觉信号为非线性图像变换）。
- H-F：`a_t = pi_theta(v_<=t, a_<t, g_t)`。
- H-D：`z_t = Opp(v_<=t)`，`a_t = pi_theta(z_t,g_t)`。
- H-P：`rhat_t = P_theta(a_<t,h_t)`，`z_t = phi(v_t-rhat_t)`，`a_t = pi_theta(z_t,g_t)`。

关键的可识别比较是同时操纵 `(自运动预测有效/失效) × (外部扰动有/无) × (视觉-动作时延) × (视觉对称性)`，产生三种模型不同的**神经响应、行为转向或闭环稳定性预测**。仅拟合已有开环转向曲线不能识别 H-P。

### 2.5 重要解剖边界

Flyvis 的视叶模型、FlyWire/optic-lobe 连接组、2026 brain-and-cord connectome、2025 视觉去抑制论文的回路与 FlyGym 的具身仿真**不是同一份整合数据集**。必须记录每个轴的物种、雌雄、成虫/幼虫、脑区、细胞身份映射、记录环境、采样频率及采集/处理过程。

如无法建立输出细胞与行动命令回路的可信跨数据映射，只可声称 `visual computation module + behavioural decoder`，不能声称真实完整的 connectome-to-action 因果链。

---

## 3. WP0：决定生物实验是否真的可做（第一优先、低成本）

**目标**：在模型拟合前证明至少有一项独立生物结局 *可取得、可追溯、可解释*。本阶段不检验哪个模型更强。

### 3.1 已核实的公开入口（不等于已经检查字段匹配）

| 来源 | 可确认内容 | 本项目允许的角色 | 目前尚未核实 |
|---|---|---|---|
| flyvis 官方仓库 | 预训练连接组约束视觉模型、定制刺激、神经响应研究工具 | 感觉端模拟基线与信息提取 | 与具体转向动物实验的数据键/时序一致性 |
| FlyGym 2.x | 视觉、具身移动和闭环仿真；2026 年 API 重大改版，旧版不兼容 | 工程仿真与任务/预算基线 | 是否能不修改生物接口即得到所需动作读数 |
| Erginkaya et al. 2025 数据/代码 | 公开 Zenodo 数据、GitHub 预处理与分析，含视运动、细胞调控、转向相关实验 | 生物真值可行性检查、已知机制 baseline | 文件级是否具备逐动物、逐 trial 的共同 stimulus/activity/behaviour 键 |
| 2025 Dryad `10.5061/dryad.kkwh70sgw` | 有处理后的神经影像与行为序列；总体约 214 GB，另有约 1.19 MB 处理后行为文件 | 低成本样本字段探测，可能的生物 held-out 验证 | LC15 是否直接反映本研究定义的转向机制；各文件是否配对 |
| 2022 Dryad `10.5061/dryad.h44j0zpp8` | 视觉与运动状态影响特征编码，约 53 GB | 候选交叉任务和行为状态对照 | 与本项目干预条件/同一动物读数是否满足 |
| 2026 BANC brain-cord connectome | 脑与神经索的结构数据及分布式控制分析 | 连通途径候选和回路限制 | 与不同个体的活动及因果实验是否能合法外推 |

**资料获取策略**：先读公开 README、文件清单、格式/metadata 和小型处理文件，不预下载 50–200 GB 大包；先证实必要字段存在，再下载对应分片。严格版本绑定、许可审计；不得将第三方全文重新公开到仓库。

### 3.2 逐数据集填写的 `BIO_DATA_ELIGIBILITY.csv` 字段

`dataset_id,source_url,doi,version,license,organism,sex,age_stage,neural_region,cell_identity_resolved,stimulus_present,action_present,behaviour_present,perturbation_present,animal_id,session_id,trial_id,timebase,heldout_possible,used_in_source_paper,redistribution_allowed,accessible_bytes,eligible_reason,provenance_sha256`。

### 3.3 G0 硬门

- **G0-A（启动生物计算）**：至少找到一个完整 `stimulus → neural response` 数据路径，以及一个完整 `stimulus → action/behaviour` 路径；若不同动物/来源，明确不把二者伪称配对。
- **G0-B（Nature 旗舰资格）**：找到具有独立样本、独立干预或新合作方可采集的**前瞻生物验证**路径，能区分至少两个竞争机制；否则仅授权 `COMPUTATIONAL_PILOT`，不能声称 Nature 旗舰主结果已经可行。
- **G0-C（解剖）**：合法、科学可辩护的细胞类型/连接来源/神经区域对应。不满足则缩小机制主张。
- **G0-D（近邻）**：完成 2024–2026+ 文献逐项排重，不存在完全等价的刺激×机制×结果主实验。

**停止条件**：若没有独立生物干预或神经活动结局且无潜在合作方，暂停 Nature 主刊确认研究；保留成体系计算/方法论文路线。不能以模拟动物替代真实生物确认。

---

## 4. WP1：生物端的可区分机制预测（AI → Biology）

### 4.1 先冻结、后揭盲

1. 用已经公开的训练/开发刺激确定观测尺度和基本反应指标，但不能看确认动物/确认刺激结果。
2. 预先提交三模型（H-F/H-D/H-P）的原始模型参数哈希、预测表、允许的拟合程序及确定性处理方式。
3. 对每个预选细胞类型与行为读数写出 `stimulus × intervention -> predicted sign, latency, effect magnitude interval, model_disagreement`。
4. 为其中区分度最高但不属于原论文已验证的刺激/干预，要求**新的动物观测或真正未用于任何模型开发的独立记录**。
5. 一次性揭盲分析；额外发现作为探索，不倒填确认假说。

### 4.2 推荐正交操纵（依数据/伦理/设备可用性裁剪）

- 视觉：共同平移光流 vs 左右差分旋转光流，速度与对比度分层。
- 动作：动物主动转向、被动视觉回放/重播、预期动作与实际反馈错配。
- 时序：视觉反馈人为延迟与相位扰动，保持刺激功率/总能量匹配。
- 生物干预：在满足细胞特异性时，对目标回路进行沉默/激活及 sham；需要遗传线特异性、动作能力和视觉能力的 off-target 检查。

**必须注意**：真实动物的“主动 vs 被动”会引入状态、注意与唤醒等协变量；预先记录速度、姿态、目标任务与运动强度，同刺激并不等于同内部状态。

### 4.3 生物端主终点候选（WP0 后只能选择一项确认主终点）

- `neural_response`：指定细胞类型的 stimulus × intervention 交互效应及其时间曲线；独立动物为统计单位。
- `steering_response`：左右转向的反应方向、幅度与时间常数，或扰动恢复的预定义行为指标。
- `model_discrimination`：确认数据对于 H-P vs H-D/H-F 的 out-of-sample predictive log likelihood 差值，并提供动物级不确定性。

**推荐主终点**：一个预先明确的 `intervention × sensory-feedback condition` 交互，以及它对两种竞争机制的辨别能力。**神经与行为**两类读数至少一类为独立确认，另一类能独立验证则主刊竞争力明显更强。

### 4.4 优先的生物验证级别

`B0` 仅公开文献重述 → `B1` 独立公开数据 held-out 预测 → `B2` 新动物/新 session、盲法生理验证 → `B3` 新动物的随机干预与行为/神经响应联测（强证据）。Nature 强主张应争取 B3；B1 不自动升级为 B3。

---

## 5. WP2：人工系统中的机制识别与迁移（Biology → AI）

### 5.1 独立任务集

- **Task-A：视觉运动下的稳定转向**，含平移+旋转混合、自运动回馈、扰动恢复。
- **Task-B：延迟感知下的导航**，视觉延迟、遮挡与控制噪声变化。
- **Task-C：新领域任务**（例如摄像头移动的目标追踪、低维机器人转向或另一运动控制设置），必须不是 Task-A 图像内容的简单重采样；如依赖真实机器人另行核实设备与数据。

任务 C 是跨用途检验，不要求用生物学参数生搬硬套到机器人。提前定义信息映射 `sensor, reafference proxy, action history, goal, intervention`。

### 5.2 需要公平比较的控制组

| ID | 比较器 | 检验的替代解释 |
|---|---|---|
| C0 | PID / Kalman 或恰当的经典状态估计+反馈控制器 | 不是深度学习本身带来的优势 |
| C1 | GRU / LSTM 同观测同动作历史 | 通用循环记忆解释结果 |
| C2 | LTC/CfC 或通用连续时间模型 | 连续时间动力学、并非生物特有 |
| C3 | 同计算预算的结构化视觉 opponency/竞争性去抑制 | 已知生物先例能否完全解释 |
| C4 | 生物约束候选计算机制（事前冻结） | 目标模型 |
| C5 | C4 的随机/degree-preserving rewiring、机制符号翻转、时序错位或无反馈版本 | 拓扑、类型和动作耦合的特异性 |
| C6 | 固定同参数量、同训练 token/steps/optimizer search、同输入信息量的通用替代器 | 超参数搜索/容量和数据差异 |

`C5` 的重连必须满足生物映射所需的细胞类型/输入输出约束，既报告稀疏匹配，也报告 degree/type/weight 分布合理匹配的 null；null 不能拥有不同训练起点或明显不同的总输入量。

### 5.3 强制消融和匹配

匹配参数量（在预先规定容差内）、FLOPs、训练样本/更新次数、总调参搜索预算与离线/在线可用信息；至少 5 独立训练 seeds 作为**模型随机性**，不是生物重复。对关键机制实施：动作历史错位、反馈通道切断、观测相位扰动、回路连线重置、受控信息遮蔽。不得拿 oracle 状态模型与普通观测模型直接宣称网络优势。

### 5.4 人工主终点与边界

可从 `(OOD steering error, disturbance recovery time, failures per episode)` 预注册**一个主终点**，另以参数、能耗和延迟作为限制或 Pareto 代价；其余为次要指标。应报告 across-task family 的任务级效应，不能以成千 episodes 代替独立任务设置/随机地图/训练重复。

**关键成功门**：生物约束机制相对 C1/C2/C3/C5/C6 中最强合格对照，超出预先规定的最小重要效应，且在不见任务族维持方向；如果性能改进完全来自任务调参、额外状态或容量，判 `AI_TRANSFER_NOT_ESTABLISHED`。

---

## 6. WP3：双向机制的共同可识别性（旗舰关键）

### 6.1 “共享机制”的联合判据

- **生物端**：针对事前注册机制的干预，对神经活动/行动产生预期方向和时序的影响，并优于主要竞争机制的前瞻预测。
- **人工端**：针对该机制而不是任意容量的匹配干预，造成对应的、独立测得的功能响应变化；不同任务的作用边界可解释。
- **连接层**：定义一个明确中介变量，如 `action-conditioned residual`, `rotation/translation separation index`, `feedback-delay tolerance`，并事先固定生物/人工各自测量映射与允许差异。

不可仅因为两端都出现“改善”“下降”就判机制相同。正确的主张层级依次为：`qualitative analogy` → `quantitative correspondence` → `interventional correspondence` → `jointly predictive mechanism`。

### 6.2 跨系统预测指标（预注册）

对每个扰动 j，先由独立开发数据计算生物与 AI 的机制敏感性签名：

`Delta_B(j) = Y_B(intervention_j) - Y_B(sham_j)`；
`Delta_A(j) = Y_A(intervention_j) - Y_A(matched_control_j)`。

共同机制的核心检验不直接比较任意量纲数值，而对**预先指定的方向、时序特征、相对排序或无量纲响应**建立映射 `M(Delta_A) -> predicted Delta_B`。映射参数只能在开发干预集合拟合，确认干预不能重新拟合。

至少保留一个不用于机制选择的**新刺激族或新干预类**作为 cross-system challenge；否则只是校准，不是预测。

### 6.3 对称失败设计

- 若 Bio 成功 / AI 失败：机制或许解释了神经活动，但不说明有人工迁移价值。
- 若 AI 成功 / Bio 失败：是有效人工技巧，**不是**新生物机制发现。
- 若两者成功 / 映射失败：两个独立结果，**不是**已证实同一计算机制。
- 若都失败：预注册的模型或干预假说被否证，完整公开。

只有联合结果与替代机制区分同时成立，才可讨论 general computational principle。

---

## 7. WP4：独立系统推广与 Route A 的真正角色

### 7.1 第二生物/行动场景必须防止选择偏差

推荐从同一果蝇中**不同回路或行为状态**开始（例如视觉平衡调节 vs 目标导向转向），若数据/人员允许再扩展到另一物种（斑马鱼或线虫），但跨物种解剖和同源性无依据时不做过度映射。第二系统可作为挑战，不可在看到结果后从很多失败系统中挑成功的发布。

### 7.2 Route A 从“审稿表”升级为可实测验证合同

为每个研究结论输出五段记录：
1. `T1_SOURCE`：每项真实解剖与生理事实及允许的身份粒度。
2. `T2_BIO_MATCH`：在未参与拟合的真实活动/行为中是否有定量生物对应。
3. `T2_ATTRIBUTION`：经过匹配的干预与替代模型后，特定计算机制是否被识别。
4. `T3_UTILITY`：独立人工任务的效用、预算、失败率和 matched comparator。
5. `T4_GENERALITY / T5_SCOPE`：在哪些新任务/生物状态成立和论文允许声称的范围。

这是真正整合 Route A 的方式：**使评估合同能够约束实验，实验又能用其成功/失败反证或改进合同**。不是把旧的 58 篇与新的神经元读数放入同一统计模型。

### 7.3 M2A 原历史资产如何进入

原有 `S-only measurable / C not identified`、合成律修正、theory NO_GO 作为研究设计的**已知失败风险**和 Supplementary 的审计案例，不做确认性正结果。若新研究得到不同机制，不将其追认成原合成式的正确版本；新 estimand、新实验、新结论须另建证据链。

---

## 8. 数据分析、统计与预注册规则

### 8.1 独立单位和避免伪重复

- **生物学**：动物是主要独立单位；若跨天/批次不同动物，多层模型显式处理动物、session、trial 和实验批次。细胞、帧、时间点不等于独立动物 n。
- **连接组**：一个动物的 connectome 不能靠多个 cell classes 变成多个独立个体；基于连接组的外推须审查动物与性别差异。
- **AI**：seeds 是训练随机性重复；任务族/环境/传感器变化才是外推单位。多个 clip 非独立任务族。
- **跨系统**：成对扰动比较的单位是机制条件/回路，在 biological animal × AI seed × perturbation 的层级分析；不可对两个系统的原始量纲作无效合并。

### 8.2 先导后功效分析

先做盲法开发 pilot 以估计方差、动物间 ICC、可评估率和主变量方差；随后采用嵌套动物 bootstrap 或混合效应模拟，确定能检出预先声明的**最小有意义效果**所需独立动物数和可执行干预条件数。当前**不得声称 12、20 或 30 只就一定有 80% 功效**。若动物数不够，缩小问题或止步，不以 trial 数填补。

### 8.3 冻结的确认性分析建议

- 生物主检验：层级混合效应模型估计 `intervention × feedback_condition`；动物级 cluster bootstrap CI，同时报告效应大小、扰动效力和 sham 检验。
- 竞争机制预测：比较 prequential / held-out log likelihood 或 proper score；模型复杂度、读数噪声、任务设置标准化。
- AI 主检验：跨未见任务族的 paired performance difference、seed+environment 分层不确定性和预算匹配表。
- 联合检验：两个 co-primary 域均过各自预注册门，且 cross-system 挑战预测达到事前规定要求。任一失败均不得用探索指标替代；多主要检验控制整体错误率。
- “无差异”不可仅靠 p>0.05 宣称等价；若要声称通用控制足够，需要事前等效界限和 TOST/区间论证。
- 任何缺失/生物实验失败：分开 `NOT_OBSERVABLE`, `TECHNICAL_FAILURE`, `BIOLOGICAL_NULL`, `MECHANISM_CONTRADICTED`；不得把不可用数据按 0 填。

### 8.4 确认与探索隔离

探索可发生但必须在新 branch/new dataset，所有关键提名都绑定之前的发布日期、sha256、随机种子、动物名单与解封时间。用完全新的动物、记录批次或预留刺激集做最终判决。看到最终结果后不准更换 primary endpoint、阈值、对照或机制定义。

---

## 9. 六道 Nature 级硬门与分流

| 门 | 必须证实 | 未通过的动作 |
|---|---|---|
| **G0 数据** | 真实生物刺激/神经/行为输入，独立干预或合作实验路径，合法可访问性 | 停 Nature 旗舰确认；仅计算 pilot |
| **G1 新颖性** | 相对 flyvis/FlyGym/Erginkaya/BANC/FlyHack/FlyGM 有预先书面列出的**非重合**新问题 | 重选具体机制或停止 |
| **G2 预测** | 在看目标生物结果前冻结多个竞争机制的不同预测，独立神经/行为数据可以判别 | 停机制发现叙事；不挑成功案例 |
| **G3 人工** | 匹配最强通用对照和机制 null，独立任务迁移有可归因且重要的作用 | AI 转移不成立；保留生物机理稿或负结果 |
| **G4 联合** | 生物干预效应与 AI 干预预测形成可量化的**跨系统一致性**，并支持一个未见扰动/状态 | 不声称共同机制与 Nature 完整故事 |
| **G5 科学/投稿** | 独立人类复核、论文重合和数据许可、人类伦理/动物实验审批、可复现包、作者/审稿披露、真实新发现足够广泛 | 不标 `NATURE_READY`；按实际结果分流 |

特别说明：科研可能证明一个“强而有边界的负结果”，但其是否达到 Nature 主刊的重大科学意义仍需另做跨领域外部评估；不会因其是负结果就自动达到或不达到。

---

## 10. 实际人员、资源与成本：分阶段而非一次性砸预算

| 阶段 | 人员最低配置 | 主要硬件 | 支出与风险控制 |
|---|---|---|---|
| WP0（资格） | 1 计算 lead、1 神经科学顾问或共同作者、1 数据/协议审计者 | 普通电脑；访问公开元数据 | **优先零 GPU 重训**；不下载全部原始数据 |
| WP1 开发模拟 | 1–2 计算研究员、1 机制评审 | 一张 8–16GB GPU 或租用短时服务器，视 flyvis/flygym 实测要求 | 先做预训练模型与简化回路；设 GPU-hours 上限、日志化训练次数 |
| WP1 真正生物验证 | 果蝇生理/行为合作实验室、实验与统计人员 | 成像/电生理/光遗传/闭环行为设备由合作方提供 | **没有实验室，就不能承诺有新的生物干预数据**；独立公开数据是较低证据等级 |
| WP2 AI | 1–2 机器学习研究员 | 根据基线实测升级 GPU；算力预算按 C0–C6 调参分配 | 预注册参数与训练预算，不只给候选机制更多训练 |
| WP3–WP4 | 生物与计算各有独立负责人；第三方盲审与复算 | 合作实验与计算服务器 | 根据 G2/G3 是否通过决定是否扩展第二生物系统 |

**关于 FlyGym**：2026 年 FlyGym 2.x 是重写 API，与 1.x 不兼容；不能照旧版 tutorial 混用。关于 flyvis 的训练规模和内存占用，必须先运行单个 30–60 秒 profiler，再填写资源表，不能预言某型号显卡保证跑完全量。

### 时间计划（仅项目规划，不是执行承诺）

- **第 0–2 周：** WP0 元数据+最新先例+rights，定 1 个可识别 primary bio mechanism，`G0/G1`。
- **第 3–6 周：** 预训练 flyvis + FlyGym 低成本 pilot，机制竞争预测表，统计与功效计划；未过 `G0` 不训练昂贵模型。
- **第 2–4 月：** 开发数据、冻结并交付独立生物预测；启动合作方伦理审批/遗传线与刺激校准。
- **第 4–10 月：** 新生物 session/动物与随机干预；AI 公平对照，分支间盲法；不满足功效与伦理则延后或停止。
- **第 10–15 月：** 未见刺激/环境与必要的第二证据家族、独立复算、挑战评审。
- **第 15–18+ 月：** 若 G0–G5 有科学支持，准备 *Nature* Article、预投稿询问及审稿复现包。**这是高目标的资源规划区间，实际完成时间高度依赖实验室，不构成保证。**

---

## 11. 完整提交包：新仓库规范

```
M2A-BRIDGE/
  00_CHARTER_AND_SCOPE.md
  01_PRIOR_ART_AND_NOVELTY_MATRIX.csv
  02_DATA_FEASIBILITY/
    BIO_DATA_ELIGIBILITY.csv
    CROSS_SOURCE_IDENTITY_MAP.csv
    RIGHTS_AND_LICENSE_LEDGER.csv
    DATA_ACCESS_REPORT.md
  03_THEORY/
    MOTION_ACTION_OBSERVABILITY.md
    COMPETING_MECHANISMS_v0.md
    COMPETING_PREDICTIONS_FROZEN.csv
    ASSUMPTIONS_AND_FAILURES.md
  04_BIO/
    PILOT_ONLY/
    CONFIRMATORY_PROTOCOL.md
    EXPERIMENT_RANDOMIZATION.csv
    RAW_DATA_POINTERS.csv
    INTERVENTION_TARGETS.csv
    BIO_MODEL_REPORT.json
  05_AI/
    TASK_REGISTRY.csv
    BASELINE_MATRIX.csv
    MATCHING_AUDIT.csv
    TRAINING_RUN_LEDGER.csv
    OOD_EVAL_CONTRACT.md
    AI_MODEL_REPORT.json
  06_JOINT/
    VARIABLE_MAPPING.csv
    INTERVENTION_PREDICTIONS.csv
    CROSS_SYSTEM_TEST_REPORT.json
  07_AUDIT/
    T1_T5_EVIDENCE_LEDGER.csv
    HASH_MANIFEST.json
    DECISION_AND_AMENDMENT_LEDGER.md
    INDEPENDENT_RECOMPUTATION.md
  08_MANUSCRIPT/
    FIGURE_CONTRACTS.md
    CLAIM_TO_EVIDENCE_MAP.csv
    MANUSCRIPT_DRAFT.md
    SUPPLEMENTARY_INFORMATION.md
    RIGHTS_AUTHORS_AND_OVERLAP.md
  GATE_STATUS.yaml
```

所有 CSV 建立 schema 与跨文件 ID 断言，model report 具备自动校验的科学单元 `animal`, `session`, `environment`, `seed`, `perturbation`, `source_version`。报告脚本必须允许读者从保存的许可数据/可重新获取来源重算，不能依赖原作者机器上的绝对路径或不可分发的论文全文。

### 11.1 第一轮可交给 Agent 的精确任务（限于资格与先导）

> **ASSIGNMENT M2A-BRIDGE/P0**  
> 目标是识别可独立检验的生物机制预测，不得训练确认模型或宣布新自然规律。  
> 1. 阅读 M2A 和 Route A 冻结权威记录，分别制作 evidence boundary 表，不更改两个原项目。  
> 2. 核对本文近邻论文和代码发布日期，提供论文 DOI、code commit、数据 DOI、文件大小与许可证；只记录已核实信息。  
> 3. 为 flyvis、FlyGym 2.x、Erginkaya 2025 数据、BANC 2026，以及一个可用的小型行为数据集制作身份/时基/刺激/行为/干预匹配审计。  
> 4. 定义 H-F、H-D、H-P 的至少三条互相不同且能够通过公开数据/未来生物实验判别的预测，包括测量单位、符号、时间尺度和 null。  
> 5. 运行**一次**最小 flyvis/FlyGym smoke test，保留版本、运行时、显存、CPU/RAM、断言结果；即使 API 不兼容也记 FAIL。  
> 6. 形成 `G0_G1_FEASIBILITY_DECISION.md`，唯一允许状态 `GO_PILOT / GO_CONFIRMATORY_PENDING_LAB / NO_GO`，并列出 owner 必须补齐的人类实验资源。  
> 禁止：把可下载当成同动物配对；把公开既有机制重述称为新发现；因先导结果强行更换主机制；更改历史结果或复制未获授权的第三方全文；擅自标 `NATURE_READY`。

### 11.2 首轮最重要的交付验收

- 最少两种竞争机制已经写出**不会因任务成功与否而自动成立**的可证伪预测。
- 至少一个生物数据源字段实际可读；记录具体 key、shape、物种/动物/刺激/神经读数、时间单位、缺失和许可证。
- 一份明确的 `NEURAL_ACTIVITY_PRESENT` 与 `BEHAVIOR_PRESENT` 状态表，不能默认两者同动物。
- 一份生物合作需求表：最少的基因/细胞类群、干预方法、动物数功效前置参数、实验时间窗与盲法。
- 对比文献写出**我们比各前例多验证什么**，每项必须是可实验检验的差异。
- 如 G0 失败，保持 `NO_GO_FOR_NATURE_CONFIRMATORY`，而非把模拟输出当做成功。

---

## 12. 论文架构（科学结果未知，仅作为因果叙事的框架）

候选结果导向题名，**不能在看到确认结果前强行确定**：

- `From neural motion processing to action: a bidirectional test of shared computational mechanisms`
- `When does a neural circuit mechanism transfer to artificial action?`
- `Predicting sensorimotor interventions across biological and artificial neural systems`

候选 Nature 主文六图（实际按 Nature 版式调整）：

1. Fig 1：生物 → AI → 生物的机制假说与真正独立证据路径，含数据身份边界。
2. Fig 2：竞争性机制在神经活动、行为与动作-视觉错配下的可区分预测。
3. Fig 3：独立果蝇新数据与生物干预，按**动物**而非 trial 统计。
4. Fig 4：相同信息、参数、计算预算的 AI 机制迁移与通用比较器，在 OOD 任务中测试。
5. Fig 5：预先冻结的跨系统扰动响应、模型反证与机制共同解释力。
6. Fig 6：第二任务/回路、失败边界与普遍性，Route A 证据合同用于限定 claim。

M2A 旧结果与 Route A 旧 58 条审计放入 Methods/SI 的*provenance and motivation*，**不做为这些新图的独立确认材料**。如果没有 Fig 3 的真实新生物验证以及 Fig 5 的跨系统机制连接，不能靠其他图填补。

---

## 13. 最新外部来源与核验入口（2026-10-27）

1. Nature Article 格式与标准：https://www.nature.com/nature/for-authors/formatting-guide ；https://www.nature.com/nature/for-authors/initial-submission
2. Lappalainen et al. 2024，flyvis：https://doi.org/10.1038/s41586-024-07939-3 ；https://github.com/TuragaLab/flyvis
3. Wang-Chen et al. 2024，NeuroMechFly v2：https://doi.org/10.1038/s41592-024-02497-y ；https://github.com/NeLy-EPFL/flygym
4. Westeinde et al. 2024，goal-to-steering：https://doi.org/10.1038/s41586-024-07039-2
5. Erginkaya et al. 2025，competitive disinhibition：https://www.nature.com/articles/s41593-025-01948-9 ；https://doi.org/10.5281/zenodo.14967806 ；https://github.com/ChiappeLab/Erginkaya_et_al_2025
6. Bates et al. 2026，BANC brain-and-cord：https://www.nature.com/articles/s41586-026-10735-w
7. 2025 视觉连接组：https://www.nature.com/articles/s41586-025-08746-0
8. Dryad visual distance/LC15：https://doi.org/10.5061/dryad.kkwh70sgw
9. Dryad visual & motor dynamics：https://doi.org/10.5061/dryad.h44j0zpp8
10. FlyHack (2026 preprint)：https://arxiv.org/abs/2610.13018
11. Topological Sensitivity (2026 preprint)：https://arxiv.org/abs/2604.04033
12. FlyGM (2026 preprint)：https://arxiv.org/abs/2602.17997
13. ConnectomeX / FlyVision (2026 preprint)：https://arxiv.org/abs/2610.08418

引用既有研究必须核对预印本与正式发表状态；预印本不能因为现在声称了某个优势就视为独立证实。上述链接支持项目起点与新颖性风险，并**不证明本项目已有新发现**。

---

## 14. 最终状态与可以立刻执行的决策

```
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

**Owner 现在可以批准 WP0/P0 的低成本可行性核验，不等于批准 WP1–WP4 的确认性实验。** 唯一必须尽早解决的人力问题，是能否与果蝇神经生理/行为实验室合作，取得独立干预数据；没有该路径就不能向 Nature 主刊强行保证双向机制结论。

**评价成功的方式不是“做完所有步骤”，而是让多个竞争机制在真实生物数据和独立人工系统中接受相同思想的反事实检验，并允许事实淘汰自己的假说。**
