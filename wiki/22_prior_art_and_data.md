# 先例与数据入口

> 来源：master protocol §2.2、§3.1、§13。所有链接都需要在 P0 重新核对发表状态、版本与许可证。
> 关键提醒：**“可下载”不等于“字段匹配”，也不等于“可以配对”。**

## 1 已覆盖的先例

| 先例 | 已实现 | 对本项目的含义 |
| --- | --- | --- |
| Lappalainen et al., *Nature* 2024（flyvis） | 连接组约束视觉模型、任务优化、结构消融、神经数据比较 | 不能重复“flyvis 能预测细胞响应”作为新发现 |
| Wang-Chen et al., *Nature Methods* 2024（NeuroMechFly v2 / FlyGym） | 视觉、运动、具身闭环任务 | 不能重复“具身仿真平台”本身 |
| Westeinde et al., *Nature* 2024 | PFL 类群把方向 / 目标信号变成转向命令 | 转向回路已有生理、成像、干预 |
| Erginkaya et al., *Nature Neuroscience* 2025 | 竞争性去抑制提高旋转光流选择性 | H-D 若再现只算 baseline reproduction |
| Bates et al., *Nature* 2026（BANC） | 脑-神经索完整连接组、分布式局部感觉运动反馈 | 连接组到行动的强先例 |
| FlyHack（arXiv 2026） | flyvis 模型、干预、拓扑对照 | “消融后有差异就是新机制”不新 |
| Topological Sensitivity（arXiv 2026） | flyvis 拓扑敏感性 | 同上 |
| FlyGM（arXiv 2026） | 全脑连接组图控制具身果蝇 | “把连接组放进控制器”不新 |
| ConnectomeX / FlyVision（arXiv 2026） | 连接组启发视觉网络跨任务应用 | 仅在分类数据集改善不新 |
| Kim et al., *Nat. Neurosci.* 2015 | HS/VS 接收 sign/latency 合适的 motor-related input，抵消自运动视觉流 | **H-P 已有直接生物证据**；“发现 efference copy”不能作为新意 |
| Hartman et al., *Curr. Biol.* 2025 | LT52 在 grooming 中接收肢体运动反馈，抑制自体动作引起的转向 | H-P 在第二个行为中成立；仍非跨系统模型 |
| Zenodo 23018266（2026-09） | FlyGym 中单侧 DNa01 消融产生 38.19±10.83°/s 转向，与在体光遗传一致；20 个 degree-matched null 中 0 个复现 | **最接近的跨系统运动消融先例**；但它只测运动回路，不测视觉 reafference |
| arXiv 2610.33881（2026-10） | 未训练 brain-VNC 连接组驱动身体，导航成功率 95% vs rewired twin 18% | 全脑具身行为先例；无视觉 reafference 操纵 |
| Digital Sphinx（bioRxiv 2026） | 线虫连接组驱动果蝇身体也能产生逼真行走 | 行为逼真≠生物逼真；必须做 null/rewired 对照 |
| Vaxenburg et al., *Nature* 2025 | flybody 全身物理仿真与 RL 运动 | 非连接组约束；作为身体/任务基线（DOI 待核） |
| Shiu et al., *Nature* 2024 | FlyWire 计算脑模型复现 sensorimotor 处理 | 全脑模型基线（DOI 待核） |

**唯一可竞争新增点**：同一个事前定义的计算变量 / 干预，对**先前不可见的生物-行动结果**和**独立 AI 行为结果**形成联合、能排除替代模型的预测。

## 2 数据入口（字段级未核验）

| 来源 | 可确认内容 | 本项目允许角色 | 尚未核实 |
| --- | --- | --- | --- |
| flyvis 官方仓库 | 预训练连接组约束视觉模型、定制刺激、神经响应工具 | 感觉端模拟基线与信息提取 | 与具体转向动物实验的数据键 / 时序一致性 |
| FlyGym 2.x | 视觉、具身移动、闭环仿真 | 工程仿真与任务 / 预算基线 | 能否不改生物接口就得到所需动作读数 |
| Erginkaya et al. 2025（Zenodo + GitHub） | 视运动、细胞调控、转向相关实验数据与预处理 | 生物真值可行性检查、已知机制 baseline | 是否具备逐动物、逐 trial 共同的 stimulus / activity / behaviour 键 |
| Dryad `10.5061/dryad.kkwh70sgw`（2025） | 处理后神经影像与行为序列；约 214 GB，另有约 1.19 MB 处理后行为文件 | 低成本字段探测、可能的 held-out 验证 | LC15 是否直接反映本研究定义的转向机制；文件是否配对 |
| Dryad `10.5061/dryad.h44j0zpp8`（2022） | 视觉与运动状态影响特征编码；processed 约 53 GB，含 HDF5 响应 + 行走 tracking | **最理想的同动物视觉+神经+行为候选** | 下载被 Dryad 登录拦截（401/403）；字段级核验待访问 |
| Rayshubskiy 2025 / Dataverse `10.7910/DVN/0NCLP1` | 380 个 `.mat`，157.9 GB；同动物 stimulus + DNa01/02 ephys + yaw/fwd/lat | action→neural→behavior 的强候选 | `stim` 是二值光遗传/嗅觉事件，不是视觉光流；不能单独检验 H-P 的视觉自运动预测 |
| Hartman 2025 / Zenodo `15530926` | LT52 钙成像 + 行为，2.3 GB，CC BY 4.0 | H-P / reafference 的第二行为证据 | grooming 任务，不是光流转向；无 AI 对应 |
| BANC 2026 brain-cord connectome | 脑与神经索结构数据、分布式控制分析 | 连通途径候选和回路限制 | 与不同个体活动及因果实验能否合法外推 |

## 2.1 P0 实测（2026-10-27）

- 已下载 Rayshubskiy `dual_13.mat`（71 MB，SHA-256 `a460eb31…`）：`stim` 二值 {0,5}，`ephys_A/B` 5.75M @ 10 kHz，`yaw/fwd/lat` 57.5k @ 100 Hz，575 s，同时间基。
- 已用 HTTP Range 从 Erginkaya 23.5 GB zip 读取 1 个 HS 文件（2.37 MB）：`DFF (2,78,48)`，48 trials × 78 timepoints × 2 ROIs，`StimNames/Speeds/OFPatterns` 完整；行为在独立文件。
- Dryad Turner 数据下载返回 401/403；需要登录或作者镜像。
- 结论：G0-A `PASS_WITH_CAVEAT`；G0-B `FAIL_NO_LAB`；决策 `GO_PILOT`。

**状态**：`BIO_DATA_FIELD_LEVEL_ELIGIBILITY = NOT_VERIFIED`。P0 的任务就是把它变成逐数据集、逐字段的证据。

## 3 资料获取策略

1. 先读 README、文件清单、格式 / metadata、小型处理文件；
2. 确认必要字段存在后，再下载对应分片；
3. 不预下载 50–200 GB 大包；
4. 严格版本绑定、许可审计；
5. 不把第三方全文或受限数据重新公开到仓库。

## 4 `BIO_DATA_ELIGIBILITY.csv` 必填字段

```text
dataset_id, source_url, doi, version, license, organism, sex, age_stage,
neural_region, cell_identity_resolved, stimulus_present, action_present,
behaviour_present, perturbation_present, animal_id, session_id, trial_id,
timebase, heldout_possible, used_in_source_paper, redistribution_allowed,
accessible_bytes, eligible_reason, provenance_sha256
```

每个数据集一行；`eligible_reason` 必须写“为什么这个数据集能或不能支持某个具体预测”，不能只写“可用”。

## 5 关键工程注意

- **FlyGym 2.x 是重写 API，与 1.x 不兼容**；不能照旧版 tutorial 混用。
- flyvis 的训练规模和显存占用必须先跑单个 30–60 秒 profiler，再填资源表；不能预言某型号显卡保证跑完全量。
- 身份映射必须记录物种、雌雄、成虫 / 幼虫、脑区、细胞类型映射、记录环境、采样频率、处理流程。
- 若无法建立输出细胞到行动命令回路的可信映射，只能声称 `visual computation module + behavioural decoder`。

## 6 权利与合规

- 第三方数据 / 全文按原许可使用；仓库只放可再分发部分或获取脚本 + 哈希清单。
- 动物实验需伦理 / 审批；涉及人类数据另论。
- 论文重合、作者贡献、数据许可在 G5 前单独审查。
