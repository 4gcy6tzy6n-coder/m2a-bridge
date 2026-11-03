# 计算 pilot：EC 类型 × 反馈延迟

> **2026-10-27 审稿后更正（重要）**：本页早期记录的 “allnone 100/200 ms 鲁棒” 已被 window、V-clip、gate-threshold 实验推翻。6 s 窗口下 allnone 在 140 ms 从 3/16 升到 11/16；smooth V 下 100 ms 从 0% 升到 75%。当前有效结论以 [33 修订稿](33_manuscript_track_c.md) 为准。本页保留为历史实验记录，不再作为论文主张。

> 轮次：`P1-EC-DELAY-01`（2026-10-27）
> 代码：`M2A-BRIDGE/06_JOINT/ec_model.py`、`run_delay_sweep.py`
> 结果：`runs/P1-EC-DELAY-01/experiment/outputs/`

## 1 问题

Canelo et al. 2024（eLife 93487）比较了 addition-only、graded EC、all-or-none EC 三种飞行转向模型，支持 all-or-none。但他们的延迟比较只在 Fig. S3，且不是“EC 类型 × 感觉反馈延迟”的主实验。本 pilot 补这一格：

> 在显式感觉运动反馈延迟下，四种 EC 变体的稳定性是否分开？

四种变体：

- `addition`：bar + grating 扭矩直接相加，无 EC。
- `graded_sensory`：`omega_ec` 由延迟的 `F_bar` 驱动，代表延迟的感觉估计。
- `graded_motor`：`omega_ec` 由当前 bar 扭矩驱动，代表运动拷贝。
- `allnone`：`|F_bar| > 1.5e-11` 时把 grating 增益置零。

## 2 方法

- 方程移植自 `nisl-hyu/flightsim` 的 MATLAB 实现（`sim_bar1`、`sim_ek1`、`sim_allnone`）。
- 参数：`I=6e-14`、`beta=1e-11`、`tau_bar=0.05`、`tau_opto=0.04`、`k_opto=25e-12`、`gate_threshold=1.5e-11`。
- 扩展：对 `(theta_bar, dtheta_bar, theta_grating, dtheta_grating, heading, omega)` 加显式延迟。
- 网格：4 模型 × 12 参数组（I、beta、k_opto）× 16 延迟（0–0.30 s，20 ms 步长）= 768 runs。
- 失败定义：heading > 2π 或 |omega| > 100 rad/s 或状态非有限。

## 3 结果

| 模型 | 临界延迟中位数 | 均值 | 140 ms 失败率 |
| --- | --- | --- | --- |
| addition | 0.04 s | 0.037 s | 12/12 |
| graded_sensory | 0.03 s | 0.030 s | 12/12 |
| graded_motor | 0.02 s | 0.137 s | 4/12 |
| allnone | 0.25 s | 0.240 s | 2/12 |

- **graded_sensory 最脆弱**：临界延迟几乎不受身体参数影响，说明问题在 EC 回路本身。
- **allnone 最稳健**：0–0.12 s 失败率为 0；少数失败出现在高 grating 增益 + 小身体时间常数。
- **graded_motor 双峰**：低惯性/高阻尼组可存活到 0.30 s；`I ≥ 1.2e-13` 且 `drag=1e-11` 组在 0.02 s 就失败。
- **addition 早期失败**：没有 EC，延迟自运动反馈直接破坏稳定。

## 4 解释（待验证）

- 延迟的 `-omega_d` 项是一个延迟负反馈；高增益下会产生振荡。
- graded_sensory 把 `omega_ec` 也放进这个延迟回路，形成第二个积分器，因此最早失稳。
- allnone 在 bar 转向时切断 grating 回路，移除了延迟反馈，因此最稳健；代价是失去连续控制。
- graded_motor 用当前运动拷贝替代延迟感觉估计，部分恢复稳定，但是否成功取决于身体时间常数与 grating 增益的相位关系。

## 5 不能说的话

- 不能声称“果蝇使用 all-or-none EC”；这只是一个 toy model 的稳定性预测。
- 不能把 140 ms 的失败率写成生物实验结论；延迟是模型参数，不是测量值。
- 不能把 `graded_motor` 的双峰写成“运动拷贝更好”；它依赖参数，且没有数据拟合。
- 不能把本 pilot 当作 M2A-BRIDGE 的跨系统证据；它是 B0 级计算工作。

## 5.1 鲁棒性轮次（P1-EC-DELAY-02）

在噪声 `1e-13`、2 seeds、4 个身体时间常数（3/6/12/24 ms）、2 个 grating 增益下，1,520 runs：

| 模型 | 临界延迟中位数 | 140 ms 失败率 |
| --- | --- | --- |
| addition | 0.02 s | 16/16 |
| graded_sensory | 0.02 s | 16/16 |
| graded_motor | 0.015 s | 10/16 |
| allnone | 0.20 s | 3/16 |
| allnone_motor | 0.11 s | 12/16 |

- 排序保持：allnone 最稳健，graded_sensory/addition 最脆弱。
- **门控信号本身是变量**：用延迟感觉信号门控（allnone）比用当前运动拷贝门控（allnone_motor）更稳；后者会在转向未结束时提前重开 grating 回路。
- phase diagram 显示 graded_sensory 的失败几乎与 `tau_body` 无关；allnone 的失败集中在高 grating 增益 + 特定 `tau_body`。

## 5.2 1 ms 细网格（P1-EC-DELAY-03）

0–100 ms 步长 1 ms、100–300 ms 步长 10 ms；三个代表参数集（源参数、高增益、慢身体）。1,815 runs。

| 模型 | critical delay 中位数 |
| --- | --- |
| addition | 18 ms |
| graded_sensory | 15 ms |
| graded_motor | 10 ms |
| allnone_motor | 110 ms |
| allnone | 200 ms |

细网格确认排序，并把 graded_sensory 与 allnone 的差距拉到 13 倍。主图改用 `fig2b_critical_delays.png` 的点图；`failure_rate_fine.png` 因只有 3 个参数集而呈锯齿，仅作补充。

**阈值敏感性（post-hoc）**：把失败判据改为 `|ω|>50` 后，allnone 的中位临界延迟降到 ~56 ms，allnone_motor ~58 ms；两者基本重合。`|ω|>100` + heading>2π 时才是 200 ms vs 110 ms。稳健的是“graded 最先失稳”，而 gating 优势的大小和门控信号差异依赖失败判据。

**零延迟背景增益检查（重要 caveat）**：在单 bar + 单 grating step 的刺激下，高/低 grating 增益的峰值转向比为 addition 0.9148、allnone 0.9830、graded_motor 0.9996、graded_sensory 0.9998。也就是说，本模型在零延迟下**没有复现** Canelo 2024 的“all-or-none 才解释背景不变性”排序。论文已明确写成“动机引用，不是复制”。

**源协议检查**：用源论文的缩放参数（I=6e-4、beta=1e-1、P=1.0、V=1e-2）、恒定 grating 和 0.05/0.7 增益重跑：门控阈值接近 0（1.5e-12）时 allnone 完全不变（59.956 vs 59.956°）；graded 在单位 EC 增益下也不变，部分增益 0.5 时略敏感（59.923 vs 59.770°）；addition 明显变化（59.846 vs 50.846°）。源论文排序可在“近零门控阈值 + 亚单位 EC 增益”的窄区内恢复，但不是固定增益模型的通用性质。

## 5.3 增益扫描（P1-EC-GAIN-01）

1,440 runs：5 模型 × 6 个 EC 增益（0、0.05、0.25、0.5、0.75、1.0）× 4 个延迟（0.02/0.05/0.10/0.20 s）× 12 参数组。

| 模型 | 关键读数 |
| --- | --- |
| addition | 0.42 / 0.75 / 1.00 / 1.00（增益无关，作为对照） |
| graded_sensory，gain 0/0.05 | 与 addition 完全同轨 |
| graded_sensory，gain ≥0.25 | 0.42 / **1.00** / 1.00 / 1.00（50 ms 比 no-EC 更差） |
| graded_motor，gain ≥0.5 | 短延迟更差，但 200 ms 失败率降到 0.25–0.42 |
| allnone | 0 / 0 / 0 / 0.50（增益无关） |
| allnone_motor | 0 / 0 / 0.08 / 0.50 |

**解释**：源论文固定增益 0.05 太弱，graded 根本不参与；增益 ≥0.25 时，delayed sensory EC 增加第二个延迟回路，变成有害；current motor EC 高增益提供超前信号，长延迟有益但短延迟过冲。gating 不依赖增益，是唯一“不用调参就稳”的策略。

## 5.4 自适应 MLP（P1-EC-ADAPTIVE-01）

源论文 Figure 5 的 adaptive MLP（5 个 sigmoid 隐藏单元，输入 `F_bar`，输出 `ro`，用 ideal bar-only 轨迹的平方误差在线更新）复刻结果：

| 模型 | 0.02 s | 0.05 s | 0.10 s | 0.20 s |
| --- | --- | --- | --- | --- |
| adaptive MLP（learned ro） | 0.42（ro 0.38） | 1.00（ro 0.75） | 1.00（ro 0.97） | 1.00（ro 1.06） |
| fixed graded, gain 0.05 | 0.42 | 0.75 | 1.00 | 1.00 |
| fixed graded, gain 1.0 | 0.50 | 1.00 | 1.00 | 1.00 |
| no EC | 0.42 | 0.75 | 1.00 | 1.00 |
| delayed sensory gating | 0.00 | 0.00 | 0.00 | 0.50 |

**结论**：adaptive MLP 没有救回稳定性；它把增益从 0.38 学到 1.06，50 ms 起 100% 失败，比 no-EC 的 75% 更差，落入高增益有害区。这关闭了“固定增益对 graded 不公平”的审稿意见（在步进近似下）。

## 5.5 Adaptive 学习率/seed 稳健性（P1-EC-ADAPTIVE-02）

576 runs：α = 1e-5、8e-5、5e-4、1e-3 × 3 seeds × 4 delays × 12 参数组。

- 所有 α 都在 100 ms 前达到 100% 失败。
- 50 ms：α=1e-5 为 75%（与 no-EC 持平）；α≥8e-5 为 100%（比 no-EC 更差）。
- 学到的 `ro` 随延迟和 α 上升；α=1e-5 从 0.26 到 0.93，α=1e-3 从 0.77 到 1.10。
- 没有任何学习率救回稳定性；快学习率只是更早进入有害区。

## 5.6 线性稳定性分析

在目标点线性化 `x_dot = A x(t) + B x(t-d)`，数值求 `det(λI − A − B e^{−λd}) = 0` 的右most根：

| 模型 | 线性临界延迟 |
| --- | --- |
| addition | 29 ms |
| graded_sensory, gain 0.05 | 31 ms |
| graded_sensory, gain 1.0 | 43 ms |
| graded_motor, gain 1.0 | 300 ms |
| allnone（门开分支） | 29 ms |

**解释**：线性分析复现了连续 cancellation 失稳的量级，但**不能**区分 gating 与 addition，也不能解释 motor-copy 的长延迟收益。gating 只有在 bar torque 超过阈值后才关闭，motor-copy 收益出现在大偏离之后——这些都是大信号/非线性效应，不是局部线性不稳定性。主文的分离是 non-linear phenomenon。

## 5.7 真正的 command copy（P1-EC-COMMAND-01）

560 runs：7 模型 × 5 延迟 × 2 EC 增益 × 8 参数组，6 s 窗口。

- graded command 与 graded filtered 完全同轨：20 ms 87.5%，50/100/140/200 ms 100%。
- gate command 与 gate filtered 同为：20/50/100 ms 0%，140/200 ms 75%。
- 只有 current-visual oracle 在长延迟更低：20 ms 75%，50 ms 62.5%，100/140 ms 75%，200 ms 62.5%。
- gate duty：command 低于 filtered（0.35/0.65/0.79/0.82/0.85 vs 0.44/0.78/0.85/0.87/0.87），但不改变失败率。

**结论**：pre-plant-filter command copy 不救回延迟；旧 `graded_motor`/`allnone_motor` 的收益是 current-visual oracle 效应，不是 motor-copy 效应。当前有效结论见 [33 修订稿](33_manuscript_track_c.md)。

## 6 下一轮

1. 噪声 + 多 seed 的稳健性。
2. 1 ms 细网格 + 线性稳定性分析。
3. `tau_body = I/beta` 相图，解释 graded_motor 双峰。
4. 与 Canelo 2024 的 Fig. S3/Fig. 5 数值对照。
5. 若稳健，写计算/理论论文草稿（PLOS Comp Biol / eLife 级别），并明确 B0。
