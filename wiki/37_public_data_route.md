# D8 公开数据路线（P0–P4）

> 2026-10-28 起的主路线（owner 指令，决策记录见 [40 决策日志](40_decisions_and_risks.md) D8）。
> 与 Track C 计算稿的关系：**并行分支**——Track C 作为可独立投递成果保留；本分支用公开真实数据做机制识别与反向检验。
> 不变的纪律：无独立生物证据前，任何计算预测不得称为"已验证的生物学机制"；每轮仍走门禁流程。

## 路线

**真实公开生物数据 → 计算机制识别 → AI 迁移 → 独立公开生物数据反向检验**

| 阶段 | 内容 | 通过条件 | 当前状态 |
| --- | --- | --- | --- |
| P0 数据资格审计 | 字段级核验 OSF 与两份 Dryad | 有可用于模型预测的独立真实行为结局 | **进行中**：见 [审计报告](../M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/AUDIT_REPORT.md)——D1（Cubico2023/OSF）空壳 `BLOCKED_FILES_MISSING`；**D2（Dryad 26.6MB）已由 owner 下载并完成字段级审计 → `QUALIFIED_BEHAVIORAL`**（50 Hz 闭环转向、逐蝇逐试次 H/dH、风/触角条件；无本体感觉操纵与延迟维度）；**D3（13.8GB, Tanaka/Clark CB 论文）已下载并完成字段级审计 → `QUALIFIED_NEURAL_AND_BEHAVIORAL`**（T4/T5、LPTC、Mi4 成像 + 逐细胞类型筛选 + 行为，同管线；stationarity 反证据刺激可参数化；无延迟维度） |
| P1 基础复现 | 来源模型零延迟行为 + 2025 更新版核对 | 解释排序差异 | **已关闭**：eLife 93487 V2（2025-08-20 改题）核实为同 DOI 稿件更新；`nisl-hyu/flightsim` 代码自 2024-08-05 零变更（本地审计副本 == 远端 HEAD `02515aad`），"基础实现差异"风险低 |
| P2 等信息经典控制对照 | 同等观测/动作历史下与 PD/PID、观测器、Smith predictor、MPC、GRU 比较 | 优势非单纯信息可用性 | **第一阶段完成**：P1-EC-OBSERVER-01——平凡 Taylor 估计器（只用延迟观测）不能替代新鲜 self-state（50 ms 起 50–100% 失败 vs current 的 0%）；完美内部模型未测（已在稿件 Limitations 声明，claim C37）。后续经典控制器族对照在 P3 数据到手后再扩 |
| P3 公开数据验证 | 冻结预测 → 未用于开发的动物/条件检验 | 预定义指标优于合理对照 | **第一轮已完成（P3-VISORIENT-01，confirmatory）**：在 m715hp3 上检验"风载荷↑转向间歇性、消融组增量更大"的可迁移预测（预注册 + 修正案 A1 均冻结于结局前；两次实现 bug 修复留痕）。结果：交互 +2.81（方向一致）但置换 p=0.128 → 按预注册规则记为**预测未获支持**（有限样本方向性证据）；hump 次要指标方向不一致；exp4h 复现集方向一致（median Δ +7.25）。**D9 审计更正（2026-10-28）**：组名正确表述为 antenna-stabilized（UV 胶固定触角，阻断风感），此前"消融"用语错误（`runs/P3-VISORIENT-01/AUDIT_ADDENDUM.md`）；本轮维持 `INCONCLUSIVE` 封存，机制解释只到"触角风感输入"层面，不涉本体感觉。**注意**：三份候选数据都未操纵 self-state 延迟，20–30 ms 阈值无法直接验证。**第二候选已探索（P3-CE-EXPLORE-01，exploratory，2026-10-28 门禁 pass）**：Tanaka fig3 sweeps 的 preprocess 移植完成，逐蝇 turnmat 冻结为 `runs/P3-CE-EXPLORE-01/experiment/outputs/turnmat_fig3.npz`（SHA-256 `f04f22b4…93ce`，19/20 蝇）；候选判别量（双峰系数、LFO-CV Hill）在 n=19 下判别力有限，确认性设计（P3-ROUND-2：参数自助零分布 + 功效声明 + 解读边界）见该轮 `EXPLORATION_REPORT.md`，待 owner 批准后冻结预注册。**确认性轮已执行（P3-ROUND-2，2026-10-28，owner 批准后冻结预注册再跑）**：嵌套 LFO-CV ΔRMSE=−0.091，p=0.534，按冻结规则记 **did_not_distinguish + INCONCLUSIVE_BY_RESOLUTION**（最低可检测效应 0.454；逐蝇胜负 9:10）；次要终点双峰系数无两态证据（Holm p=1.0，CI 宽）。探索轮粗网格差（−0.54）经精化拟合后消失——是拟合伪差非稳健信号。**该行为级模型选择线在 n=19 下无结论，不作任何方向主张**。**神经臂探索（P3-CE-FIG4-EXPLORE-01，2026-10-28）**：T4/T5（13/15 蝇）对外部静止棋盘平均抑制≈0（与原论文"抑制不在 EMD 层"一致，锚定管线正确）；闪烁抑制存在（+0.6~0.75）；`neural_integ.npz` 冻结（`5a394ef8…cc7f`）。**D10/D11 阶段（2026-10-28，权威记录见 wiki/40）**：LPTC 降为负对照/机制边界（原论文已证抑制不在该层）；P3-A 三分支基准复算 PASS（Mi4 逐值 r=1.0）；新增并行候选 Fischer & Schnell 2022（EDMOND doi:10.17617/3.92，N=13，同步 HS 膜电位+WSA，无神经干预轴）为优先线 P3-F；fig1_05_onset 单调预测被 owner 否决（T1 映射：666/500 ms 两延迟与批次+运动时长三重混淆，只能做视觉整合探索判别 P3-T）；H0/H1/H2+时间核/泄漏积分/状态空间竞争模型族已预冻结（`09_P3_MECH_IDENT/COMPETING_MECHANISMS_PREREG.md`）；当前裁决 `CONDITIONAL_GO`，Nature 确认性生物检验未授权 |
| P4 双向迁移 | 通过验证的机制迁移到人工控制任务 | 可重复、机制特异的收益 | 未启动 |

## 关键边界

- 三个候选数据集的原论文结论不是我们的新发现；只有独立建模 + 留出验证 + 排除替代解释后才可能产生新知识。
- Nature 门槛：NOT READY（owner 判断，2026-10-28）；若 P2/P3 显示只是普通状态反馈优势，就如实保留计算成果，不为旗舰无限扩充。

## 需要 owner 的动作

1. ~~浏览器下载 Dryad `m715hp3~~ 已完成（2026-10-28）。仍需：OSF/CB 数据声明核查（D1）。
2. OSF 7mq9j 空壳：查 Current Biology 数据可用性声明或联系作者。
3. Track C 审稿意见与投稿元数据（并行推进）。
