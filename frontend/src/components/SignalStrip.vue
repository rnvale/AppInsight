<template>
  <section class="signal-strip" aria-labelledby="signal-strip-title">
    <div class="signal-strip-intro">
      <div class="signal-strip-kicker">Signal map / current slice</div>
      <h2 id="signal-strip-title">当前情绪结构</h2>
      <p>把筛选结果压缩成一条可扫描的信号带，快速判断反馈是否集中在单一方向。</p>
    </div>

    <div class="signal-strip-data">
      <div class="signal-strip-header">
        <span>评论分布</span>
        <span class="signal-live"><i></i>实时切片</span>
      </div>
      <div class="signal-track" role="img" :aria-label="`正面 ${positiveRate}%、负面 ${negativeRate}%、其他 ${otherRate}%`">
        <span class="signal-segment signal-positive" :style="{ width: `${positiveRate}%` }"></span>
        <span class="signal-segment signal-negative" :style="{ width: `${negativeRate}%` }"></span>
        <span class="signal-segment signal-other" :style="{ width: `${otherRate}%` }"></span>
      </div>
      <div class="signal-legend">
        <div class="signal-legend-item"><i class="signal-dot positive"></i><strong>{{ positiveRate }}%</strong><span>正面</span></div>
        <div class="signal-legend-item"><i class="signal-dot negative"></i><strong>{{ negativeRate }}%</strong><span>负面</span></div>
        <div class="signal-legend-item"><i class="signal-dot other"></i><strong>{{ otherRate }}%</strong><span>其他</span></div>
        <div class="signal-spark" aria-hidden="true"><span v-for="(height, index) in sparkBars" :key="index" :style="{ height: `${height}%`, animationDelay: `${index * 70}ms` }"></span></div>
      </div>
    </div>

    <aside class="signal-strip-visual">
      <img src="/img/app-analysis.jpg" alt="用户在设备上查看分析数据" loading="lazy">
      <div class="signal-visual-overlay">
        <span>FIELD NOTE / 03</span>
        <strong>从趋势回到真实使用场景</strong>
      </div>
    </aside>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ positive: number; negative: number; total: number }>()

const safeTotal = computed(() => Math.max(props.total, props.positive + props.negative, 1))
const positiveRate = computed(() => Math.min(100, Math.max(0, Number(((props.positive / safeTotal.value) * 100).toFixed(1)))))
const negativeRate = computed(() => Math.min(100 - positiveRate.value, Math.max(0, Number(((props.negative / safeTotal.value) * 100).toFixed(1)))))
const otherRate = computed(() => Number(Math.max(0, 100 - positiveRate.value - negativeRate.value).toFixed(1)))
const sparkBars = computed(() => {
  const base = [32, 48, 38, 64, 50, 72, 58, 78, 44, 66, 55, 86]
  const factor = Math.max(0.72, Math.min(1.1, (positiveRate.value + 20) / 80))
  return base.map((value, index) => Math.min(100, Math.round(value * factor + (index % 3) * 2)))
})
</script>

<style scoped>
.signal-strip { display: grid; grid-template-columns: minmax(200px, 0.72fr) minmax(360px, 1.18fr) minmax(180px, 0.64fr); min-height: 176px; overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius-md); background: var(--panel); box-shadow: var(--shadow-sm); }
.signal-strip-intro { display: flex; flex-direction: column; justify-content: center; padding: 22px 22px 20px; border-right: 1px solid var(--line); }
.signal-strip-kicker { color: var(--accent); font-family: var(--font-mono); font-size: 9px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.signal-strip h2 { margin: 8px 0 6px; color: var(--ink); font-family: var(--font-display); font-size: 19px; line-height: 1.2; }
.signal-strip p { max-width: 265px; margin: 0; color: var(--text-muted); font-size: 11px; line-height: 1.65; }
.signal-strip-data { display: flex; flex-direction: column; justify-content: center; min-width: 0; padding: 22px 26px; }
.signal-strip-header { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 13px; color: var(--ink-soft); font-size: 11px; font-weight: 700; }
.signal-live { display: inline-flex; align-items: center; gap: 6px; color: var(--text-faint); font-family: var(--font-mono); font-size: 9px; font-weight: 500; }
.signal-live i { width: 6px; height: 6px; border-radius: 50%; background: var(--positive); box-shadow: 0 0 0 4px rgba(46,139,120,0.12); animation: signalPulse 1.8s ease-in-out infinite; }
.signal-track { display: flex; width: 100%; height: 28px; overflow: hidden; border-radius: 6px; background: var(--neutral-soft); box-shadow: inset 0 0 0 1px rgba(22,32,31,0.04); }
.signal-segment { position: relative; min-width: 0; transition: width 720ms cubic-bezier(0.2, 0.8, 0.2, 1); }
.signal-segment::after { position: absolute; inset: 0; content: ""; background: linear-gradient(105deg, transparent 18%, rgba(255,255,255,0.22) 48%, transparent 78%); transform: translateX(-120%); animation: segmentSweep 4.8s ease-in-out infinite; }
.signal-positive { background: var(--positive); }.signal-negative { background: var(--negative); }.signal-other { background: #b4c1bd; }
.signal-legend { display: flex; align-items: center; gap: 17px; margin-top: 15px; }
.signal-legend-item { display: inline-flex; align-items: baseline; gap: 5px; white-space: nowrap; }.signal-legend-item strong { color: var(--ink); font-family: var(--font-mono); font-size: 13px; }.signal-legend-item span { color: var(--text-faint); font-size: 10px; }.signal-dot { display: block; width: 7px; height: 7px; border-radius: 50%; }.signal-dot.positive { background: var(--positive); }.signal-dot.negative { background: var(--negative); }.signal-dot.other { background: #9caaa5; }
.signal-spark { display: flex; align-items: end; gap: 3px; height: 26px; margin-left: auto; padding-left: 15px; border-left: 1px solid var(--line); }.signal-spark span { width: 3px; min-height: 4px; border-radius: 3px 3px 0 0; background: var(--accent); opacity: 0.78; transform-origin: bottom; animation: sparkPulse 1.6s ease-in-out infinite alternate; }
.signal-strip-visual { position: relative; min-height: 176px; overflow: hidden; background: var(--ink); }.signal-strip-visual::after { position: absolute; inset: 0; content: ""; background: linear-gradient(135deg, rgba(22,32,31,0.08), rgba(22,32,31,0.78)); }.signal-strip-visual img { width: 100%; height: 100%; object-fit: cover; filter: saturate(0.78) contrast(1.04); transition: transform 600ms ease, filter 600ms ease; }.signal-strip:hover .signal-strip-visual img { filter: saturate(0.98) contrast(1.06); transform: scale(1.04); }.signal-visual-overlay { position: absolute; right: 16px; bottom: 14px; left: 16px; z-index: 1; display: flex; flex-direction: column; gap: 4px; color: #fff; }.signal-visual-overlay span { color: #b9d1c7; font-family: var(--font-mono); font-size: 8px; letter-spacing: 0.08em; }.signal-visual-overlay strong { max-width: 160px; font-size: 12px; line-height: 1.35; }
@keyframes signalPulse { 0%, 100% { opacity: 0.55; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.1); } }
@keyframes segmentSweep { 0%, 55% { transform: translateX(-120%); } 75%, 100% { transform: translateX(120%); } }
@keyframes sparkPulse { from { opacity: 0.42; transform: scaleY(0.72); } to { opacity: 0.95; transform: scaleY(1); } }
@media (max-width: 1160px) { .signal-strip { grid-template-columns: minmax(220px, 0.8fr) minmax(0, 1.2fr); }.signal-strip-visual { display: none; } }
@media (max-width: 900px) { .signal-strip { grid-template-columns: 1fr; }.signal-strip-intro { border-right: 0; border-bottom: 1px solid var(--line); }.signal-strip-data { padding: 20px 22px 22px; } }
@media (max-width: 560px) { .signal-strip-intro { padding: 18px; }.signal-strip-data { padding: 18px; }.signal-legend { flex-wrap: wrap; gap: 10px 15px; }.signal-spark { width: 100%; margin: 2px 0 0; padding: 8px 0 0; border-top: 1px solid var(--line); border-left: 0; }.signal-spark span { flex: 1; width: auto; } }
@media (prefers-reduced-motion: reduce) { .signal-live i, .signal-segment::after, .signal-spark span { animation: none; }.signal-segment, .signal-strip-visual img { transition: none; } }
</style>
