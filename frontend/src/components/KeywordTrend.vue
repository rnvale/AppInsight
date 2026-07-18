<template><div class="kt-wrap"><div class="kt-input"><input v-model="keyword" placeholder="输入关键词如 update" @keyup.enter="search" class="kt-field"/><button @click="search" class="kt-btn">搜索</button></div><div ref="chartRef" style="height:200px"></div><div v-if="noData" class="kt-empty">输入关键词查看评分趋势</div></div></template>
<script setup lang="ts">
import { ref,onMounted,onUnmounted } from 'vue'
import * as echarts from 'echarts'
import http from '../http'
const props=defineProps<{sentimentFilter?:string;aspectFilter?:string}>()
const keyword=ref(''); const noData=ref(true); const chartRef=ref<HTMLElement|null>(null); let chart:echarts.ECharts|null=null
async function search(){
  if(!keyword.value.trim()||!chartRef.value) return; if(!chart) chart=echarts.init(chartRef.value)
  try{
    const r=await http.post('/keyword_trend',{keyword:keyword.value.trim()}); const data=r.data.trend||[]
    noData.value=data.length===0
    chart.setOption({tooltip:{trigger:'axis'},grid:{top:15,left:45,right:20,bottom:25},xAxis:{type:'category',data:data.map((d:any)=>'⭐'.repeat(d.rating)),axisLabel:{fontSize:11}},yAxis:{type:'value',name:'出现率(%)',axisLabel:{fontSize:10,formatter:'{value}%'}},series:[{type:'line',data:data.map((d:any)=>d.frequency),lineStyle:{color:'#7c3aed',width:2},areaStyle:{color:'rgba(124,58,237,0.1)'},symbol:'diamond',symbolSize:8,markLine:{data:[{type:'average',name:'平均值'}],lineStyle:{color:'#94a3b8',type:'dashed'}}}],animationDuration:1000})
  }catch{noData.value=true}
}
</script>
<style scoped>
.kt-wrap{padding:12px}.kt-input{display:flex;gap:8px;margin-bottom:12px}.kt-field{flex:1;padding:8px 12px;border:1px solid #e2e8f0;border-radius:8px;font-size:13px;font-family:inherit;outline:none}.kt-field:focus{border-color:#7c3aed;box-shadow:0 0 0 3px rgba(124,58,237,0.1)}.kt-btn{padding:8px 16px;background:#7c3aed;color:#fff;border:none;border-radius:8px;font-size:13px;cursor:pointer;font-family:inherit}.kt-btn:hover{background:#6d28d9}.kt-empty{text-align:center;color:#94a3b8;padding:40px 0;font-size:13px}
</style>
