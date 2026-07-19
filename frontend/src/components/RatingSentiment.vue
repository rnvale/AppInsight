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
    const res = await http.post('/rating_sentiment', filters)
    const data = res.data
    if (!Array.isArray(data)) { loading.value = false; return }

    const ratings = data.map((item: any) => `${item.rating} 星`)
    const positives = data.map((item: any) => item.positive ?? 0)
    const negatives = data.map((item: any) => item.negative ?? 0)
    const maxCount = Math.max(...data.map((item: any) => Math.max(item.positive ?? 0, item.negative ?? 0)), 1)
    const axisMax = Math.ceil(maxCount * 1.18)

    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'axis', axisPointer: { type: 'shadow' },
        formatter: (params: any[]) => {
          const row = data[params[0]?.dataIndex]
          return `<strong>${row.rating} 星</strong><br/>正面 ${row.positive} 条（${row.positive_rate}%）<br/>负面 ${row.negative} 条（${row.negative_rate}%）<br/>样本量 ${row.sample_size}`
        },
      },
      legend: { data: ['负面', '正面'], top: 0, textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 } },
      grid: { left: '12%', right: '6%', bottom: '7%', top: '16%', containLabel: true },
      xAxis: {
        type: 'value', min: -axisMax, max: axisMax,
        axisLabel: { color: SIGNAL_COLORS.faint, fontSize: 10, formatter: (value: number) => Math.abs(value).toLocaleString() },
        axisLine: { lineStyle: { color: SIGNAL_COLORS.line } },
        splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } },
        splitNumber: 4,
      },
      yAxis: {
        type: 'category', data: ratings,
        axisLabel: { color: SIGNAL_COLORS.ink, fontSize: 11, fontWeight: 600 },
        axisLine: { show: false }, axisTick: { show: false }
      },
      series: [
        {
          name: '负面', type: 'bar', data: negatives.map((value: number) => -value),
          itemStyle: { color: SIGNAL_COLORS.negative, borderRadius: [4, 0, 0, 4] }, barWidth: '52%',
          label: { show: true, position: 'left', color: SIGNAL_COLORS.negative, fontSize: 10, formatter: (p: any) => Math.abs(p.value) ? Math.abs(p.value) : '' }
        },
        {
          name: '正面', type: 'bar', data: positives,
          itemStyle: { color: SIGNAL_COLORS.positive, borderRadius: [0, 4, 4, 0] }, barWidth: '52%',
          label: { show: true, position: 'right', color: SIGNAL_COLORS.positive, fontSize: 10, formatter: (p: any) => p.value ? p.value : '' }
        }
      ]
    })
  } catch (e) {
    console.error('RatingSentiment:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => initChart())
onUnmounted(() => chartInstance?.dispose())
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchData())
</script>
<style scoped>
.chart-container { width: 100%; height: 300px; position: relative; }
.chart { width: 100%; height: 100%; }
.chart-overlay {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 8px;
  color: #94a3b8; font-size: 13px; background: white; z-index: 2;
}
.spinner {
  width: 20px; height: 20px; border: 2px solid #e2e8f0;
  border-top-color: var(--accent); border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
