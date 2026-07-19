<template>
  <section class="band-capabilities">
    <div class="capability-shell">
      <div class="capability-overview">
        <div class="section-kicker"><i></i>分析工作台 / 交互预览</div>
        <h2>把复杂反馈<br><span>拆成可行动信号</span></h2>
        <p>从全局健康度到单条评论，六个模块连接成一条清晰的分析路径。</p>
        <div class="capability-stats">
          <div><strong>06</strong><span>分析模块</span></div>
          <div><strong>12</strong><span>可视化图表</span></div>
          <div><strong>04</strong><span>数据来源</span></div>
        </div>
        <div class="capability-active"><span>当前模块</span><strong>{{ activeFeature.label }}</strong><small>{{ activeFeature.short }}</small></div>
      </div>

      <div class="capability-workspace">
        <div class="workspace-head"><span>ANALYSIS WORKSPACE</span><span><i></i>LIVE MODULES / 06</span></div>
        <div class="feature-grid">
          <button v-for="(feature, index) in features" :key="feature.key" class="feature-tile" :class="{ active: activeFeatureKey === feature.key }" type="button" :aria-pressed="activeFeatureKey === feature.key" @mouseenter="activeFeatureKey = feature.key" @focus="activeFeatureKey = feature.key" @click="activeFeatureKey = feature.key">
            <span class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path :d="feature.icon"/></svg></span>
            <span class="feature-copy"><strong>{{ feature.label }}</strong><small>{{ feature.short }}</small></span>
            <span class="feature-index">0{{ index + 1 }}</span>
          </button>
        </div>
        <Transition name="feature-swap" mode="out-in">
          <div :key="activeFeature.key" class="feature-preview" :style="{ '--feature-accent': activeFeature.accent }">
            <div class="preview-copy"><span class="preview-kicker">{{ activeFeature.code }}</span><h3>{{ activeFeature.label }}</h3><p>{{ activeFeature.description }}</p><button class="preview-link" type="button" @click="$emit('enter')">进入分析 <b aria-hidden="true">→</b></button></div>
            <div class="preview-visual" aria-hidden="true">
              <div class="preview-grid-lines"></div>
              <div class="preview-bars"><span v-for="(bar, index) in activeFeature.bars" :key="index" :style="{ height: `${bar}%`, animationDelay: `${index * 80}ms` }"></span></div>
              <svg class="preview-line" viewBox="0 0 240 100" preserveAspectRatio="none"><polyline :points="activeFeature.points" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span class="preview-orbit"></span><span class="preview-orbit orbit-two"></span>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

defineEmits<{ (event: 'enter'): void }>()

const features = [
  { key: 'dashboard', label: '总览仪表盘', short: '全局健康度', code: '01 / OVERVIEW', description: '一屏查看正面率、评分、NPS 与领域变化，先确定全局信号，再进入细节。', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 011 1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6', accent: '#5dd5ff', bars: [38, 52, 46, 65, 56, 78, 68, 88], points: '0,74 28,62 56,66 84,42 112,48 140,28 168,36 198,18 240,24' },
  { key: 'sentiment', label: '情感深度分析', short: '趋势与关联', code: '02 / SENTIMENT', description: '从评分、词频和情感趋势交叉观察反馈，找到正在升高或反复出现的信号。', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z', accent: '#75a7ff', bars: [70, 52, 64, 48, 58, 34, 48, 28], points: '0,28 28,40 56,31 84,54 112,44 140,64 168,51 198,76 240,68' },
  { key: 'topics', label: '主题与方面', short: '关注点聚类', code: '03 / TOPICS', description: '把评论拆成用户真正讨论的方面，结合主题聚类判断关注度与情感方向。', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10', accent: '#70d5ff', bars: [42, 76, 55, 88, 60, 48, 73, 62], points: '0,68 28,54 56,61 84,24 112,45 140,35 168,58 198,40 240,50' },
  { key: 'rankings', label: 'App 排行与 NPS', short: '竞争位置', code: '04 / RANKINGS', description: '将评分、评论量与推荐值放进同一个比较框架，快速识别领先者和风险位。', icon: 'M9 5l7 7-7 7', accent: '#8aa9ff', bars: [28, 44, 66, 54, 78, 68, 92, 74], points: '0,78 28,70 56,56 84,62 112,38 140,45 168,22 198,34 240,14' },
  { key: 'compare', label: '多数据集对比', short: '跨源观察', code: '05 / COMPARE', description: '在综合、游戏、生产力和社交数据集之间切换，观察不同场景的差异。', icon: 'M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M7 12l3 3 7-7', accent: '#60b9ed', bars: [58, 42, 72, 50, 66, 58, 82, 64], points: '0,48 28,64 56,36 84,52 112,28 140,44 168,30 198,52 240,32' },
  { key: 'explorer', label: '数据浏览与钻取', short: '追踪原文', code: '06 / EXPLORER', description: '从统计结果回到原始评论，搜索关键词、排序和分页，验证每一条结论。', icon: 'M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7m-6 5H7m10 0h0M7 12l3-3m-3 3l3 3', accent: '#6ab5ff', bars: [30, 38, 50, 45, 60, 72, 54, 86], points: '0,70 28,60 56,65 84,48 112,62 140,34 168,44 198,18 240,28' },
]

const activeFeatureKey = ref('dashboard')
const activeFeature = computed(() => features.find((feature) => feature.key === activeFeatureKey.value) ?? features[0])
</script>

<style scoped>
.band-capabilities { position: relative; overflow: hidden; background: #eef4fa; color: #10203b; }
.band-capabilities::before { position: absolute; top: 0; right: 0; width: 46%; height: 100%; content: ""; background: linear-gradient(135deg, transparent, rgba(81, 145, 219, 0.08)); pointer-events: none; }
.capability-shell { position: relative; z-index: 1; display: grid; max-width: 1240px; grid-template-columns: minmax(240px, 0.68fr) minmax(0, 1.32fr); gap: clamp(28px, 5vw, 72px); margin: 0 auto; padding: 86px 32px; }
.capability-overview { display: flex; flex-direction: column; justify-content: center; min-width: 0; }
.section-kicker { display: inline-flex; align-items: center; gap: 9px; color: #3975b6; font-family: 'Google Sans Code', monospace; font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; }.section-kicker i { width: 22px; height: 2px; background: #3975b6; }
.capability-overview h2 { margin: 16px 0 12px; color: #10203b; font-size: clamp(26px, 3vw, 40px); font-weight: 700; letter-spacing: 0; line-height: 1.14; }.capability-overview h2 span { color: #3975b6; }
.capability-overview > p { max-width: 300px; margin: 0; color: #657b98; font-size: 13px; line-height: 1.8; }
.capability-stats { display: flex; gap: 0; margin-top: 30px; padding: 15px 0; border-top: 1px solid rgba(48, 88, 132, 0.16); border-bottom: 1px solid rgba(48, 88, 132, 0.16); }.capability-stats div { display: flex; min-width: 76px; flex-direction: column; gap: 4px; padding-right: 14px; margin-right: 14px; border-right: 1px solid rgba(48, 88, 132, 0.14); }.capability-stats div:last-child { padding-right: 0; margin-right: 0; border-right: 0; }.capability-stats strong { color: #204d87; font-family: 'Google Sans Code', monospace; font-size: 22px; font-weight: 600; }.capability-stats span { color: #7890aa; font-size: 10px; white-space: nowrap; }
.capability-active { display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; margin-top: 24px; padding-left: 12px; border-left: 2px solid #5dd5ff; }.capability-active span { grid-column: 1 / -1; color: #87a0ba; font-family: 'Google Sans Code', monospace; font-size: 9px; text-transform: uppercase; }.capability-active strong { color: #10203b; font-size: 14px; }.capability-active small { align-self: end; color: #6d86a1; font-size: 10px; }
.capability-workspace { min-width: 0; padding: 20px; border: 1px solid rgba(95, 143, 196, 0.26); border-radius: 16px; background: #07162f; box-shadow: 0 24px 70px rgba(39, 78, 125, 0.18); }.workspace-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 15px; color: #7d9ac0; font-family: 'Google Sans Code', monospace; font-size: 9px; letter-spacing: 0.08em; }.workspace-head span:last-child { display: inline-flex; align-items: center; gap: 7px; color: #75d5c0; }.workspace-head i { width: 5px; height: 5px; border-radius: 50%; background: #75d5c0; box-shadow: 0 0 0 4px rgba(117, 213, 192, 0.1); }
.feature-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }.feature-tile { position: relative; display: flex; min-height: 92px; flex-direction: column; align-items: flex-start; justify-content: space-between; padding: 12px; overflow: hidden; border: 1px solid rgba(137, 174, 218, 0.14); border-radius: 9px; background: rgba(24, 51, 89, 0.54); color: #e8f3ff; cursor: pointer; text-align: left; transition: border-color 220ms ease, background 220ms ease, transform 220ms ease; }.feature-tile::after { position: absolute; right: -18px; bottom: -18px; width: 68px; height: 68px; content: ""; border: 1px solid rgba(93, 213, 255, 0.14); border-radius: 50%; transition: transform 300ms ease, border-color 300ms ease; }.feature-tile:hover, .feature-tile.active { border-color: rgba(93, 213, 255, 0.62); background: linear-gradient(145deg, rgba(35, 83, 139, 0.86), rgba(18, 43, 81, 0.78)); transform: translateY(-2px); }.feature-tile:hover::after, .feature-tile.active::after { border-color: rgba(93, 213, 255, 0.45); transform: scale(1.45); }.feature-icon { display: grid; width: 27px; height: 27px; place-items: center; border: 1px solid rgba(129, 198, 255, 0.24); border-radius: 6px; background: rgba(105, 167, 226, 0.12); color: #81dfff; }.feature-icon svg { width: 16px; height: 16px; }.feature-copy { display: flex; flex-direction: column; gap: 3px; }.feature-copy strong { font-size: 12px; font-weight: 600; }.feature-copy small { color: #8eadd0; font-size: 9px; }.feature-index { position: absolute; top: 12px; right: 12px; color: #6687ae; font-family: 'Google Sans Code', monospace; font-size: 9px; }
.feature-preview { display: grid; min-height: 188px; grid-template-columns: minmax(0, 0.86fr) minmax(230px, 1.14fr); gap: 24px; margin-top: 12px; padding: 18px; overflow: hidden; border: 1px solid rgba(137, 174, 218, 0.16); border-radius: 10px; background: linear-gradient(110deg, rgba(8, 27, 57, 0.9), rgba(13, 42, 82, 0.62)); }.preview-copy { display: flex; min-width: 0; flex-direction: column; align-items: flex-start; justify-content: center; }.preview-kicker { color: var(--feature-accent); font-family: 'Google Sans Code', monospace; font-size: 9px; letter-spacing: 0.08em; }.preview-copy h3 { margin: 8px 0 5px; color: #f1f7ff; font-size: 18px; }.preview-copy p { max-width: 270px; margin: 0; color: #9db7d3; font-size: 11px; line-height: 1.65; }.preview-link { display: inline-flex; align-items: center; gap: 7px; margin-top: 13px; padding: 0; border: 0; background: transparent; color: var(--feature-accent); cursor: pointer; font-size: 10px; font-weight: 700; }.preview-link b { font-size: 13px; font-weight: 500; transition: transform 220ms ease; }.preview-link:hover b { transform: translateX(4px); }
.preview-visual { position: relative; min-height: 150px; overflow: hidden; border: 1px solid rgba(102, 175, 235, 0.15); border-radius: 8px; background: #081a36; }.preview-grid-lines { position: absolute; inset: 0; opacity: 0.36; background-image: linear-gradient(rgba(109, 180, 237, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(109, 180, 237, 0.1) 1px, transparent 1px); background-size: 30px 25px; }.preview-bars { position: absolute; right: 16px; bottom: 19px; left: 16px; display: flex; height: 94px; align-items: end; gap: 7px; }.preview-bars span { flex: 1; min-width: 5px; border-radius: 3px 3px 0 0; background: linear-gradient(180deg, var(--feature-accent), rgba(93, 213, 255, 0.08)); opacity: 0.7; transform-origin: bottom; animation: previewBarRise 780ms cubic-bezier(0.2, 0.8, 0.2, 1) both; }.preview-line { position: absolute; right: 16px; bottom: 26px; left: 16px; width: calc(100% - 32px); height: 87px; overflow: visible; color: var(--feature-accent); filter: drop-shadow(0 0 5px var(--feature-accent)); }.preview-orbit { position: absolute; top: 21px; right: 33px; width: 46px; height: 18px; border: 1px solid var(--feature-accent); border-radius: 50%; opacity: 0.55; transform: rotate(-22deg); animation: previewOrbit 4.5s linear infinite; }.orbit-two { top: 34px; right: 14px; width: 29px; height: 12px; opacity: 0.3; animation-direction: reverse; }
.feature-swap-enter-active, .feature-swap-leave-active { transition: opacity 180ms ease, transform 180ms ease; }.feature-swap-enter-from, .feature-swap-leave-to { opacity: 0; transform: translateY(7px); }
@keyframes previewBarRise { from { opacity: 0; transform: scaleY(0.1); } to { opacity: 0.7; transform: scaleY(1); } }
@keyframes previewOrbit { to { transform: rotate(338deg); } }
@media (max-width: 900px) { .capability-shell { grid-template-columns: 1fr; padding: 64px 24px; }.capability-overview { max-width: 600px; }.capability-overview > p { max-width: 500px; }.capability-stats { max-width: 380px; }.capability-workspace { padding: 15px; } }
@media (max-width: 580px) { .capability-shell { padding: 54px 16px; }.capability-overview h2 { font-size: 30px; }.feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }.feature-tile { min-height: 88px; }.feature-preview { grid-template-columns: 1fr; gap: 14px; }.preview-visual { min-height: 138px; }.workspace-head { align-items: flex-start; flex-direction: column; gap: 5px; } }
@media (prefers-reduced-motion: reduce) { .feature-tile, .feature-tile::after, .preview-bars span, .preview-orbit, .preview-link b { transition: none; animation: none; }.feature-swap-enter-active, .feature-swap-leave-active { transition: none; } }
</style>
