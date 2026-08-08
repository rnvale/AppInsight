<template><div class="kt-wrap"><div class="kt-input"><input v-model="keyword" placeholder="输入关键词如 update" @keyup.enter="search" class="kt-field"/><button @click="search" class="kt-btn">搜索</button></div><div ref="chartRef" style="height:200px"></div><div v-if="noData" class="kt-empty">输入关键词查看评分趋势</div></div></template>
<script setup lang="ts">
import { ref,onMounted,onUnmounted } from 'vue'
import * as echarts from 'echarts'
import http from '../http'
import { chartBase, chartTooltip, SIGNAL_COLORS } from '../utils/chartTheme'
const props=defineProps<{sentimentFilter?:string;aspectFilter?:string}>()
const keyword=ref(''); const noData=ref(true); const chartRef=ref<HTMLElement|null>(null); let chart:echarts.ECharts|null=null
async function search(){
  if(!keyword.value.trim()||!chartRef.value) return; if(!chart) chart=echarts.init(chartRef.value)
  try{
    const r=await http.post('/keyword_trend',{keyword:keyword.value.trim()}); const data=r.data.trend||[]
    noData.value=data.length===0
    chart.setOption({...chartBase,tooltip:{...chartTooltip,trigger:'axis'},grid:{top:15,left:45,right:20,bottom:25},xAxis:{type:'category',data:data.map((d:any)=>'⭐'.repeat(d.rating)),axisLabel:{fontSize:11,color:SIGNAL_COLORS.muted}},yAxis:{type:'value',name:'出现率(%)',axisLabel:{fontSize:10,color:SIGNAL_COLORS.faint,formatter:'{value}%'},splitLine:{lineStyle:{color:SIGNAL_COLORS.grid}}},series:[{type:'line',data:data.map((d:any)=>d.frequency),lineStyle:{color:SIGNAL_COLORS.accent,width:2},areaStyle:{color:'rgba(229,107,85,0.12)'},symbol:'diamond',symbolSize:8,markLine:{data:[{type:'average',name:'平均值'}],lineStyle:{color:SIGNAL_COLORS.faint,type:'dashed'}}}],animationDuration:720})
  }catch{noData.value=true}
}
</script>
<style scoped>
.kt-wrap{padding:12px}.kt-input{display:flex;gap:8px;margin-bottom:12px}.kt-field{flex:1;padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:13px;font-family:inherit;outline:none}.kt-field:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--focus)}.kt-btn{padding:8px 16px;background:var(--ink);color:#fff;border:none;border-radius:8px;font-size:13px;cursor:pointer;font-family:inherit}.kt-btn:hover{background:var(--accent-hover)}.kt-empty{text-align:center;color:var(--text-faint);padding:40px 0;font-size:13px}
</style>
