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

const appNameMap: Record<string, string> = {
  'notability': '笔记大师',
  'evernote': '印象笔记',
  'evernote-notes-organizer': '印象笔记',
  'bear': '小熊笔记',
  'onenote': 'OneNote',
  'notion': 'Notion',
  'google-keep': '谷歌 Keep',
  'things-3': '事情3',
  'todoist': '任务大师',
  'microsoft-to-do': '微软待办',
  'microsoft-word': '微软 Word',
  'gmail': '谷歌邮箱',
  'gmail-email-by-google': '谷歌邮箱',
  'discord': 'Discord',
  'whatsapp': 'WhatsApp',
  'whatsapp-messenger': 'WhatsApp',
  'monopoly': '大富翁',
  'among-us': '我们之中',
  'among-us-': '我们之中',
  'homescapes': '梦幻家园',
  'free-tone-calling-texting': '免费通话'
}

const getChineseAppName = (appName: string): string => {
  if (!appName) return '未知'
  if (appNameMap[appName]) return appNameMap[appName]
  const firstWord = appName.split('-')[0]
  if (firstWord && appNameMap[firstWord]) return appNameMap[firstWord]
  if (appName.length > 15) return appName.slice(0, 12) + '...'
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
    const res = await http.post('/top_apps', filters)
    const data = res.data as any[]
    if (data && data.length > 0) drawChart(data)
  } catch (error) {
    console.error('TopAppsChart fetch error:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = (data: any[]) => {
  if (!chartRef.value) return
  if (chartInstance) { chartInstance.dispose() }

  const top8 = data.slice(0, 8)
  const appNames = top8.map(item => getChineseAppName(item.app))

  chartInstance = echarts.init(chartRef.value)

  chartInstance.setOption({
    ...chartBase,
    tooltip: {
      ...chartTooltip,
      trigger: 'axis',
      axisPointer: { type: 'line' },
      formatter: (params: any) => {
        const idx = params.data?.dataIndex ?? 0
        const app = top8[idx]
        if (!app) return ''
        return `<strong>${appNames[idx]}</strong><br/>正面率: ${app.positive_rate}%<br/>评论量: ${app.sample_size}<br/>平均评分: ${app.avg_rating ?? '—'}`
      }
    },
    legend: { show: false },
    grid: { left: '22%', right: '10%', bottom: '8%', top: '15%', containLabel: true },
    xAxis: {
      type: 'value', min: 0, max: 100,
      name: '正面率', nameLocation: 'middle', nameGap: 28,
      axisLabel: { color: SIGNAL_COLORS.faint, formatter: '{value}%' },
      axisLine: { lineStyle: { color: SIGNAL_COLORS.line } },
      splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } },
    },
    yAxis: { type: 'category', data: appNames, inverse: true, axisLabel: { color: SIGNAL_COLORS.ink, fontSize: 11, fontWeight: 600 }, axisLine: { show: false }, axisTick: { show: false } },
    series: [{
      name: '正面率', type: 'scatter',
      data: top8.map((item, index) => ({ value: [item.positive_rate, index], dataIndex: index, total: item.sample_size, rate: item.positive_rate })),
      symbolSize: (value: any, params: any) => Math.min(30, Math.max(12, 10 + Math.log10(top8[params.dataIndex]?.sample_size || 1) * 5)),
      itemStyle: { color: (params: any) => params.data.rate >= 50 ? SIGNAL_COLORS.positive : SIGNAL_COLORS.negative, opacity: 0.9, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, position: 'right', color: SIGNAL_COLORS.ink, fontSize: 10, fontWeight: 700, formatter: (p: any) => `${p.data.rate}%` },
      markLine: { silent: true, symbol: 'none', lineStyle: { color: SIGNAL_COLORS.neutralSoft, type: 'dashed' }, label: { formatter: '50% 基线', color: SIGNAL_COLORS.faint, fontSize: 9 }, data: [{ xAxis: 50 }] },
      emphasis: { itemStyle: { opacity: 1, shadowBlur: 14, shadowColor: 'rgba(46,139,120,.2)' }, label: { fontSize: 11 } }
    }]
  })
}

onMounted(() => { fetchDataAndDraw() })
onUnmounted(() => { if (chartInstance) chartInstance.dispose() })
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchDataAndDraw())
</script>

<style scoped>
.chart-container { width: 100%; min-height: 340px; position: relative; }
.chart { width: 100%; height: 340px; }
.loading { text-align: center; padding: 40px; color: #94a3b8; font-size: 13px; }
</style>
