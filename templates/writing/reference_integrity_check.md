# Reference Integrity & Competition-format Check

本模板只负责正式参考文献的**真实性、元数据、正文映射与用户/竞赛格式锁**。它不替代 Citation Evidence 的“这个 claim 是否真的需要外部来源”判断，也不规定某一种比赛必须使用某一种参考文献格式。

## 1. Correct order

```text
claim needs external evidence
→ find authoritative source
→ verify source exists
→ verify source actually supports the claim
→ capture source-type metadata
→ apply current competition/user reference style
→ insert in-text citation
→ create bibliography entry
→ two-way mapping audit
```

禁止先编一条“看起来像真的”参考文献，再去寻找能否对应的网页/论文。

## 2. Source existence gate

正式入文前至少确认：

- 来源可被独立定位；
- 作者/机构真实；
- 标题真实；
- 出版物/出版社/官方站点真实；
- 年份与版本真实；
- 论文 DOI/卷期页或书籍出版信息/网页 URL 等可核验字段真实。

若只找到二手转载而找不到声称的一手论文/书/官方资源，保持 `review_required`，不得写成“已核验”。

AI 助手、搜索结果页和聚合摘要不能作为定理来源、算法原创来源、经验参数或领域事实的正式权威。

## 3. Claim-support gate

“来源真实”不等于“支持当前句子”。逐条检查：

```text
paper claim
→ source passage/result/theorem/data
→ support strength: direct / contextual / insufficient
```

- `direct`：来源直接支持当前事实/方法来源/参数/定理；
- `contextual`：仅支持背景，正文措辞不得扩大到更强结论；
- `insufficient`：删除引用、改写 claim 或寻找更合适来源。

本文自己推导出的公式、模型结果和工作簿数值不应靠外部引用“证明”。

## 4. Metadata by source type

最终字段由官方格式/Presentation Lock 决定；下面是**核验字段池**而非固定输出格式。

### Journal article
- authors；
- article title；
- journal title；
- year；
- volume；
- issue（若有/若格式要求）；
- page range 或 article number；
- DOI/official landing page（适用时）。

### Book / monograph
- authors/editors；
- book title；
- edition（若非首版或格式要求）；
- publication place；
- publisher；
- year；
- cited page locator（当竞赛规则/用户格式明确要求）。

### Online / official web resource
- authoring organization/person；
- resource/page title；
- canonical URL；
- publication/update date（若可得）；
- access date（当竞赛规则/用户格式要求）。

### Standard / official dataset / report
- issuing organization；
- title；
- identifier/version；
- year/date；
- publisher/platform；
- URL/DOI/access date（适用时）。

## 5. Competition-format lock

若题目/官方说明/用户提供了具体格式，先写入 `presentation_lock.reference_style`。之后：

- 不擅自改成 APA / IEEE / GB/T / BibTeX 默认风格；
- 不因 LaTeX package 默认输出不同而静默改变官方格式；
- 书籍页码、网页访问时间等一旦被锁为 required，最终审计必须逐条检查；
- 官方格式只决定“怎么写”，不降低真实性核验要求。

## 6. In-text ↔ bibliography two-way audit

正式交付前必须双向检查：

```text
每个正文 citation → 恰有一个有效 bibliography entry
每个 bibliography entry → 至少有一个真实正文 citation，除非官方要求独立参考书目
```

并检查：

- 编号/排序符合当前格式；
- citation 未引用错误条目；
- 同一来源无重复条目；
- 作者、年份、标题在正文描述与文末条目一致；
- 删除正文段落后没有遗留“装饰性文献”。

## 7. Page locator / access-date semantics

页码与访问日期不是装饰字段：

- 若规则要求“引用书籍还必须指出页码”，页码应对应真正支撑 claim 的位置，而不是随意填整本书页段；
- 期刊页码是文章出版元数据，不等价于正文引用定位页码；
- web access date 使用实际访问/核验日期，不伪造为发布日期；
- 若页面持续更新，优先同时记录可得的 update date 与 required access date。

## 8. Final reference QA

每条正式参考文献回答：

1. 它真实存在吗？
2. 我核对的是一手/权威页面吗？
3. 元数据字段准确吗？
4. 它真的支持正文那个 claim 吗？
5. 正文 citation 与文末条目双向对应吗？
6. 当前格式是否服从官方规则/Presentation Lock？
7. required page locator / access date 是否真实且齐全？

任一核心项回答“不确定”，保持 `review_required`，不要为了凑文献数量强行入文。
