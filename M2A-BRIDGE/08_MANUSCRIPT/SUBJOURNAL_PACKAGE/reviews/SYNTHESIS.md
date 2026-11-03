# CROSS-REVIEW SYNTHESIS（post-review；不展示给审稿人）

> 2026-10-29。基于三份冻结报告（R1 计算可靠性 / R2 实证统计 / R3 NMI 适配）
> 与各自立场：R1 = Major revision with path to acceptance（2 阻断）；
> R2 = Major revision（0 阻断）；R3 = Reject & resubmit（2 阻断）。
> 取证审计（FORENSIC_AUDIT.md）另列，不并入审稿共识。

## 1. 共识阻断项（≥2 独立报告）

### C-B1 估计器类不公平 / "Smith"标签过强（R1-M2 + R3-M2，双阻断）
两审稿人独立指出：实现的是**朴素前向模型**（claim map C39 自己承认
"DDE-aware observer untested"），不是含延迟的经典 Smith/Artstein 构造；
而标题"not delayed extrapolation"与摘要"a full forward-model observer"
以此为支撑。另 R1-m2 与 R3-m2 **独立发现同一处文档矛盾**：Limitations 写
"only a trivial Taylor estimator"，Results/C39 却描述了 Smith 样观测器。
**修法（二选一或都做）**：(a) 实现延迟感知观测器（内部模型嵌入传输延迟
或 Artstein 型约简）重跑 50–200 ms 网格；(b) 收窄标题/摘要措辞到
"delayed extrapolation and naive forward-model observers"。同时修复
Limitations/Results 矛盾。

### C-B2 经典对照混淆（R1-M1 阻断 + R3 技术失败#3 共识）
pd_instant 在**未门控的延迟光动回路**存在时失败——重新演示了"延迟通路
必须被门控"，没有隔离"经典即时状态控制本身是否足够"。R1 指出关键点：
**gate_goal 本身就是经典 PD-on-current-state + 门控**——决定性的
"门控×经典"交叉条件从未跑过。**修法**：跑 (i) pd_instant+grating 门控、
(ii) pd_instant+光动通路移除、(iii) 可选整定 PD（留出参数子集调参）。
若它们救回 → 重写必要性图景（必要的是即时状态+慢通路抑制，快通路不必
非经典）；若失败 → 现主张获得真正支撑。

### C-B3 单模型 AI 泛化性（R3-M1 阻断 + R1-m8 + R3-M4 共识）
NMI 判据核心：贡献须推进智能系统设计。单一果蝇玩具模型 + 无人工控制
任务演示 = 不成立。**修法**：P4-AI 迁移实验（计划已起草
`P4_AI_TRANSFER_PLAN.md`：延迟倒立摆/姿态保持/部分观测 LQR ×
估计器/经典/新鲜+门控/上界四族；失稳边界+扰动恢复判据）。

## 2. 共识主要项（非阻断但必修）

| 项 | 来源 | 修法 |
| --- | --- | --- |
| 门控独立贡献的分解缺口（跨架构比较而非同架构消融；torque vs trigger 未分离） | R1-M3 | 四格消融：gate goal 关门控 / 门触发仅用\|F_bar\| / 互换 |
| 延迟构造制造必要性（ψ/ω 只延迟于非救回通路） | R1-M4 | ψ/ω 不延迟的 addition/graded/gate filtered 稳健性扫描 |
| D12 阶段门治理不可评估（C44） | R2-M2 | Methods 引 D12 规则原文 + 冻结时序 + 检验单侧声明；摘要去"consistent" |
| C46 地板 vs 超出量统计（p=1/64 测的是阳性不是特异性；"+2~5"与中位差 +1.7 不可对账） | R2-M3 + R2-m1 | 动物级配对 real-vs-control 检验或明示未设计；净超额+区间；重写 Discussion 功效句；删/改"+2 to +5" |
| "four datasets" 与 Methods 三个不符 | R2-M1 + R3-m5 | 补第四数据集（Currier m715hp3：资格+封存轮状态）或全文改 three |
| 必要性语义超出方法（枚举消除 ≠ 必要） | R3-M3 | 标题/摘要改为有界充分性措辞（"within this model class and the enumerated architectures"），或补形式论证 |
| 伪脉冲方法无真值验证 + 全领域处方过强 | R3-M5 + R3 TF#6 | 注入-恢复实验（半合成：在真实行为上植入已知状态依赖效应验证管线灵敏度）；"must report"降为recommendation；补 ML 离线评估偏倚关联段 |

## 3. 三/二方共识文书项

- **图号冲突**（R1-m1+R2-m2+R3-m1）：新图统一改为 15–19，全文+claim map 指针更新。
- **参考文献 [21] 占位**（三方）：补全；另 R3-m6 修复参考文献列表碎裂。
- **C37 status 空缺**（三方）；C7/C8 指向旧稿件文件（R2-m7）。
- **单 seed 边界扫描**（R3 TF#5 + R2-m8）：C27/C30 关键单元补多 seed；
  0/N 单元补 rule-of-three 上界。
- 措辞集（R1-m5/6/7/9、R2-m4/5/6、R3-m7）：新鲜度网格披露、k/N 报告、
  MDE 计算披露、"matched-budget"定义、定位动词归属、预测幅度措辞。

## 4. 修订计划（执行序）

**W1 模型补跑套件**（解决 C-B1a、C-B2、§2 前两项、R3 TF#5——全部轻量模拟）：
延迟感知观测器；门控×经典交叉；四格分解；ψ/ω 免延迟扫描；边界单元多 seed。
**W2 P4-AI 迁移**（C-B3；计划已备，预注册后运行）。
**W3 伪脉冲注入-恢复验证**（R3 TF#6）。
**W4 文书修订**（图号、数据集计数、D12 披露、C46 统计、必要性措辞、
参考文献、claim map 卫生、全部 minor）。
**W5 复审**（修订后同三视角复检关键点 + 审计数字复核）→ 投稿包。

## 5. 综合评估

三审稿共同认可的资产：负结果纪律、预注册+哈希、控制决定解释、claim map。
共同要求的核心：把"必要性"主张补上**公平的估计器与经典对照**（W1）并
证明**跨系统迁移**（W2）——这恰好也是 D10 假说第三腿的完成。
方向明确、全部可解、无需新生物数据。

---

## 6. 取证审计补充（FORENSIC_AUDIT.md，23 项）

与审稿交叉验证一致，并新增精确修法（并入 W4）：
- **确认错误×1**：标题/摘要/引言/Methods 的"four datasets"仅枚举三个
  （与 R2-M1/R3-m5 同源）→ 补 Currier m715hp3 数据集条目（资格+封存轮）。
- **聚合歧义×3**：(a) T4/T5 "r≥0.94 仅实验 epoch"需明示 epoch 编号
  （probe epoch 1–2 为 0.84–0.90/0.54–0.75）；(b) LPTC "11/12"实为
  HS 11/12、CH **10/12**——按类型分列；(c) 见下。
- **出处缺口×3**：(a) "c4eb583f" 是探索轮 round_manifest 哈希而非
  PREREGISTRATION——改标签；(b) "75cc2434" 确为 P3-VISORIENT-01 预注册
  但须点名 Currier 数据集；(c) Discussion "+2~5 LL/动物"不可溯源
  （真实中位净超额=+1.69，与 R2-m1 同源）→ 改为 +1.7 并给区间。
- **其余数字全部对账通过**（38–62%、Smith 8/8、Mi4 r=1.0、−0.091/0.534/
  0.454、9/12/+0.056/0.0503、+28.1/+20.1、6/6/+8.57/1/64/+6.9/0.24、
  六个 prereg 前缀、C39–C46 行文一致）。
