# Response to Reviewers（三互盲报告 + 取证审计，逐条回应）

> 提交组件：MANUSCRIPT_DRAFT_V2.md（修订版）、CLAIM_TO_EVIDENCE_MAP.csv（C1–C55）、
> 修订图件（Fig 15/16/19–23）、runs/ 工件（全部数字可复核）。
> 缩写：DRAFT = 修订稿正文；MAP = claim map；W1 = runs/W1-REVISION-01。

## 总致谢

三位审稿人的核心判断都被实验证实或按其建议执行。特别是 R1-M1 与 R1-M2
的两项"阻断"质疑，直接产生了本稿最重要的修正：**必要性图景从"非经典快通路"
改写为"新鲜自身状态是根本成分、门控是条件性替代架构"**。所有新实验无论方向
均已入稿。

## Reviewer 1（计算可靠性）

- **R1-M1（经典对照混淆，阻断）** → 承认并解决。W1 跑了交叉条件：
  **pd_gate（即时 PD+门控）全延迟 0/8 失败；去光动通路 PD 0/8（含 p_gain
  ×0.5–×5）**（DRAFT R3、Fig 15、MAP C47）。原"快通路超出经典手段"的表述已
  **撤回**（DRAFT Abstract/R3/Discussion 均改写）；现在的主张：必要的是
  即时状态+慢通路抑制，快通路可为经典 PD。
- **R1-M2（Smith 标签过强，阻断）** → 双管齐下。(a) 实现**延迟内嵌观测器
  smith_dde**（内部回路携带传输延迟、区间创新校正）：8/8 全延迟失败（含
  50 ms，MAP C48、Fig 15）——标题主张获得公平检验；(b) 措辞收敛：
  Abstract 不再称 "full forward-model observer"，Limitations 与 Results 的
  观测器清单矛盾已修复（R1-m2 同步解决）；Artstein 型约简作为未测上界明示。
- **R1-M3（门控分解）** → 四格消融入 W1(c)：同架构内关门控 7/8–8/8 失败；
  触发信号仅用 |F_bar| 即保持 0/8（goal 增广非必需）（MAP C49、Fig 16）。
- **R1-M4（延迟构造）** → 承认成立并升级为正文核心：ψ/ω 免延迟时
  addition/graded/gate 全 0/8（MAP C50、Fig 16、DRAFT R3 末段与 Discussion
  重写段）。门控现在明确表述为"条件于自身状态被扣留"。
- **R1-m1（图号冲突）** → 全稿统一 1–14（模型）+ 15–16（W1 对照/消融）+
  19–22（实证）；指针与 MAP 同步。
- **R1-m2（Limitations 矛盾）** → 已修复（见 R1-M2a）。
- **R1-m3（C37 status）** → 已填 `current`。
- **R1-m4（参考文献 [21] 占位）** → 补全 Tanaka et al., Curr Biol 33,
  4960–4979.e7 (2023)。
- **R1-m5（新鲜度阈值精度）** → Discussion 增加网格披露（10 ms 间隔、
  30/40 ms 点夹逼、单 seed）。
- **R1-m6（dt 验证广度）** → 保留为 Limitations 既有条目并在 C38 表述中
  指向；本轮未扩验证（如实保留）。
- **R1-m7（k/N）** → 新章节全部改计数（3/8–5/8、7/8–8/8、8/8）；
  Statistics 增加全稿速率口径说明；旧章节逐图注明 run 数。
- **R1-m8（AI/ML 相关段）** → R3/Discussion 已含迁移段落；AI 迁移实验
  （W2，P4 计划）进行中，将增 Results 章节。
- **R1-m9（matched-budget 措辞）** → 定义入 R3 首次使用处（增益/结构匹配，
  非算力匹配）。

## Reviewer 2（实证统计）

- **R2-M1（四 vs 三数据集）** → Methods 新增 (iv) Currier m715hp3 条目
  （资格、预注册 75cc2434、封存状态与 +2.81/p=0.128 结果如实列出）；
  Intro 同步点名第四数据集；"four" 现与正文一致。
- **R2-M2（D12 治理）** → R5 明文披露：阶段门裁决发生在**看过分析之后**、
  数字不改、结论上限不变、常规读法为 null-convergent；MAP C44 同步改写。
  （C44 检验为预注册单侧方向；见 F2 轮 prereg。）
- **R2-M3（C46 地板统计）** → R6 重写：p=1/64 只测阳性不测特异性；
  净超额中位差 = +1.7；**声明未预注册配对检验故不作配对主张**；
  Discussion 功效句改为以净超额为锚（不再用原始统计量）。
- **R2-m1（+2~5 不可溯源）** → 同上，已改正为 +1.7。
- **R2-m2（图号）** → 同 R1-m1。
- **R2-m3（[21]）** → 同 R1-m4，并在 Results 首次提及处引用。
- **R2-m4（MDE 定义与 n=19）** → Statistics 增加：MDE=零分布 5% 分位绝对值
  （预注册分辨率规则，非功效曲线）；R4 注明 19 蝇为该数据集全部可用蝇、
  MDE≈5×观察效应——该样本下不可判定近乎必然。
- **R2-m5（定位动词）** → 改为"consistent with the source's localization"，
  并声明本工作未设排除边界。
- **R2-m6（预测幅度）** → 改为"positive increment, magnitude re-estimated"。
- **R2-m7（C37 status；C7/C8 重指）** → 均已修复。
- **R2-m8（0% 单元不确定性）** → Statistics 增加 rule-of-three 上界
  （0/8→37.5%、0/24→12.5%）；边界单元单/三种子标注（W1(e) 提供三种子，
  MAP C51）。

## Reviewer 3（NMI 适配）

- **R3-M1（单模型 AI 泛化，阻断）** → 接受并已执行。**W2/P4-AI 迁移实验完成**
  （三任务×六控制器族×30 随机植物×0–600 ms，预注册 6e56c187；结果见
  "The freshness principle transfers..." 章节与 Fig 23：F 全稳、C/E1 50–200 ms、
  F+ 退化 150–400 ms——C50 条件性跨系统迁移）。
- **R3-M2（估计器基线弱，阻断）** → 同 R1-M2（smith_dde 实现 + 措辞收窄 +
  Limitations 矛盾修复）。我们未实现 Artstein 约简——如实列为未测上界，
  不再以"full forward-model"覆盖。
- **R3-M3（必要性语义）** → 全稿改为**有界充分性措辞**（"within this model
  class and the enumerated architectures"，MAP C52 caveat 同步）；Abstract 主张句
  已加同款限定（"Within this model class and the enumerated architectures, fresh
  current self-state..."); 现行标题不含 unbounded 的 necessary 措辞。
- **R3-M4（包装）** → Abstract/Discussion 重排：AI 面向的三资产
  （必要性测绘、新鲜度阈值、伪脉冲方法学）前置于数据集角色；数据集角色
  在 Discussion 表述为 "a set of empirical constraints"（约束设定）。
- **R3-M5（方法学泛化）** → 注入-恢复验证列为 W3（进行中）；"must report"
  已降为对自相关行为数据的 state-dependent 检验建议；ML 离线评估偏倚关联
  段并入 Discussion（W3 一起交付）。
- **R3-m1（图号）/ m2（Limitations）/ m3（[21]）/ m4（C37）/ m5（数据集数）
  / m6（参考列表碎裂）/ m7（matched-budget 定义）** → 全部修复（同上各条；
  m6 已合并为单一 1–21 列表）。
- **技术失败 #4（形式稳定性）** → 全部"stabilize"表述已限定为有限窗口
  （2.5/6/10 s 失败判据）语境；无渐近主张。
- **技术失败 #5（单 seed）** → W1(e) 补三种子（C51）；MAP 逐行 seed 标注。
- **技术失败 #6（伪脉冲真值验证）** → W3 注入-恢复实验进行中，
  结果将并入 Empirical layer III 与图注。

## 取证审计（FORENSIC_AUDIT.md，23 项）

- 1 项确认错误（数据集计数）→ 已修（R2-M1 同源）。
- 3 项聚合歧义 → T4/T5 epoch 编号与 LPTC 分型计数已改；"+2~5"已改 +1.7。
- 3 项出处缺口 → c4eb583f 标签改为"探索轮 turn-manifest"；75cc2434 点名
  Currier；+2~5 见上。
- 2 项不可评估 + 14 项通过 → 无需改动。
- 其余全部数字（38-62%、8/8、r=1.0、-0.091/0.534/0.454、9/12/0.0503、
  +28.1/+20.1、6/6/+8.57/1/64/+6.9/0.24、六个 prereg 哈希）复核一致。

## 已补齐的实验性回应（原"尚在进行"项）

1. **W2/P4-AI 完成**：三任务×六族×30 随机植物×0–600 ms 栅格，预注册
   （SHA-256 6e56c187）单次运行。F 全栅格 0% 失败；C/E1 临界 50–200 ms；
   延迟内嵌观测器 150–300 ms 仍不及 F；**F+ 未门控叠加延迟项退化至
   150–400 ms（迁移了 C50 的门控条件性）**；恢复时间 F≈0.43 s vs C 2.7–4.1 s
   （幸存者内）。新 Results 章节 + 图 23 + claims C54/C55。
   过程修正全部留痕（零延迟 LQR 缺陷、σ 离散化解释、E2m 越界、
   hash() 种子不可复现——最终为存档性重跑）。
2. **W3 完成**：注入-恢复单调曲线，检测阈值 β=8（p=0.020）、β≥16 稳健
   （p≤4e-5）；地板指标与 RNG 漂移两次设计修正留痕。claim C53；
   R6 已扩写；ML 离线评估关联段入 Discussion。
3. 剩余：最终排版（图表嵌入、DOI 声明、补充材料）。
