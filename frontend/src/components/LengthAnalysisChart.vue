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
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'

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
  const positiveData = data.map((d: any) => d.total ? d.positive / d.total * 100 : 0)
  const negativeData = data.map((d: any) => d.total ? d.negative / d.total * 100 : 0)
  const positiveRates = data.map((d: any) => d.positive_rate)

  chart.setOption({
    ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: (params: any[]) => {
          const row = data[params[0]?.dataIndex]
          return `<strong>${groupMap[row.length_group] || row.length_group}</strong><br/>正面 ${row.positive} 条（${row.positive_rate}%）<br/>负面 ${row.negative} 条（${row.negative_rate}%）<br/>平均长度 ${row.avg_length} 字`
        },
      },
    legend: { data: ['负面构成', '正面构成'], top: 0, textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 } },
    grid: { left: '16%', right: '8%', bottom: '7%', top: '15%', containLabel: true },
    xAxis: {
      type: 'value', min: 0, max: 100,
      axisLabel: { color: SIGNAL_COLORS.faint, formatter: '{value}%' },
      axisLine: { lineStyle: { color: SIGNAL_COLORS.line } },
      splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } },
    },
    yAxis: { type: 'category', data: lengthGroups, inverse: true, axisLabel: { color: SIGNAL_COLORS.ink, fontSize: 10, fontWeight: 600 }, axisLine: { show: false }, axisTick: { show: false } },
    series: [
      {
        name: '负面构成',
        type: 'bar',
        data: negativeData,
        stack: 'share',
        barWidth: '58%',
        itemStyle: { color: SIGNAL_COLORS.negative, borderRadius: [5, 0, 0, 5] }
      },
      {
        name: '正面构成',
        type: 'bar',
        data: positiveData,
        stack: 'share',
        barWidth: '58%',
        itemStyle: { color: SIGNAL_COLORS.positive, borderRadius: [0, 5, 5, 0] },
        label: { show: true, position: 'right', color: SIGNAL_COLORS.positive, fontSize: 10, formatter: (p: any) => `${positiveRates[p.dataIndex]}%` }
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
