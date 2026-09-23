# phatxm 医学公开数据分析

分析基准：本地 `phatxm/meddata` 快照，主要抓取于 2026-09-08 至 2026-09-11；复核日期：2026-09-23。

## 已有资产

| 证据层 | 数据源 | 本地规模 | 适合回答的问题 |
|---|---|---:|---|
| 监管标签 | openFDA drug/label | 1,125 条病种/皮肤标签样本 | 药品成分、适应证、剂型、厂商 |
| 临床研究注册 | ClinicalTrials.gov API v2 | 5,237 条样本 | 研究状态、阶段、入组、干预和时间线 |
| 文献 | Europe PMC 开放获取检索结果 | 1,500 篇 | 研究主题、摘要级证据和引用线索 |
| 药物靶点 | DrugCentral、DGIdb、ChEMBL 映射、Repurposing Hub | 约 15 万条关系/映射 | 靶点、作用类型、老药新用候选 |
| 营养 | USDA FoodData Central Foundation/SR Legacy | 约 82.8 万行落地表 | 食物、营养素和含量关联 |
| 衰老 | HAGR DrugAge、GenAge、CellAge、LongevityMap | 4,559 条 | 模式生物寿命、衰老基因和遗传关联 |
| 皮肤/成分 | PubChem、FDA 皮肤标签、皮肤试验和文献 | 约 4,585 条关系/记录 | 皮肤疾病药物、成分结构和试验线索 |

仓库中的文件大多是“按关键词取前 N 条”的派生样本，不是对应数据库的全量数据。openFDA 样本尤其不能当作药品全目录；ClinicalTrials.gov 文件也应视为检索快照。

## 可形成的医学分析

1. **药品—疾病—靶点证据图谱**：先用 FDA 标签确认监管适应证，再用 DrugCentral/DGIdb/ChEMBL 连接靶点和作用类型，最后用 ClinicalTrials.gov 与 Europe PMC 标注人体研究证据。这样可以把“已批准”“正在试验”“仅有机制或动物证据”分开。
2. **常见病研究地图**：失眠、过敏性鼻炎、头痛、肥胖、勃起功能障碍和避孕已有标签、试验、文献三层数据；可按研究阶段、干预类型、研究状态和年份统计研究密度。
3. **皮肤健康证据链**：痤疮、银屑病、特应性皮炎、湿疹、玫瑰痤疮和脱发已有同样的三层数据，PubChem 42/48 个成分成功匹配，可做成分标准化和结构去重。
4. **营养干预关联**：USDA 只提供食物成分事实，不能单独证明疗效。疗效判断必须回到临床试验或系统综述，并保留人群、剂量、结局和随访时间。
5. **老药新用候选**：Repurposing Hub、靶点关系和临床试验状态可用于生成候选清单；候选清单不是疗效结论，必须再查注册试验结果、监管标签和安全性。

## 关键质量问题

- `summary.json` 中常见病的 openFDA 与 ClinicalTrials.gov 命中数出现 `skip` 或 `0`，但 CSV 有记录；这说明汇总元数据没有可靠记录服务端总数，不能据此推断“没有研究”。
- 大多数 CSV 是前 75、150、237 或 400 条，存在截断和关键词偏倚；需要在分析中明确排序规则，并保存 API 请求参数和分页游标。
- 同一研究可能跨多个主题文件出现，FDA 标签也可能同一产品多版本重复。应以 `nct_id`、FDA `id/label_id`、标准化成分和规范化药物标识去重。
- openFDA 官方说明明确提醒：其公开数据并非全部经过临床或生产用途验证；不良事件报告是信号，不是发生率或因果关系证明。
- 数据源许可不同：HAGR 为 CC BY；ChEMBL 为 CC BY-SA；FDA/ClinicalTrials.gov 多为公有领域；DGIdb、DrugCentral、Europe PMC 的再分发和下游来源条款需要逐项核对。商用发布前必须保留来源和许可字段。
- `db_dump/meddata_20260911.dump` 是 PostgreSQL 自定义格式备份，恢复前需准备 PostgreSQL；当前仓库不复制 111 MB 原始数据，避免把快照和代码混在 Git 历史中。

## 推荐的下一步实现

1. 建立标准化层：疾病词表、药物/RxNorm 或 UniChem 标识、基因符号、成分同义词和单位转换。
2. 为每个来源保存 `source_url`、`retrieved_at`、`source_version`、`license`、`query`、`record_id` 和 `raw_hash`。
3. 对 ClinicalTrials.gov 按 `nct_id` 去重，保留最新 `last_update_date`；对 FDA 标签按 `set_id`/标签版本去重。
4. 把“监管批准”“人体试验”“观察性研究”“体外/动物”“推测关系”做成互斥证据等级，查询结果按等级展示。
5. 用 PostgreSQL 或 DuckDB 建分析视图，再添加小规模可复现 SQL/Notebook；不要把抓取快照直接当作医学结论。

## 官方来源与边界

- [FDA openFDA 药物 API](https://open.fda.gov/apis/drug/)：标签、事件、NDC 等端点；官方说明包含数据限制和 API 使用方式。
- [ClinicalTrials.gov Data API](https://clinicaltrials.gov/data-api)：临床试验注册数据与 API 文档。
- [Europe PMC RESTful Web Service](https://europepmc.org/RestfulWebService)：文献检索与开放获取标识。
- [WHO Clinical Trials](https://www.who.int/health-topics/clinical-trials/)：临床试验与证据质量的公共卫生背景。
- [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets.html)：营养成分数据下载入口。

这份报告用于项目数据工程和证据检索设计，不构成医疗建议；任何个体化诊疗或用药决定都应由合格临床专业人员完成。
