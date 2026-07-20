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

const COLORS = [
  SIGNAL_COLORS.accent, SIGNAL_COLORS.positive, SIGNAL_COLORS.negative, SIGNAL_COLORS.warning,
  '#8B6E63', '#5E9C91', '#B7746A', '#7692A0', '#D0A969', '#3E776B',
  '#A65D4E', '#4D6673'
]

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

    const pieData = items.map((item: any) => ({
      ...item,
      name: LABEL_MAP[item.aspect] || item.aspect || '未知',
      value: (item.positive ?? 0) + (item.negative ?? 0)
    })).filter((d: any) => d.value > 0)

    chartInstance.clear()
    chartInstance.setOption({
      ...chartBase,
      tooltip: {
        ...chartTooltip,
        trigger: 'item',
        formatter: (params: any) => {
          const row = params.data
          return `<strong>${row.name}</strong><br/>${row.value.toLocaleString()} 条（${params.percent}%）<br/>正面 ${row.positive} 条（${row.positive_rate}%）<br/>负面 ${row.negative} 条（${row.negative_rate}%）`
        },
      },
      legend: {
        orient: 'vertical', right: 8, top: 'center',
        textStyle: { color: SIGNAL_COLORS.muted, fontSize: 10 }
      },
      series: [{
        type: 'pie',
        roseType: 'radius',
        radius: ['15%', '75%'],
        center: ['40%', '50%'],
        data: pieData,
        itemStyle: {
          borderRadius: 4,
          borderColor: SIGNAL_COLORS.panel,
          borderWidth: 2,
          color: (params: any) => COLORS[params.dataIndex % COLORS.length]
        },
        label: {
          color: SIGNAL_COLORS.ink, fontSize: 11, fontWeight: 500,
          formatter: (params: any) => `${params.name}\n${params.value.toLocaleString()} 条`
        },
        labelLine: { length: 10, length2: 8, lineStyle: { color: SIGNAL_COLORS.neutralSoft } },
        animationDuration: 800,
        animationEasing: 'cubicOut'
      }]
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
