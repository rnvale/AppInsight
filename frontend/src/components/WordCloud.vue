<template>
  <div class="chart-container">
    <div class="cloud-tabs">
      <button :class="{ active: activeTab === 'positive' }" @click="activeTab = 'positive'; drawCurrentCloud()">正面词云</button>
      <button :class="{ active: activeTab === 'negative' }" @click="activeTab = 'negative'; drawCurrentCloud()">负面词云</button>
      <span class="cloud-divider"></span>
      <button :class="{ active: visualMode === 'ranking' }" @click="setMode('ranking')">关键词排名</button>
      <button :class="{ active: visualMode === 'cloud' }" @click="setMode('cloud')">词云视图</button>
    </div>
    <div v-if="visualMode === 'ranking'" :class="['keyword-ranking', activeTab]">
      <div v-for="(word, index) in currentWords.slice(0, 12)" :key="word.name" class="keyword-row">
        <span class="keyword-rank">{{ String(index + 1).padStart(2, '0') }}</span>
        <strong>{{ word.name }}</strong>
        <span class="keyword-bar"><i :style="{ width: `${(word.value / (currentWords[0]?.value || 1)) * 100}%` }"></i></span>
        <span class="keyword-value">{{ word.value }}</span>
      </div>
    </div>
    <div v-else ref="chartRef" class="chart"></div>
    <div v-if="loading" class="loading">生成词云中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import http from '../http'
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'

const chartRef = ref<HTMLElement | null>(null)
const loading = ref(true)
const activeTab = ref('positive')
const visualMode = ref<'ranking' | 'cloud'>('ranking')
let chartInstance: any = null
const positiveWords = ref<any[]>([])
const negativeWords = ref<any[]>([])

const props = defineProps<{
  sentimentFilter: string
  aspectFilter: string
}>()

const fetchDataAndDraw = async () => {
  loading.value = true
  try {
    const filters = {
      sentiment: props.sentimentFilter === '全部' ? 'all' : (props.sentimentFilter === '正面' ? 'positive' : 'negative'),
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter
    }
    const res = await http.post('/wordcloud', filters)
    const data = res.data
    positiveWords.value = data.positive || []
    negativeWords.value = data.negative || []
    drawCurrentCloud()
  } catch (error) {
    console.error('WordCloud fetch error:', error)
  } finally {
    loading.value = false
  }
}

const currentWords = computed(() => activeTab.value === 'positive' ? positiveWords.value : negativeWords.value)
const setMode = (mode: 'ranking' | 'cloud') => {
  visualMode.value = mode
  if (mode === 'cloud') window.setTimeout(drawCurrentCloud, 0)
  else if (chartInstance) { chartInstance.dispose(); chartInstance = null }
}

const drawCurrentCloud = () => {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()
  const words = activeTab.value === 'positive' ? positiveWords.value : negativeWords.value
  if (!words || words.length === 0) {
    chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption({ title: { text: '暂无数据', left: 'center', top: 'center', textStyle: { color: '#94a3b8' } } })
    return
  }
  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    ...chartBase,
    tooltip: {
      ...chartTooltip,
      trigger: 'item',
      formatter: (params: any) => `<strong>${params.name}</strong><br/>出现次数: ${params.value}`,
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      width: '100%',
      height: '100%',
      gridSize: 10,
      sizeRange: [12, 48],
      rotationRange: [-30, 30],
      rotationStep: 15,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'Inter, sans-serif',
        fontWeight: 500,
        color: () => {
          const greens = ['#2E8B78', '#4D9D8A', '#77B7A8', '#9ECDBF', '#C7E3DA']
          const reds = ['#C95C57', '#D47770', '#E39A91', '#EBC0B9', '#F2D9D4']
          const colors = activeTab.value === 'positive' ? greens : reds
          return colors[Math.floor(Math.random() * colors.length)]
        }
      },
      emphasis: {
        textStyle: { fontWeight: 700, shadowBlur: 8 }
      },
      data: words.slice(0, 50)
    }]
  })
}

onMounted(() => { fetchDataAndDraw() })
onUnmounted(() => { if (chartInstance) chartInstance.dispose() })
watch(() => [props.sentimentFilter, props.aspectFilter], () => fetchDataAndDraw())
</script>

<style scoped>
.chart-container { width: 100%; min-height: 340px; position: relative; }
.chart { width: 100%; height: 300px; }
.cloud-tabs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}
.cloud-tabs button {
  padding: 6px 16px;
  border: 1px solid var(--border-default);
  background: transparent;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
  border-radius: 20px;
  transition: all var(--transition-fast);
}
.cloud-tabs button:hover {
  border-color: var(--accent-border);
  color: var(--accent);
}
.cloud-tabs button.active {
  background: var(--accent-subtle);
  border-color: var(--accent-border);
  color: var(--accent);
  font-weight: 600;
}
.cloud-divider { width: 1px; height: 18px; margin: 0 3px; background: var(--line); }
.keyword-ranking { display: flex; flex-direction: column; gap: 9px; padding: 8px 18px 16px; }
.keyword-row { display: grid; grid-template-columns: 28px 76px minmax(80px, 1fr) 36px; align-items: center; gap: 9px; min-height: 22px; color: var(--ink); font-size: 12px; }
.keyword-rank, .keyword-value { color: var(--text-faint); font-family: var(--font-mono); font-size: 10px; }
.keyword-value { text-align: right; color: var(--ink-soft); }
.keyword-bar { display: block; height: 5px; overflow: hidden; border-radius: 4px; background: var(--neutral-soft); }
.keyword-bar i { display: block; height: 100%; border-radius: inherit; background: var(--positive); transition: width 500ms ease; }
.keyword-ranking.positive .keyword-row:nth-child(-n + 3) .keyword-bar i { background: var(--positive); }
.keyword-ranking.negative .keyword-row:nth-child(-n + 3) .keyword-bar i { background: var(--negative); }
.loading { text-align: center; padding: 40px; color: #94a3b8; font-size: 13px; }
</style>
