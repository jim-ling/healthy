# healthy

面向健康顾问的医学与传统健康公开资料分析工程。项目提供可追溯的本地资料检索工具，不替代医生诊断、处方或个体化治疗建议。

## 当前状态

完整数据快照不随仓库发布，避免把受不同许可约束的原始数据混入代码历史。数据源、许可、快照范围和恢复说明见[数据说明](docs/data-sources.md)。

## 文档

- [公开医学资料分析](docs/medical-data-analysis.md)：数据盘点、证据层级、质量问题和下一步建议。
- [健康科普更新与咨询流程](docs/health-advisor-workflow.md)：资料更新、检索、脚本和发布前核验流程。

## 本地检索

首次运行可直接使用仓库内的示例资料：

```bash
python3 tools/build_index.py
python3 tools/search_index.py melatonin
python3 tools/consult.py 睡眠和褪黑素安全吗
```

使用自己的资料目录时：

```bash
python3 tools/build_index.py --source /path/to/your/data
```

项目只使用 Python 标准库，无需安装第三方依赖。支持 CSV、TSV、JSON、Markdown、TXT 和 LOG 文件。

索引位于 `.local/health_rag.sqlite3`，不会提交到 Git；原始文件位置、行号和文件哈希会保留在索引中，方便追溯。

## 数据原则

数据用于检索、科研和假设生成，不直接替代医生诊断、处方或个体化治疗建议。每条结论应保留来源、抓取日期、版本、许可和原始记录 ID。

## License

代码和原创文档以 MIT License 发布，详见 [LICENSE](LICENSE)。第三方数据和资料仍受其各自的许可和使用条款约束。
