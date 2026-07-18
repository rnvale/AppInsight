<template>
  <div ref="chartRef" style="height:320px;width:100%"></div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import http from '../http'

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
      tooltip: { trigger: 'axis' },
      legend: { data: ['正面', '负面', '正面率'], bottom: 0, textStyle: { fontSize: 11 } },
      grid: { top: 35, left: 55, right: 55, bottom: 40 },
      xAxis: { type: 'category', data: d.map((x: any) => x.label), axisLabel: { fontSize: 11 } },
      yAxis: [
        { type: 'value', name: '数量', axisLabel: { fontSize: 10 } },
        { type: 'value', name: '%', max: 100, axisLabel: { fontSize: 10 } },
      ],
      series: [
        {
          name: '正面',
          type: 'bar',
          data: d.map((x: any) => x.positive),
          itemStyle: { color: '#16a34a', borderRadius: [3, 3, 0, 0] },
        },
        {
          name: '负面',
          type: 'bar',
          data: d.map((x: any) => x.negative),
          itemStyle: { color: '#dc2626', borderRadius: [3, 3, 0, 0] },
        },
        {
          name: '正面率',
          type: 'line',
          yAxisIndex: 1,
          data: d.map((x: any) => x.positive_rate),
          lineStyle: { color: '#2563eb', width: 2 },
          symbol: 'circle',
          symbolSize: 6,
        },
      ],
      animationDuration: 1200,
    })
  } catch (e) {
    console.error('SentimentTrend error:', e)
  }
}

onMounted(() => setTimeout(render, 100))
watch(() => [props.sentimentFilter, props.aspectFilter], render)
onUnmounted(() => chart?.dispose())
</script>
