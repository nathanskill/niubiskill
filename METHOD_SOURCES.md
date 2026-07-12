# 方法来源与独立实现说明

## 1. 原始方法

NIUBI Skill 由 Zhennan Yu（Nathan Yu）维护。

本项目的核心组合来自维护者对项目变现、内容获客、销售成交、商业合作、资源协调和创业系统的独立整理：

- `A — Acquisition`：获得闭环缺少的合格节点；
- `B — Bargaining`：形成明确规则、责任、下一步和有成本承诺；
- `C — Customer Care`：维持交付、结算、反馈、信任和续用；
- `D — Development`：持续沉淀产品、工具、数据、案例、SOP、内容和伙伴能力；
- 用“底牌、付款方、付费理由、商品、收钱事件、验证证据”定义一个可执行赚钱点；
- 用“引流 / 成交”把内容获客和销售转化拆成两条不同路线；
- 每次最多比较三个候选，只推荐一个并生成一份行动资产；
- 用价值流、钱流、权力流和信息流拆解多角色商业网络；
- 用“一链、一环、一诺、一入口、一周”进行最小验证；
- 用持续价值测试区分真实贡献与人为制造的信息壁垒。

这里的 ABCD 字母和英文单词均为描述性术语；本项目不声称对这些普通词汇拥有排他权。独特之处在于赚钱点定义、模式匹配、引流/成交路由、ABCD后台判断、单卡输出和证据边界的组合。

公开版本只包含抽象方法和跨行业合成案例，不包含维护者雇主、客户、佣金、内部PPT、CRM、真实业务数据或现有项目流程。

## 2. 理论校正来源

以下公开研究用于校正概念边界，不代表作者为本项目背书，也不构成收益保证：

- Stigler, G. J. (1961). *The Economics of Information*. [DOI](https://doi.org/10.1086/258464)
- Coase, R. H. (1937). *The Nature of the Firm*. [DOI](https://doi.org/10.1111/j.1468-0335.1937.tb00002.x)
- Brandenburger, A. M., & Stuart, H. W. (1996). *Value-based Business Strategy*. [DOI](https://doi.org/10.1111/j.1430-9134.1996.00005.x)
- Teece, D. J. (1986). *Profiting from technological innovation*. [DOI](https://doi.org/10.1016/0048-7333(86)90027-2)
- Rochet, J.-C., & Tirole, J. (2003). *Platform Competition in Two-Sided Markets*. [DOI](https://doi.org/10.1162/154247603322493212)
- Grossman, S. J., & Hart, O. D. (1986). *The Costs and Benefits of Ownership*. [DOI](https://doi.org/10.1086/261404)
- Granovetter, M. S. (1973). *The Strength of Weak Ties*. [DOI](https://doi.org/10.1086/225469)
- Burt, R. S. (2004). *Structural Holes and Good Ideas*. [DOI](https://doi.org/10.1086/421787)

## 3. 与 DBskill 的关系

[DBskill](https://github.com/dontbesilent2025/dbskill) 是一个优秀的公开商业 Skill 项目。本项目从它的公开发布实践中学习：

- 用清晰入口降低第一次使用成本；
- 用固定输出和阶段门槛提高一致性；
- 用渐进加载保持核心 Skill 简洁；
- 用案例、测试、版本和社区形成持续反馈。

DBskill 本地公开版本采用 `CC BY-NC 4.0`。NIUBI Skill 因此坚持 clean-room 独立实现：

- 不复制或改写 DBskill 的文字；
- 不导入其推文、知识原子、案例或数据；
- 不复制其 Skill 路由表或独特结构；
- 不暗示合作、授权、继承或背书关系。

两者解决的问题也不同：DBskill 的公开优势是作者思想、诊断与内容工具箱；NIUBI Skill 只做一个任务——为具体项目匹配、比较并验证赚钱点，判断当前先引流还是先成交。

## 4. 相邻公开 Skill 的取舍

本项目还把以下公开仓库作为相邻设计参考。学习对象是可观察的工程原则，不复制其文本、模板、案例、私有资料或独特编排：

| 公开项目 | NIUBI Skill吸收什么 | 本项目边界 |
|---|---|---|
| [Corey Haines Marketing Skills](https://github.com/coreyhaines31/marketingskills/blob/main/skills/product-marketing/SKILL.md) 与其 [Sales Enablement](https://github.com/coreyhaines31/marketingskills/blob/main/skills/sales-enablement/SKILL.md) | 复用项目上下文、优先使用客户原话、只追问缺口、让销售材料可快速扫描 | 不扩张成营销工具箱，不导入任何预置行业数字 |
| [sales-skills/sales](https://github.com/sales-skills/sales) | 单一入口与“信息够用就行动” | 让用户进入多层路由或维护庞大工具目录 |
| [Rebecca Rae Claude Marketing](https://github.com/thatrebeccarae/claude-marketing) 与其 [Market Research](https://github.com/thatrebeccarae/claude-marketing/blob/main/skills/market-research/SKILL.md) | 核心说明、参考资料和案例分层；重要断言保留来源 | 不默认生成多页报告或无来源评分 |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills/blob/main/pm-product-discovery/skills/brainstorm-experiments-new/SKILL.md) 与其 [Monetization Strategy](https://github.com/phuryn/pm-skills/blob/main/pm-product-strategy/skills/monetization-strategy/SKILL.md) | 用预售、订金、明确价格接受等真实行为验证需求 | 不在没有基线时估算成功率、CAC、LTV或市场规模 |
| [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 主 Skill 保持简洁、按需加载、新旧版盲测和正负触发测试 | 开发期评测不进入每次用户输出 |

这些项目大多分别解决营销、销售、研究、产品发现或 Skill 工程。NIUBI Skill不试图覆盖它们；它只做决策压缩：`一个项目 → 一个赚钱点 → 一条路线 → 一份材料 → 一个短期证据`。

任何外部项目中的通用价格、转化率、回复率、样本量、时间表或成功阈值，都不能直接成为 NIUBI Skill 的事实。关键商业数字必须来自用户或当前证据、透明推导，或明确标为本轮实验参数。

## 5. 证据边界

当前公开版本证明的是：

- Skill 文件结构有效；
- 固定输出、边界和合成场景可以被自动检查；
- 独立 forward tests 可以检查方法是否按预期工作。

它不证明：

- 使用者一定获得收入、成交或合作；
- 任一合成案例代表真实客户结果；
- 方法已经完成大样本或同行评审验证；
- 在任何特定行业、地区或受监管场景中可以直接执行。
