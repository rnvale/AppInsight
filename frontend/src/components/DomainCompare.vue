<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="chart-overlay"><div class="spinner"></div><span>加载图表</span></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import http from '../http'
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'

const props = defineProps<{
  sentimentFilter: string
  aspectFilter: string
}>()

const chartRef = ref<HTMLElement>()
const loading = ref(true)
let chartInstance: echarts.ECharts | null = null

function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  fetchData()
}

async function fetchData() {
  if (!chartInstance) return
  loading.value = true
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/domain_compare', filters)
    const data = res.data
    if (!Array.isArray(data) || data.length === 0) { loading.value = false; return }

    const sorted = [...data].sort((a: any, b: any) => (b.positive_rate ?? 0) - (a.positive_rate ?? 0))
    const domains = sorted.map((d: any) => d.domain || '未知')
    const positives = sorted.map((d: any) => d.total ? (d.positive / d.total * 100) : 0)
    const negatives = sorted.map((d: any) => d.total ? (d.negative / d.total * 100) : 0)
    const rates = sorted.map((d: any) => d.positive_rate ?? 0)

    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'axis', axisPointer: { type: 'shadow' },
        formatter: (params: any[]) => {
          const row = sorted[params[0]?.dataIndex]
          return `<strong>${row.domain || '未知'}</strong><br/>正面 ${row.positive} 条（${row.positive_rate}%）<br/>负面 ${row.negative} 条（${row.negative_rate}%）<br/>样本量 ${row.sample_size}`
        },
      },
      legend: { data: ['正面构成', '负面构成'], top: 0, textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 } },
      grid: { left: '15%', right: '7%', bottom: '7%', top: '15%', containLabel: true },
      xAxis: {
        type: 'value', min: 0, max: 100,
        axisLabel: { color: SIGNAL_COLORS.faint, formatter: '{value}%' },
        axisLine: { lineStyle: { color: SIGNAL_COLORS.line } },
        splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } },
      },
      yAxis: { type: 'category', data: domains, inverse: true, axisLabel: { color: SIGNAL_COLORS.ink, fontSize: 11, fontWeight: 600 }, axisLine: { show: false }, axisTick: { show: false } },
      series: [
        { name: '负面构成', type: 'bar', stack: 'share', data: negatives, itemStyle: { color: SIGNAL_COLORS.negative, borderRadius: [4, 0, 0, 4] }, barWidth: '54%' },
        { name: '正面构成', type: 'bar', stack: 'share', data: positives, itemStyle: { color: SIGNAL_COLORS.positive, borderRadius: [0, 4, 4, 0] }, barWidth: '54%', label: { show: true, position: 'right', color: SIGNAL_COLORS.positive, fontSize: 10, formatter: (p: any) => `${rates[p.dataIndex]}%` } }
      ]
    })
  } catch (e) {
    console.error('DomainCompare:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => initChart())
onUnmounted(() => chartInstance?.dispose())
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchData())
</script>

<style scoped>
.chart-container { width: 100%; height: 360px; position: relative; }
.chart { width: 100%; height: 100%; }
.chart-overlay {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 8px;
  color: #94a3b8; font-size: 13px; background: white; z-index: 2;
}
.spinner {
  width: 20px; height: 20px; border: 2px solid #e2e8f0;
  border-top-color: var(--accent); border-radius: 50%; animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
