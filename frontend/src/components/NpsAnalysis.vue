<template><div ref="wrapRef" class="nps-wrap"><div v-if="loading" class="nps-loading">加载中...</div><template v-else><div class="nps-score-row"><div class="nps-big">{{ npsData.nps_score }}</div><div class="nps-lbl">NPS 净推荐值</div></div><div class="nps-bar"><div class="nps-bar-seg nps-detractors" :style="{flex:npsData.detractors}" :title="'贬损者: '+npsData.detractors"><span v-if="npsData.detractors>0">贬损 {{npsData.detractors}}</span></div><div class="nps-bar-seg nps-passives" :style="{flex:npsData.passives}" :title="'被动者: '+npsData.passives"><span v-if="npsData.passives>0">被动 {{npsData.passives}}</span></div><div class="nps-bar-seg nps-promoters" :style="{flex:npsData.promoters}" :title="'推荐者: '+npsData.promoters"><span v-if="npsData.promoters>0">推荐 {{npsData.promoters}}</span></div></div></template></div></template>
<script setup lang="ts">
import {ref,reactive,onMounted,watch} from 'vue'
import http from '../http'
const props=defineProps<{sentimentFilter?:string;aspectFilter?:string}>()
const wrapRef=ref<HTMLElement|null>(null); const loading=ref(true)
const npsData=reactive({nps_score:0,promoters:0,passives:0,detractors:0})
async function load(){
  loading.value=true
  try{const r=await http.post('/nps',{sentiment:props.sentimentFilter==='全部'?'all':props.sentimentFilter,category:props.aspectFilter==='全部'?'all':props.aspectFilter});Object.assign(npsData,r.data)}catch{}
  loading.value=false
}
onMounted(load);watch(()=>[props.sentimentFilter,props.aspectFilter],load)
</script>
<style scoped>
.nps-wrap{padding:20px;text-align:center}.nps-loading{text-align:center;color:#94a3b8;padding:40px}.nps-score-row{margin-bottom:20px}.nps-big{font-size:48px;font-weight:800;line-height:1;background:linear-gradient(135deg,#2563eb,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.nps-lbl{font-size:12px;color:#64748b;margin-top:4px}.nps-bar{display:flex;height:32px;border-radius:8px;overflow:hidden}.nps-bar-seg{display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#fff}.nps-detractors{background:#ef4444}.nps-passives{background:#f59e0b}.nps-promoters{background:#22c55e}
</style>
