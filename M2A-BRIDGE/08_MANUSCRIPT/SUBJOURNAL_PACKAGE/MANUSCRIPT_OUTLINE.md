# SUBJOURNAL_PACKAGE — 完整稿件架构（D16）

> 2026-10-29。目标：一篇完整的子刊级论文（推荐投递顺序见 §7）。
> 本文件是逐节蓝图：每节列出内容、claim、证据指针（工件路径）、图件。
> Track C 的已审章节与图件直接复用（不重开已关闭的审稿问题）。

## 1. 题名候选

1. **"Fresh self-state, not delayed extrapolation, stabilizes delayed visual
   steering: modeling and tests across four public neural-behavioral datasets"**
2. "When is action-related state information necessary for feedback control?
   Computation, classical controls, and public-data tests in Drosophila"
3. （短版）"The freshness advantage: self-state, delay, and gating in fly
   steering across model and data"

## 2. 一句话论点（全文骨架）

在延迟视觉转向模型中，**维持稳定性所需的是新鲜自身状态进入快速反馈通路**
（而非对延迟观测的任何阶估计器），门控具有模型内的独立贡献；在四个公开
神经-行为数据集上的系列实测给出了这一命题的经验边界、一个真实运动历史
的预测信息信号、以及"状态依赖扰动检验"的方法学陷阱——全部结果无论方向
如实呈现。

## 3. 章节架构（claim → 证据 → 图）

### Intro（~700 词）
- 延迟视觉反馈的控制问题；EC/自身状态假说；Fuller 2014 等先例（refs 14–17
  沿用）；本文问题：什么信息是计算必要的 + 真实回路是否有其痕迹 + 怎样
  才算证据（方法学立场）。

### R1 计算框架与延迟失稳（复用 Track C 主体）
- 增益 × 来源 × 门控；临界延迟；判据敏感性（C10/C33）；窗口效应（C23）。
- 证据：P1-EC-DELAY/GAIN/WINDOW 全链；图 2–5（复用）。

### R2 失效的替代解释：估计器与经典控制（P2-OBSERVER 两阶段）
- R2a 平凡 Taylor 估计器不救回（C37）；R2b **Smith 前向模型观测器
  （精确/10% 失配）≥100 ms 全失败**；R2c **匹配预算即时经典 PD 38–65% 失败**；
  R2d 门控独立贡献（对 C19：同即时状态 gated 0% vs ungated 62–75%）；
  R2e 必要成分=新鲜自身状态（C35 阻尼）。
- 证据：`runs/P1-EC-OBSERVER-01/`、`runs/P2-OBSERVER-02/`、CLAIM C39–C44（待编）。
- 图：新 fig —— 失败率热图（规格 × 延迟，六规格）+ 机制示意。

### R3 新鲜度阈值（复用 Track C self-state 章节）
- 20–30 ms 阈值 dose-response；onset 解耦；无 goal 阻尼（C34–C36）。图 14。

### R4 公开数据实测 I：Tanaka 反证数据集的基准与模型选择
- R4a 三分支基准复算（Mi4 逐值 r=1.0；T4/T5 实验 epoch r≥0.94；LPTC
  无一致静止抑制——**外部锚定**）（`P3-A-BASELINE-01`）。
- R4b 行为级 graded-vs-gate 模型选择：`INCONCLUSIVE_BY_RESOLUTION`
  （P3-ROUND-2，诚实分辨率声明）。
- R4c T4/T5 层抑制≈0 与闪烁抑制存在（P3-CE-FIG4）——机制定位约束。
- 图：新 fig —— 基准对账散点 + 模型选择 ΔR² 点图（含零分布）。

### R5 公开数据实测 II：F&S 飞行 HS——运动历史的增量信息
- 同步膜电位+翅拍（12 动物 LOMO）：ΔR² 中位 +0.056、9/12 正、p=0.0503、
  CI 跨 0（D12 数字保留）；跨动物尺度失配 caveat；主张="额外预测信息"。
- 图：新 fig —— 逐动物 ΔR²森林图 + 偏差防范示意。

### R6 公开数据实测 III：状态依赖扰动检验——陷阱与残差方法
- R6a naive 终点被自相关伪影击穿（DISCRIM-01：+28.1 vs 伪脉冲 +20.1）；
  R6b 残差管线压缩伪影（+6.88）但 6/6 正超出（+8.57）低于 3× 门槛
  （DISCRIM-02）；R6c **方法学结论**：状态依赖扰动分析必须有伪脉冲对照
  与基线图谱剔除；净超出量记录为候选信号。
- 图：新 fig —— 两轮判别的对照阶梯图（主效应 vs 三对照，01 与 02 并排）。

### Discussion（~1200 词）
- 综合：必要信息=新鲜自身状态（模型内）；真实回路携带运动相关信息
  （F&S）但状态依赖的扰动特异性在此 n 不可建立；计算与生物的差距本身
  是本文结果。定位：计算约束 + 实证边界 + 方法学，非机制发现。
- 预测：可检验清单（新鲜度阈值实验、残差终点在可扩 n 数据上的复检）。
- 限制：模型内结论边界；每数据集 n 与混淆；无环路因果。

### Methods（复用+新增）
- Track C Methods（原样）；observer 对照实现；四个数据集的字段级资格与
  预处理（指针到资格文档）；统计（置换/自助/LOMO）；预注册与冻结哈希表
  （全部轮次的 prereg SHA 列表——透明性卖点）。

## 4. 声明地图（扩展现有 CLAIM_TO_EVIDENCE_MAP）

新增行（编号续 C38 后）：
- C39 Smith 观测器（精确/失配）不救回（P2-OBSERVER-02 summary.json）
- C40 匹配预算即时 PD 不救回（同上）
- C41 门控独立贡献（C19 对照 + P2-OBSERVER-02）
- C42 Tanaka 三分支基准复现（P3-A summary）
- C43 行为级模型选择不可判定（P3-ROUND-2 summary，含 Δ_crit）
- C44 F&S 运动历史增量信息（D12 数字+裁定并列）
- C45 naive 状态依赖检验被自相关击穿（DISCRIM-01 summary + 对照）
- C46 残差方法压缩伪影但未达特异性门槛（DISCRIM-02 summary + 对照）
- 全部 status=current；caveat 列逐一填写。

## 5. 图件计划（10 图）

| # | 内容 | 来源 |
| --- | --- | --- |
| 1 | 模型与延迟问题示意 | fig_mechanism 复用改版 |
| 2 | 失稳图景（增益×门控×延迟） | fig2/3 复用 |
| 3 | 观测器/经典控制失败热图 | 新（P2-02 数据） |
| 4 | 新鲜度阈值 | fig14 复用 |
| 5 | Tanaka 基准对账 | 新（P3-A） |
| 6 | graded-vs-gate 不可判定 | 新（P3-ROUND-2） |
| 7 | F&S 逐动物 ΔR² | 新（F2） |
| 8 | 判别两轮对照阶梯 | 新（DISCRIM-01/02） |
| 9 | 方法学流程图（预注册/对照阶梯） | 新示意 |
| 10 | 综合讨论图（必要信息层级） | 新示意 |

## 6. 期刊定位（推荐顺序）

1. **eLife**（Reviewed Preprint 路径快；计算+实证+方法学的组合接受度高）
2. **PLOS Biology**（完整叙事+开放数据纪律契合）
3. **Nature Communications**（若强调"跨数据集的计算约束"框架）
4. 备选：Current Biology（短版+方法学焦点）

Track C 原稿（PLOS CB 计算版）保留为可独立投递的备选；若子刊整合稿
先投，Track C 作为其"计算专文"引用自己（避免一稿多投冲突——投稿前
须最终二选一，见 D16 后续）。

## 7. 执行顺序

1. 本架构 owner 过目（题名/定位/是否吸收 Track C）；
2. 扩展 claim map（C39–C46）；
3. R1–R3 复用章节并稿（从 MANUSCRIPT_REVISED.md 抽取）；
4. R4–R6 新写作；Methods 冻结哈希表；
5. 新图件制作（dataviz 规范）；
6. 独立审稿轮（nature-reviewer 三互盲）→ 修订 → 投稿包。
