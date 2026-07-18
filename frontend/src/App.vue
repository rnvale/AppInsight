<template>
  <div v-if="showLanding" class="landing-wrapper">
    <LandingPage3D @enter="enterApp" />
  </div>
  <div v-else ref="appRoot" class="app-root">
    <svg style="position:absolute;width:0;height:0" aria-hidden="true">
      <defs>
        <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#E56B55"/>
          <stop offset="100%" stop-color="#2E8B78"/>
        </linearGradient>
      </defs>
    </svg>

    <!-- Sidebar -->
    <aside ref="sidebarRef" class="sidebar" role="navigation" aria-label="主导航">
      <div class="sidebar-header">
        <svg class="brand-icon" viewBox="0 0 28 28" fill="none" aria-hidden="true">
          <rect x="2" y="2" width="24" height="24" rx="6" fill="url(#brandGrad)"/>
          <path d="M10 14l3 3 5-6" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="brand-text">
          <span class="brand-name">AppInsight</span>
          <span class="brand-ver">v3.0</span>
        </div>
      </div>
      <div class="nav-rail">
        <div class="rail-track" aria-hidden="true">
          <div class="rail-indicator" :style="{ transform: 'translateY(' + navIndex * 48 + 'px)' }"></div>
        </div>
        <nav class="nav-list">
          <button v-for="(item, i) in nav" :key="item.key"
            class="nav-item" :class="{ active: view === item.key }"
            @click="switchView(item.key)">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path :d="item.icon"/></svg>
            <span>{{ item.label }}</span>
          </button>
        </nav>
      </div>
      <div class="sidebar-footer">
        <div class="sf-row"><span class="sf-label">数据来源</span><span class="sf-value">AWARE</span></div>
        <div class="sf-row"><span class="sf-label">记录数</span><span class="sf-value">{{ fmt(total) }} 条</span></div>
        <div class="sf-row" style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(220,232,227,0.1)">
          <span class="sf-label">作者</span><span class="sf-value">RainVale</span>
        </div>
        <div class="sf-row" style="align-items:center">
          <span class="sf-label">GitHub</span>
          <a href="https://github.com/rnvale/myweb1" target="_blank" class="sf-value" style="display:inline-flex;align-items:center;gap:4px;color:inherit;text-decoration:none">
            <svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.26.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.09-.745.083-.73.083-.73 1.205.085 1.84 1.237 1.84 1.237 1.07 1.835 2.807 1.305 3.492.998.108-.776.42-1.305.762-1.605-2.665-.305-5.467-1.332-5.467-5.93 0-1.31.467-2.38 1.235-3.22-.135-.303-.535-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.4 3-.405 1.02.005 2.045.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z"/></svg>
            @rnvale
          </a>
        </div>
        <button @click="backToLanding" class="back-landing-btn" title="返回介绍页">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><path d="M3 12l9-9 9 9M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          返回介绍页
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="main" id="main-content" ref="mainRef">
      <WorkspaceBar
        :page-label="currentPage.label"
        :page-description="currentPage.description"
        dataset-label="AWARE / 综合数据集"
        :filters="activeFilters"
        :updated-at="updatedAt"
        :exporting="exporting"
        @clear-filter="clearFilter"
        @refresh="refreshData"
        @export="downloadFilteredData"
      />

      <!-- Dashboard -->
      <section v-if="view === 'dashboard'" ref="pageRef" class="page">
        <header class="page-header hero-cyan">
          <div class="hero-content">
            <div class="page-tag-group">
              <span class="tag tag-dark">概览</span>
              <span class="tag tag-dark-outline">仪表盘</span>
            </div>
            <h1 class="page-title hero-title">App 智能分析仪表盘</h1>
            <p class="page-desc hero-desc">基于 AWARE 数据集对 <strong>{{ fmt(total) }}</strong> 条应用评论进行多维度情感分析</p>
            <div class="hero-stats">
              <div class="hs-item"><span class="hs-num">{{ anim.total }}</span><span class="hs-lbl">评论总数</span></div>
              <div class="hs-divider"></div>
              <div class="hs-item"><span class="hs-num hs-pos">{{ anim.pos }}</span><span class="hs-lbl">正面</span></div>
              <div class="hs-divider"></div>
              <div class="hs-item"><span class="hs-num hs-neg">{{ anim.neg }}</span><span class="hs-lbl">负面</span></div>
              <div class="hs-divider"></div>
              <div class="hs-item"><span class="hs-num hs-accent">{{ posPct }}<small>%</small></span><span class="hs-lbl">正面率</span></div>
            </div>
          </div>
        </header>
        <div class="content">
          <InsightSummary
            :positive-rate="posPct"
            :avg-rating="avgRating"
            :nps-score="npsScore"
            :total="total"
            :aspect-count="aspectCount"
            :avg-length="avgLen"
            :sentiment="sf"
            :category="af"
            @open="switchView"
          />
          <div class="metrics-bar">
            <div class="mb-item"><span class="mb-lbl">平均评分</span><span class="mb-val">{{ avgRating }}</span><div class="mb-stars">{{ '★'.repeat(Math.round(Number(avgRating))) }}{{ '☆'.repeat(5 - Math.round(Number(avgRating))) }}</div></div>
            <div class="mb-divider"></div>
            <div class="mb-item"><span class="mb-lbl">正面率</span><span class="mb-val mb-val-grn">{{ posPct }}<small>%</small></span><div class="bar-track"><div class="bar-fill" :style="{ width: posPct + '%' }"></div></div></div>
            <div class="mb-divider"></div>
            <div class="mb-item"><span class="mb-lbl">方面类别</span><span class="mb-val">{{ aspectCount }}</span><span class="mb-sub">分析维度</span></div>
            <div class="mb-divider"></div>
            <div class="mb-item"><span class="mb-lbl">NPS 评分</span><span class="mb-val" :class="npsClass">{{ npsScore }}</span><span class="mb-sub">净推荐值</span></div>
            <div class="mb-divider"></div>
            <div class="mb-item"><span class="mb-lbl">评价均长</span><span class="mb-val">{{ avgLen }}<small>字</small></span><span class="mb-sub">平均长度</span></div>
          </div>
          <div ref="chartsRow1" class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">情感仪表盘</h2><p class="card-desc">正面评论占比实时监控</p></div><span class="tag tag-live">实时</span></div><div class="card-body"><SentimentGauge :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">评分情感</h2><p class="card-desc">各星级评论的情感分布</p></div><span class="tag">分布</span></div><div class="card-body"><RatingSentiment :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
          <div ref="magSectionRef" class="mag-section">
            <div class="mag-image"><img src="/img/mag-domain.jpg" alt="" loading="lazy"></div>
            <div class="mag-text">
              <span class="mag-label">领域分析</span>
              <h3 class="mag-title">各 App 领域情感对比</h3>
              <p class="mag-desc">正面率最高的领域为娱乐和美观性类应用，而可靠性、价格类别的负面反馈较多。不同 App 领域的正面率与评论量呈现明显分化。</p>
              <div class="mag-stat-row">
                <div class="mag-stat"><span class="mag-stat-val mag-grn">{{ posPct }}<small>%</small></span><span class="mag-stat-lbl">总体正面率</span></div>
                <div class="mag-stat"><span class="mag-stat-val" style="color:#d97706">{{ aspectCount }}</span><span class="mag-stat-lbl">方面类别</span></div>
                <div class="mag-stat"><span class="mag-stat-val" style="color:#2563eb">{{ fmt(total) }}</span><span class="mag-stat-lbl">评论总数</span></div>
              </div>
            </div>
          </div>
          <div class="card"><div class="card-header"><div><h2 class="card-title">各领域情感对比</h2><p class="card-desc">不同 App 领域的正面率与评论量对比</p></div></div><div class="card-body"><DomainCompare :sentiment-filter="sf" :aspect-filter="af"/></div></div>
        </div>
      </section>

      <!-- Sentiment -->
      <section v-if="view === 'sentiment'" ref="pageRef" class="page">
        <header class="page-header page-header-sm hero-purple">
          <div class="hero-content">
            <div class="page-tag-group"><span class="tag tag-dark">情感</span></div>
            <h1 class="page-title hero-title">情感深度分析</h1>
            <p class="page-desc hero-desc">评分与方面的多维情感关联洞察</p>
          </div>
        </header>
        <div class="content">
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">情感热力图</h2><p class="card-desc">评分与方面类别的情感矩阵</p></div></div><div class="card-body"><EmotionHeatmap :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">3D 气泡图</h2><p class="card-desc">气泡大小=评论量，颜色=正面率</p></div></div><div class="card-body"><BubbleChart3D :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">评论长度分析</h2><p class="card-desc">短评倾向正面，长评蕴含更多信息</p></div></div><div class="card-body"><LengthAnalysisChart :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">高频词云</h2><p class="card-desc">正负面评论关键词对比</p></div></div><div class="card-body"><WordCloud :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">情感趋势</h2><p class="card-desc">各评分等级的情感变化趋势</p></div></div><div class="card-body"><SentimentTrend :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">关键词搜索</h2><p class="card-desc">搜索关键词在各评分中的出现频率</p></div></div><div class="card-body"><KeywordTrend :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
        </div>
      </section>

      <!-- Topics -->
      <section v-if="view === 'topics'" ref="pageRef" class="page">
        <header class="page-header page-header-sm hero-emerald">
          <div class="hero-content">
            <div class="page-tag-group"><span class="tag tag-dark">挖掘</span></div>
            <h1 class="page-title hero-title">方面挖掘与主题聚类</h1>
            <p class="page-desc hero-desc">评论方面类别分布、主题聚类与关键词洞察</p>
          </div>
        </header>
        <div class="content">
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">玫瑰图</h2><p class="card-desc">方面类别评论量分布</p></div></div><div class="card-body"><RoseChart :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">热门 App 情感对比</h2><p class="card-desc">评论量最高的应用情感表现</p></div></div><div class="card-body"><TopAppsChart :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
          <div class="card"><div class="card-header"><div><h2 class="card-title">主题聚类分析</h2><p class="card-desc">各方面类别的关键词云与情感分布</p></div></div><div class="card-body"><TopicClusters :sentiment-filter="sf" :aspect-filter="af"/></div></div>
        </div>
      </section>

      <!-- Rankings -->
      <section v-if="view === 'rankings'" ref="pageRef" class="page">
        <header class="page-header page-header-sm hero-amber">
          <div class="hero-content">
            <div class="page-tag-group"><span class="tag tag-dark">排行</span></div>
            <h1 class="page-title hero-title">App 排行与竞争分析</h1>
            <p class="page-desc hero-desc">评分排行榜、四象限矩阵与 NPS 净推荐值</p>
          </div>
        </header>
        <div class="content">
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">评分排行榜</h2><p class="card-desc">Top 应用按平均评分排名</p></div></div><div class="card-body"><AppRatings :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">四象限分析</h2><p class="card-desc">评分与评论量矩阵</p></div></div><div class="card-body"><QuadrantScatter :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
          <div class="grid-2">
            <div class="card"><div class="card-header"><div><h2 class="card-title">NPS 净推荐值</h2><p class="card-desc">推荐者 vs 贬损者分析</p></div></div><div class="card-body"><NpsAnalysis :sentiment-filter="sf" :aspect-filter="af"/></div></div>
            <div class="card"><div class="card-header"><div><h2 class="card-title">App 评分详细</h2><p class="card-desc">各应用平均评分分布</p></div></div><div class="card-body"><AppRatingsDetail :sentiment-filter="sf" :aspect-filter="af"/></div></div>
          </div>
        </div>
      </section>

      <!-- Compare -->
      <section v-if="view === 'compare'" ref="pageRef" class="page">
        <header class="page-header page-header-sm">
          <div class="hero-content">
            <div class="page-tag-group"><span class="tag tag-dark">对比</span></div>
            <h1 class="page-title hero-title">多数据集对比分析</h1>
            <p class="page-desc hero-desc">跨数据集的多维度对比，发现不同领域的差异</p>
          </div>
        </header>
        <div class="content">
          <div class="card"><div class="card-header"><div><h2 class="card-title">数据集对比</h2><p class="card-desc">综合 vs 游戏 vs 生产力 vs 社交</p></div></div><div class="card-body"><CompareDatasets :sentiment-filter="sf" :aspect-filter="af"/></div></div>
        </div>
      </section>

      <!-- Explorer -->
      <section v-if="view === 'explorer'" ref="pageRef" class="page">
        <header class="page-header page-header-sm">
          <div class="hero-content">
            <div class="page-tag-group"><span class="tag tag-dark">浏览</span></div>
            <h1 class="page-title hero-title">数据浏览与钻取</h1>
            <p class="page-desc hero-desc">浏览原始评论数据，支持筛选、搜索、排序和翻页</p>
          </div>
        </header>
        <div class="content">
          <div class="card"><div class="card-header"><div><h2 class="card-title">评论数据表</h2><p class="card-desc">浏览和搜索评论内容</p></div></div><div class="card-body"><DataExplorer :sentiment-filter="sf" :aspect-filter="af"/></div></div>
        </div>
      </section>

      <!-- Mobile Nav -->
      <nav class="mobile-nav" role="navigation" aria-label="移动端导航">
        <button v-for="(item, i) in nav" :key="item.key" class="mobile-nav-item" :class="{ active: view === item.key }" @click="switchView(item.key)">
          <svg class="mobile-nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path :d="item.icon"/></svg>
          <span class="mobile-nav-label">{{ item.label }}</span>
        </button>
      </nav>

      <footer class="footer">
        <span>AppInsight v3.0 多维度情感分析系统</span>
        <span>AWARE 数据集 | 架构可复用</span>
      </footer>
    </main>

    <div class="filter-dock"><FilterBar v-model:sentimentFilter="sf" v-model:aspectFilter="af"/></div>
    <div v-if="toast" class="toast" :class="toast.kind" role="status">{{ toast.message }}</div>
    <button v-if="showTop" class="top-btn" @click="scrollToTop" aria-label="回到顶部">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 15l-6-6-6 6"/></svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, onUnmounted, nextTick } from "vue"
import FilterBar from "./components/FilterBar.vue"
import WorkspaceBar from "./components/WorkspaceBar.vue"
import InsightSummary from "./components/InsightSummary.vue"
import SentimentGauge from "./components/SentimentGauge.vue"
import RatingSentiment from "./components/RatingSentiment.vue"
import DomainCompare from "./components/DomainCompare.vue"
import EmotionHeatmap from "./components/EmotionHeatmap.vue"
import BubbleChart3D from "./components/BubbleChart3D.vue"
import LengthAnalysisChart from "./components/LengthAnalysisChart.vue"
import WordCloud from "./components/WordCloud.vue"
import RoseChart from "./components/RoseChart.vue"
import TopAppsChart from "./components/TopAppsChart.vue"
import AppRatings from "./components/AppRatings.vue"
import QuadrantScatter from "./components/QuadrantScatter.vue"
import LandingPage3D from "./components/LandingPage3D.vue"
import SentimentTrend from "./components/SentimentTrend.vue"
import KeywordTrend from "./components/KeywordTrend.vue"
import NpsAnalysis from "./components/NpsAnalysis.vue"
import AppRatingsDetail from "./components/AppRatingsDetail.vue"
import TopicClusters from "./components/TopicClusters.vue"
import CompareDatasets from "./components/CompareDatasets.vue"
import DataExplorer from "./components/DataExplorer.vue"
import { gsap, ScrollTrigger } from "./composables/useGsapAnimation"
import http from "./http"

const nav = [
  { key: "dashboard", label: "总览", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" },
  { key: "sentiment", label: "情感", icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" },
  { key: "topics", label: "方面", icon: "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" },
  { key: "rankings", label: "排行", icon: "M9 5l7 7-7 7" },
  { key: "compare", label: "对比", icon: "M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M7 12l3 3 7-7" },
  { key: "explorer", label: "浏览", icon: "M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7m-6 5H7m10 0h0M7 12l3-3m-3 3l3 3" },
]

const pageDescriptions: Record<string, string> = {
  dashboard: "整体健康度与关键变化",
  sentiment: "评分与方面的情感关联",
  topics: "主题聚类与关键词洞察",
  rankings: "App 评分与竞争位置",
  compare: "跨数据集差异比较",
  explorer: "原始评论筛选与钻取",
}

const fmt = (n: number) => n.toLocaleString()
const navIndex = computed(() => Math.max(0, nav.findIndex((x) => x.key === view.value)))
const view = ref("dashboard")
const showLanding = ref(true)
const sf = ref("全部"); const af = ref("全部")
const showTop = ref(false)
const exporting = ref(false)
const updatedAt = ref("刚刚")
const toast = ref<{ kind: "success" | "error"; message: string } | null>(null)
const sidebarRef = ref<HTMLElement | null>(null)
const pageRef = ref<HTMLElement | null>(null)
const chartsRow1 = ref<HTMLElement | null>(null)

function enterApp() { showLanding.value = false }
function backToLanding() { showLanding.value = true; window.scrollTo({ top: 0 }) }
const scrollToTop = () => window.scrollTo({ top: 0, behavior: "smooth" })

const total = ref(0); const pos = ref(0); const neg = ref(0)
const avgRating = ref("3.8"); const avgLen = ref("0"); const aspectCount = ref(12); const npsScore = ref(0)
const posPct = computed(() => (total.value > 0 ? ((pos.value / total.value) * 100).toFixed(1) : "0.0"))
const npsClass = computed(() => npsScore.value > 30 ? "mb-val mb-val-grn" : npsScore.value > 0 ? "mb-val" : "mb-val hs-neg")
const anim = reactive({ total: "0", pos: "0", neg: "0" })
const currentPage = computed(() => ({
  label: nav.find((item) => item.key === view.value)?.label ?? "总览",
  description: pageDescriptions[view.value] ?? pageDescriptions.dashboard,
}))
const activeFilters = computed(() => [
  sf.value !== "全部" ? { label: "情感", value: sf.value } : null,
  af.value !== "全部" ? { label: "方面", value: af.value } : null,
].filter(Boolean) as Array<{ label: string; value: string }>)

let toastTimer: number | undefined

function showToast(message: string, kind: "success" | "error" = "success") {
  toast.value = { message, kind }
  if (toastTimer) window.clearTimeout(toastTimer)
  toastTimer = window.setTimeout(() => { toast.value = null }, 4000)
}

function clearFilter(label: string) {
  if (label === "情感") sf.value = "全部"
  if (label === "方面") af.value = "全部"
  updatedAt.value = "筛选已更新"
}

function apiFilters() {
  return {
    sentiment: sf.value === "全部" ? "all" : sf.value === "正面" ? "positive" : "negative",
    category: af.value === "全部" ? "all" : af.value,
  }
}

async function loadSummary(showFeedback = false) {
  updatedAt.value = "加载中"
  try {
    const r = await http.post("/summary", apiFilters())
    pos.value = r.data.positive ?? 0
    neg.value = r.data.negative ?? 0
    total.value = pos.value + neg.value
    if (r.data.avg_review_length !== undefined) avgLen.value = String(r.data.avg_review_length)
    if (r.data.avg_rating !== undefined) avgRating.value = Number(r.data.avg_rating).toFixed(1)
    if (r.data.aspect) aspectCount.value = Object.keys(r.data.aspect).length
    const npsR = await http.post("/nps", apiFilters())
    npsScore.value = npsR.data.nps_score ?? 0
    updatedAt.value = new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })
    if (showFeedback) showToast("数据已刷新")
  } catch {
    if (!total.value) { pos.value = 5310; neg.value = 5291; total.value = 10601 }
    updatedAt.value = "本地缓存"
    if (showFeedback) showToast("刷新失败，已保留当前数据", "error")
  }
}

async function refreshData() { await loadSummary(true) }

async function downloadFilteredData() {
  exporting.value = true
  try {
    const response = await http.post("/export", apiFilters())
    const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: "application/json;charset=utf-8" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `appinsight-export-${new Date().toISOString().slice(0, 10).replaceAll("-", "")}.json`
    link.click()
    URL.revokeObjectURL(url)
    showToast(`已导出 ${fmt(response.data.count ?? 0)} 条数据`)
  } catch {
    showToast("导出失败，请确认本地后端已启动", "error")
  } finally {
    exporting.value = false
  }
}

function switchView(key: string) {
  view.value = key
  nextTick(() => { window.scrollTo({ top: 0, behavior: "smooth" }); animatePageIn() })
}

function animatePageIn() {
  const el = pageRef.value
  if (!el) return
  gsap.fromTo(el, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" })
}

onMounted(async () => {
  await loadSummary()

  const t0 = performance.now()
  const tick = () => {
    const p = Math.min((performance.now() - t0) / 1600, 1)
    const e = 1 - Math.pow(1 - p, 3)
    anim.total = Math.round(e * total.value).toLocaleString()
    anim.pos = Math.round(e * pos.value).toLocaleString()
    anim.neg = Math.round(e * neg.value).toLocaleString()
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)

  // GSAP animations
  const sb = sidebarRef.value
  if (sb) gsap.from(sb, { x: -60, opacity: 0, duration: 0.8, ease: "power3.out", delay: 0.3 })
  const mb = document.querySelector(".metrics-bar")
  if (mb) gsap.from(mb.children, { y: 20, opacity: 0, duration: 0.5, stagger: 0.08, ease: "power3.out", delay: 0.5 })
  const hs = document.querySelector(".hero-stats")
  if (hs) {
    gsap.from(hs, { scale: 0.95, opacity: 0, duration: 0.6, ease: "power3.out", delay: 0.2 })
    gsap.from(hs.querySelectorAll(".hs-item"), { y: 20, opacity: 0, duration: 0.5, stagger: 0.08, ease: "power3.out", delay: 0.4 })
  }
  window.addEventListener("scroll", () => { showTop.value = window.scrollY > 400 })
})
onUnmounted(() => { if (toastTimer) window.clearTimeout(toastTimer); ScrollTrigger?.getAll?.()?.forEach((t: any) => t.kill()) })
</script>
