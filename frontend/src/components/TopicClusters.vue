<template><div ref="wrapRef" class="tc-wrap"><div v-if="loading" class="tc-loading">加载中...</div><div v-else class="tc-grid"><div v-for="(cl, name) in clusters" :key="name" class="tc-card"><div class="tc-header"><span class="tc-name">{{ name }}</span><span class="tc-count">{{ cl.total }} 条</span></div><div class="tc-bar"><div class="tc-bar-pos" :style="{width:cl.positive_rate+'%'}"></div></div><div class="tc-rate-row"><span class="tc-pos">+{{cl.positive}}</span><span class="tc-pct">{{cl.positive_rate}}%</span><span class="tc-neg">-{{cl.negative}}</span></div><div class="tc-keywords"><span v-for="kw in cl.top_keywords" :key="kw" class="tc-kw">{{kw}}</span></div></div></div></div></template>
<script setup lang="ts">
import {ref,onMounted,watch} from 'vue'
import http from '../http'
const props=defineProps<{sentimentFilter?:string;aspectFilter?:string}>()
const wrapRef=ref<HTMLElement|null>(null); const loading=ref(true); const clusters=ref<Record<string,any>>({})
async function load(){
  loading.value=true
  try{const r=await http.post('/topic_clusters',{sentiment:props.sentimentFilter==='全部'?'all':props.sentimentFilter,category:props.aspectFilter==='全部'?'all':props.aspectFilter});clusters.value=r.data}catch{}
  loading.value=false
}
onMounted(load);watch(()=>[props.sentimentFilter,props.aspectFilter],load)
</script>
<style scoped>
.tc-wrap{padding:16px}.tc-loading{text-align:center;color:#94a3b8;padding:40px}.tc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}.tc-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px;transition:all.2s}.tc-card:hover{border-color:#cbd5e1;box-shadow:0 4px 12px rgba(0,0,0,0.04)}.tc-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.tc-name{font-size:13px;font-weight:600;color:#0f172a}.tc-count{font-size:11px;color:#94a3b8}.tc-bar{height:4px;background:#e2e8f0;border-radius:2px;overflow:hidden;margin-bottom:6px}.tc-bar-pos{height:100%;background:#22c55e;border-radius:2px}.tc-rate-row{display:flex;gap:12px;font-size:11px;font-weight:600;margin-bottom:8px}.tc-pos{color:#16a34a}.tc-neg{color:#dc2626;margin-left:auto}.tc-pct{color:#64748b}.tc-keywords{display:flex;flex-wrap:wrap;gap:4px}.tc-kw{padding:2px 7px;background:#eef2ff;color:#4f46e5;border-radius:4px;font-size:10px;font-weight:500}
</style>
