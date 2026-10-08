# Big Data Competition Skill v2.1.0

面向**未知赛题、最终以论文为核心成果**的 MathorCup 等大数据竞赛通用 Skill。主入口见仓库根目录 [SKILL.md](../../SKILL.md)；本目录为按需加载的方法、证据与辅助预检层。

它不是 Kaggle leaderboard 流程，也不是以传统数学建模固定套路选择算法。以当届题面和数据决定所需方法，先确保验证可信，再尝试复杂模型。

## 入口与功能

- [本模块 SKILL.md](SKILL.md)：按需执行与动态路由。
- [方法手册目录](playbooks/00-index.md)：已有表格、时间序列、视觉、优化等任务手册，以及大规模数据、时空/图模型补充。
- [外部 Skill 参考路由](references/external-skill-routing.md)：Probabl、K-Dense、Ultralytics、Hugging Face 的限定式参考；不强制安装。
- [比赛验收门](references/competition-validation-gates.md)：数据、泄漏、实验、论文证据与官方交付检查。
- [优秀论文复盘协议](references/award-paper-audit.md)：配合 [逐篇审查表](./templates/award-paper-audit.md)，从实际 PDF 页码提取可迁移经验。
- [标准库预检工具](tools/bigdata_preflight.py)：`assets` / `yolo` / `csv` 三种只读模式。

## 本地运行

```bash
python skills/big-data-competition-skill/tools/bigdata_preflight.py assets --root path/to/dataset --strict-lfs
python skills/big-data-competition-skill/tools/bigdata_preflight.py yolo --root path/to/yolo_dataset --split train --task detect --classes 3
python skills/big-data-competition-skill/tools/bigdata_preflight.py csv --template official.csv --candidate result.csv --id-column order_id --numeric amount --enum risk=0,1,2
python -m unittest tests/test_bigdata_preflight.py
```

以上仅检查文件级约束，不执行赛题模型、GPU 训练或证明预测效果。具体文件格式、提交方式与评价指标必须按当届官方通知核验；没有完整读取的获奖论文不得当作已分析数据。
