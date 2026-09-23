# healthy

面向健康顾问的医学与传统健康公开资料分析工程。

## 当前状态

本仓库已配置远程地址 `git@github.com:jim-ling/healthy.git`。当前远程仓库为空，工作区中的分析文档先作为项目基线提交。

现有抓取资产位于 [`/Users/mac/Documents/phatxm/meddata`](../phatxm/meddata)，其中对本项目最有用的是 HAGR 衰老/长寿、睡眠与营养相关的 ClinicalTrials.gov/Europe PMC、癌症与补充剂安全线索，以及 FDA 标签。药物靶点研发数据暂作为辅助，不作为主线。国产药草、中药方剂、跌打损伤和中国监管信息目前尚未进入这套快照，需要单独补充。数据清单、许可和恢复说明见 phatxm 目录中的 `README-下载数据清单.md` 与 `RESTORE_GUIDE.md`。

## 文档

- [公开医学资料分析](docs/medical-data-analysis.md)：数据盘点、证据层级、质量问题和下一步建议。
- [健康科普更新与咨询流程](docs/health-advisor-workflow.md)：资料更新、检索、脚本和发布前核验流程。

## 本地检索

构建本地索引（默认读取 `/Users/mac/Documents/phatxm/meddata`）：

```bash
python3 tools/build_index.py
python3 tools/search_index.py 睡眠 褪黑素
```

索引位于 `.local/health_rag.sqlite3`，不会提交到 Git；原始文件位置、行号和文件哈希会保留在索引中，方便追溯。

## 数据原则

数据用于检索、科研和假设生成，不直接替代医生诊断、处方或个体化治疗建议。每条结论应保留来源、抓取日期、版本、许可和原始记录 ID。
