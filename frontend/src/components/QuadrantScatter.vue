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
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'

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
    const payload = res.data as { data: AppData[]; mid_positive_rate: number; mid_reviews: number }
    if (payload?.data?.length > 0) drawChart(payload.data, payload.mid_positive_rate, payload.mid_reviews)
  } catch (error) {
    console.error('QuadrantScatter fetch error:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = (data: AppData[], midRating: number, midReviews: number) => {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()

  const validData = data.filter(d => d.avg_rating > 0 && d.total_reviews > 0)
  if (validData.length === 0) return

  const reviews = validData.map(d => d.total_reviews)
  const yMax = Math.ceil(Math.max(...reviews, midReviews) * 1.08)

  const seriesData = validData.map(item => ({
    name: getChineseAppName(item.app),
    value: [item.positive_rate, item.total_reviews],
    symbolSize: Math.min(36, Math.max(10, 12 + Math.log10(item.total_reviews) * 5)),
    rating: item.avg_rating,
    reviews: item.total_reviews,
    positiveRate: item.positive_rate
  }))

  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    ...chartBase,
    tooltip: {
      ...chartTooltip,
      trigger: 'item',
      formatter: (params: any) => {
        const d = params.data
        return '<strong>' + d.name + '</strong><br/>正面率: ' + (d.positiveRate || 0).toFixed(1) + '%<br/>平均评分: ' + d.rating + ' 星<br/>评论数: ' + d.reviews
      }
    },
    grid: { left: '10%', right: '8%', top: '8%', bottom: '10%', containLabel: true },
    xAxis: {
      name: '正面率',
      nameLocation: 'middle', nameGap: 35,
      type: 'value', min: 0, max: 100,
      axisLabel: { color: SIGNAL_COLORS.faint, fontSize: 11, formatter: '{value}%' },
      splitLine: { lineStyle: { type: 'dashed', color: SIGNAL_COLORS.grid } },
      axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
    },
    yAxis: {
      name: '评论量（对数）', type: 'log',
      nameLocation: 'middle', nameGap: 40,
      min: 1, max: yMax,
      axisLabel: { color: SIGNAL_COLORS.faint, fontSize: 11, formatter: (v: number) => v >= 1000 ? (v / 1000).toFixed(1) + 'k' : '' + v },
      splitLine: { lineStyle: { type: 'dashed', color: SIGNAL_COLORS.grid } },
      axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
    },
    series: [{
      type: 'scatter',
      data: seriesData,
      symbolSize: (params: any) => params.symbolSize || 18,
      itemStyle: {
        color: (params: any) => {
          return params.data.positiveRate >= midRating ? SIGNAL_COLORS.positive : SIGNAL_COLORS.negative
        },
        opacity: 0.75,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.7)'
      },
      label: { show: false, formatter: (params: any) => params.name, color: SIGNAL_COLORS.ink, fontSize: 10, position: 'right' },
      emphasis: {
        itemStyle: { opacity: 1, shadowBlur: 12, shadowColor: 'rgba(0,0,0,0.1)' },
        label: { show: true, fontSize: 11, fontWeight: 600 }
      },
      markArea: {
        silent: true,
        itemStyle: { opacity: 0.035 },
        data: [
          [{ xAxis: 0, yAxis: midReviews }, { xAxis: midRating, yAxis: yMax, itemStyle: { color: SIGNAL_COLORS.negative } }],
          [{ xAxis: midRating, yAxis: midReviews }, { xAxis: 100, yAxis: yMax, itemStyle: { color: SIGNAL_COLORS.positive } }],
        ]
      },
      markLine: {
        silent: true, symbol: 'none',
        lineStyle: { color: SIGNAL_COLORS.line, type: 'solid', width: 1 },
        data: [
          { xAxis: midRating, label: { formatter: '中位正面率 ' + midRating + '%', color: SIGNAL_COLORS.faint, fontSize: 9 } },
          { yAxis: midReviews, label: { formatter: '中位评论量 ' + midReviews, color: SIGNAL_COLORS.faint, fontSize: 9 } }
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
