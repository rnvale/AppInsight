# AppInsight v3.0

多维度 App 评论情感分析系统，基于 AWARE 数据集，支持 6 个分析页面、20+ 交互式图表、多数据集对比与数据钻取。

**网址：** [https://www.haolin-zone.xyz](https://www.haolin-zone.xyz)

---

## 项目架构

```
myweb1/
├── backend/             # Flask API 后端
│   ├── app.py           # 主程序 (780行, 20+ API端点)
│   ├── data/            # AWARE 数据集 (4个域)
│   └── requirements.txt
├── frontend/            # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── App.vue      # 6 个导航页面
│   │   ├── components/  # 20 个 Vue 组件
│   │   ├── composables/ # GSAP 动画组合式函数
│   │   └── http.ts      # API 请求配置
│   ├── vercel.json      # Vercel 部署配置
│   └── index.html
└── README.md
```

## 功能特性

### 6 个分析页面
| 页面 | 功能 |
|------|------|
| 总览仪表盘 | 情感仪表盘、评分分析、领域对比 |
| 情感深度分析 | 情感趋势、热力图、3D 气泡、词云、评论长度、关键词搜索 |
| 方面挖掘与主题聚类 | 玫瑰图、热门 App 对比、主题聚类 |
| App 排行与竞争分析 | 评分排行、四象限散点、NPS 净推荐值 |
| 多数据集对比 | 综合/游戏/生产力/社交 四域交叉对比 |
| 数据浏览与钻取 | 原始评论分页浏览、搜索、排序 |

### 20+ API 端点
涵盖情感分析、方面挖掘、主题聚类、NPS、关键词趋势、多源对比、数据钻取、导出等。

### 动画效果
使用 GSAP 3 实现页面过渡、数字计数、滚动触发、悬停动效等。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端框架 | Vue 3 + TypeScript + Vite |
| 图表 | ECharts 5 + echarts-gl |
| 动画 | GSAP 3.12 + ScrollTrigger |
| UI | Element Plus |
| 后端 | Python Flask + Pandas |

## 本地启动

```bash
# 后端
cd backend
pip install flask flask-cors pandas numpy
python app.py

# 前端
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173

## 部署

- **前端** 部署在 Vercel（自动检测 Vite 框架）
- **后端** 部署在 Render / 自有服务器
- 生产环境设置环境变量 `VITE_API_BASE_URL` 指向后端地址

## 数据集

AWARE (App Review AWareness) 学术研究数据集，涵盖 Productivity、Games、Social Networking、Comprehensive 四个领域，共 21,922 条标注评论。
