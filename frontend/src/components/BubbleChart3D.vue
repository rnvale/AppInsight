<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
    <div v-if="loading" class="chart-overlay"><div class="spinner"></div><span>加载气泡图</span></div>
    <div v-if="!loading && noData" class="chart-overlay"><span>暂无数据</span></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-gl'
import http from '../http'
import { SIGNAL_COLORS, SIGNAL_SCALES } from '../utils/chartTheme'

const props = defineProps<{ sentimentFilter: string; aspectFilter: string }>()
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
  loading.value = true; noData.value = false
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/aspect_sentiment', filters)
    const items = res.data
    if (!Array.isArray(items) || items.length === 0) { noData.value = true; return }

    const names: string[] = []
    // 纯数组 [正面率, 类别索引, 评论量_缩放]
    const rawData: number[][] = []

    items.forEach(function(item: any, i: number) {
      var p = item.positive ?? 0
      var n = item.negative ?? 0
      var t = p + n
      var rate = t > 0 ? p / t : 0.5
      names.push(LABEL_MAP[item.aspect] || item.aspect || '未知')
      // z 轴表示评论量的相对大小，用 sqrt 缩放但别太大
      rawData.push([Math.round(rate * 100), i, Math.round(Math.sqrt(t) * 0.5)])
    })

    chartInstance.setOption({
      tooltip: { formatter: (params: any) => { const row = items[params.dataIndex]; return `<strong>${names[params.dataIndex]}</strong><br/>正面率: ${row.positive_rate}%<br/>正面 ${row.positive} 条 · 负面 ${row.negative} 条<br/>样本量 ${row.sample_size}` } },
      grid3D: {
        boxWidth: 150,
        boxHeight: 120,
        boxDepth: 100,
        viewControl: {
          autoRotate: true,
          autoRotateSpeed: 3,
          distance: 250,
          alpha: 20,
          beta: 30
        },
        light: {
          main: { intensity: 1.2, shadow: true },
          ambient: { intensity: 0.5 }
        }
      },
      xAxis3D: {
        name: '正面率',
        type: 'value',
        min: 0, max: 100,
        axisLabel: { color: '#94a3b8', formatter: '{value}%' },
        nameTextStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 }
      },
      yAxis3D: {
        name: '方面类别',
        type: 'category',
        data: names,
        axisLabel: { show: false },
        nameTextStyle: { color: '#94a3b8', fontSize: 11 }
      },
      zAxis3D: {
        name: '评论量',
        type: 'value',
        axisLabel: { color: '#94a3b8' },
        nameTextStyle: { color: '#94a3b8', fontSize: 11 }
      },
      visualMap: {
        show: true,
        min: 0, max: 100,
        dimension: 0,
        inRange: { color: SIGNAL_SCALES.positive },
        text: ['高正面率', '低正面率'],
        textStyle: { color: SIGNAL_COLORS.muted, fontSize: 10 },
        calculable: true,
        left: 10, bottom: 10,
        orient: 'horizontal',
        itemWidth: 12, itemHeight: 100
      },
      series: [{
        type: 'scatter3D',
        data: rawData,
        // symbolSize: z 轴值代表 sqrt(t)*0.5，乘据让范围在 10~35 之间
        symbolSize: function(dataItem: any, params: any) {
          var z = dataItem ? dataItem[2] : 1
          return Math.max(10, Math.min(35, z * 3))
        },
        itemStyle: {
          opacity: 0.85,
          borderColor: '#ffffff',
          borderWidth: 1
        },
        label: {
          show: false,
          formatter: function(params: any) {
            return params.dataIndex != null ? names[params.dataIndex] : ''
          },
          color: SIGNAL_COLORS.ink,
          fontSize: 10,
          position: 'top'
        },
        emphasis: {
          itemStyle: { opacity: 1 },
          label: { fontSize: 12, fontWeight: 700, color: '#0f172a' }
        }
      }]
    })
  } catch (e: any) {
    console.error('BubbleChart3D:', e)
    noData.value = true
  } finally { loading.value = false }
}

onMounted(function() { initChart(); window.addEventListener('resize', function() { chartInstance?.resize() }) })
onUnmounted(function() { chartInstance?.dispose(); window.removeEventListener('resize', function() { chartInstance?.resize() }) })
watch(function() { return [props.sentimentFilter, props.aspectFilter] }, function() { fetchData() })
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
