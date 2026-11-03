# Cross-review synthesis — Round 2 (post-review; not shown to reviewers)

- 日期：2026-10-27
- 输入：三份互盲冻结报告 `REVIEW_ROUND2_R1.md`（一致性/证据）、`REVIEW_ROUND2_R2.md`（设计/稳健性）、`REVIEW_ROUND2_R3.md`（定位/可读性），以及独立取证审计 `FORENSIC_AUDIT_ROUND2.md`。
- 规则：共识 = 至少两份报告独立提出同一底层问题；审计发现单列，不冒充审稿共识；冻结报告未被改动。
- 说明：R2 首个实例运行 2 小时无产出被终止，重试实例在 11 分钟内完成并落盘；两实例互盲规则均未被破坏（重试实例被明确禁止读取 R1/R3 报告）。

## Consensus strengths

- **自我纠错文化**（三份一致）：窗口伪影、V-clip 伪影、撤回的 200 ms 临界延迟、撤回的线性稳定性都公开报告而非掩盖；R1 称其为论文最有价值的部分之一。
- **数字可追溯**（三份一致）：三份报告各自抽查的 run 汇总与正文几乎全部吻合；审计 AUD-14 复核了全部 run 计数与头条数字，全部 reconcile。
- **机制控制阶梯设计**（R1、R2、R3 均点名）：command copy → current-visual oracle → goal delay → self-state ablation 构成连贯的定位链；self-state ablation 数字被 R2、R3 分别独立验证为精确吻合。
- **范围纪律**（三份一致）：Scope note、Limitations、摘要都明确不声称生物机制、不复现 source 零延迟排序、feedforward 是上界。
- **统计哲学显式**（R2、R3）：参数网格是设计不是样本，不乱加 p 值。

## Consensus blocking concerns（修稿前必须解决）

1. **Gate-threshold 概括句与其自身证据矛盾**（R1-M1 + R2-M2；R2 标 Blocking；审计 AUD-01 证明）。`allnone_motor` 在 threshold 0.5、50 ms、clip 下为 25%（4/16），100 ms clip 为 62.5%；Fig. 4 只画了 `allnone`。摘要、Results、Discussion、Fig. 4 图注四处的 "0% across every threshold" 必须按变体重新表述，并补 run 名称映射。
2. **Claim-to-evidence map 与修订稿互相矛盾**（R1-M2 + R2-M6 + R3-M1，三份一致；审计 AUD-12）。C2/C3 仍断言已撤回的 200 ms 临界延迟与 motor-copy 主张，C7/C8 指向旧稿，C9/C15/C16 指向已删除的图，窗口/V/阈值/adaptive-03/goal-mismatch 等修订稿主张没有行。必须按修订稿重建。

## Other consensus major concerns（≥2 份独立提出）

3. **"The continuous models failed in 100% of runs at 100 ms" 为假**（R1-M3 + R2-m1；AUD-02）：graded_motor 为 62.5/75/75%。
4. **"reproduced identically across three seeds" 过强**（R1-M5 + R2-M1；AUD-04）：graded 家族与 gate goal 属实；gate filtered 在 100 ms 为 0/0/12.5%、140 ms 为 75/62.5/62.5%。
5. **变体命名映射缺失**（R1-m7 + R2-M2/m7 + R3-m5，三份一致）：稿件名（gate filtered / graded unfiltered oracle…）与 run 名（allnone / graded_motor…）之间没有映射表。
6. **预测数量不符**（R1-m2 + R2-m5 + R3-m2，三份一致）："five predictions" 后只有 4 条编号，散文里另有 2 条。
7. **六条参考文献只出现在文献表**（R1-m5 + R3-m1；AUD-13）：Erginkaya、Lappalainen、Wang-Chen、Westeinde、von Holst、Dhiman。von Holst 未被引用在一篇 reafference 论文里尤其刺眼。
8. **0.15% 与 0.3% 矛盾**（R1-m1 + R3-m3；AUD-09）：Discussion 把 0.15 度的绝对差标成了百分比；正确值 0.255% ≈ 0.3%。
9. **"the same as the current-visual oracle" 在 200 ms 为假**（R1-m4 + R2-m3；AUD-11）：0.75 vs 0.625，仅 4/5 个延迟相同。
10. **头条一（gain）的配置范围**（R2-M4 + R1-m6；AUD-08）：单配置无噪声无 seed（n=12，9/12 vs 12/12），而 addition 基线在带噪声运行中从 75% 漂到 100%；Methods 未枚举哪些 sweep 带噪声。

## 单份报告的 major（无共识，但有审计支持或值得处理）

- **R1-M4 / AUD-03**：140/200 ms "75% to 100%" 区间下限错误（实际 62.5%）。
- **R1-M6 / AUD-07**：ODE 等价句的 "floating-point precision" 措辞被 0.205/4.12 rad 的前缀差证伪；失败分类 96/96 一致的主结论不受影响。
- **R2-M3**：failure-criterion 敏感性（claim map C10 已记录 ~60 ms 边界）正文未报告，而窗口与 V 都做了同等透明度的敏感性。
- **R2-M5**：feedforward 的三个叠加特权（goal 与刺激同振幅同起始、当前本体感觉无延迟假设、同一增强信号同时驱动扭矩与 gate）——现有 ablation 只证明 self-state 的必要性；建议窄化措辞或补一个无 goal 的等幅 current-state 对照 + goal onset 解耦对照（可选强化，非接收条件）。
- **R3-M2**：未与 forward-model / Smith predictor / delay-compensation 文献对话——定位与原创性轴的最大缺口。
- **R3-M3**：摘要与 Results 的 self-state 结论缺 "in this architecture" 限定（Discussion 有）。
- **R3-M4**：command-copy/feedforward 段落在 Discussion 里排在 Limitations 之后，以 "We then implemented" 开头，像 Results 续写。
- **R3-M5**：可用性声明指向工作区相对路径，PLOS 需要公共仓储 + DOI（owner-side）。
- **R1-M5 之外的 R1-m8**：gain 200 ms 的 25–42%（GAIN-01）与 window 的 62.5%（WINDOW-01）被并置成同一句话，需标注各自来源。
- **R1-m10**：Fig. 4 图注未注明阈值面板是 gate filtered。
- **R1-m12 / R2-m8 / R2-m9 / R2-m6**：sweep 维度欠说明、dt=2e-4 与 solver_check 未引用、0 失败格无不确定性表述、长延迟轮未列入 Methods（后者在本轮整合时一并处理）。

## Where emphasis differs across reviewers

- R1 最在意**每一句数字与其工件的逐字对账**，给出了最细的修正文案。
- R2 最在意**设计是否支撑措辞的强度**（seed、criterion、feedforward 特权、gain 配置），并是唯一标 Blocking 的人。
- R3 最在意**读者与定位**（control-theory 对话、摘要密度、Discussion 顺序、DOI），并认为核心案例在实质上已成立。
- 三者对"核心方向成立、修的是文本与文档"完全一致。

## Forensic consistency findings（审计层，非审稿共识）

- confirmed_internal_error ×9：AUD-01、02、03、04、05、07、09、10、11（详见 `FORENSIC_AUDIT_ROUND2.md`）。
- aggregation_ambiguity ×2：AUD-06（18.8% vs 12.5% 属不同 run）、AUD-08（75% vs 100% 属不同配置）。
- provenance_gap ×2：AUD-12（claim map）、AUD-13（Methods 清单 / /tmp 路径 / 未引用文献 / 陈旧图）。
- passed ×2：AUD-14（全部 run 计数与头条数字 reconcile）、AUD-15（复现门：16 测试 + 各轮确定性证据 + P1 快照 768 行）。
- 审计与审稿的差异：AUD-03（75–100% 区间）与 AUD-07（ODE 措辞）只有单份报告对应，属编辑层补充；AUD-01/02/04 与审稿共识重合，属审计强化。

## Minor revision checklist

1. 修正 75%–100% 区间为 62.5%–100% 或限定变体（AUD-03）。
2. 修正 duty 第四值 0.65 → 0.64（AUD-05）。
3. 删除或限定 ODE "floating-point precision" 从句（AUD-07）。
4. 统一 0.3% / 0.15%（AUD-09）。
5. 修正预测计数（AUD-10）。
6. "same as the oracle" → "four of five delays" 或给双序列（AUD-11）。
7. 18.8% 与 12.5% 各自标注 run 与 n（AUD-06）。
8. Methods 枚举带噪声的 sweep；标注 GAIN-01 与 WINDOW-01 来源（AUD-08）。
9. 补 run 名 ↔稿件名映射表（共识 5）。
10. 六条文献入正文或删除（共识 7）。
11. 归档八张陈旧图（R1-m9）；Fig. 4 图注注明 gate filtered（R1-m10）；C6 的 /tmp 路径改持久化（R1-m11）。
12. 摘要自状态句加 "in this architecture"（R3-M3）；摘要 382 词、先用平实语言替换 "V-term treatments"（R3-m4）。
13. Discussion 把 command-copy/feedforward 段前移到 Limitations 之前并改写为讨论语气（R3-M4）。
14. 引言/讨论补 forward-model 与 Smith predictor 段落 + von Holst 引用（R3-M2）。
15. 可用性声明指向公共仓储 DOI（R3-M5，owner-side）。
16. 整合本轮新实验（fine/long-delay、noise、phase、traj）与新图到 Methods/Results/图组，并重建 claim map（AUD-12/13 的整合部分）。

## Broad-interest / significance readout

- 面向计算神经科学与控制取向读者：把 graded vs gating 的定性争论变成可操纵变量（gain、delay、threshold、V 形状、self-state 通路），并给出带参数的可证伪预测。
- 方法学价值可迁移：有限窗口与饱和非线性会"制造"稳定性排序——对任何闭环仿真稳定性主张都是警示。
- 无新生物数据、不复现 source 行为排序、单一体系结构内结论——重要性评为中等，适配 PLOS Computational Biology 而非旗舰。

## Most important issues to resolve before a strong PLOS CB case is established

1. 修掉三个摘要级假句（gate-threshold 概括、continuous100%、three-seeds identical）并同步 Fig. 4（共识 + 审计）。
2. 按修订稿重建 claim map（三份一致）。
3. 补名称映射、预测计数、0.3%、oracle 4/5 等对账修正（共识清单 5、6、8、9）。
4. 补 control-theory 定位段与六条文献引用（R3）。
5. Methods 纳入本轮全部新 sweep 与噪声枚举；整合新图（含长延迟、细网格、机制图）。
6. Owner-side：DOI 仓储与作者信息。

结论：三份报告与审计一致认为**核心计算结论成立，修订是文本、对账与文档层面的**；按上述清单完成即可达到可投稿状态。
