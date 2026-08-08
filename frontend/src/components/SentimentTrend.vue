<template>
  <div ref="chartRef" style="height:320px;width:100%"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import http from '../http'
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'

const props = defineProps<{ sentimentFilter?: string; aspectFilter?: string }>()
const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

async function render() {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  try {
    const r = await http.post('/sentiment_trend', {
      sentiment: props.sentimentFilter === '全部' ? 'all' : props.sentimentFilter,
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter,
    })
    const d = r.data
    if (!d || d.length === 0) return
    chart.setOption({
      ...chartBase,
      legend: { data: ['正面率', '上界', '下界'], bottom: 0, textStyle: { color: SIGNAL_COLORS.muted, fontSize: 11 } },
      grid: { top: 35, left: 48, right: 24, bottom: 40 },
      xAxis: { type: 'category', data: d.map((x: any) => x.label), axisLabel: { fontSize: 11, color: SIGNAL_COLORS.muted } },
      yAxis: { type: 'value', name: '正面率', min: 0, max: 100, axisLabel: { color: SIGNAL_COLORS.faint, fontSize: 10, formatter: '{value}%' }, splitLine: { lineStyle: { color: SIGNAL_COLORS.grid, type: 'dashed' } } },
      series: [
        {
          name: '上界', type: 'line', data: d.map((x: any) => x.rate_high), symbol: 'none', lineStyle: { color: 'rgba(46,139,120,.35)', type: 'dashed', width: 1 },
        },
        {
          name: '下界', type: 'line', data: d.map((x: any) => x.rate_low), symbol: 'none', lineStyle: { color: 'rgba(46,139,120,.35)', type: 'dashed', width: 1 },
        },
        {
          name: '正面率', type: 'line', data: d.map((x: any) => ({ value: x.positive_rate, positive: x.positive, negative: x.negative, total: x.sample_size, low: x.rate_low, high: x.rate_high })), smooth: 0.28,
          lineStyle: { color: SIGNAL_COLORS.positive, width: 3 }, itemStyle: { color: SIGNAL_COLORS.positive }, symbol: 'circle', symbolSize: (value: any, params: any) => Math.min(16, Math.max(7, 5 + Math.log10(d[params.dataIndex]?.sample_size || 1))),
          label: { show: true, position: 'top', color: SIGNAL_COLORS.ink, fontSize: 10, formatter: (p: any) => `${p.value}%` },
          markLine: { silent: true, symbol: 'none', lineStyle: { color: SIGNAL_COLORS.neutralSoft, type: 'dashed' }, label: { formatter: '50% 基线', color: SIGNAL_COLORS.faint, fontSize: 9 }, data: [{ yAxis: 50 }] },
        },
      ],
      tooltip: { ...chartTooltip, trigger: 'axis', formatter: (params: any[]) => { const row = d[params[0]?.dataIndex]; return `<strong>${row.label}</strong><br/>正面率: ${row.positive_rate}%<br/>区间: ${row.rate_low}% 至 ${row.rate_high}%<br/>正面 ${row.positive} 条 · 负面 ${row.negative} 条<br/>样本量 ${row.sample_size}` } },
      animationDuration: 720,
    })
  } catch (e) {
    console.error('SentimentTrend error:', e)
  }
}

onMounted(() => setTimeout(render, 100))
watch(() => [props.sentimentFilter, props.aspectFilter], render)
onUnmounted(() => chart?.dispose())
</script>
