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

    const domains = data.map((d: any) => d.domain || '未知')
    const positives = data.map((d: any) => d.positive ?? 0)
    const negatives = data.map((d: any) => d.negative ?? 0)
    const rates = data.map((d: any) => d.positive_rate ?? 0)

    chartInstance.setOption({
      tooltip: {
        trigger: 'axis', axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e2e8f0',
        textStyle: { color: '#0f172a' }
      },
      legend: {
        data: ['正面评论', '负面评论', '正面率'],
        top: 0, textStyle: { color: '#64748b', fontSize: 12 }
      },
      grid: { left: '3%', right: '5%', bottom: '3%', top: '15%', containLabel: true },
      xAxis: {
        type: 'category', data: domains,
        axisLabel: { color: '#64748b', fontWeight: 500, rotate: domains.length > 6 ? 20 : 0 },
        axisLine: { lineStyle: { color: '#e2e8f0' } }
      },
      yAxis: [
        {
          type: 'value', name: '评论数量',
          nameTextStyle: { color: '#94a3b8', fontSize: 11, fontWeight: 500 },
          axisLabel: { color: '#94a3b8' },
          splitLine: { lineStyle: { color: '#f1f5f9' } }
        },
        {
          type: 'value', name: '正面率', min: 0, max: 100,
          nameTextStyle: { color: '#0066FF', fontSize: 11, fontWeight: 500 },
          axisLabel: { color: '#0066FF', formatter: '{value}%' },
          splitLine: { show: false }
        }
      ],
      series: [
        { name: '正面评论', type: 'bar', stack: 'total', data: positives, itemStyle: { color: '#16a34a', borderRadius: [4, 4, 0, 0] }, barWidth: '50%' },
        { name: '负面评论', type: 'bar', stack: 'total', data: negatives, itemStyle: { color: '#dc2626', borderRadius: [0, 0, 4, 4] } },
        { name: '正面率', type: 'line', yAxisIndex: 1, data: rates, lineStyle: { color: '#0066FF', width: 2 }, itemStyle: { color: '#0066FF' }, symbol: 'circle', symbolSize: 6 }
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
  border-top-color: #0066FF; border-radius: 50%; animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
