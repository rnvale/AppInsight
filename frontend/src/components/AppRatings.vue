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

interface AppRating {
  app: string
  avg_rating: number
  total: number
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

const getBarColor = (rating: number) => {
  if (rating >= 4.5) return SIGNAL_COLORS.positive
  if (rating >= 4.0) return SIGNAL_COLORS.accent
  if (rating >= 3.5) return SIGNAL_COLORS.warning
  return SIGNAL_COLORS.negative
}

const fetchDataAndDraw = async () => {
  if (!chartRef.value) return
  loading.value = true
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/app_ratings', filters)
    const data = res.data as AppRating[]
    drawChart(data)
  } catch (error) {
    console.error('AppRatings fetch error:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = (data: AppRating[]) => {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()

  const top12 = data.slice(0, 12)
  const appNames = top12.map(item => getChineseAppName(item.app))
  const ratings = top12.map(item => item.avg_rating)

  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    ...chartBase,
    tooltip: {
      ...chartTooltip,
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
    },
    grid: { left: '15%', right: '8%', top: '5%', bottom: '5%', containLabel: true },
    xAxis: {
      type: 'value',
      min: 1, max: 5,
      axisLabel: { formatter: '{value}星', color: SIGNAL_COLORS.faint, fontSize: 11 },
      splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } },
      axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
    },
    yAxis: {
      type: 'category',
      data: appNames,
      axisLabel: { fontSize: 11, fontWeight: 500, color: SIGNAL_COLORS.ink },
      axisLine: { show: false }
    },
    series: [{
      type: 'bar',
      data: ratings,
      barWidth: '50%',
      itemStyle: {
        color: (params: any) => getBarColor(params.data),
        borderRadius: [0, 6, 6, 0]
      },
      label: {
        show: true, position: 'right',
        formatter: '{c}星', fontWeight: 600, fontSize: 11, color: SIGNAL_COLORS.ink
      }
    }]
  })
}

onMounted(() => fetchDataAndDraw())
onUnmounted(() => { if (chartInstance) chartInstance.dispose() })
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchDataAndDraw())
</script>

<style scoped>
.chart-container { width: 100%; min-height: 340px; position: relative; }
.chart { width: 100%; height: 340px; }
.loading { text-align: center; padding: 40px; color: #94a3b8; font-size: 13px; }
</style>
