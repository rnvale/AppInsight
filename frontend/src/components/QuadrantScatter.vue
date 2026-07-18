<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import http from '../http'

interface AppData {
  app: string
  avg_rating: number
  total_reviews: number
  positive_rate: number
}

const appNameMap: Record<string, string> = {
  'notability': '笔记大师', 'evernote': '印象笔记', 'evernote-notes-organizer': '印象笔记',
  'things-3': '事情3', 'todoist': '任务大师', 'microsoft-to-do': '微软待办',
  'microsoft-word': '微软 Word', 'gmail': '谷歌邮箱', 'gmail-email-by-google': '谷歌邮箱',
  'discord': 'Discord', 'whatsapp': 'WhatsApp', 'whatsapp-messenger': 'WhatsApp',
  'monopoly': '大富翁', 'among-us': '我们之中', 'among-us-': '我们之中',
  'homescapes': '梦幻家园', 'free-tone-calling-texting': '免费通话',
  'google-keep': '谷歌Keep', 'onenote': 'OneNote', 'bear': '小熊笔记', 'notion': 'Notion'
}

const getChineseAppName = (appName: string): string => {
  if (!appName) return '未知'
  if (appNameMap[appName]) return appNameMap[appName]
  const firstWord = appName.split('-')[0]
  if (firstWord && appNameMap[firstWord]) return appNameMap[firstWord]
  if (appName.length > 12) return appName.slice(0, 10) + '..'
  return appName
}

const chartRef = ref<HTMLElement | null>(null)
const loading = ref(true)
let chartInstance: any = null

const props = defineProps<{
  sentimentFilter: string
  aspectFilter: string
}>()

const fetchDataAndDraw = async () => {
  if (!chartRef.value) return
  loading.value = true
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/quadrant_scatter', filters)
    const data = res.data as AppData[]
    if (data && data.length > 0) drawChart(data)
  } catch (error) {
    console.error('QuadrantScatter fetch error:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = (data: AppData[]) => {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()

  const validData = data.filter(d => d.avg_rating > 0 && d.total_reviews > 0)
  if (validData.length === 0) return

  const ratings = validData.map(d => d.avg_rating)
  const reviews = validData.map(d => d.total_reviews)
  const minRating = Math.max(1, Math.floor(Math.min(...ratings) * 10) / 10 - 0.2)
  const maxRating = Math.min(5, Math.ceil(Math.max(...ratings) * 10) / 10 + 0.2)
  const sortedReviews = [...reviews].sort((a, b) => a - b)
  const yMin = Math.max(0, Math.floor((sortedReviews[Math.floor(sortedReviews.length * 0.1)] || 0) / 10) * 10)
  const yMax = Math.ceil(((sortedReviews[Math.floor(sortedReviews.length * 0.9)] || 500) + 50) / 10) * 10
  const midRating = 3.8
  const midReviews = sortedReviews[Math.floor(sortedReviews.length / 2)] || 200

  const seriesData = validData.map(item => ({
    name: getChineseAppName(item.app),
    value: [item.avg_rating, item.total_reviews],
    symbolSize: Math.min(36, Math.max(10, 12 + Math.log10(item.total_reviews) * 5)),
    rating: item.avg_rating,
    reviews: item.total_reviews,
    positiveRate: item.positive_rate
  }))

  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#0f172a' },
      formatter: (params: any) => {
        const d = params.data
        return '<strong>' + d.name + '</strong><br/>评分: ' + d.rating + ' 星<br/>评论数: ' + d.reviews + '<br/>正面率: ' + (d.positiveRate || 0).toFixed(1) + '%'
      }
    },
    grid: { left: '8%', right: '10%', top: '5%', bottom: '8%', containLabel: true },
    xAxis: {
      name: '平均评分',
      nameLocation: 'middle', nameGap: 35,
      min: minRating, max: maxRating, interval: 0.5,
      axisLabel: { color: '#94a3b8', fontSize: 11 },
      splitLine: { lineStyle: { type: 'dashed', color: '#f1f5f9' } },
      axisLine: { lineStyle: { color: '#e2e8f0' } }
    },
    yAxis: {
      name: '评论数量',
      nameLocation: 'middle', nameGap: 40,
      min: yMin, max: yMax,
      axisLabel: { color: '#94a3b8', fontSize: 11, formatter: (v: number) => v >= 1000 ? (v / 1000).toFixed(1) + 'k' : '' + v },
      splitLine: { lineStyle: { type: 'dashed', color: '#f1f5f9' } },
      axisLine: { lineStyle: { color: '#e2e8f0' } }
    },
    series: [{
      type: 'scatter',
      data: seriesData,
      symbolSize: (params: any) => params.symbolSize || 18,
      itemStyle: {
        color: (params: any) => {
          const r = params.data.rating
          const rc = params.data.reviews
          if (r >= midRating && rc >= midReviews) return '#16a34a'
          if (r < midRating && rc >= midReviews) return '#dc2626'
          if (r >= midRating && rc < midReviews) return '#2563eb'
          return '#94a3b8'
        },
        opacity: 0.75,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.7)'
      },
      label: {
        show: true, formatter: (params: any) => params.name, color: '#475569', fontSize: 9, position: 'right'
      },
      emphasis: {
        itemStyle: { opacity: 1, shadowBlur: 12, shadowColor: 'rgba(0,0,0,0.1)' },
        label: { fontSize: 11, fontWeight: 600 }
      },
      markLine: {
        silent: true, symbol: 'none',
        lineStyle: { color: '#cbd5e1', type: 'solid', width: 1 },
        data: [
          { xAxis: midRating, label: { formatter: '中值 ' + midRating, color: '#94a3b8', fontSize: 9 } },
          { yAxis: midReviews, label: { formatter: '', color: '#94a3b8', fontSize: 9 } }
        ]
      }
    }]
  })
}

onMounted(() => { fetchDataAndDraw() })
onUnmounted(() => { if (chartInstance) chartInstance.dispose() })
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchDataAndDraw())
</script>

<style scoped>
.chart-container { width: 100%; min-height: 380px; position: relative; }
.chart { width: 100%; height: 380px; }
.loading { text-align: center; padding: 40px; color: #94a3b8; font-size: 13px; }
</style>
