# AppInsight 品牌图标替换设计

## 背景

浏览器标签页当前使用 Vue 模板自带的 `frontend/public/favicon.ico`。AppInsight 的介绍页和分析页虽然没有引用 `frontend/src/assets/logo.svg`，但各自内嵌了不同版本的柱状图品牌标志，造成品牌图形不统一。

## 目标

- 移除用户可见的 Vue 默认 favicon。
- 为浏览器标签页、介绍页顶部和分析页侧栏提供同一个 AppInsight 品牌图形。
- 图形在 16px favicon 尺寸下保持可辨识，并同时适配深色介绍页与浅色侧栏。
- 使用来源清晰、许可允许项目内使用的在线图标素材。

## 方案

采用 Tabler Icons 官方 `chart-dots` 图标作为路径基础。该图标由坐标轴、数据节点和连接线组成，语义贴合应用评论数据分析与洞察场景；Tabler Icons 以 MIT License 发布。

项目内新增一份独立品牌 SVG：保留 `chart-dots` 的简洁几何结构，坐标轴使用项目现有翡翠绿 `#2E8B78`，数据节点与连接线使用项目现有珊瑚色 `#E56B55`，不添加背景色，以适应两个页面的不同背景。

## 替换范围

- `frontend/public/favicon.svg`：新增品牌 favicon。
- `frontend/index.html`：优先引用 SVG favicon，并保留现有 ICO 作为兼容回退。
- `frontend/src/App.vue`：侧栏顶部品牌图标改用统一 SVG。
- `frontend/src/components/LandingPage3D.vue`：介绍页顶部品牌图标改用统一 SVG。
- `frontend/public/THIRD-PARTY-NOTICES.txt`：记录 Tabler Icons 的来源与 MIT 许可。

不修改导航、GitHub 和内容卡片中的功能图标。

## 验证标准

1. `npm run build` 成功。
2. 构建产物包含新的品牌 SVG，且 HTML 不再将 Vue 图标作为首选 favicon。
3. 页面源码中介绍页和分析页顶部品牌图标均引用同一路径。
4. 在浏览器中确认 favicon、介绍页顶部和侧栏图标均可显示，且无 404 资源请求。
