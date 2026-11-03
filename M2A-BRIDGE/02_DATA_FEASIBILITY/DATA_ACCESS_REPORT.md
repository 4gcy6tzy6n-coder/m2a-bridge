# 数据访问与字段审计报告（P0）

- 日期：2026-10-27
- 环境：macOS 26.2 / Apple M4 / 16 GB RAM / 35 GB free；Python 3.12；scipy 1.17；h5py 3.16
- 原则：先字段、后下载；不下载 50–200 GB 大包；不同来源不伪称配对。

## 1 已完成

| 来源 | 访问方式 | 实际字节 | 状态 |
| --- | --- | --- | --- |
| Rayshubskiy 2025 / Harvard Dataverse `10.7910/DVN/0NCLP1` | 直接下载单个 `.mat` | 71,381,032 | 已读取字段 |
| Erginkaya 2025 / Zenodo `14967806` | HTTP Range + 远程 zip | 2,369,424（1 个 HS 文件） | 已读取字段 |
| Erginkaya 2025 | zip central directory | 857,396 | 已列 5,518 个文件 |
| Turner 2022 / Dryad `h44j0zpp8` | API 元数据 + 页面 | 元数据 | 下载被 401/403 拦截 |
| BANC 2026 | 元数据 | — | 结构数据，未下载 |

## 2 Rayshubskiy 字段（`dual_13.mat`，71 MB）

```text
ball_SR   100
ephys_SR  10000
ephys_A   (5,750,000,)  float64  membrane potential, mV
ephys_B   (5,750,000,)  float64  second cell
stim      (5,750,000,)  uint8    binary events; unique values {0, 5}
fwd       (57,500,)     float64  forward velocity
lat       (57,500,)     float64  lateral velocity
yaw       (57,500,)     float64  yaw velocity
t_ephys   (5,750,000,)  0–575 s
t_ball    (57,500,)     0–575 s
```

结论：

- **同动物、同 trial、同时间基**的 stimulus → neural → behavior 成立。
- `stim` 是二值事件通道（0/5），不是视觉光流；该数据集不能单独检验 H-P 的“视觉自运动预测”，但能检验 action-copy / neural→behavior。
- `ephys_A/B` 是原始膜电位；需要 spike threshold / PSTH 处理，不能直接当发放率。
- 一个 71 MB 文件足以做字段级资格核验；全量 157.9 GB 不下载。

## 3 Erginkaya 字段（HS 预处理文件，2.37 MB）

```text
DFF                 (2, 78, 48)     ROI x time x trial
DFF_All             (78, 6, 8, 2)   time x speed? x pattern? x ROI
StimNames           (48,)           per-trial stimulus names
Speeds              (48,)           per-trial speeds
Stimuli             (8,)            stimulus classes
OFPatterns          (8,)            optic-flow patterns
PatternIDs          (48,)
TrialNum            48
FrameRate           float
DateIndividualBeh   string          pointer to behavioral session
```

结论：

- 视觉光流 → HS/H2 神经响应成立，48 trials × 78 timepoints × 2 ROIs。
- 行为在该 Zenodo 记录的 `data/Behavior/.../DataLowHighRes.mat`（约 25 MB/文件），与预处理神经文件分开；是否同一动物需按 fly ID/date 核验，当前标记 `partial`。
- 23.5 GB zip 可通过 Range 只取单文件；全量不下载。

## 4 被拦截的来源

| 来源 | 结果 | 影响 |
| --- | --- | --- |
| Dryad `h44j0zpp8`（Turner 2022） | API 元数据可读；`/downloads/file_stream/*` 返回 403，API download 返回 401 | 最佳“同动物视觉+神经+行为”候选暂时不可字段核验；需 Dryad 登录或作者镜像 |
| Dryad raw（`jwstqjqdd` 等） | 未尝试，约 297 GB | 暂不需要 |
| BANC Dataverse | 未下载 | 结构约束可后续用 |

## 5 G0-A 判定

- **PASS WITH CAVEAT**：至少存在完整的 `stimulus → neural` 路径（Erginkaya HS/H2）和完整的 `stimulus → behavior` 路径（Erginkaya Behavior；Rayshubskiy 同动物 optogenetic/odor → neural → behavior）。
- 但**没有已验证的同一动物、同一视觉光流刺激、同时含神经与行为的数据**。不得把 Erginkaya 的神经文件与行为文件、或 Erginkaya 与 Rayshubskiy 伪称配对。
- 若要检验 H-P 的视觉 reafference，需要：
  1. Dryad Turner 数据访问；或
  2. 新合作实验室的同动物视觉闭环数据；或
  3. 计算 pilot 中用 flyvis/FlyGym 生成预测，再用公开数据做外部一致性检查（证据等级 B1，不宣称生物确认）。

## 6 下一步

1. 尝试 Dryad 登录 / 联系作者获取 `datafiles.zip` 的单个 HDF5 或文件清单。
2. 在 `M2A-BRIDGE/02_DATA_FEASIBILITY/tools/` 固化远程 zip 读取脚本，并加 selftest。
3. 用 Rayshubskiy 单文件做 action→neural 的最小分析，验证 spike/PSTH 管线。
4. 用 Erginkaya HS 单文件做 H-D 模型的最小拟合，验证 48×78×2 的数据管线。
5. 在 flyvis/FlyGym 上运行一次最小 smoke test，记录版本、运行时、内存与断言。
