<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import http from '../http'

const groupMap: Record<string, string> = {
  '短评论(≤20字)': '短评论 (≤20字)',
  '中评论(21-50字)': '中评论 (21-50字)',
  '长评论(51-100字)': '长评论 (51-100字)',
  '超长评论(>100字)': '超长评论 (>100字)'
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
    const res = await http.post('/length_analysis', filters)
    const data = res.data
    drawChart(data)
  } catch (error) {
    console.error('LengthAnalysisChart fetch error:', error)
  } finally {
    loading.value = false
  }
}

const drawChart = (data: any[]) => {
  if (!chartRef.value) return
  if (chartInstance) { chartInstance.dispose() }
  const chart = echarts.init(chartRef.value)
  chartInstance = chart

  const lengthGroups = data.map((d: any) => groupMap[d.length_group] || d.length_group)
  const positiveData = data.map((d: any) => d.positive)
  const negativeData = data.map((d: any) => d.negative)
  const positiveRates = data.map((d: any) => d.positive_rate)

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#0f172a' }
    },
    legend: {
      data: ['正面评论', '负面评论', '正面率'],
      top: 0,
      textStyle: { color: '#475569', fontSize: 12 }
    },
    grid: { left: '3%', right: '5%', bottom: '3%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      data: lengthGroups,
      axisLabel: { color: '#475569', fontWeight: 500 },
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
        data: positiveData,
        barWidth: '35%',
        itemStyle: { color: '#16a34a', borderRadius: [6, 6, 0, 0] }
      },
      {
        name: '负面评论',
        type: 'bar',
        data: negativeData,
        barWidth: '35%',
        itemStyle: { color: '#dc2626', borderRadius: [6, 6, 0, 0] }
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
onUnmounted(() => { if (chartInstance) { chartInstance.dispose() } })
</script>

<style scoped>
.chart-container { width: 100%; min-height: 340px; position: relative; }
.chart { width: 100%; height: 340px; }
.loading { text-align: center; padding: 40px; color: #94a3b8; font-size: 13px; }
</style>
