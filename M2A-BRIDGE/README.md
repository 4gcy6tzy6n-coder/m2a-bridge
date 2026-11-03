# M2A-BRIDGE

> 状态：`PROPOSED_NOT_PREREGISTERED`；P0 可行性核验进行中。
> 上级方案：[../M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md](../M2A_BRIDGE_NATURE_ARTICLE_MASTER_PROTOCOL_2026-10-27.md)
> 项目 wiki：[../wiki/index.md](../wiki/index.md)

## 这个目录是什么

M2A-BRIDGE 的独立研究仓库。旧 M2A 与 Route A 只作为冻结历史证据、形式化接口和审计模板，不并入本仓库的确认性数据。

## 目录

| 路径 | 内容 |
| --- | --- |
| `00_CHARTER_AND_SCOPE.md` | 章程、边界、当前授权 |
| `01_PRIOR_ART_AND_NOVELTY_MATRIX.csv` | 近邻论文、DOI、重叠点、剩余缺口 |
| `02_DATA_FEASIBILITY/` | 数据字段审计、跨来源身份映射、访问报告 |
| `03_THEORY/` | H-F/H-D/H-P 竞争机制与可判别预测 |
| `04_BIO/` | 生物实验协议与 pilot（当前未启动） |
| `05_AI/` | AI 任务、对照、匹配审计（当前未启动） |
| `06_JOINT/` | 跨系统变量映射与联合检验（当前未启动） |
| `07_AUDIT/` | 证据台账、哈希、决策记录 |
| `08_MANUSCRIPT/` | 图契约、claim-evidence map、稿件 |
| `G0_G1_FEASIBILITY_DECISION.md` | P0 决策 |
| `GATE_STATUS.yaml` | 当前门禁状态 |

## 当前允许做的事

- 公开数据的字段级核验；
- 计算 pilot 的代码与最小 smoke test；
- 预注册草案与模型比较设计。

## 当前禁止做的事

- 确认性生物实验；
- 训练确认模型或宣布新机制；
- 下载 50–200 GB 大包；
- 修改旧 M2A / Route A 冻结资产；
- 标 `NATURE_READY`。
