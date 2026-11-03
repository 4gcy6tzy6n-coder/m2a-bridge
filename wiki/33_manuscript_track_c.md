# Track C 修订稿（审稿后）

> 状态：2026-10-27 完成独立三审 + 补实验 + 重写；未投稿；B0 计算研究，无新生物数据。
> 目标：PLOS Computational Biology。Nature 旗舰不适用。

## 审稿结论

三份互盲 reviewer 报告一致给出 **major revision**，并指出原稿的 blocking 问题：

- 2.5 s 窗口截断晚发失败，gating 的 140 ms 优势是窗口伪影。
- V 项 clip 在大偏离区被激活，100 ms gating 优势在 smooth V 下消失。
- “motor copy”实际是未延迟视觉信号，source 主张混淆了 timing 与 filtering。
- adaptive MLP 使用非负平方误差，增益只能单调上升，不是梯度。
- linear stability 的 300 ms 是 censoring，不是 crossing；根追踪不连续。
- 主 gate threshold 未扫描；source-protocol 检查是退化极限。
- 图、引用、reproducibility 与 Discussion/Limitations 存在多处不一致。

详见 `CROSS_REVIEW_SYNTHESIS.md` 和 `FORENSIC_AUDIT.md`。

## 修订后保留的结论

1. **Gain**：源论文固定增益 0.05 下，graded cancellation 与 no-EC 完全同轨；增益 ≥0.25 时，50 ms 失败率 100%（no-EC 75%）。
2. **短延迟 gating**：20–50 ms 下，gating 在 gate threshold 0.01–0.5、clip/smooth/unclipped V 下均 0% 失败；连续模型 62.5–100% 失败。
3. **100 ms 不是稳健优势**：clip 下 0%，smooth V 下 75%；gate threshold 0.5 下 clip 也升到 37.5%。
4. **140 ms 以上无优势**：6 s 窗口下 allnone 68.8%，allnone_motor 75%；10 s 下两者 75%。
5. **Adaptive 不救回**：source 更新 mean gain 0.51→1.05；signed gradient 0.22→0.40；两者失败率都是 20 ms 50%、50 ms 起 100%。
6. **Command copy 不救回**：pre-plant-filter command copy 与 filtered plant state 完全同轨（graded：20 ms 87.5%，50 ms 起 100%；gate：20–100 ms 0%，140–200 ms 75%）；只有 current-visual oracle 在长延迟更低。原 “motor copy” 的收益是 oracle 效应。

## 已删除/降级的主张

- 删除 “gating robust through 100/200 ms”。
- 删除 “source/motor copy 是决定性变量”；改为 filtered vs unfiltered 的操作化说明。
- 删除 current-visual oracle 的 motor-copy 解释；真正的 command copy 已检验，不救回，旧收益是 oracle 效应。
- 删除 linear stability section 和当时的 Fig. 6（该图号现用于 command copy）。
- 删除 “source ranking recoverable”；改为“未在 meaningful effect size 上复现，source 只是 motivation”。

## 文件

- 修订稿：[MANUSCRIPT_REVISED.md](../M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.md)
- 修订 PDF：[MANUSCRIPT_REVISED.pdf](../M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/MANUSCRIPT_REVISED.pdf)（19 页，14 图）
- 审稿综合：[CROSS_REVIEW_SYNTHESIS.md](../M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/CROSS_REVIEW_SYNTHESIS.md)
- 取证审计：[FORENSIC_AUDIT.md](../M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/FORENSIC_AUDIT.md)
- 投稿清单：[SUBMISSION_CHECKLIST.md](../M2A-BRIDGE/08_MANUSCRIPT/TRACK_C_EC_DELAY/SUBMISSION_CHECKLIST.md)
- 新实验：[window](../runs/P1-EC-WINDOW-01/experiment_log.md)、[V-clip](../runs/P1-EC-VCLIP-01/experiment_log.md)、[gate threshold](../runs/P1-EC-GATE-01/experiment_log.md)、[adaptive gradient](../runs/P1-EC-ADAPTIVE-03/experiment_log.md)、[command copy](../runs/P1-EC-COMMAND-01/experiment_log.md)、[feedforward](../runs/P1-EC-FEEDFORWARD-01/experiment_log.md)、[feedforward window](../runs/P1-EC-FEEDFORWARD-02/experiment_log.md)、[goal mismatch](../runs/P1-EC-GOAL-MISMATCH-01/experiment_log.md)、[goal delay](../runs/P1-EC-GOAL-DELAY-01/experiment_log.md)、[self-state ablation](../runs/P1-EC-FF-STATE-01/experiment_log.md)、[multi-seed](../runs/P1-EC-MULTISEED-01/experiment_log.md)、[adaptive ODE](../runs/P1-EC-ADAPTIVE-ODE-01/experiment_log.md)

## 第二轮独立审稿（2026-10-27/28）

- 三份互盲报告（一致性 R1、设计 R2、定位 R3）+ 取证审计（15 项：9 confirmed_internal_error、2 aggregation_ambiguity、2 provenance_gap、2 passed）+ 交叉综合，见 `REVIEW_ROUND2_R1/R2/R3.md`、`FORENSIC_AUDIT_ROUND2.md`、`REVIEW_ROUND2_SYNTHESIS.md`。
- 三份一致：核心计算结论成立，修订是对账/文本/文档层面。共识必修：gate-threshold 概括句按变体收窄（allnone_motor 在 th=0.5/50ms/clip 为 25%）、claim map 重建、多 seed 句收窄、连续模型 100% 句点名、命名映射、预测计数、六条文献入正文、0.15%/0.3% 统一。
- 已全部修入修订稿：摘要/Results/Discussion/Methods/图注重写；新增 criterion 敏感性段、噪声枚举、名称映射表、forward-model/Smith-predictor 定位段（von Holst、Westeinde、Lappalainen、Erginkaya、Wang-Chen、Dhiman 入正文）；claim map 重建为 33 行（7 行退役隔离）；八张旧图归档；新实验（细网格/长延迟/噪声/相图/轨迹）与新图（Fig.8–13）并入；PDF 17 页 13 图。
- R2 首个实例卡死 2 小时被终止，重试实例 11 分钟完成（互盲未破坏）。
- D8 后补（2026-10-28）：等信息估计器基线（P1-EC-OBSERVER-01）入稿——平凡 Taylor 估计器救不回，claim C37；文献核查四篇（refs 14–17）入稿。

## self-state 命题的实验化（2026-10-28）

- 三个新轮次把命题变成可证伪数字（Fig. 14，claims C34–C36）：
  1. **新鲜度剂量曲线**（P1-EC-SELFSTATE-01）：gate goal 在 self-state 采样年龄 ≤10 ms（视觉 200 ms）/ ≤30 ms（视觉 100 ms）时 0%，≥40 ms 回到 gate filtered 水平——实验可测的本体感觉延迟阈值约 20–30 ms。
  2. **goal 时序解耦**（P1-EC-ONSET-01）：goal 起始 0.3–0.8 s（bar 固定 0.5 s）失败率完全不变——rescue 不依赖时序对齐。
  3. **无 goal 阻尼对照**（P1-EC-DAMP-01）：纯 current-state 阻尼（≥1e-11）救回 gate 的 200 ms 失败——goal 内容不特殊，救回成分就是零延迟自身状态反馈。
- 模型新增 `ff_mode`（goal/damping）、`ff_damp_gain`、`ff_self_state_lag_s`；20 个测试通过；Limitations 中 "goal onset mismatch was not tested" 已删除。

## 剩下的科学实验

1. **实验检验**：在施加视觉延迟时，稳定是否依赖携带当前 self-state 或 goal 的通路，而不是 efference copy 本身（模型侧已给出可证伪命题）。
2. **goal onset 失配**与更多 body 参数下的 feedforward 稳健性（可选）。
3. source 自适应求解器的精确语义（前向 Euler 下已证等价）。

## 边界

- 不是“果蝇使用 gating”的生物结论。
- 不是连接组约束模型。
- 不声称 100/200 ms 鲁棒性。
- 不声称 source/motor 差异。
- goal feedforward 是上界（goal 为指令、与刺激共享振幅/起始；假定当前本体感觉可用），不是生物机制主张。
- 不能替代 M2A-BRIDGE 的生物实验。
