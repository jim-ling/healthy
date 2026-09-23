# phatxm 健康顾问资料分析

分析基准：本地 `phatxm/meddata` 快照，主要抓取于 2026-09-08 至 2026-09-11；复核日期：2026-09-23。

## 项目定位

目标是把公开资料整理成健康顾问可检索的证据卡片：围绕衰老、长寿、睡眠、精力与“年轻化”、癌症相关支持、常见病痛和跌打损伤，回答“有哪些证据、适用边界和安全风险”。输出应是资料导航、风险提示和就医分流，不是诊断或处方。

## 已有资产

| 证据层 | 数据源 | 本地规模 | 适合回答的问题 |
|---|---|---:|---|
| 监管标签 | openFDA drug/label | 1,125 条病种/皮肤标签样本 | 药品成分、适应证、剂型、厂商 |
| 临床研究注册 | ClinicalTrials.gov API v2 | 5,237 条样本 | 研究状态、阶段、入组、干预和时间线 |
| 文献 | Europe PMC 开放获取检索结果 | 1,500 篇 | 研究主题、摘要级证据和引用线索 |
| 药品与安全辅助 | DrugCentral、DGIdb、FDA 标签 | 约 15 万条关系/映射 | 药品成分、适应证和相互作用线索；不作为研发主线 |
| 营养 | USDA FoodData Central Foundation/SR Legacy | 约 82.8 万行落地表 | 食物、营养素和含量关联 |
| 衰老 | HAGR DrugAge、GenAge、CellAge、LongevityMap | 4,559 条 | 模式生物寿命、衰老基因和遗传关联 |
| 皮肤/成分 | PubChem、FDA 皮肤标签、皮肤试验和文献 | 约 4,585 条关系/记录 | 皮肤疾病药物、成分结构和试验线索 |

仓库中的文件大多是“按关键词取前 N 条”的派生样本，不是对应数据库的全量数据。openFDA 样本尤其不能当作药品全目录；ClinicalTrials.gov 文件也应视为检索快照。

## 按健康顾问主题的可用程度

| 主题 | 当前基础 | 缺口 |
|---|---|---|
| 衰老/长寿 | HAGR 四库、营养表、开放文献 | 需要把动物/细胞/人群证据严格分层，不能把延寿实验外推成人 |
| 睡眠 | 失眠标签、试验和营养文献样本 | 需要加入 CBT-I、睡眠卫生、昼夜节律和指南级资料 |
| 年轻化/精力 | 衰老基因、营养、补充剂文献 | “年轻化”不是医学终点，应改成体能、认知、皮肤、代谢等可测指标 |
| 癌症 | 文献与补充剂线索、部分药品关系 | 需要 NCI/WHO 指南、肿瘤类型和治疗阶段；草药只能作为支持治疗/相互作用检索 |
| 病痛/跌打损伤 | 现有资料很少 | 需要急救红旗、骨折/脱位分流、康复和疼痛指南；不能用草药替代影像和复位 |
| 国产药草/中药 | 当前没有结构化数据 | 需要药材标准名、别名、部位、炮制、剂量、禁忌、相互作用、来源和中国批准信息 |

## 可形成的医学分析

1. **药品—疾病—靶点证据图谱**：先用 FDA 标签确认监管适应证，再用 DrugCentral/DGIdb/ChEMBL 连接靶点和作用类型，最后用 ClinicalTrials.gov 与 Europe PMC 标注人体研究证据。这样可以把“已批准”“正在试验”“仅有机制或动物证据”分开。
2. **常见病研究地图**：失眠、过敏性鼻炎、头痛、肥胖、勃起功能障碍和避孕已有标签、试验、文献三层数据；可按研究阶段、干预类型、研究状态和年份统计研究密度。
3. **皮肤健康证据链**：痤疮、银屑病、特应性皮炎、湿疹、玫瑰痤疮和脱发已有同样的三层数据，PubChem 42/48 个成分成功匹配，可做成分标准化和结构去重。
4. **营养干预关联**：USDA 只提供食物成分事实，不能单独证明疗效。疗效判断必须回到临床试验或系统综述，并保留人群、剂量、结局和随访时间。
5. **老药新用候选**：Repurposing Hub、靶点关系和临床试验状态可用于生成候选清单；候选清单不是疗效结论，必须再查注册试验结果、监管标签和安全性。

6. **药草资料卡**：每味国产药草单独记录标准中文名、拉丁学名、药用部位、炮制方式、传统用途、现代人体证据、毒性、妊娠/肝肾风险、药物相互作用和原始出处；“传统用途”与“临床疗效”必须是不同字段。

## 关键质量问题

- `summary.json` 中常见病的 openFDA 与 ClinicalTrials.gov 命中数出现 `skip` 或 `0`，但 CSV 有记录；这说明汇总元数据没有可靠记录服务端总数，不能据此推断“没有研究”。
- 当前快照没有国产药草和跌打损伤的专门资料表；不能从已有 FDA/USDA 数据推导中药疗效或外伤处理方案。
- 大多数 CSV 是前 75、150、237 或 400 条，存在截断和关键词偏倚；需要在分析中明确排序规则，并保存 API 请求参数和分页游标。
- 同一研究可能跨多个主题文件出现，FDA 标签也可能同一产品多版本重复。应以 `nct_id`、FDA `id/label_id`、标准化成分和规范化药物标识去重。
- openFDA 官方说明明确提醒：其公开数据并非全部经过临床或生产用途验证；不良事件报告是信号，不是发生率或因果关系证明。
- 数据源许可不同：HAGR 为 CC BY；ChEMBL 为 CC BY-SA；FDA/ClinicalTrials.gov 多为公有领域；DGIdb、DrugCentral、Europe PMC 的再分发和下游来源条款需要逐项核对。商用发布前必须保留来源和许可字段。
- `db_dump/meddata_20260911.dump` 是 PostgreSQL 自定义格式备份，恢复前需准备 PostgreSQL；当前仓库不复制 111 MB 原始数据，避免把快照和代码混在 Git 历史中。

## 推荐的下一步实现

1. 建立健康顾问主题词表：衰老、睡眠、疼痛、外伤红旗、癌症支持治疗、药草和补充剂，并把用户问题映射到可验证的健康结局。
2. 为每个来源保存 `source_url`、`retrieved_at`、`source_version`、`license`、`query`、`record_id` 和 `raw_hash`。
3. 新增药草数据模型：`herb`、`preparation`、`traditional_claim`、`clinical_evidence`、`toxicity`、`interaction`、`source`，并支持中文别名和拉丁学名。
4. 对 ClinicalTrials.gov 按 `nct_id` 去重，保留最新 `last_update_date`；对 FDA 标签按 `set_id`/标签版本去重。
5. 把“指南/监管”“系统综述”“人体试验”“观察性研究”“体外/动物”“传统经验/推测”做成互斥证据等级，查询结果按等级展示。
6. 为跌打损伤先做安全分流卡：开放性伤口、明显畸形、不能负重、麻木无力、进行性肿胀、头颈/胸腹部外伤等情况直接建议急诊评估；外用药草只能放在完成分流之后。
7. 用 PostgreSQL 或 DuckDB 建分析视图，再添加小规模可复现 SQL/Notebook；不要把抓取快照直接当作医学结论。

## 官方来源与边界

- [FDA openFDA 药物 API](https://open.fda.gov/apis/drug/)：标签、事件、NDC 等端点；官方说明包含数据限制和 API 使用方式。
- [ClinicalTrials.gov Data API](https://clinicaltrials.gov/data-api)：临床试验注册数据与 API 文档。
- [Europe PMC RESTful Web Service](https://europepmc.org/RestfulWebService)：文献检索与开放获取标识。
- [WHO Clinical Trials](https://www.who.int/health-topics/clinical-trials/)：临床试验与证据质量的公共卫生背景。
- [USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets.html)：营养成分数据下载入口。
- [NCCIH 草药与膳食补充剂](https://www.nccih.nih.gov/health/dietary-and-herbal-supplements)：补充剂证据与安全边界。
- [NCCIH 草药-药物相互作用](https://www.nccih.nih.gov/health/providers/digest/herb-drug-interactions)：相互作用、毒性和污染风险。
- [WHO 传统医学战略 2025–2034](https://www.who.int/publications/i/item/9789240113176)：传统医学证据、安全、监管和整合原则。
- [NCI 癌症与补充替代医学](https://www.cancer.gov/about-cancer/treatment/cam)：癌症中草药、补充剂和标准治疗的边界。

这份报告用于项目数据工程和证据检索设计，不构成医疗建议；任何个体化诊疗或用药决定都应由合格临床专业人员完成。
