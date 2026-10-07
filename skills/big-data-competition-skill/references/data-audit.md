# Data Audit

## Mandatory non-destructive audit

先盘点文件、表、字段、类型、单位、样本量、缺失、重复、异常、时间覆盖、实体键、跨表连接和数据粒度。

## Quality dimensions

- completeness
- consistency
- validity
- uniqueness
- timeliness
- coverage
- measurement quality
- leakage risk

## Cleaning decision

不要默认“有异常就清洗”。记录问题 → 影响 → 是否影响当前模型 → 处理方式 → 验证证据。

任何项目级处理都应可重跑且保留原始数据不变。