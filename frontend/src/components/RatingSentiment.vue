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
    const totals = data.map((item: any) => item.total ?? 0)

    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
      },
      legend: {
        data: ['正面评论', '负面评论', '总计'],
        top: 0,
        textStyle: { color: SIGNAL_COLORS.muted, fontSize: 12 }
      },
      grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
      xAxis: {
        type: 'category', data: ratings,
        axisLabel: { color: SIGNAL_COLORS.muted, fontWeight: 500 },
        axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: SIGNAL_COLORS.faint },
        splitLine: { lineStyle: { color: SIGNAL_COLORS.grid } }
      },
      series: [
        {
          name: '正面评论', type: 'bar', stack: 'sentiment', data: positives,
          itemStyle: { color: SIGNAL_COLORS.positive, borderRadius: [4, 4, 0, 0] }, barWidth: '50%'
        },
        {
          name: '负面评论', type: 'bar', stack: 'sentiment', data: negatives,
          itemStyle: { color: SIGNAL_COLORS.negative, borderRadius: [0, 0, 4, 4] }
        },
        {
          name: '总计', type: 'line', data: totals,
          lineStyle: { color: SIGNAL_COLORS.accent, width: 2 },
          itemStyle: { color: SIGNAL_COLORS.accent }, symbol: 'circle', symbolSize: 6
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
