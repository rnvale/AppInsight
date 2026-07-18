<template>
  <div ref="chartRef" style="height:280px;width:100%"></div>
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
    const r = await http.post('/app_ratings', {
      sentiment: props.sentimentFilter === '全部' ? 'all' : props.sentimentFilter,
      category: props.aspectFilter === '全部' ? 'all' : props.aspectFilter,
      top_n: 10,
      sort_by: 'avg_rating',
    })
    const data = (r.data || []).slice().sort((a: any, b: any) => a.avg_rating - b.avg_rating)
    if (data.length === 0) return
    chart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { top: 10, left: 120, right: 30, bottom: 20 },
      xAxis: { type: 'value', min: 0, max: 5, axisLabel: { fontSize: 10 } },
      yAxis: {
        type: 'category',
        data: data.map((d: any) => (d.app?.length > 15 ? d.app.slice(0, 15) + '...' : d.app)),
        axisLabel: { fontSize: 10 },
      },
      series: [
        {
          type: 'bar',
          data: data.map((d: any) => d.avg_rating),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#2563eb' },
              { offset: 1, color: '#06b6d4' },
            ]),
            borderRadius: [0, 4, 4, 0],
          },
          label: {
            show: true,
            position: 'right',
            formatter: (p: any) => p.value.toFixed(2),
            fontSize: 11,
            fontWeight: 600,
          },
        },
      ],
      animationDuration: 1200,
    })
  } catch (e) {
    console.error('AppRatingsDetail error:', e)
  }
}

onMounted(() => setTimeout(render, 100))
watch(() => [props.sentimentFilter, props.aspectFilter], render)
onUnmounted(() => chart?.dispose())
</script>
