# 变更日志

> 只追加，不删除。每条写：日期、变更、依据、影响。
> 每轮实验结束必须在此追加一行，并链接 `runs/<round_id>/experiment_log.md`。

## 2026-10-27

- 读取 `~/Downloads/M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md`（v1.0，立项候选），并复制为工作区根目录的 `M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md`；SHA-256 `2a9422480fc1a65e9961f7199a77505ac7d7f197a0cdf18f3ba32f817fdf146e`。
- 建立项目级 `CLAUDE.md`：每轮“代码 → debug → 门禁 → 实验 → 核验 → wiki”规则。
- 建立 `PROCESS/ROUND_PROTOCOL.md`、模板与 `PROCESS/round_gate.py`；门禁自测通过（pass / blocked 两条路径）。
- 建立本 wiki：两个冻结历史项目、M2A-BRIDGE 总体、门禁与统计、先例与数据、流程、P0、决策与风险。
- 当前状态未改变任何冻结资产；M2A-BRIDGE 仍为 `PROPOSED_NOT_PREREGISTERED`。
- **P0 执行（2026-10-27）**：核验 18 条近邻（含 Kim 2015、Hartman 2025、Zenodo 23018266、arXiv 2610.33881、Digital Sphinx）；实测 Rayshubskiy `dual_13.mat`（71 MB）与 Erginkaya HS 文件（2.37 MB，HTTP Range）；Dryad Turner 下载被 401/403 拦截。
- **P0 决策**：`GO_PILOT`；G0-A `PASS_WITH_CAVEAT`，G0-B `FAIL_NO_LAB`，G0-C `PARTIAL`，G0-D `CONDITIONAL_PASS`，G1 `CONDITIONAL_PASS_NARROW`。
- 产出：`M2A-BRIDGE/01_PRIOR_ART_AND_NOVELTY_MATRIX.csv`、`02_DATA_FEASIBILITY/*`、`03_THEORY/*`、`07_AUDIT/LEGACY_EVIDENCE_BOUNDARY.md`、`G0_G1_FEASIBILITY_DECISION.md`、`GATE_STATUS.yaml`。
- **P0-SMOKE-01（2026-10-27）**：flyvis 1.2.0 + FlyGym 2.1.1 最小 smoke test 通过（round gate pass）；flyvis 连接组 45,669 nodes / 1,513,231 edges；FlyGym 自由体 50 步，qpos/positions finite；RSS ~1.0 GB。全驱动 FlyBody/MusculoskeletalFly 因 `datasets.epfl.ch` TLS 失败，记录 `BLOCKED_BY_ASSET_HOST`。
- **P1-EC-DELAY-01（2026-10-27）**：把 Canelo 2024 的 flight-sim 方程移植为 Python，比较 addition / graded_sensory / graded_motor / allnone 在显式反馈延迟下的稳定性。768 runs × 16 delays；allnone 临界延迟中位 0.25 s、140 ms 失败 2/12；graded_sensory 0.03 s、12/12；addition 0.04 s、12/12；graded_motor 双峰、均值 0.137 s、4/12。结果见 `runs/P1-EC-DELAY-01/experiment/outputs/` 与 [32 计算 pilot](32_ec_delay_pilot.md)。
- **Track C 计算论文草稿（2026-10-27）**：完成 `M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_DRAFT.md`，含摘要、引言、结果、讨论、方法、局限、参考文献、图注；新增 `CLAIM_TO_EVIDENCE_MAP.csv`、`FIGURE_CONTRACTS.md`、`fig1_model.png`、`fig5_gating_signal.png`。目标 PLOS Computational Biology，B0 级，不声称生物机制。
- **P1-EC-DELAY-03（2026-10-27）**：1 ms 细网格（0–100 ms）确认 critical delay 中位数：addition 18 ms、graded_sensory 15 ms、graded_motor 10 ms、allnone_motor 110 ms、allnone 200 ms；1,815 runs。新增 `fig2b_critical_delays.png` 并更新 Track C 稿件数字。
- **阈值与求解器敏感性（2026-10-27）**：`analyze_thresholds.py` 重分类 P3 数据：`|ω|>50` 时 allnone ~56 ms、allnone_motor ~58 ms；`|ω|>100` + heading>2π 时 200 ms vs 110 ms。稳健结论改为“graded 最先失稳”，gating 优势与门控信号差异是判据依赖的。`solver_check.py`：dt 减半，gating 变体差 <0.3%，fast-failing 变体 2–16%（临界区几 ms 不确定度）。
- **零延迟背景增益检查（2026-10-27）**：从 P1 delay=0 数据计算高/低 grating 增益的峰值转向比：addition 0.9148、allnone 0.9830、graded_motor 0.9996、graded_sensory 0.9998。未复现 Canelo 2024 的排序，论文已明确写成“动机引用，不是复制”。
- **源协议检查（2026-10-27）**：`source_protocol_check.py` 用源论文缩放参数 + 恒定 grating + 0.05/0.7 增益。近零门控阈值（1.5e-12）时 allnone 完全不变（59.956 vs 59.956°）；graded 单位增益也不变，EC 增益 0.5 时略敏感（59.923 vs 59.770°）；addition 明显变化（59.846 vs 50.846°）。源论文排序可在窄区恢复，但不是固定增益模型的通用性质。
- **P1-EC-GAIN-01（2026-10-27）**：增益扫描（0–1.0）× 延迟（0.02/0.05/0.10/0.20 s）× 12 参数组，1,440 runs。源增益 0.05 下 graded 与 no-EC 同轨；增益 ≥0.25 时 delayed sensory 在 50 ms 100% 失败（no-EC 75%）；current motor 高增益在 200 ms 把失败率降到 25–33%；gating 不受增益影响（100 ms 前 0%）。论文主线改为“gain × source × gating”。
- **P1-EC-ADAPTIVE-01（2026-10-27）**：复刻源论文的自适应 5-unit MLP（步进近似），12 参数组 × 4 延迟 × 5 模型 = 240 runs。learned ro 从 0.38 升到 1.06；失败率 0.42 / 1.00 / 1.00 / 1.00，50 ms 起比 no-EC 的 0.75 更差；adaptive 没有救回稳定性。固定 0.05 为 0.42/0.75/1/1，固定 1.0 为 0.50/1/1/1，allnone 为 0/0/0/0.5。
- **P1-EC-ADAPTIVE-02（2026-10-27）**：自适应 MLP 的学习率/seed 扫描（α=1e-5..1e-3，3 seeds，576 runs）。所有 α 在 100 ms 前 100% 失败；α≥8e-5 在 50 ms 就 100%，α=1e-5 在 50 ms 与 no-EC 持平（75%）。learned ro 随延迟和 α 上升；没有学习率救回稳定性。
- **Track C PDF（2026-10-27）**：用 pandoc/xelatex 生成 14 页 `MANUSCRIPT_DRAFT.pdf`，嵌入 9 张图；图件统一为 PNG 220 dpi + PDF；自适应 MLP 的学习率/seed 扫描已写入 Results 和图 2e。
- **线性稳定性分析（2026-10-27）**：线性化延迟系统并求特征方程右most根。临界延迟：addition 29 ms、graded_sensory 31/43 ms（gain 0.05/1.0）、graded_motor 300 ms、allnone 门开分支 29 ms。线性分析复现连续 cancellation 失稳量级，但不能区分 gating 与 addition，也不能解释 motor-copy 长延迟收益——主文分离是大信号/非线性效应。新增 `fig6_linear_stability.png`。
- **PDF 重建（2026-10-27）**：加入 Fig. 6（线性稳定性），图注路径改为相对文件名；14 页、10 个 display items。
- **独立三审 + 修订（2026-10-27）**：用 `nature-reviewer` 启动 3 个互盲 reviewer，结论为 major revision。补做 window（2.5/6/10 s）、V-clip、gate-threshold、adaptive signed-gradient 四个实验；确认 100/200 ms gating 主张不成立，source/motor 主张混淆，linear stability 不可靠。重写 `MANUSCRIPT_REVISED.md` 与 10 页 PDF，删除上述主张，保留 gain、短延迟 gating、window/V-mode/threshold 限制和 adaptive 负结果。
- **P1-EC-COMMAND-01（2026-10-27）**：真正的 pre-plant-filter command copy 实验，560 runs（7 模型 × 5 延迟 × 2 增益 × 8 参数组，6 s）。graded command 与 graded filtered 完全同轨（20 ms 87.5%，50–200 ms 100%）；gate command 与 gate filtered 同为 0%/0%/0%/75%/75%；只有 current-visual oracle 在长延迟更低（62.5–75%）。结论：command copy 不救回；旧 motor-copy 收益是 oracle 效应。新增 `fig_command_copy.png`，修订稿加入 Results 小节与 Fig. 6，PDF 重建为 11 页 6 图。
- **P1-EC-FEEDFORWARD-01（2026-10-27）**：新增 goal-based feedforward 分支（前馈项进入 bar torque，并被 EC/gate 使用；goal 由 instructed 指令 + 当前本体感觉计算）。600 runs（15 模型-增益组合 × 5 延迟 × 1 seed × 8 参数组，6 s）。`gate goal` ff≥0.5 在 20–200 ms 全部 0% 失败；`graded goal` ff=1.0 与 current-visual oracle 同水平（0.625–0.75）；ff=0 时与 baseline 逐点一致。新增 `run_feedforward.py`。
- **P1-EC-FEEDFORWARD-02（2026-10-27）**：10 s 窗口复核。`gate goal` ff=0.5/1.0 在 10 s 下 20–200 ms 仍全部 0%；`gate filtered` 在 100 ms 反而从 0% 升到 12.5%（窗口伪影）；`graded goal` 6 s 与 10 s 相同。结论：feedforward 的 gate 收益不是 6 s 窗口伪影。
- **P1-EC-GOAL-MISMATCH-01（2026-10-27）**：goal 振幅 45/60/75° × τ 0.05/0.10/0.20 s 失配，648 runs。`gate goal` ff=1.0 对全部失配组合保持 0%；ff=0.5 仅在 45° 欠幅、200 ms 出现 12.5%；`graded goal` ff=1.0 对所有失配失败率不变（0.625–0.75）。结论：收益不是精确 oracle 才有。
- **P1-EC-GOAL-DELAY-01（2026-10-27）**：goal 本身延迟 0/50/100/200 ms × 视觉延迟 100/200 ms，256 runs。`gate goal` ff=0.5/1.0 在所有 goal 延迟下仍 0%；`graded goal` 失败率不变；`gate filtered` 只随视觉延迟变化。结论：收益不来自“提前知道目标”，而来自 feedforward 分支使用当前本体感觉的零延迟回路；需要用 `ff_self_state=delayed` ablation 确认。
- **P1-EC-FEEDFORWARD-01（2026-10-27）**：goal-based feedforward 分支（instructed goal + 当前本体感觉，前馈项进入 bar torque 并被 EC/gate 使用）。600 runs。`gate goal` ff≥0.5 在 20–200 ms 全 0%；`graded goal` ff=1.0 与 oracle 同水平（0.625–0.75）；ff=0 与 baseline 逐点一致。新增 `run_feedforward.py` 与 `fig_feedforward.png` 的数据基础。
- **P1-EC-FEEDFORWARD-02（2026-10-27）**：10 s 窗口复核，400 runs。`gate goal` ff=0.5/1.0 仍全 0%；`gate filtered` 100 ms 从 0% 升到 12.5%（窗口伪影）。结论：feedforward 收益不是 6 s 窗口伪影。
- **P1-EC-GOAL-MISMATCH-01（2026-10-27）**：goal 振幅 45/60/75° × τ 0.05/0.10/0.20 s，648 runs。`gate goal` ff=1.0 全失配仍 0%；ff=0.5 仅 45°/200 ms 12.5%；graded 不变。结论：不是精确 oracle 才有收益。
- **P1-EC-GOAL-DELAY-01（2026-10-27）**：goal 延迟 0/50/100/200 ms × 视觉延迟 100/200 ms，256 runs。延迟 goal 不改变任何失败率。结论：收益不来自提前知道目标。
- **P1-EC-FF-STATE-01（2026-10-27）**：`ff_self_state` ablation，96 runs。当前本体感觉时 `gate goal` 0%；改为延迟自身状态后 0.75–1.0%，100 ms 比 `gate filtered` 更差。结论：救回来自零延迟自身状态回路。
- **P1-EC-MULTISEED-01（2026-10-27）**：判别条件 3 seeds，960 runs。graded command 与 filtered 逐 seed 一致；`gate goal` ff≥0.5 三 seed 全 0%；oracle/goal 长延迟优势保持。结论：主结论不依赖单一 seed。
- **P1-EC-ADAPTIVE-ODE-01（2026-10-27）**：MLP 权重作为 ODE 状态积分与步进更新的配对比较，96 对。失败分类与失败时间 96/96 一致；轨迹在发散前因浮点噪声被混沌放大。结论：关闭 step-wise vs ODE 实现差异；source 求解器语义仍未复现。
- **Track C 稿件再修订（2026-10-27）**：标题改为 “Efference-copy gain, gating, and current self-state in a delayed fly steering model”；新增 Results 小节 “A goal feedforward rescues delay, and it requires current self-state”、Fig. 7（2×2 机制图）、Methods feedforward 方程与全部新 sweep 计数、Discussion/Limitations/Abstract 更新；PDF 重建为 13 页 7 图。
- **P1-EC-LONGDELAY-01（2026-10-27）**：延迟边界推到 250–500 ms（10 s 窗口），240 runs。`gate goal` ff=1 在 200–500 ms 全部 0%；ff=0.5 在 250 ms 起退化（12.5%→62.5%→50%）；gate filtered 恒 0.75。结论：救回延伸到 500 ms，边界由 ff 增益决定。
- **P1-EC-FINEDELAY-01（2026-10-27）**：10 ms 细网格 0–250 ms，832 runs。临界延迟（failure≥0.5）：graded filtered 20 ms、graded goal 10 ms、gate filtered 130 ms、gate goal ff=1 无（0–250 ms 未达）。
- **P1-EC-NOISE-01（2026-10-27）**：噪声 SD 0–1e-11（高出主实验 100 倍），800 runs。所有结论不变；唯一变化是 gate filtered 100 ms 从 0% 升到 12.5%（1e-12/1e-11），gate goal 不受影响。
- **P1-EC-PHASE-01（2026-10-27）**：身体参数相图（4 惯量 × 3 阻尼 × 2 grating 增益 × 8 延迟），384 runs。gate goal 的稳定区域显著大于 gate filtered。
- **P1-EC-TRAJ-01（2026-10-27）**：200 ms / 10 s 示例轨迹导出。addition 与 graded filtered 发散到 1e8–1e13 rad；gate filtered（1.27 rad）与 gate goal（1.11 rad）有界。
- **新图（2026-10-27）**：按 dataviz 规范（色板通过六项验证）新增 `fig_delay_limits.png`（细网格+长延迟）、`fig_noise.png`、`fig_phase.png`、`fig_trajectories.png`、`fig_survival.png`、`fig_mechanism.png`（三联机制示意图），共享 `fig_style.py`。
- **CodeGraph 安装与索引（2026-10-27）**：安装 `colbymchenry/codegraph` v1.6.2（自包含 bundle，遥测已关），`codegraph install --yes` 写入 Claude Code 等代理的 MCP 配置，工作区根目录 `codegraph init` 建立索引（408 文件 / 8,086 节点 / 16,251 边，`codegraph status`）。新增根 `.gitignore` 排除 venv/实验输出/快照/日志；用法写入 `CLAUDE.md` 第 5 节与 [wiki/34_codegraph.md](34_codegraph.md)。重启代理后 `codegraph_explore` 自动可用。
- **第二轮独立审稿 + 审计 + 修订（2026-10-27/28）**：3 份互盲报告（R1/R2/R3）+ 15 项取证审计 + 交叉综合；9 项 confirmed_internal_error 全部为数字对账问题，方向性结论无一动摇。按综合清单修稿：gate-threshold 句按变体收窄、三处摘要级假句修正、预测计数/0.3%/oracle 4/5/duty 0.64 等对账修正、criterion 敏感性与噪声枚举入 Methods、名称映射表、control-theory 定位段与六条文献入正文；claim map 重建（33 行，7 行 retired）；八张旧图归档至 `archive_superseded_figures/`；新实验（P1-EC-FINEDELAY/LONGDELAY/NOISE/PHASE/TRAJ）与 Fig.8–13（机制图/延迟边界/噪声/轨迹/生存/相图）并入；PDF 重建 17 页 13 图。
- **codegraph-workflow skill（2026-10-28）**：新增用户级 skill `~/.claude/skills/codegraph-workflow/SKILL.md`，把“装 CodeGraph → 建索引 → 先查图再 grep/impact 后改”的流程固化为可复用规范，适用于任何大项目开工。
- **self-state 命题实验化（2026-10-28）**：三个过门禁轮次（P1-EC-SELFSTATE-01 272 runs、P1-EC-ONSET-01 360 runs、P1-EC-DAMP-01 192 runs）+ 模型扩展（`ff_mode`/`ff_damp_gain`/`ff_self_state_lag_s`，20 测试）。结果：(1) gate goal 的救回要求 self-state 采样年龄 ≤20–30 ms，≥40 ms 失效（新鲜度阈值，实验可测）；(2) goal 起始 ±200 ms 完全无影响；(3) 无 goal 的纯阻尼（≥1e-11）即可救回 gate——goal 内容不特殊。Fig. 14 三联图 + claim map C34–C36；稿件 Limitations/Methods/Prediction 6/Discussion 同步；PDF 重建 18 页 14 图。
- **self-state 命题文献核查（2026-10-28）**：PubMed 系统检索四条线（视觉延迟干预/本体感觉时序/corollary discharge/跨物种延迟补偿）。结论：**无任何研究直接证明** prediction 6（施加视觉延迟 + 操纵 self-state 通路延迟的实验在文献中为空白）；果蝇内定性支撑强——Bartussek & Lehmann 2016（本体感觉决定 visuomotor 增益）、Fuller et al. 2014（触角稳定约 100 ms 延迟的视觉地速控制器）、Sherman & Dickinson 2004（视觉+haltere 求和）、Warzecha & Egelhaaf 2000（视觉通路数十毫秒延迟）。四篇已核实（PMID+DOI）并补入稿件引言/讨论与文献表（14–17），PDF 重建 18 页。核查页：[36](36_selfstate_prior_evidence.md)。
- **D8 路线调整 + P0/P1/P2 首批执行（2026-10-28）**：owner 指令取消"自行开展动物实验"硬门槛，改走公开数据路线（决策 D8；[wiki/37](37_public_data_route.md)）。**P0**：三个候选数据集元数据核验——OSF 7mq9j（Cubico 2023 CB 论文）为空壳 `BLOCKED_FILES_MISSING`；Dryad m715hp3（26.6MB .mat 行为，CurrierNagel2018）与 bcc2fqzjz（13.8GB 行为+成像）元数据通过、自动下载被反爬拦，等 owner 浏览器下载；审计报告：`M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/AUDIT_REPORT.md`。**P1**：Canelo 更新版核实为 eLife 93487 V2（2025-08-20 改题），代码自 2024-08-05 零变更（本地副本==远端 HEAD）——基础实现差异风险低。**P2 第一阶段**：P1-EC-OBSERVER-01（320 runs，22 测试）——只用延迟观测的二阶 Taylor 估计器不能替代新鲜 self-state（50 ms 起 50–100% 失败），rescue 非平凡估计器可回收的信息优势；完美内部模型未测（稿件 Limitations + claim C37）。PDF 重建 19 页。
- **m715hp3 字段级资格审计（2026-10-28）**：owner 浏览器下载 `Raw Data.zip`，md5 与 Dryad 公布值一致（`6244e885…`）。实测 13 个 .mat：50 Hz、25 s 试次、闭环增益 0.04、逐蝇逐试次 H/dH（±180°）、条件含 wind/light/ms × 0°/90°、antenna-stabilized vs control、风速梯度。**无本体感觉操纵、无延迟维度**——可做行为级 P3（动物为独立单位），不能验证 20–30 ms 阈值。状态 `QUALIFIED_BEHAVIORAL`：`M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/QUALIFICATION_m715hp3.md`。
- **P1-EC-CLASSIFIER-01（2026-10-28）**：修复历史「失败分类器瞬时翻转」问题。新增共享模块 `failure_classifier.py`（旧峰值判据逐位兼容 + ≥10 ms 持续越界判据 + 记录最长连续越界时长，任何 dwell 事后可从 CSV 重算），TDD 10 项测试含 50 组随机数组等价性。720 runs（5 条件 × 8 参数组 × 噪声 {0,1e-12,1e-11} × 3 seeds × dt {1e-4,5e-5}，6 s 窗口）结果：(1) 两判据零分歧——「单样本闪烁误判」假设否定，失败轨迹是真实发散（max|heading| 中位 4.0e12 rad）；(2) 历史翻转全部集中在 `gate filtered, drag=1e-11, k_opto=5e-11, τ=100–140 ms`（seed 7 / 噪声 10 / dt 9 个翻转组），是轨迹级边稳敏感性，正确做法是系综失败率而非单次标签；(3) 369 失败中 20 个为 omega 越界 ~28 ms 后 heading 有界的可恢复偏移。26 个 runner 的判据迁移为后续 dev 轮。证据：`runs/P1-EC-CLASSIFIER-01/`。
- **P3-VISORIENT-01（2026-10-28）**：D8 路线 P3 首轮 confirmatory 反向检验（预注册先于结局冻结；nostim0 缺失→修正案 A1；逐蝇结构 bug 修复均留痕重过门禁）。在 Dryad m715hp3（exp2c 11 / exp2s 12 蝇）检验"风载荷增加转向间歇性（dH 峰度）、消融组增量更大"：交互 +2.81（median Δ：control −0.93 vs ablated +1.88），置换 p=0.128 → 按预注册停止规则记为**预测未获支持**；hump 次要指标方向相反；exp4h 单组复现方向一致（median Δ +7.25，66.7% 为正）。有限样本方向性证据，不构成反证；Track C 稿件边界不变。`runs/P3-VISORIENT-01/experiment_log.md`。
- **bcc2fqzjz 字段级资格审计（2026-10-28）**：owner 下载 Tanaka/Clark（Current Biology）counterevidence 全包（13.8 GB，SHA-256 与 Dryad 一致）。小文件+23 个原分析脚本解包审计：统一 indFly（逐蝇）× snipMat（epoch×ROI）× time×reps 结构；行为与成像同管线；数据含 T4/T5（1.10 GB）、LPTC（1.76 GB）、Mi4 与逐细胞类型遗传筛选。状态 `QUALIFIED_NEURAL_AND_BEHAVIORAL`——三份候选中唯一神经分辨率级；下一 P3 候选 = graded-vs-gate 抑制动力学模型选择（fig3_sweeps+fig4）。大数据不解包，按需流式提取。`M2A-BRIDGE/02_DATA_FEASIBILITY/public_data_audit/QUALIFICATION_bcc2fqzjz.md`。
- **Track C 稿件：边界区失败率=系综量（2026-10-28，owner 批准）**：依据 P1-EC-CLASSIFIER-01，在 `MANUSCRIPT_REVISED.md` 三处补充——Methods「Failure criteria and windows」加入 720-run 分类器稳健性检查（两判据零分歧；翻转定位 `gate filtered` 100–140 ms 边稳区；该区失败率是 seed/噪声/dt 扰动的系综量，不解读单次标签）、「Sweeps」清单补 720 runs、「Statistics」加一句指针；判据本身未改（仍为瞬时峰值）。`CLAIM_TO_EVIDENCE_MAP.csv` 新增 C38（status=current）。PDF 重建 19 页，`pdftotext` 核验两处 "ensemble quantities" 在文。依据：`runs/P1-EC-CLASSIFIER-01/experiment/outputs/summary.json`。
- **P3-CE-EXPLORE-01（2026-10-28）**：Tanaka/Clark counterevidence fig3 sweeps 探索轮（exploratory，门禁 pass）。移植原 MATLAB preprocess 提取逐蝇 turnmat（contrast 19 蝇 × 12 epochs、velocity 20 蝇 × 18 epochs，全有限），群体曲线与原文定性一致；冻结 `turnmat_fig3.npz`（SHA-256 `f04f22b4…93ce`）供确认性轮消费。候选判别量探索值：双峰系数 5 个对比度全 <0.555；LFO-CV Hill graded 9.180 vs gated 8.638（无零分布不解读）。**过程事故与修复**：`unwrap()` 对多维 object 数组死循环导致三次挂起（最长 1 h 53 m，内存钉死 903 MB），`sample` 调用栈定位后修复并加回归自测；连带修复 reps==1 squeeze 静默作废（会致整列 NaN）。修复后全程 ~60 s。确认性设计提案（P3-ROUND-2）见 `runs/P3-CE-EXPLORE-01/EXPLORATION_REPORT.md`，待 owner 批准冻结预注册。依据：`runs/P3-CE-EXPLORE-01/`。
- **P3-ROUND-2（2026-10-28，confirmatory）**：Tanaka fig3 contrast 扫描的 graded-vs-gate 模型选择，预注册（SHA-256 `9563d8c2…9e94`，含探索暴露声明与最低可检测效应规则）先于结局冻结；单次运行，npz 哈希校验通过，19 蝇 0 剔除。结果：ΔRMSE=−0.091、p=0.534 → **did_not_distinguish + INCONCLUSIVE_BY_RESOLUTION**（Δ_crit=0.454；逐蝇 9:10 平分；零分布中位 −0.105 显示嵌套选择柔性偏置已被校准）。次要双峰系数 Holm p=1.0、CI 宽，无两态证据。探索轮粗网格差 −0.54 经精化拟合消失，判定为拟合伪差。过程留痕：自测夹具/断言两次失败 + build_sup 花式索引 IndexError 一次，均修复并保留日志。**不作方向主张；该线在 n=19 分辨率下关闭候选，去向待 owner 选择**。依据：`runs/P3-ROUND-2/experiment_log.md` 与 `experiment/outputs/summary.json`。
- **P3-CE-FIG4-EXPLORE-01（2026-10-28）**：fig4 T4/T5 神经臂探索轮（exploratory，门禁 pass）。从 ZIP64 归档流式提取 `fig4_01_T4T5.mat`（1.10 GB；Info-ZIP 误报 corrupt 改用 Python zipfile）；结构内省后按原脚本移植（a/b 组 ROI 级合并、b 组 epoch 翻转、0–3 s 积分）。结果：**T4(13 蝇)/T5(15 蝇) 对外部静止棋盘的平均抑制 ≈0**（−0.023/+0.155，与原论文"抑制不在 EMD 层"一致，外部锚定验证管线）；外部闪烁抑制真实（+0.75/+0.60）；stationary 高双峰系数（0.64/0.77）由少数负值离群驱动，n 下不可解读。冻结 `neural_integ.npz`（SHA-256 `5a394ef8…cc7f`）。**推论：graded-vs-gate 效应若存在，位置在下游 LPTC**；下一步候选 (a) LPTC 提取探索 (b) flicker 分布确认性轮（预计分辨率不足）(c) 回 Track C。依据：`runs/P3-CE-FIG4-EXPLORE-01/experiment_log.md`。
- **D9 owner 裁决 + 两项核验（2026-10-28）**：owner 六项状态裁决登记（wiki/40 D9）。执行：(1) **Currier 来源身份审计**（`runs/P3-VISORIENT-01/AUDIT_ADDENDUM.md`，不改动封存文件）——antenna-stabilized = UV 胶固定触角（原文 PMC6503675 方法学），此前"消融/ablated"用语错误已更正，机制解释降级为"触角风感输入"层面；ms0 vs light0 可比性核验通过（唯一差异=风并置）；exp1 120 条目定案=**120 只独立蝇的被试内 4 条件设计**（N=120 原文核实），结构资格通过但启用须新预注册，与 exp2 队列重叠不可由数据排除。P3-VISORIENT-01 维持 INCONCLUSIVE。(2) **Tanaka 四分支独立单位核验**（QUALIFICATION_bcc2fqzjz 修订）：LPTC 5 组 10–12 蝇/组（fliesUsed 互不重叠）、Mi4 10 蝇、onset 27+17 蝇（行为）、T4/T5 13/15 蝇；ROI 一律不计独立样本；成像功效不预设高于行为。数据流式提取至审计目录（LPTC 1.76 GB 等，仅审计用）。依据：`fig_branch_structure.json`。
- **D10 P3 神经机制可识别性审查（2026-10-28）**：owner 主刊路线裁决（wiki/40 D10）执行完毕。**P3-A 基准复算轮（P3-A-BASELINE-01，门禁 pass）**：三分支蝇级复现作者 respMatPlot——Mi4 逐值一致（r=1.0、diff=0）、T4/T5 实验 epoch r=0.94–0.997、LPTC 11/12 epoch r≥0.85（HS e6/CH e3,e10 孤立低点如实记录）；LPTC 无一致静止抑制 + HS 部分增强，与原文方向一致；只作管线验证。**P3-B**：Fischer & Schnell 2022（iScience doi:10.1016/j.isci.2022.105143）EDMOND 数据集元数据级审计——194 文件 9.49 GB、N=13 蝇、9 列共享时间基准（Vm+WSA+刺激）、saccading/straight 预分选、**无实验者神经干预**（hyperpolarization=生理性；hyPol/noPol/DePol=试次分类）、代码 Zenodo 6988868；状态 `QUALIFIED_PENDING_FILE_SAMPLE`。**P3-C**：H0/H1/H2 竞争机制与判别预测表**先于任何检验结果**冻结（SHA-256 `6496b3f2…da4d`）。**裁决 `CONDITIONAL_GO`**：当前手里唯一 H2 独有方向性预测的条件 = Tanaka fig1_05_onset（延迟长度轴，27 蝇，行为级）；条件=F&S 抽样核验 + fig1_05 单预测新预注册轮；双线不可分则 `MECHANISM_NOT_IDENTIFIABLE` 并停止主刊升级。交付件四文件：`M2A-BRIDGE/09_P3_MECH_IDENT/`（ELIGIBILITY_MATRIX / PRIOR_ART_BOUNDARY / COMPETING_MECHANISMS_PREREG / GATE_REPORT）。依据：`runs/P3-A-BASELINE-01/experiment_log.md`。
- **D11 修正案 + T1 时序映射（2026-10-28）**：owner 否决 fig1_05_onset 单调预测的确认性预注册（该延迟为视觉证据出现顺序而非反馈传输延迟；H0/H1 可经视觉时间积分预测起始响应）；竞争模型集扩充（时间核/泄漏积分/状态空间必须入列）；P3-F（F&S）升为优先线，F2 偏差防范入 prereg（修正案 A1，追加于任何 fig1_05 结局检验之前）。**T1 完成**（`M2A-BRIDGE/09_P3_MECH_IDENT/T1_TIMING_MAP_fig1_05.md`）：脚本全文核实 fig1_05 含两个 brief-wait 实验——666 ms 等待+333 ms 运动（27 蝇）与 500 ms+500 ms（17 蝇）；**两延迟水平与动物批次、运动时长三重混淆**，该设计无法承载延迟剂量判别；可用定位=视觉证据整合的探索性模型判别（P3-T）。F1（F&S 原始 .mat 核验）进行中（EDMOND 下载断点续传）。授权状态：P3-A PASS；P3-B 待样本；fig1_05 预测不批；P3 识别性分析批准；Nature 确认性检验未授权。依据：wiki/40 D11。
- **D11 F1+F1 收尾（2026-10-28）**：Fischer & Schnell 原始 .mat 样本核验 **PASS**（`fs2022_audit/F1_VERIFICATION.md`）：24,358,344 B 全尺寸、v7.3/HDF5、`experParams` 与文件名 ID 链逐字一致、5 硬件通道共享单一时钟（Vm+WBA_L/R+刺激 marker 0/3V 打标，179.5 s @ 10 kHz——**srate 逐会话，10k/15k 并存，不得假设统一**）、9 列表为衍生处理格式（L−R WSA 可由原始通道+Zenodo 代码重建）。F&S 状态 `QUALIFIED_PENDING_FILE_SAMPLE` → **`QUALIFIED`**。T1 时序映射已完成（fig1_05 两延迟水平与批次+运动时长三重混淆）。下一轮 = F2 识别性分析（同视觉刺激下运动历史对 HS 的增量预测，偏差防范已入 prereg 修正案 A1）。样本 md5 已入核验报告。
- **F2 管线就绪 + 全量下载启动（2026-10-28）**：P3-F-F2-01 轮建置完成（门禁 pass）。`fs_f2_identifiability.py`：H0/H0noise/H1 容量匹配岭回归（ raised-cosine 视觉基 0–1.5 s；运动基滞后严格 ≥20 ms；显式截距），按整动物 LOMO，动物级符号置换 + bootstrap CI，主张上限写入产物。debug 修复两个实质 bug：一维 ones 列、**标准化常数列塌缩导致测试段伪常数偏置（R²=−115）**——均修复并留痕。真实数据烟测披露为"未运行（数据未到）"。后台启动 64 会话/1.99 GB 全量下载（EDMOND ~35 KB/s 波动，逐文件断点续传+尺寸校验；12 只动物）；下载完成监听已挂，到齐后自动进入全量 LOMO 运行。依据：`runs/P3-F-F2-01/debug/debug_report.md`。
- **P3-F-F2-01（2026-10-29，识别性分析）**：F&S 全量 64 会话/12 动物 LOMO 完成（数据经浏览器代下失败后由 8 路并行 API 下载器取得，2 损坏文件重拉修复，逐文件尺寸校验）。结果（`runs/P3-F-F2-01/`）：ΔR²（H1−H0）9/12 为正、中位 +0.056、bootstrap CI95 [−0.013,+0.107]、符号置换 **p=0.0503** → 按冻结规则记 **`NOT_DISCRIMINATED`**（不作接近显著的再解释）。识别性 caveat：留出动物上 H0 绝对 R² 深负（−0.07~−5.4），跨动物 Vm 尺度失配主导绝对指标；会话内标准化是显然的后续选项但属事后设计变更，须新预注册并声明。运行修复一处模型标志捕获 bug（留痕）。**F2 单线不可分；按 D11 剩余路径 = P3-T 或（若也不可分）`MECHANISM_NOT_IDENTIFIABLE`**。依据：`runs/P3-F-F2-01/experiment_log.md`（summary SHA-256 `8e29b2f1…4c1b`）。
- **D12 + P3-T-EXPLORE-01（2026-10-29）**：owner 裁定 F2 识别性门**按通过处理**（D12：数值原样保留 p=0.0503/CI 跨 0，升级的是阶段门；主张上限维持"额外预测信息"）。P3-T 探索轮（门禁 pass）：A 迟步/B 前景斜坡/C 前景时间核三模型 fig1_05 留出动物比较——A/B 均 R²≈0 不可区分，C 优势为容量效应（0.064/0.105）；预声明判别量（运动+100 ms 差值）呈 +10.4 deg/s 间隙依赖方向（利 B），但批次混淆+逐蝇 IQR 跨 0 → **视觉整合层 NOT_DISCRIMINATED**。**识别性阶段总盘点：F2 过门（D12）+ P3-T 不可判定（已知限制）→ 不触发停止规则**；Nature 确认性生物检验仍未授权；下一步候选 = F&S 确认性设计冻结（唯一主终点+动物切分+统计规则）。依据：`runs/P3-T-EXPLORE-01/experiment_log.md`。
- **D13 双轨执行第一批（2026-10-29）**：(1) **P3-F-LOCK 完成**——F&S 预测协议冻结（SHA-256 `339dfbf3…2ad7`）：主终点=动物级留出对数似然增量、次终点=会话内 z-score ΔR²、五条硬约束（因果输入/动物切分/三类负对照/超参固定/报告规范）；同批 F&S 数据永为协议开发集，不重切做确认。(2) **P2-OBSERVER-02 完成**（门禁 pass，ec_model 新增 pd_instant/smith/smith_pert + 3 恒等性测试，38 项全过；48 单元格 384 runs）：延迟基线 50–200 ms 全失败；gate filtered 短延迟 0%/长延迟 0.75（复现已知）；gate goal 即时状态参照全 0%；**即时经典 PD（匹配增益）38–62% 失败；Smith 前向模型观测器（精确/10% 失配）≥100 ms 全失败**——报告一结论：经典控制未解释 Track C 全部优势；门控在模型内有独立贡献（对 C19）；必要成分=新鲜自身状态（对 C35）。限制如实：pd_instant 未整定增益、smith 未嵌 DDE。(3) **P3-EXTERNAL-01 审计**：**DNp03（Croke 2025）数据仓四重核验 404**（论文声明 GitHub 入口不可用）→ `BLOCKED_REPO_UNAVAILABLE`，理论上判别轴最全（干预+神经+行为）；Rayshubskiy（158 GB，行走+csChrimson 干预系）为跨行为形式候选，字段级抽样进行中。(4) 两份 D13 判据报告落档：`REPORT_CLASSICAL_CONTROLS.md`（答：否）与 `REPORT_EXTERNAL_DATA.md`（答：尚不能，阻塞点=数据可得性）。旗舰投入判据：计算侧半分已答（经典未全解释），生物侧半分待数据。依据：`runs/P2-OBSERVER-02/`、`09_P3_MECH_IDENT/`。
- **Rayshubskiy 神经侧资格核验通过（2026-10-29）**：owner 下载干预系
  （161218_…83blexA_ss731_02，105.2 MiB）与 GFP 对照（170802_gfp_ss731_03，
  96.1 MiB）两会话，尺寸与 Dataverse 清单精确一致。逐通道实测：`ephys_A`
  单通道膜电位 4 kHz（−72…+105 mV，动作电位可见）、`fwd/lat/yaw` 球速度
  100 Hz、`t_ephys`/`t_ball` 同 session 同起点对齐、**`stim` 通道 0/5 V 含
  261 个光遗传时段（对照文件全 0）**——判别六轴（神经/行为/干预/标记/时钟/
  蝇级单位）全部就位，状态 `QUALIFIED`。**报告二数据侧答案转为"具备判别
  条件"**；判别预注册（P3-F-LOCK 五约束的跨系统版）待 owner 批准后起草冻结。
  依据：`EXTERNAL_DATA_AUDIT.md` §2。
- **P3-RAY-DISCRIM-01 建置完成（2026-10-29）**：owner 授权直推后，跨系统判别
  确认轮全部就绪——预注册冻结（SHA-256 `06813365…317a`：M0 刺激历史 vs
  M1 +起始前行为状态、主终点=留出动物 epoch 级 ΔLL、精确符号置换 n=6、
  三负对照（伪脉冲/时间错位/容量）、开发会话 161218+170802 永久排除出检验集）；
  管线 `run_ray_discrim.py` 门禁 pass（5 项检查；修复行为响应窗口索引 bug 并留痕；
  开发会话冒烟：261 epoch 提取成功、行为响应 std≈75 量级合理、对照会话实测
  0 真实脉冲→伪脉冲路径成立）。**阻塞项 = 检验集 12 个文件（~1.1 GB）待 owner
  浏览器下载**（6 干预 + 6 对照，清单已交付）；到位后单次运行并报告。
  依据：`runs/P3-RAY-DISCRIM-01/`。
- **P3-RAY-DISCRIM-01 结果（2026-10-29，confirmatory 单次运行）**：6 干预动物
  （144–246 epoch/只）主终点过线——ΔLL 5/6 为正（+18.6/+220.4/−5.3/+14.3/
  +60.6/+37.6），精确符号置换 **p=0.03125**，冻结标签
  `STATE_DEPENDENT_PERTURBATION_RESPONSE`；神经次终点 4/6 为正（中位+5.0）。
  **但负对照击穿特异性解释**：伪脉冲对照（对照蝇随机时刻）中位 ΔLL=+20.1，
  与主效应 +28.1 同量级——M1 优势主要是**行为自相关的普遍可预测性**而非
  扰动特异状态依赖；时间错位对照归零（符合）；**容量对照未实现（协议偏离，
  披露）**。最终记录：主标签 + 解释层 `CONTROL_EXPECTATION_FAILED`——
  **本系统本终点设计未建立扰动特异状态依赖**。教训：未来须以脉冲触发残差
  为终点（新预注册）；M0 基线太弱是设计层失败，数据轴资格不受影响。
  依据：`runs/P3-RAY-DISCRIM-01/experiment_log.md`（summary SHA-256
  `3501f589…17d`）。
- **P3-RAY-DISCRIM-02 结果（2026-10-29，残差终点二次判别，confirmatory）**：
  基线图谱 g 仅从伪 epoch 学习（三负对照全部实现）。结果：行为残差 ΔLL
  **6/6 动物为正**（中位 +8.57），精确符号置换 p=1/64=0.0156；但**伪脉冲
  对照中位 +6.88 ≥ 主效应 1/3——预注册特异性量级条件再次未满足**；神经
  5/6 为正（+2.50）；容量对照 +0.24 ✓；时间错位 +2.24（未完全归零）。
  判定：`STATE_DEPENDENT_PERTURBATION_RESPONSE_WITH_FAILED_CONTROL`。
  残差管线将伪影从 01 的 +20.1 压到 +6.88，主效应净超出量仅 ~2–5 LL 单位，
  n=6（干预动物已全部在场，无法扩）不可分离。**两轮判别均未通过自身特异性
  对照——对应 D13 停止条件第三档；旗舰主刊升级路径按规则应停止**，
  保留 Track C + 方法学结论 + 全部诚实记录；生物学判别留待可扩 n 的新数据。
  依据：`runs/P3-RAY-DISCRIM-02/experiment_log.md`（summary SHA-256
  `c3420bad…92b3`）。
- **D16 定位 + 完整稿件架构（2026-10-29）**：owner 裁决——主刊停止、
  **目标降为子刊、内容必须完整**。执行：`08_MANUSCRIPT/SUBJOURNAL_PACKAGE/
  MANUSCRIPT_OUTLINE.md` 落档——完整论文蓝图（题名候选、逐节 claim→证据
  指针、10 图计划、C39–C46 声明扩展、期刊顺序 eLife→PLOS Biology→NatCom），
  覆盖 Track C 计算核心 + P2 经典控制对照 + 四数据集实测 + 判别方法学。
  推荐默认（待 owner 可改）：吸收 Track C 进整合稿、eLife 首投。
  下一步：claim map 扩展 → R1–R3 复用并稿 → R4–R6 新写作 → 新图 →
  三互盲审稿轮。依据：wiki/40 D16。
- 未启动确认性生物实验；未下载 50–200 GB 大包；未修改冻结资产。

## 轮次记录

| 日期 | round_id | 类型 | 目标 | 门禁 | 结果 | 指针 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-27 | P0-SMOKE-01 | pilot | flyvis/FlyGym 最小 smoke | pass | flyvis 连接组 + FlyGym 自由体 50 步 | `runs/P0-SMOKE-01/experiment_log.md` |
| 2026-10-27 | P1-EC-DELAY-01 | pilot | 4 模型 × 延迟粗网格 | pass | allnone 0.25 s / graded_sensory 0.03 s | `runs/P1-EC-DELAY-01/experiment_log.md` |
| 2026-10-27 | P1-EC-DELAY-02 | pilot | 噪声 + 身体时间常数 + allnone_motor | pass | allnone 0.20 s / graded_sensory 0.02 s / allnone_motor 0.11 s | `runs/P1-EC-DELAY-02/experiment_log.md` |
| 2026-10-27 | P1-EC-DELAY-03 | pilot | 1 ms 细网格 | pass | 18 / 15 / 10 / 110 / 200 ms | `runs/P1-EC-DELAY-03/experiment_log.md` |
| 2026-10-27 | P1-EC-COMMAND-01 | pilot | 真 command copy vs filtered vs oracle | pass | command = filtered；oracle 才低 | `runs/P1-EC-COMMAND-01/experiment_log.md` |
| 2026-10-27 | P1-EC-FEEDFORWARD-01 | pilot | goal feedforward 扫 ff 增益 | pass | gate goal ff≥0.5 全 0% | `runs/P1-EC-FEEDFORWARD-01/experiment_log.md` |
| 2026-10-27 | P1-EC-FEEDFORWARD-02 | pilot | 10 s 窗口复核 | pass | gate goal 10 s 仍全 0% | `runs/P1-EC-FEEDFORWARD-02/experiment_log.md` |
| 2026-10-27 | P1-EC-GOAL-MISMATCH-01 | pilot | goal 振幅/时间常数失配 | pass | ff=1 全失配仍 0% | `runs/P1-EC-GOAL-MISMATCH-01/experiment_log.md` |
| 2026-10-27 | P1-EC-GOAL-DELAY-01 | pilot | 延迟 goal 控制 | pass | 延迟 goal 不消除收益 | `runs/P1-EC-GOAL-DELAY-01/experiment_log.md` |
| 2026-10-27 | P1-EC-FF-STATE-01 | pilot | feedforward 自身状态 ablation | pass | 延迟自身状态后收益消失 | `runs/P1-EC-FF-STATE-01/experiment_log.md` |
| 2026-10-27 | P1-EC-MULTISEED-01 | pilot | 关键结论 3 seeds | pass | 结论逐 seed 保持 | `runs/P1-EC-MULTISEED-01/experiment_log.md` |
| 2026-10-27 | P1-EC-ADAPTIVE-ODE-01 | pilot | ODE-internal 权重等价 | pass | 96/96 失败一致 | `runs/P1-EC-ADAPTIVE-ODE-01/experiment_log.md` |
| 2026-10-27 | P1-EC-LONGDELAY-01 | pilot | 延迟边界 250–500 ms | pass | gate goal ff=1 全 0% | `runs/P1-EC-LONGDELAY-01/experiment_log.md` |
| 2026-10-27 | P1-EC-FINEDELAY-01 | pilot | 10 ms 细网格 | pass | gate filtered 130 ms / gate goal >250 ms | `runs/P1-EC-FINEDELAY-01/experiment_log.md` |
| 2026-10-27 | P1-EC-NOISE-01 | pilot | 噪声 0–1e-11 | pass | 结论不变 | `runs/P1-EC-NOISE-01/experiment_log.md` |
| 2026-10-27 | P1-EC-PHASE-01 | pilot | 身体参数相图 | pass | gate goal 稳定区更大 | `runs/P1-EC-PHASE-01/experiment_log.md` |
| 2026-10-27 | P1-EC-TRAJ-01 | pilot | 示例轨迹导出 | pass | gate 两变体有界 | `runs/P1-EC-TRAJ-01/experiment_log.md` |
| 2026-10-28 | P1-EC-SELFSTATE-01 | pilot | self-state 新鲜度曲线 | pass | 阈值 20–30 ms | `runs/P1-EC-SELFSTATE-01/experiment_log.md` |
| 2026-10-28 | P1-EC-ONSET-01 | pilot | goal 起始解耦 | pass | ±200 ms 无影响 | `runs/P1-EC-ONSET-01/experiment_log.md` |
| 2026-10-28 | P1-EC-DAMP-01 | pilot | 无 goal 阻尼对照 | pass | 阻尼≥1e-11 救回 gate | `runs/P1-EC-DAMP-01/experiment_log.md` |
| 2026-10-28 | P1-EC-OBSERVER-01 | pilot | 等信息估计器对照 | pass | 平凡估计器救不回 | `runs/P1-EC-OBSERVER-01/experiment_log.md` |
| 2026-10-28 | P3-VISORIENT-01 | confirmatory | 公开数据反向检验 #1 | pass | 方向一致、p=0.128 未获支持 | `runs/P3-VISORIENT-01/experiment_log.md` |
| 2026-10-28 | P1-EC-CLASSIFIER-01 | pilot | 失败分类器瞬时翻转修复 | pass | 零判据分歧；翻转=轨迹级边稳敏感性 | `runs/P1-EC-CLASSIFIER-01/experiment_log.md` |
| 2026-10-28 | P3-CE-EXPLORE-01 | pilot | Tanaka fig3 preprocess 移植 + graded-vs-gate 候选统计 | pass | turnmat 冻结（19/20 蝇）；unwrap 死循环修复；判别力有限 | `runs/P3-CE-EXPLORE-01/experiment_log.md` |
| 2026-10-28 | P3-ROUND-2 | confirmatory | graded-vs-gate 剂量反应模型选择（嵌套 LFO-CV + 自助零分布） | pass | Δ=−0.091，p=0.534，未能区分 + 分辨率不足；粗网格差=拟合伪差 | `runs/P3-ROUND-2/experiment_log.md` |
| 2026-10-28 | P3-CE-FIG4-EXPLORE-01 | pilot | fig4 T4/T5 移植 + 抑制分布探索 | pass | T4/T5 静止抑制≈0（管线外部锚定成立）；闪烁抑制存在；效应或在 LPTC | `runs/P3-CE-FIG4-EXPLORE-01/experiment_log.md` |
| 2026-10-28 | P3-A-BASELINE-01 | pilot | Tanaka 三分支基准复算（D10 P3-A） | pass | Mi4 逐值 r=1.0；T4/T5 实验 epoch r≥0.94；LPTC 方向与原文一致 | `runs/P3-A-BASELINE-01/experiment_log.md` |

## 追加规则

1. 每轮结束追加一行轮次记录；
2. 重大决策同时写 `40_decisions_and_risks.md`；
3. 冻结历史页的修改只追加“日期 + 修正 + 理由”，不改原文；
4. 数字必须带来源路径。
- **D16 执行第一批（2026-10-29）**：完整子刊稿并稿完成——`08_MANUSCRIPT/SUBJOURNAL_PACKAGE/MANUSCRIPT_DRAFT_V2.md`（417+ 行完整初稿：新 Abstract/Intro、复用 Track C 全部已审 Results、新写 R3 经典控制对照 / R4 Tanaka / R5 F&S / R6 判别方法学、新 Discussion、Methods 含**全部预注册 SHA-256 冻结表**、图例/限制/21 条参考文献）。`CLAIM_TO_EVIDENCE_MAP.csv` 扩至 **C46**（C39–C46 覆盖 observer 对照、基准复现、模型选择不可判定、F&S 增量信息、判别两轮）。待办：新 5 张图件（dataviz 规范）、参考文献 [21] 作者核实、三互盲审稿轮。依据：wiki/40 D16。
- **D16 执行第二批（2026-10-29）**：五张新图件完成并验证（`SUBJOURNAL_PACKAGE/figs/`，PNG220dpi+PDF，dataviz 验证色板，全分辨率像素探针确认系列色命中）——fig3 经典控制失败线图、fig5 基准对账散点、fig6 模型选择不可判定双panel、fig7 F&S 逐动物 ΔR²、fig8 判别两轮对照阶梯；五条对应图例已插入 MANUSCRIPT_DRAFT_V2。稿件剩余：in-text 引用编号打通、三互盲审稿轮、投稿包。
- **D17 + 三互盲审稿轮启动（2026-10-29）**：owner 定刊 **Nature Machine Intelligence** 并批准审稿轮。稿件冻结（MANUSCRIPT_DRAFT_V2 SHA-256 `22b9535e…c18`）；三位互盲审稿人（计算可靠性 / 实证统计严谨性 / NMI 适配与 AI 相关性三个工作视角）并行启动，各自只读稿件+claim map、只写各自报告（reviews/REVIEW_R{1,2,3}.md）。预计审稿核心意见之一：NMI 需要 AI 侧贡献（D10 第三腿"人工控制器失效与恢复"缺项）——已并行起草 P4-AI 迁移实验计划。审后流程：取证审计 → 综合 → 修订 → 投稿包。依据：wiki/40 D17。
- **三互盲审稿完成 + 交叉综合（2026-10-29）**：三报告冻结入档（reviews/REVIEW_R{1,2,3}.md）——R1 Major revision（2 阻断：经典 PD 对照被未门控光动回路混淆；"Smith"标签过强/朴素前向模型）、R2 Major revision（0 阻断：四数据集计数、D12 治理披露、C46 地板统计）、R3 Reject&resubmit（2 阻断：单模型 AI 泛化、估计器基线弱）。共识阻断 3 组（估计器公平性、门控×经典交叉缺失、AI 迁移演示缺失）+ 共识主要 7 项 + 三方文书共识（图号/占位引用/C37）。综合与修订计划：`reviews/SYNTHESIS.md`——W1 模型补跑套件、W2 P4-AI 迁移、W3 伪脉冲注入-恢复验证、W4 文书修订、W5 复审。取证审计代理并行运行中。依据：wiki/40 D17 流程。
- **取证审计完成（2026-10-29）**：23 项（1 确认错误=四数据集计数；3 聚合歧义=T4/T5 epoch 措辞、LPTC 11/12 实为 CH 10/12、"+2~5"不可溯源（真实中位净超额 +1.69）；3 出处缺口=c4eb583f 标签、75cc2434 需点名 Currier、+2~5；14 通过）。全部数字主体对账正确；修法已并入 SYNTHESIS §6 并入 W4 文书修订。reviews/FORENSIC_AUDIT.md。
- **W1-REVISION-01 完成（2026-10-29）**：审稿修订套件（门禁 pass，45 测试）五实验全部出结果，**改写必要性图景**：(a) 即时经典 PD+门控（pd_gate）全延迟 0%——R1-M1 质疑成立，快通路可以是经典 PD；(b) 延迟内嵌观测器 smith_dde 在全部延迟 8/8 失败（含50 ms，比朴素 smith 更差）——"not delayed extrapolation"获得公平检验支撑；(c) 同架构内关门控 88–100% 失败、\|F_bar\| 触发即足——R1-M3 解决；(d) **ψ/ω 免延迟时 addition 等全部稳定（0% 全延迟）**——R1-M4 成立且升级为新核心：门控是条件性的替代架构，根本必要成分是新鲜自身状态进入闭合回路；(e) 边界主张三种子稳健。诚实重写版必要性图景入 `runs/W1-REVISION-01/experiment_log.md`；下一步 W4 大幅改写 Abstract/R3/Discussion + claim map C47–C52 + 审稿逐条回应。
- **W4 修订主体完成（2026-10-29）**：(1) 必要性图景诚实重写——Abstract/R3/Discussion 全部按 W1 结果改写（新鲜自身状态=根本成分、门控=条件性替代架构、非经典快通路主张撤回）；(2) claim map 至 52 行（C40 superseded_by_C47、C41 收窄、C47–C52 新增）；(3) 九项共识/审计修正落地（数据集 (iv) Currier 入 Methods、D12 事后治理披露原文、C46 净超额 +1.7 与配对检验缺失声明、R4 epoch 措辞、哈希标签、定位动词、预测幅度）；(4) 图号统一 15–22（fig15 含 W1 系列、新 fig16 消融图、fig19–22 重命名重生成，全部指针同步）；(5) 披露类修正（matched-budget 定义、新鲜度 10ms 网格、MDE 算法、rule-of-three、C37 status、C7/C8 重指）。剩余：参考文献 [21] 补全、列表去重、k/N 全文扫、逐条审稿回应书（W5 前置）。
- **W4 收尾（2026-10-29）**：参考文献 [21] 补全（Tanaka et al., Curr Biol 33, 4960-4979.e7, 2023）并合并为单一 1–21 列表（R3-m6）；新章节 k/N 计数化 + 全稿速率口径说明（R1-m7）；**逐条审稿回应书** `reviews/RESPONSE_TO_REVIEWERS.md` 完成（R1×13、R2×11、R3×12+3 技术失败、审计 23 项逐条对应，标明已修/进行中）。稿件修订主体全部落地。剩余 W2（P4-AI 迁移实验）、W3（注入-恢复验证 + ML 关联段）后进入 W5 复审。
- **W3-INJECT-01（2026-10-29）**：伪脉冲/残差管线注入-恢复验证完成（门禁 pass，三次设计修正留痕：地板指标失效→配对 RNG 漂移→β 量级）。结果：单调恢复曲线，**检测阈值 β=8（p=0.020），β≥16 稳健（p≤4e-5，90–100% seeds）**，β≤4 不可检（占残差方差 <1%）。R3 TF#6 关闭：方法灵敏度量化，为 DISCRIM 两轮的"未建立"提供互补强度边界。依据 `runs/W3-INJECT-01/experiment_log.md`。
- **P4-AI-01 完成（2026-10-29，confirmatory 存档跑）**：AI 迁移实验（R3-M1 回应）——三任务×六控制器族×30 随机植物×0–600 ms，预注册 `6e56c187`。**预测全部成立**：F（新鲜状态+延迟参考）全栅格 0% 失败；C/E1 临界 50–200 ms；延迟内嵌观测器 150–300 ms 仍未达 F；**F+ 未门控叠加延迟项退化至 150–400 ms（C50 门控条件性跨系统迁移）**；恢复 F≈0.4 s vs C 2.7–4.1 s。过程修正 5 次全留痕（含 hash() 种子不可复现→固定 FAM_CODE 存档重跑）。Fig23 + claims C54/C55 + NEW_W2 章节入稿。summary SHA `bee2cb4c…e45`。
- **W5 复审完成（2026-10-29）**：双核验代理——阻断项核查 6 RESOLVED/4 PARTIAL/0 未解决（R1-M1、R1-M2/R3-M2、R3-M1、R2-M1/M2/M3 全部 RESOLVED）；新增数字对账 47 项（37 pass/7 error/3 n.a.）。7 错误（Taylor 出处、E2m 措辞、C53-C55 引用、β≥16 p 值 4e-5→5e-5、C53 map 同步、Fig16/Fig23 图例缺失）+ 4 部分项（Abstract 限定句、L192 门控遗留、回应书五处、R4 出处句）**全部修复**；C52 Fig18 孤儿指针改 Fig15;Fig16。核验报告：reviews/W5_VERIFICATION.md、FORENSIC_AUDIT_V2.md。进入最终打包。
- **投稿包完成（2026-10-29，D16/D17 终点）**：W5 全部修复项落地后编译 `SUBJOURNAL_PACKAGE/submission/MANUSCRIPT_NMI.pdf`（含 TOC 与全部图件嵌入、π 缺字修正），同包：CLAIM_TO_EVIDENCE_MAP（55 claims）、COVER_LETTER_DRAFT、RESPONSE_TO_REVIEWERS、W5_VERIFICATION、FORENSIC_AUDIT_V2。稿件终态：必要图景（W1 修正版）+ AI 迁移（P4）+ 四数据集实证 + 判别方法学（W3 灵敏度量化）；三互盲审稿全部阻断项 RESOLVED。剩余 owner 侧：作者元数据/资助/DOI 存放后即可投 Nature Machine Intelligence。
- **防桌拒定位调整（2026-10-29，owner 指令）**：整体改为跨领域诚实定位——(1) 标题改控制/智能系统先行："What delayed feedback control needs: fresh state, conditional gating, and tests across artificial and biological systems"；(2) 摘要重写：延迟反馈问题（人工+生物）→ 有界必要性图景 → 预注册人工任务迁移 → 四数据集约束（阴性如实点名）+ Subject terms；(3) Intro 开篇改为跨领域三解法框架（果蝇=提供独特组合的深入实例），新增 **Scope of this work** 诚实范围段（做什么/不做什么）；(4) Results 重排：AI 迁移章前移至公平对照之后（弧线=机制测绘→人工迁移→生物约束→方法学）；(5) 封面信重写为控制/ML 先行+诚实自述（"我们自己两个早期框架被公平对照推翻"写入信中）。PDF 重编译零警告 30 页，顺序/Subject terms/Scope 均验证在文。
- **D18 投稿执行阶段（2026-10-29）**：owner 确认强结论、锁定 NMI。投稿包补齐至 9 件（哈希入档）：MANUSCRIPT_NMI.pdf（30 页零警告）、COVER_LETTER_DRAFT、DECLARATIONS（数据/代码/利益/贡献模板）、REPORTING_SUMMARY（NMI 表单骨架，随机化/盲法/统计条目预填）、OWNER_CHECKLIST（必填6项=作者/ORCID/资助/DOI/利益/通讯作者）、CLAIM_TO_EVIDENCE_MAP（C1–C55）、RESPONSE_TO_REVIEWERS、W5_VERIFICATION、FORENSIC_AUDIT_V2。D18 已登记 wiki/40。投稿动作 = owner 清单完成 + 导师意见后在 NMI 系统提交。
- **官方模板排版 + humanizer 润色 + 图件合并（2026-10-31，owner 指令）**：(1) 下载 Springer Nature 官方 LaTeX 模板包（2024-12 版，cms-resources 官方源，SHA 入包内 latex_template/），采用 `sn-jnl.cls` + `sn-nature` 风格（Nature Portfolio 专用）+ `sn-nature.bst`；(2) humanizer 全稿润色出 `MANUSCRIPT_DRAFT_V3.md`：修复引言三解法重复陈述段、"challenged in review"改为内部对抗审（不谎称外审）、摘要压至 148 词（NMI 150 词限内）、正文叙述性破折号全部改为逗号/括号（数字范围与公式保留）、装饰性粗体削减（保留 D12 治理与 "not established" 两处诚实性强调）；(3) 图件合并：figs/make_composite_fig15.py 将旧 Fig15/16/19/20/21/22 六图合成为 **Fig. 15（2×3 面板 a–f，无重叠，300 dpi）**，旧 Fig23 重编号为 **Fig. 16**，正文指针/图例全部同步（图号缺口 17/18 消除）；(4) 全稿转 LaTeX（latex_nmi/manuscript.tex，461 行；21 条参考文献入 sn-bibliography.bib，正文实引 10 条经 bibtex 解析零未定义），pdflatex+bibtex 全流程编译通过：**31 页、零未定义引用、零 overfull**，首 Nature 版式（标题/作者占位/摘要/Subject terms）渲染验证；新 PDF 覆盖 submission/MANUSCRIPT_NMI.pdf。构建源：SUBJOURNAL_PACKAGE/latex_nmi/（自包含：cls/bst/bib/figs）。owner 侧清单不变（作者/资助/DOI/通讯作者）。
