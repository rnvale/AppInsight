<template><div ref="wrapRef" class="cd-wrap"><div class="cd-controls"><label v-for="ds in datasets" :key="ds.key" class="cd-check"><input type="checkbox" :value="ds.key" v-model="selected"/><span>{{ds.label}}</span></label><button @click="loadCompare" class="cd-btn">对比</button></div><div v-if="loading" class="cd-loading">加载中...</div><div v-else-if="Object.keys(compareData).length>0"><div class="cd-grid"><div v-for="(data,key) in compareData" :key="key" class="cd-card"><div class="cd-ds-name">{{datasets.find(d=>d.key===key)?.label||key}}</div><div class="cd-stat"><span class="cd-stat-val">{{data.total}}</span><span class="cd-stat-lbl">评论数</span></div><div class="cd-stat"><span class="cd-stat-val cd-pos">{{data.positive_rate}}%</span><span class="cd-stat-lbl">正面率</span></div><div class="cd-stat"><span class="cd-stat-val">{{data.avg_rating}}</span><span class="cd-stat-lbl">平均评分</span></div><div class="cd-stat"><span class="cd-stat-val">{{data.categories}}</span><span class="cd-stat-lbl">类别</span></div><div class="cd-stat"><span class="cd-stat-val">{{data.apps}}</span><span class="cd-stat-lbl">App数</span></div></div></div></div></div></template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
import http from '../http'
const props=defineProps<{sentimentFilter?:string;aspectFilter?:string}>()
const wrapRef=ref<HTMLElement|null>(null); const loading=ref(false); const selected=ref(['comprehensive','games','productivity']); const compareData=ref<Record<string,any>>({})
const datasets=[{key:'comprehensive',label:'综合'},{key:'games',label:'游戏'},{key:'productivity',label:'生产力'},{key:'social',label:'社交'}]
async function loadCompare(){
  if(selected.value.length<2)return; loading.value=true
  try{const r=await http.post('/compare_datasets',{sources:selected.value});compareData.value=r.data}catch{}
  loading.value=false
}
onMounted(loadCompare)
</script>
<style scoped>
.cd-wrap{padding:16px}.cd-controls{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:16px}.cd-check{display:flex;align-items:center;gap:6px;font-size:13px;color:#475569;cursor:pointer}.cd-check input{accent-color:#2563eb}.cd-btn{padding:6px 16px;background:#2563eb;color:#fff;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-family:inherit;margin-left:auto}.cd-btn:hover{background:#1d4ed8}.cd-loading{text-align:center;color:#94a3b8;padding:40px}.cd-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.cd-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px;text-align:center}.cd-ds-name{font-size:14px;font-weight:700;color:#0f172a;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #e2e8f0}.cd-stat{display:flex;justify-content:space-between;padding:3px 0;font-size:12px}.cd-stat-val{font-weight:700;color:#0f172a}.cd-stat-lbl{color:#94a3b8}.cd-pos{color:#16a34a}
</style>
