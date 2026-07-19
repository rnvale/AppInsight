<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="chart-overlay"><div class="spinner"></div><span>生成玫瑰图</span></div>
    <div v-if="!loading && noData" class="chart-overlay"><span>暂无数据</span></div>
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
const noData = ref(false)
let chartInstance: echarts.ECharts | null = null

const LABEL_MAP: Record<string, string> = {
  'usability': '可用性', 'general': '整体评价', 'effectiveness': '有效性',
  'cost': '价格', 'compatibility': '兼容性', 'reliability': '可靠性',
  'efficiency': '效率', 'security': '安全性', 'safety': '安全',
  'enjoyability': '娱乐性', 'learnability': '易学性', 'aesthetics': '美观性'
}

function initChart() {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()
  chartInstance = echarts.init(chartRef.value)
  fetchData()
}

async function fetchData() {
  if (!chartInstance) return
  loading.value = true
  noData.value = false
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/aspect_sentiment', filters)
    const items = res.data
    if (!Array.isArray(items) || items.length === 0) {
      noData.value = true
      return
    }

    const ranked = items.map((item: any) => ({
      ...item,
      name: LABEL_MAP[item.aspect] || item.aspect || '未知',
      value: (item.positive ?? 0) + (item.negative ?? 0)
    })).filter((d: any) => d.value > 0).sort((a: any, b: any) => b.value - a.value)

    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'axis', axisPointer: { type: 'shadow' },
        formatter: (params: any[]) => {
          const row = ranked[params[0]?.dataIndex]
          return `<strong>${row.name}</strong><br/>正面 ${row.positive} 条（${row.positive_rate}%）<br/>负面 ${row.negative} 条（${row.negative_rate}%）<br/>样本量 ${row.sample_size}`
        },
      },
      legend: { data: ['负面', '正面'], top: 0, textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 } },
      grid: { left: '20%', right: '10%', top: '14%', bottom: '7%', containLabel: true },
      xAxis: { type: 'value', axisLabel: { color: SIGNAL_COLORS.faint }, splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } } },
      yAxis: { type: 'category', data: ranked.map((row: any) => row.name), inverse: true, axisLabel: { color: SIGNAL_COLORS.ink, fontSize: 10, fontWeight: 600 }, axisLine: { show: false }, axisTick: { show: false } },
      series: [
        { name: '负面', type: 'bar', stack: 'sentiment', data: ranked.map((row: any) => row.negative), barWidth: '58%', itemStyle: { color: SIGNAL_COLORS.negative, borderRadius: [4, 0, 0, 4] } },
        { name: '正面', type: 'bar', stack: 'sentiment', data: ranked.map((row: any) => row.positive), barWidth: '58%', itemStyle: { color: SIGNAL_COLORS.positive, borderRadius: [0, 4, 4, 0] }, label: { show: true, position: 'right', color: SIGNAL_COLORS.muted, fontSize: 9, formatter: (p: any) => `${ranked[p.dataIndex].positive_rate}%` } }
      ]
    })
  } catch (e) {
    console.error('RoseChart:', e)
    noData.value = true
  } finally {
    loading.value = false
  }
}

onMounted(() => { initChart(); window.addEventListener('resize', () => chartInstance?.resize()) })
onUnmounted(() => { chartInstance?.dispose() })
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
