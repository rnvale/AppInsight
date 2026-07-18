<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="chart-overlay"><div class="spinner"></div><span>加载热力图</span></div>
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

const LABEL_MAP: Record<string, string> = {
  'usability': '可用性', 'general': '整体评价', 'effectiveness': '有效性',
  'cost': '价格', 'compatibility': '兼容性', 'reliability': '可靠性',
  'efficiency': '效率', 'security': '安全性', 'safety': '安全',
  'enjoyability': '娱乐性', 'learnability': '易学性', 'aesthetics': '美观性'
}

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
    const res = await http.post('/emotion_heatmap', filters)
    const data = res.data
    if (!Array.isArray(data) || data.length === 0) { loading.value = false; return }

    const ratings = [...new Set(data.map((item: any) => item.rating))].sort()
    const aspects = [...new Set(data.map((item: any) => item.category))]

    const heatmapData: [number, number, number][] = []
    for (const rating of ratings) {
      for (const aspect of aspects) {
        const item = data.find((d: any) => d.rating === rating && d.category === aspect)
        const value = item ? ((item.positive_rate ?? 0) / 100) : 0
        heatmapData.push([ratings.indexOf(rating), aspects.indexOf(aspect), value])
      }
    }

    chartInstance.setOption({
      tooltip: {
        formatter: (p: any) => {
          const r = ratings[p.value[0]]
          const a = aspects[p.value[1]]
          const v = p.value[2]
          return `<strong>${r} 星</strong> &middot; ${LABEL_MAP[a] || a}<br/>正面率: ${(v * 100).toFixed(1)}%`
        },
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: '#e2e8f0',
        textStyle: { color: '#0f172a' }
      },
      grid: { left: '15%', right: '5%', bottom: '12%', top: '8%' },
      xAxis: {
        type: 'category',
        data: ratings.map((r: any) => `${r} 星`),
        splitArea: { show: true },
        axisLabel: { color: '#64748b', fontWeight: 600, fontSize: 11 },
        axisLine: { lineStyle: { color: '#e2e8f0' } }
      },
      yAxis: {
        type: 'category',
        data: aspects.map((a: string) => LABEL_MAP[a] || a),
        splitArea: { show: true },
        axisLabel: { color: '#64748b', fontSize: 10 },
        axisLine: { lineStyle: { color: '#e2e8f0' } }
      },
      visualMap: {
        min: 0, max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center', bottom: 0,
        inRange: { color: ['#fecaca', '#fde68a', '#86efac', '#22c55e'] },
        textStyle: { color: '#64748b', fontSize: 11 }
      },
      series: [{
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: true, color: '#0f172a', fontSize: 11, fontWeight: 600,
          formatter: (p: any) => (p.value[2] * 100).toFixed(0) + '%'
        },
        emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.15)' } }
      }]
    })
  } catch (e) {
    console.error('EmotionHeatmap:', e)
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
  border-top-color: #2563eb; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
