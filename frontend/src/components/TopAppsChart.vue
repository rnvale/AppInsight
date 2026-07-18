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
  const positiveData = top8.map(item => item.positive)
  const negativeData = top8.map(item => item.negative)
  const positiveRates = top8.map(item => item.positive_rate)

  chartInstance = echarts.init(chartRef.value)

  chartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#0f172a' },
      formatter: (params: any) => {
        const idx = params[0].dataIndex
        const app = top8[idx]
        if (!app) return ''
        return `<strong>${appNames[idx]}</strong><br/>正面: ${app.positive}<br/>负面: ${app.negative}<br/>正面率: ${app.positive_rate}%`
      }
    },
    legend: {
      data: ['正面评论', '负面评论', '正面率'],
      top: 0,
      textStyle: { color: '#475569', fontSize: 12 }
    },
    grid: { left: '3%', right: '5%', bottom: '3%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      data: appNames,
      axisLabel: { color: '#475569', fontWeight: 500, rotate: 20, interval: 0 },
      axisLine: { lineStyle: { color: '#e2e8f0' } }
    },
    yAxis: [
      {
        type: 'value',
        name: '评论数量',
        nameTextStyle: { color: '#94a3b8', fontSize: 11 },
        axisLabel: { color: '#94a3b8' },
        splitLine: { lineStyle: { color: '#f1f5f9' } }
      },
      {
        type: 'value',
        name: '正面率',
        nameTextStyle: { color: '#2563eb', fontSize: 11, fontWeight: 500 },
        min: 0, max: 100,
        axisLabel: { color: '#2563eb', formatter: '{value}%' },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '正面评论',
        type: 'bar',
        stack: 'total',
        data: positiveData,
        itemStyle: { color: '#16a34a', borderRadius: [4, 4, 0, 0] },
        barWidth: '50%'
      },
      {
        name: '负面评论',
        type: 'bar',
        stack: 'total',
        data: negativeData,
        itemStyle: { color: '#dc2626', borderRadius: [0, 0, 4, 4] }
      },
      {
        name: '正面率',
        type: 'line',
        yAxisIndex: 1,
        data: positiveRates,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { width: 2, color: '#2563eb' },
        itemStyle: { color: '#2563eb' }
      }
    ]
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
