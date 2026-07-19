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
import { chartBase, chartTooltip, SIGNAL_COLORS, SIGNAL_SCALES } from '../utils/chartTheme'

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
        const value = item ? ((item.sentiment_balance ?? 0) / 100) : 0
        heatmapData.push([ratings.indexOf(rating), aspects.indexOf(aspect), value])
      }
    }

    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        formatter: (p: any) => {
          const r = ratings[p.value[0]]
          const a = aspects[p.value[1]]
          const item = data.find((d: any) => d.rating === ratings[p.value[0]] && d.category === aspects[p.value[1]])
          const v = p.value[2]
          return `<strong>${r} 星</strong> · ${LABEL_MAP[a] || a}<br/>情感平衡: ${(v * 100).toFixed(1)}%<br/>正面 ${item?.positive ?? 0} 条 · 负面 ${item?.negative ?? 0} 条<br/>样本量 ${item?.sample_size ?? 0}`
        },
      },
      grid: { left: '15%', right: '5%', bottom: '12%', top: '8%' },
      xAxis: {
        type: 'category',
        data: ratings.map((r: any) => `${r} 星`),
        splitArea: { show: true },
        axisLabel: { color: SIGNAL_COLORS.muted, fontWeight: 600, fontSize: 11 },
        axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
      },
      yAxis: {
        type: 'category',
        data: aspects.map((a: string) => LABEL_MAP[a] || a),
        splitArea: { show: true },
        axisLabel: { color: SIGNAL_COLORS.muted, fontSize: 10 },
        axisLine: { lineStyle: { color: SIGNAL_COLORS.line } }
      },
      visualMap: {
        min: -1, max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center', bottom: 0,
        inRange: { color: SIGNAL_SCALES.balance },
        text: ['正面', '负面'],
        textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 }
      },
      series: [{
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: true, color: SIGNAL_COLORS.ink, fontSize: 11, fontWeight: 600,
          formatter: (p: any) => `${p.value[2] > 0 ? '+' : ''}${(p.value[2] * 100).toFixed(0)}%`
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
  border-top-color: var(--accent); border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
