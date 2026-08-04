# 现状发现

- 项目使用 Vue 3、Vite、ECharts、ECharts GL 和 Flask，图表组件位于 `frontend/src/components`，接口集中在 `backend/app.py`。
- `DataRepository.apply_filters` 会先按 sentiment 过滤，再由各统计接口计算 positive_rate。选择正面或负面后，部分比例图会退化为 100% 或 0%。
- `DomainCompare`、`LengthAnalysisChart`、`TopAppsChart`、`SentimentTrend`、`RatingSentiment` 普遍使用数量柱状图加比例折线和双 Y 轴，比较成本较高。
- `EmotionHeatmap` 当前只返回 positive_rate，缺少 negative、样本量和净情感指标。
- `QuadrantScatter` 前端硬编码了 3.8 的评分分界和评论量中位线，无法适配不同数据集。
- `SentimentTrend` 按评分分组，数据集没有日期字段，因此不是时间趋势。
- `WordCloud` 适合展示氛围，不适合精确比较词频，建议增加排名式关键词视图。
- CSV 字段包含 domain、app、rating、category、term、sentiment 等，但没有日期字段。

## 视觉约束

- 图表区域保持浅色。
- 正面使用青绿色体系，负面使用砖红体系，中性使用灰绿色。
- 数字使用等宽数字，Tooltip 统一显示指标、样本量和对比基线。
- 当前用户可见版本标识仍有 `v3.0`，需要统一升级到 `v4.0`。
