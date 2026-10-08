---
governance_version: 2.0.0
applies_to_skill: big-data-competition-skill
status: active
---

# Big Data Competition Skill 修改治理规范

此规范是当前论文型大数据竞赛 Skill 的权威维护规则。历史 HSK v7.13.0 的 core/bootstrap.yaml、
core/ 和旧测试保留作兼容参考，不再决定当前根 SKILL.md 的版本、主入口、验收对象。

## 一、入口与单一事实源

- 根 SKILL.md：能力边界、流程、证据标准；版本 frontmatter 是唯一活动 Skill 版本来源。
- skills/big-data-competition-skill/SKILL.md：按需子模块入口。
- skills/big-data-competition-skill/MANIFEST.json：方法手册、参考、模板和可选工具清单。
- skills/big-data-competition-skill/references/：相应专题的唯一详细规范。
- .codex-plugin/plugin.json / README.md / CHANGELOG.md：镜像当前版本，不自行定义另外版本。
- scripts/generate_indexes.py：管理 SKILL_FILE_INDEX.md、TEMPLATE_INDEX.md、MANIFEST.sha256 和历史指针。
- scripts/validate_bigdata_skill.py：静态验证当前活动 Skill，不兼任历史 HSK 运行时的校验器。
- .github/workflows/ci.yml：当前 Big Data Skill 的检查矩阵，至少应检验入口、版本、清单、引用、
  基础研究证据链、数据预检工具和生成索引。

## 二、修改流程

1. 读取当前 main 的根 SKILL.md、此治理规范、最新 main 提交和全部未合并相关 PR；
   不从旧聊天记忆反推当前代码。
2. 修改前形成简报：主题、版本、目的、明确不做、权威文件、范围、迁移、回滚、验证。
3. 一次主题一个分支/PR，禁止直接向 main 写入，禁止两个并行 PR 修改同一个入口契约。
4. 文档只摘要已有权威规则；方法手册不替代当届官方题意和数据。
5. 新增能力遵守向后兼容、先 baseline 和正确验证、留实验来源与论文证据的原则。
6. 禁止凭空声称优秀论文已经读过、真实数据已跑过、图表和结果已验收。
7. 当前有效文件至少运行以下命令，通过后方可合并：

   python scripts/validate_bigdata_skill.py

   python -m unittest discover -s tests -p 'test_bigdata_*.py'

   python scripts/generate_indexes.py --check

8. 索引由脚本或仓库自动生成工作流生成，不能手改 SHA 使 CI 变绿。
9. 历史 HSK 数学建模测试可能因根入口已转型而失败。应保留其源码供单独历史项目
   维护；不允许把旧 HSK 的 v7.x 主入口要求重新强加在大数据 Skill 上，也不允许
   通过弱化当前大数据检查来遮掩真实错误。
10. 合并前确认改变的文件不含真实赛题数据、未经许可的论文全文、私密附件或
    第三方未授权代码。报告 PR、CI 结果、合并 SHA、剩余问题。

## 三、版本与交付

- 仅文档格式修正可不升级版本；错误修复按 patch，新兼容能力按 minor，
  破坏调用或目录格式按 major。
- 修复历史版本漂移时以根 SKILL.md 已发布的 2.1.0 为准，不将旧 HSK 7.13.0
  错误认定为当前大数据 Skill 版本。
- 论文内容、图表、预处理、结果提交规范以当届赛事公告为准；不启用 Kaggle 默认提交。
- 原有 HSK 文件仅作为 historical reference，并不因此被删除；若需彻底迁出，
  必须另开迁移 PR 并提供迁移清单与回滚说明。
