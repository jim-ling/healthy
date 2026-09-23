# 数据说明

仓库中的 `data/example/` 只用于验证索引和命令是否可运行，不代表完整医学证据库，也不构成治疗建议。

完整数据快照应放在仓库外，并在导入前记录以下信息：

- 来源 URL 和 API 查询条件
- 抓取日期与来源版本
- 原始记录 ID
- 数据许可和再分发限制
- 文件 SHA-256

当前规划的数据来源包括 FDA openFDA、ClinicalTrials.gov、Europe PMC、USDA FoodData Central、HAGR、PubChem、DrugCentral 和 DGIdb。不同来源的许可不同，不能用本项目的 MIT License 覆盖第三方数据。

导入自有数据后运行：

```bash
python3 tools/build_index.py --source /path/to/data
```

索引文件位于 `.local/health_rag.sqlite3`，已被 `.gitignore` 排除，不应提交到公开仓库。
