# DATASET_ELIGIBILITY_MATRIX（P3-B / D10）

> 2026-10-28。字段级资格核验状态汇总。"准入"指可进入探索/建模轮；确认性轮须另开预注册。

| 数据集 | 入口 | 独立单位与 n | 关键字段/同步 | 干预轴 | 准入 | 阻塞项 |
| --- | --- | --- | --- | --- | --- | --- |
| **Currier & Nagel 2018**（Dryad m715hp3） | doi:10.5061/dryad.m715hp3 | 蝇；exp1=120（被试内4条件）、exp2c/s=11/12、exp4h=12 等 | 逐蝇 H/dH 50 Hz 闭环；条件级刺激标签，无逐事件日志 | antenna-stabilized（UV 胶固定触角=阻断风感）；风速梯度 | `QUALIFIED_BEHAVIORAL`（已审计+身份审计修订） | 无延迟维度；主检验已封存（INCONCLUSIVE） |
| **Tanaka/Clark 2023**（Dryad bcc2fqzjz，行为+成像） | doi:10.5061/dryad.bcc2fqzjz | 蝇；T4 13 / T5 15 / LPTC 10–12×5 类型 / Mi4 10 / fig1_05 27+17 / fig3 19–20 | indFly×snipMat（成像38–93点迹线；行为50 Hz）；**成像与行为同管线、球速度通道存在**（p2_normalizedWalking/p4_normalizedTurning 字段） | 遗传筛选（细胞类型）；刺激条件操纵（静止/闪烁/岛屿）；**无延迟操纵、无神经干预** | `QUALIFIED_NEURAL_AND_BEHAVIORAL`（四分支独立单位已核验；P3-A 复算通过） | 无延迟维度→H2 大概率 `MECHANISM_NOT_IDENTIFIABLE`（fig1_05 行为级例外） |
| **Fischer & Schnell 2022**（EDMOND doi:10.17617/3.92；代码 Zenodo 6988868） | EDMOND API 已枚举 194 文件 9.49 GB | 蝇；主实验 **N=13**（62 saccade vs 65 non-saccade 试次，ipsilateral looming）；基因型 2×WTCS + Gal4/UAS-GFP（GMR81G07/GMR27B03） | **F1 已核验（2026-10-28，`fs2022_audit/F1_VERIFICATION.md`）**：原始 .mat=v7.3，5 硬件通道共享单一时钟（Vm、WBA_L/R、辅助信号、刺激 marker 0/3V 打标）；ID 链（文件名↔experParams）逐字一致；**srate 逐会话（实测 10 kHz 与 15 kHz 并存）**；9 列处理格式为衍生输出（.neomat/管线），L−R WSA 可从原始通道+Zenodo 代码重建 | **无实验者神经干预**（GFP-only；"hyperpolarization"=HS 生理性超极化；hyPol/noPol/DePol=试次分类） | **`QUALIFIED`**（F1 样本核验通过；同步性/可配对性成立） | n=13 偏小；WSA≠运动指令；单位换算须走原代码；已知缺陷"one experiment missing hyperpolarization period"须会话级质量核验 |
| OSF 7mq9j（Cubico 2023） | osf.io/7mq9j | — | 空壳 | — | `BLOCKED_FILES_MISSING` | 数据不在 |
| Fischer & Schnell 代码 | Zenodo 10.5281/zenodo.6988868 | — | phifisch/flyEscapeSaccades v1.0.0（26.4 MB） | — | 可用（GPL 类开源，license 标"other-open"，使用前核对 LICENSE 文件） | — |

**P3-B 三问的答复（Fischer & Schnell）**：
1. **共同时间基准、逐试次配对**：成立（9 列共享 time；loom/wb/神经同文件）。
2. **刺激/转向/无转向可分、不泄漏**：成立（saccading vs straight 预分选 + CWT 检测 + looming vs spontaneous 分档；建模时按整动物切分训练/检验即可防泄漏）。
3. **存在竞争模型给出不同预测的条件**：**部分成立**——"自发 vs looming 触发转向"与"同刺激 saccade vs 直行"是 COMPETING_MECHANISMS_PREREG §3 冻结的判别条件；但无神经干预轴，H1/H2 的最终区分依赖潜伏期结构的定量预测，n=13 下预计分辨率有限。
