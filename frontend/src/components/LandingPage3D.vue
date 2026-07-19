<template>
  <div class="landing-magazine">
    <nav class="top-nav">
      <div class="nav-inner">
        <div class="logo-wrap">
          <div class="logo-mark" aria-hidden="true">
            <svg viewBox="0 0 32 24" fill="none"><path d="M3 19V9M10 19V6M17 19V3M24 19v-7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M2 21h27" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity=".55"/></svg>
          </div>
          <span class="logo-text">AppInsight</span>
          <span class="logo-ver">v4.0</span>
        </div>
        <ul class="nav-links">
          <li><button @click="$emit('enter')" class="nav-cta">进入项目 →</button></li>
        </ul>
      </div>
    </nav>

    <section ref="heroRoot" class="band-hero">
      <div class="starfield">
        <div class="sf-bg"></div>
        <div class="sf-grad"></div>
        <div v-for="i in 100" :key="'s1-'+i" class="star tiny" :style="tinyStar(i)"></div>
        <div v-for="i in 40" :key="'s2-'+i" class="star medium" :style="medStar(i)"></div>
        <div v-for="i in 10" :key="'s3-'+i" class="star bright" :style="brightStar(i)"></div>
        <div class="nebula n1"></div>
        <div class="nebula n2"></div>
        <div class="ground-glow"></div>
      </div>

      <div class="hero-spotlight" aria-hidden="true"></div>
      <div class="hero-beams" aria-hidden="true"><span class="hero-beam beam-a"></span><span class="hero-beam beam-b"></span><span class="hero-beam beam-c"></span></div>
      <div ref="threeContainer" class="hero-three-bg"></div>
      <div v-if="sceneFailed" class="scene-fallback" aria-hidden="true"><span>Signal Lab</span><small>可视化工作台</small></div>

      <div class="hero-grid">
        <div class="hero-left">
          <div class="hero-badge"><i></i><span>通用文本评论情感分析架构</span></div>
          <h1 class="hero-title"><span class="hero-title-main">App</span><span class="hero-title-accent">Insight</span></h1>
          <h2 class="hero-subtitle">洞察每一句评论</h2>
          <p class="hero-desc">从评论文本到可视化图表，<br>一套可复用的多维评论数据情感分析框架，让数据讲述完整故事。</p>
          <div class="hero-buttons">
            <button @click="$emit('enter')" class="btn btn-primary"><span>探索分析平台</span><b aria-hidden="true">→</b></button>
            <a href="https://github.com/rnvale/myweb1" class="btn btn-secondary" target="_blank"><span>查看源代码</span><b aria-hidden="true">▸</b></a>
          </div>
          <div class="hero-author-row">
            <span class="auth-label">作者</span>
            <a href="https://github.com/rnvale" target="_blank" class="auth-name">Rain Vale</a>
          </div>
        </div>
        <div class="hero-right">
          <div class="hero-readout">
            <div class="readout-head"><span class="readout-kicker">LIVE READOUT</span><span class="readout-status"><i></i>在线</span></div>
            <div class="readout-value">10,601</div>
            <div class="readout-label">评论信号已接入</div>
            <div class="readout-bars"><span style="height: 35%"></span><span style="height: 54%"></span><span style="height: 42%"></span><span style="height: 78%"></span><span style="height: 61%"></span><span style="height: 88%"></span><span style="height: 70%"></span><span style="height: 96%"></span></div>
            <div class="readout-foot"><span>positive</span><strong>50.1%</strong></div>
          </div>
        </div>
      </div>

      <div class="metrics-track">
        <div class="metrics-bar">
          <div class="m-item">
            <span class="m-num" data-count="12">0</span>
            <span class="m-lbl">可视化图表</span>
          </div>
          <div class="m-div"></div>
          <div class="m-item">
            <span class="m-num" data-count="10601">0</span>
            <span class="m-lbl">分析评论数</span>
          </div>
          <div class="m-div"></div>
          <div class="m-item">
            <span class="m-num" data-count="6">0</span>
            <span class="m-lbl">分析页面</span>
          </div>
          <div class="m-div"></div>
          <div class="m-item">
            <span class="m-num" data-count="7">0</span>
            <span class="m-lbl">分析维度</span>
          </div>
          <div class="m-div"></div>
          <div class="m-item">
            <span class="m-num">50.1<small>%</small></span>
            <span class="m-lbl">正面率</span>
          </div>
        </div>
      </div>
    </section>

    <CapabilityWorkbench @enter="$emit('enter')" />

    <section v-if="false" class="band-features">
      <div class="fi">
        <div class="fl">
          <div class="fl-badge"><i></i>核心能力</div>
          <h2 class="fl-title">多维分析能力</h2>
          <p class="fl-desc">从宏观概览到微观洞察，七个分析维度全面覆盖评论数据的情感趋势、方面分布、排行竞争、主题聚类、跨源对比与数据钻取。</p>
          <div class="mini-s-wrap"><div class="mini-s"></div></div>
        </div>
        <div class="fr">
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg></div>
            <h3>总览仪表盘</h3>
            <p>情感仪表盘 · 评分分析 · 领域对比 · 热门 App 河流图，一眼掌握全局态势。</p>
            <div class="fc-tags"><span>仪表盘</span><span>·</span><span>评分</span><span>·</span><span>领域</span></div>
          </div>
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg></div>
            <h3>情感深度分析</h3>
            <p>情感趋势 · 热力图 · 3D 气泡 · 评论长度 · 词云，挖掘评分与情感的深层关联。</p>
            <div class="fc-tags"><span>趋势</span><span>·</span><span>热力图</span><span>·</span><span>气泡</span></div>
          </div>
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg></div>
            <h3>方面挖掘与主题聚类</h3>
            <p>玫瑰图 · 热门 App 对比 · 主题聚类，揭示用户最关注的维度与情感倾向。</p>
            <div class="fc-tags"><span>玫瑰图</span><span>·</span><span>对比</span><span>·</span><span>聚类</span></div>
          </div>
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5l7 7-7 7"/></svg></div>
            <h3>App 排行与 NPS</h3>
            <p>评分排行榜 · 四象限 · NPS 净推荐值，用多维度指标定位产品竞争力。</p>
            <div class="fc-tags"><span>排行</span><span>·</span><span>象限</span><span>·</span><span>NPS</span></div>
          </div>
        </div>
      </div>
    </section>

    <section v-if="false" class="band-features2">
      <div class="fi">
        <div class="fl">
          <div class="fl-badge"><i></i>新增能力</div>
          <h2 class="fl-title">扩展分析架构</h2>
          <p class="fl-desc">可复用架构支持多数据集加载，对比分析与原始数据浏览钻取。</p>
          <div class="mini-s-wrap"><div class="mini-s s2"></div></div>
        </div>
        <div class="fr">
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M7 12l3 3 7-7"/></svg></div>
            <h3>多数据集对比</h3>
            <p>综合 · 游戏 · 生产力 · 社交，四类数据集多维度交叉对比。</p>
            <div class="fc-tags"><span>对比</span><span>·</span><span>交叉</span><span>·</span><span>多源</span></div>
          </div>
          <div class="fc">
            <div class="fc-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7m-6 5H7m10 0h0M7 12l3-3m-3 3l3 3"/></svg></div>
            <h3>数据浏览与钻取</h3>
            <p>浏览原始评论 · 关键词搜索 · 分页钻取 · 排序筛选，从宏观到微观。</p>
            <div class="fc-tags"><span>搜索</span><span>·</span><span>分页</span><span>·</span><span>钻取</span></div>
          </div>
        </div>
      </div>
    </section>

    <footer class="band-footer">
      <div class="footer-i">
        <div class="footer-c">
          <span class="footer-l">作者</span>
          <a href="https://github.com/rnvale" target="_blank" class="footer-a">Rain Vale</a>
          <a href="https://github.com/rnvale/myweb1" target="_blank" class="footer-a footer-a-sm">GitHub</a>
        </div>
        <div class="footer-c footer-c-c">
          <span class="footer-l">数据集</span>
          <span class="footer-t">AWARE 数据集</span>
          <a href="https://haolin-zone.xyz" target="_blank" class="footer-a">haolin-zone.xyz</a>
        </div>
        <div class="footer-c footer-c-r">
          <span class="footer-l">版本</span>
          <span class="footer-t">AppInsight v4.0</span>
          <span class="footer-t footer-t-sm">情感分析可视化系统</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import CapabilityWorkbench from './CapabilityWorkbench.vue'

const emit = defineEmits<{ (e: 'enter'): void }>()
const threeContainer = ref<HTMLDivElement | null>(null)
const heroRoot = ref<HTMLElement | null>(null)
const sceneFailed = ref(false)

function seeded(seed: number) {
  let s = seed; return () => { s = (s * 9301 + 49297) % 233280; return s / 233280 }
}
function tinyStar(i: number) {
  const r = seeded(i * 37); let x = r() * 100, y = r() * 100
  if (r() < 0.4) { x = 60 + r() * 40; y = r() * 40 } else if (r() < 0.7) { x = r() * 40; y = 50 + r() * 40 }
  if (Math.hypot(x - 80, y - 50) < 20) { x = (x + 80) / 2; y = (y + 50) / 2 }
  return { left: `${x}%`, top: `${y}%`, width: '1px', height: '1px', backgroundColor: '#fff', opacity: 0.2 + r() * 0.3 }
}
function medStar(i: number) {
  const r = seeded(i * 73 + 11); let x = r() * 100, y = r() * 100
  if (r() < 0.35) { x = 55 + r() * 45; y = r() * 35 } else if (r() < 0.65) { x = r() * 35; y = 45 + r() * 45 }
  if (Math.hypot(x - 80, y - 50) < 20) { x = (x + 80) / 2; y = (y + 50) / 2 }
  return { left: `${x}%`, top: `${y}%`, width: '2px', height: '2px', backgroundColor: '#bfdbfe', opacity: 0.4 + r() * 0.3 }
}
function brightStar(i: number) {
  const r = seeded(i * 131 + 23)
  const spots = [[68,12],[82,28],[92,18],[25,68],[15,82],[55,88],[88,72],[42,15],[12,38],[72,92]]
  const x = spots[i % 10][0] + (r() - 0.5) * 6, y = spots[i % 10][1] + (r() - 0.5) * 6
  return { left: `${x}%`, top: `${y}%`, width: '3px', height: '3px', backgroundColor: r() < 0.6 ? '#fff' : '#bfdbfe', opacity: 0.7 + r() * 0.3, boxShadow: `0 0 6px 2px ${r() < 0.5 ? 'rgba(147,197,253,0.4)' : 'rgba(255,255,255,0.3)'}` }
}

function animateCounters() {
  document.querySelectorAll('.landing-magazine .m-num[data-count]').forEach(c => {
    const t = parseInt(c.getAttribute('data-count') || '0', 10)
    const step = Math.max(1, Math.ceil(t / 60)); let cur = 0
    const timer = setInterval(() => { cur += step; if (cur >= t) { cur = t; clearInterval(timer) }; c.textContent = cur.toLocaleString() }, 20)
  })
}

let cleanup: (() => void) | null = null

onMounted(() => {
  animateCounters()
  const script = document.createElement('script')
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'
  script.onload = () => initScene()
  script.onerror = () => { sceneFailed.value = true }
  document.head.appendChild(script)

  function initScene() {
    const THREE = (window as any).THREE
    if (!THREE || !threeContainer.value) { sceneFailed.value = true; return }

    const container = threeContainer.value
    let W = container.clientWidth, H = container.clientHeight
    if (W < 1) { W = window.innerWidth; H = window.innerHeight }

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(28, W / H, 0.1, 100)
    camera.position.set(7.5, 0.3, 11.5)
    camera.lookAt(3.0, 0, -1.8)

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(W, H)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)
    sceneFailed.value = false

    scene.add(new THREE.AmbientLight(0x475569, 0.7))
    const key = new THREE.DirectionalLight(0xc7d2fe, 0.6)
    key.position.set(4, 6, 5); scene.add(key)
    const back = new THREE.DirectionalLight(0x93c5fd, 0.15)
    back.position.set(-3, -1, -5); scene.add(back)

    const coreGroup = new THREE.Group()
    coreGroup.position.set(3.0, 0, -1.8)
    scene.add(coreGroup)

    const core = new THREE.Mesh(new THREE.SphereGeometry(2.06, 64, 40),
      new THREE.MeshPhysicalMaterial({ color: 0x0b2d6a, emissive: 0x041637, emissiveIntensity: 0.34, specular: 0x9beaff, metalness: 0.5, roughness: 0.16, clearcoat: 0.9, clearcoatRoughness: 0.1, transparent: true, opacity: 0.92 }))
    coreGroup.add(core)

    const coreShell = new THREE.Mesh(new THREE.SphereGeometry(2.1, 26, 18),
      new THREE.MeshBasicMaterial({ color: 0x5ac9ff, wireframe: true, transparent: true, opacity: 0.15 }))
    coreGroup.add(coreShell)

    const coreHalo = new THREE.Mesh(new THREE.SphereGeometry(2.32, 32, 24),
      new THREE.MeshBasicMaterial({ color: 0x2c77d3, transparent: true, opacity: 0.035, side: THREE.BackSide }))
    coreGroup.add(coreHalo)

    const globeLines = new THREE.Group()
    const gridMaterial = new THREE.LineBasicMaterial({ color: 0x5ac9ff, transparent: true, opacity: 0.16 })
    for (let i = -3; i <= 3; i++) {
      const latitude = (i / 4) * (Math.PI / 2)
      const radius = Math.cos(latitude) * 2.08
      const points: any[] = []
      for (let j = 0; j <= 64; j++) { const theta = (j / 64) * Math.PI * 2; points.push(new THREE.Vector3(Math.cos(theta) * radius, Math.sin(latitude) * 2.08, Math.sin(theta) * radius)) }
      globeLines.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), gridMaterial.clone()))
    }
    for (let i = 0; i < 12; i++) {
      const longitude = (i / 12) * Math.PI * 2
      const points: any[] = []
      for (let j = 0; j <= 48; j++) { const latitude = (j / 48) * Math.PI - Math.PI / 2; const radius = Math.cos(latitude) * 2.08; points.push(new THREE.Vector3(Math.cos(longitude) * radius, Math.sin(latitude) * 2.08, Math.sin(longitude) * radius)) }
      globeLines.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), gridMaterial.clone()))
    }

    const arcMaterial = new THREE.LineBasicMaterial({ color: 0x8be7ff, transparent: true, opacity: 0.78 })
    const makeArc = (latitude: number, start: number, length: number) => {
      const points: any[] = []; const radius = Math.cos(latitude) * 2.12
      for (let i = 0; i <= 28; i++) { const theta = start + (i / 28) * length; points.push(new THREE.Vector3(Math.cos(theta) * radius, Math.sin(latitude) * 2.12, Math.sin(theta) * radius)) }
      return new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), arcMaterial.clone())
    }
    globeLines.add(makeArc(0.36, -1.4, 2.2)); globeLines.add(makeArc(-0.28, 1.2, 2.8)); globeLines.add(makeArc(0.08, 3.5, 1.45))
    coreGroup.add(globeLines)

    const nodeCount = 56
    const dotGeo = new THREE.BufferGeometry(); const dotPos = new Float32Array(nodeCount * 3)
    for (let i = 0; i < nodeCount; i++) {
      const latitude = Math.acos(1 - 2 * ((i + 0.5) / nodeCount)) - Math.PI / 2
      const longitude = Math.PI * (1 + Math.sqrt(5)) * i
      const radius = Math.cos(latitude) * 2.1
      dotPos[i * 3] = Math.cos(longitude) * radius
      dotPos[i * 3 + 1] = Math.sin(latitude) * 2.1
      dotPos[i * 3 + 2] = Math.sin(longitude) * radius
    }
    dotGeo.setAttribute('position', new THREE.BufferAttribute(dotPos, 3))
    const dots = new THREE.Points(dotGeo, new THREE.PointsMaterial({ color: 0x8be7ff, size: 0.055, transparent: true, opacity: 0.72, sizeAttenuation: true }))
    coreGroup.add(dots)

    const connections = globeLines

    const pulseMaterial = new THREE.MeshBasicMaterial({ color: 0x6bdbff, transparent: true, opacity: 0.42 })
    const pulseRing = new THREE.Mesh(new THREE.TorusGeometry(2.12, 0.018, 8, 96), pulseMaterial)
    pulseRing.rotation.x = Math.PI / 2.4
    coreGroup.add(pulseRing)

    const pivot = new THREE.Group()
    pivot.position.copy(coreGroup.position); scene.add(pivot)
    const rM = new THREE.MeshLambertMaterial({ color: 0x4ca7ff, transparent: true, opacity: 0.3, emissive: 0x1652a4, emissiveIntensity: 0.18 })
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(3.3, 0.012, 8, 80), rM)
    r1.rotation.x = Math.PI / 3; r1.rotation.z = 0.5; pivot.add(r1)
    const rM2 = new THREE.MeshLambertMaterial({ color: 0x7edfff, transparent: true, opacity: 0.22, emissive: 0x1977b9, emissiveIntensity: 0.12 })
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(3.7, 0.01, 8, 80), rM2)
    r2.rotation.x = Math.PI / 2.5; r2.rotation.y = 1.3; r2.rotation.z = 0.4; pivot.add(r2)

    const sDefs: any[] = [
      { a: 0, r: 3.3, sp: 0.048, yA: 0.2, yP: 0, ge: new THREE.SphereGeometry(0.13, 10, 8), co: 0x6bc9ff, sc: 1 },
      { a: 2.2, r: 4.1, sp: 0.032, yA: 0.35, yP: 1.8, ge: new THREE.SphereGeometry(0.1, 10, 8), co: 0x76aaff, sc: 1 },
      { a: 4.8, r: 4.9, sp: 0.022, yA: 0.4, yP: 3.2, ge: new THREE.OctahedronGeometry(0.14), co: 0x8be7ff, sc: 1 },
      { a: 1.2, r: 3.5, sp: 0.042, yA: 0.15, yP: 1.2, ge: new THREE.SphereGeometry(0.12, 10, 8), co: 0x5da0ff, sc: 1 },
      { a: 5.0, r: 4.5, sp: 0.028, yA: 0.3, yP: 2.8, ge: new THREE.SphereGeometry(0.09, 10, 8), co: 0x71ddff, sc: 1 },
      { a: 0.8, r: 3.1, sp: 0.055, yA: 0.12, yP: 0.5, ge: new THREE.OctahedronGeometry(0.16), co: 0x9fb8ff, sc: 1 },
      { a: 3.2, r: 3.9, sp: 0.035, yA: 0.25, yP: 2.0, ge: new THREE.SphereGeometry(0.1, 10, 8), co: 0x6bc9ff, sc: 1 },
      { a: 6.0, r: 4.7, sp: 0.025, yA: 0.38, yP: 3.5, ge: new THREE.OctahedronGeometry(0.12), co: 0x76aaff, sc: 1 },
      { a: 1.6, r: 3.6, sp: 0.045, yA: 0.18, yP: 1.0, ge: new THREE.SphereGeometry(0.1, 10, 8), co: 0x8be7ff, sc: 1 },
      { a: 4.0, r: 4.3, sp: 0.03, yA: 0.28, yP: 2.5, ge: new THREE.OctahedronGeometry(0.12), co: 0x5da0ff, sc: 1 },
    ]
    const sats: any[] = []
    const signalLines: any[] = []
    sDefs.forEach((d, i) => {
      const m = new THREE.Mesh(d.ge, new THREE.MeshLambertMaterial({ color: d.co, emissive: d.co, emissiveIntensity: 0.1, transparent: true, opacity: 0.65 }))
      m.scale.set(d.sc, d.sc, d.sc); m.position.set(Math.cos(d.a) * d.r, 0, Math.sin(d.a) * d.r)
      m.userData = { d, i }; pivot.add(m); sats.push(m)
      const lineGeo = new THREE.BufferGeometry()
      const startRadius = 2.1
      lineGeo.setAttribute('position', new THREE.Float32BufferAttribute([Math.cos(d.a) * startRadius, 0, Math.sin(d.a) * startRadius, m.position.x, m.position.y, m.position.z], 3))
      const line = new THREE.Line(lineGeo, new THREE.LineBasicMaterial({ color: d.co, transparent: true, opacity: 0.13 }))
      pivot.add(line); signalLines.push(line)
    })

    const bgGeo = new THREE.BufferGeometry(); const bgP = new Float32Array(60 * 3)
    for (let i = 0; i < 60; i++) { bgP[i * 3] = (Math.random() - 0.5) * 30; bgP[i * 3 + 1] = (Math.random() - 0.5) * 20; bgP[i * 3 + 2] = (Math.random() - 0.5) * 20 - 3 }
    bgGeo.setAttribute('position', new THREE.BufferAttribute(bgP, 3))
    const bgPts = new THREE.Points(bgGeo, new THREE.PointsMaterial({ color: 0x9bcfc1, size: 0.02, transparent: true, opacity: 0.1, sizeAttenuation: true }))
    scene.add(bgPts)

    let rx = 0, ry = 0
    const setPointerState = (clientX: number, clientY: number) => {
      ry = ((clientX / window.innerWidth) * 2 - 1) * 0.05
      rx = ((clientY / window.innerHeight) * 2 - 1) * 0.03
      heroRoot.value?.style.setProperty('--spot-x', `${clientX}px`)
      heroRoot.value?.style.setProperty('--spot-y', `${clientY}px`)
    }
    const mm = (e: MouseEvent) => setPointerState(e.clientX, e.clientY)
    const tm = (e: TouchEvent) => { if (e.touches.length > 0) setPointerState(e.touches[0].clientX, e.touches[0].clientY) }
    document.addEventListener('mousemove', mm); document.addEventListener('touchmove', tm, { passive: true })
    const resizeHandler = () => { const w = container.clientWidth, h = container.clientHeight; if (w > 0 && h > 0) { camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h) } }
    window.addEventListener('resize', resizeHandler)

    const clock = new (THREE as any).Clock(); let id: number
    function animate() {
      id = requestAnimationFrame(animate); const t = clock.getElapsedTime()
      coreGroup.rotation.x += (rx - coreGroup.rotation.x) * 0.012; coreGroup.rotation.y += (ry - coreGroup.rotation.y) * 0.012
      pivot.rotation.x += (rx - pivot.rotation.x) * 0.012; pivot.rotation.y += (ry - pivot.rotation.y) * 0.012
      core.rotation.y += 0.002; core.rotation.x = Math.sin(t * 0.008) * 0.03
      coreShell.rotation.y -= 0.0015; coreShell.rotation.x = Math.sin(t * 0.008) * 0.03
      coreHalo.rotation.y -= 0.001; globeLines.rotation.y += 0.0018
      dots.rotation.y += 0.003; dots.rotation.x = Math.sin(t * 0.008) * 0.03
      connections.rotation.y += 0.002
      pulseRing.scale.setScalar(1 + Math.sin(t * 1.3) * 0.045)
      pulseMaterial.opacity = 0.26 + (Math.sin(t * 1.3) + 1) * 0.1
      r1.rotation.z += 0.001; r2.rotation.y += 0.0008
      sats.forEach((s, i) => {
        const d = sDefs[i]; const a = d.a + t * d.sp
        s.position.x = Math.cos(a) * d.r; s.position.z = Math.sin(a) * d.r; s.position.y = Math.sin(a * 1.5 + d.yP + t * 0.12) * d.yA
        s.rotation.x = t * 0.3 + i; s.rotation.y = t * 0.5 + i
        const position = signalLines[i].geometry.attributes.position.array
        position[3] = s.position.x; position[4] = s.position.y; position[5] = s.position.z
        signalLines[i].geometry.attributes.position.needsUpdate = true
      })
      bgPts.rotation.y = t * 0.002; renderer.render(scene, camera)
    }
    animate()
    cleanup = () => {
      document.removeEventListener('mousemove', mm); document.removeEventListener('touchmove', tm)
      window.removeEventListener('resize', resizeHandler)
      cancelAnimationFrame(id); clock.stop()
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement); renderer.dispose()
    }
  }
})
onBeforeUnmount(() => { if (cleanup) cleanup() })
</script>

<style scoped>
.landing-magazine { font-family: 'Bricolage Grotesque', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif; color: #0f172a; overflow-x: hidden; }
.top-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 200; backdrop-filter: blur(14px) saturate(1.3); -webkit-backdrop-filter: blur(14px) saturate(1.3); background: rgba(15,23,42,0.55); border-bottom: 1px solid rgba(255,255,255,0.05); }
.nav-inner { display: flex; width: 100%; align-items: center; justify-content: space-between; padding: 0.78rem 3rem; margin: 0 auto; }
.nav-links { display: flex; align-items: center; gap: 12px; margin: 0; padding: 0; list-style: none; }
.logo-wrap { display: flex; align-items: center; gap: 0.6rem; }
.logo-mark { display: flex; width: 32px; height: 26px; align-items: center; justify-content: center; color: #76d8ff; }
.logo-mark svg { width: 28px; height: 22px; }
.logo-text { font-size: 1.18rem; font-weight: 700; letter-spacing: 0; color: #fff; }
.logo-ver { font-size: 0.76rem; font-weight: 500; color: #8da3c1; }
.nav-cta { padding: 0.52rem 1.25rem; border: 1px solid rgba(116,205,255,0.26); border-radius: 8px; background: #2164c5; color: #fff; font-weight: 600; font-size: 0.88rem; cursor: pointer; transition: all 0.2s; font-family: inherit; }
.nav-cta:hover { transform: translateY(-1px); background: #2f78e8; box-shadow: 0 8px 24px rgba(47,120,232,0.3); }
.starfield { position: absolute; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.sf-bg { position: absolute; inset: 0; background: #07162f url('/img/data-network.jpg') center / cover no-repeat; opacity: 0.72; filter: saturate(0.8) hue-rotate(7deg); }
.sf-grad { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(4,13,30,0.98) 0%, rgba(5,18,43,0.8) 48%, rgba(7,24,57,0.3) 100%); }
.star { display: none; position: absolute; border-radius: 50%; pointer-events: none; }
.nebula { display: none; position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
.n1 { width: 500px; height: 400px; background: radial-gradient(circle, rgba(59,130,254,0.04), transparent); top: 8%; left: 18%; }
.n2 { width: 450px; height: 380px; background: radial-gradient(circle, rgba(59,130,254,0.03), transparent); bottom: 12%; right: 12%; }
.ground-glow { display: none; }
.band-hero { --spot-x: 72vw; --spot-y: 42vh; position: relative; height: 100vh; min-height: 700px; overflow: hidden; }
.hero-spotlight { position: absolute; inset: 0; z-index: 1; pointer-events: none; background: radial-gradient(430px 340px at var(--spot-x) var(--spot-y), rgba(77,157,255,0.18), transparent 72%); mix-blend-mode: screen; transition: background 240ms ease-out; }
.hero-beams { position: absolute; inset: 0; z-index: 1; pointer-events: none; overflow: hidden; opacity: 0.65; }
.hero-beam { position: absolute; display: block; height: 1px; transform-origin: right center; background: linear-gradient(90deg, transparent, rgba(143,210,193,0.42), transparent); box-shadow: 0 0 16px rgba(143,210,193,0.24); animation: beamDrift 8s ease-in-out infinite; }
.beam-a { top: 32%; right: -8%; width: 56%; transform: rotate(-17deg); }
.beam-b { top: 61%; right: -10%; width: 48%; background: linear-gradient(90deg, transparent, rgba(114,184,255,0.42), transparent); box-shadow: 0 0 16px rgba(114,184,255,0.24); animation-delay: -2.8s; transform: rotate(12deg); }
.beam-c { top: 45%; right: 2%; width: 31%; opacity: 0.55; animation-delay: -5.2s; transform: rotate(-42deg); }
.hero-three-bg { position: absolute; inset: 0; z-index: 2; }
.hero-grid { position: relative; z-index: 3; display: grid; grid-template-columns: 54% 46%; height: calc(100vh - 56px); padding-top: 56px; }
.hero-left { display: flex; flex-direction: column; justify-content: center; gap: 0.5rem; padding: 2rem 80px 6rem 48px; }
.hero-badge { display: inline-flex; align-items: center; gap: 0.55rem; padding: 0.38rem 0.8rem; border: 1px solid rgba(117,204,255,0.24); border-radius: 7px; background: rgba(5,18,43,0.44); color: rgba(220,238,255,0.78); font-size: 0.72rem; font-weight: 500; width: fit-content; animation: contentReveal 760ms 80ms both; }
.hero-badge i, .readout-status i { width: 6px; height: 6px; flex-shrink: 0; border-radius: 50%; background: #76d8ff; box-shadow: 0 0 0 4px rgba(118,216,255,0.1); }
.hero-title { display: flex; gap: 0.22em; font-size: clamp(2.8rem, 4.5vw, 4.5rem); font-weight: 700; line-height: 1.05; margin: 0; letter-spacing: 0; background: none; background-clip: initial; -webkit-background-clip: initial; -webkit-text-fill-color: initial; }
.hero-title-main { color: #f4f8f6; animation: titleReveal 900ms 180ms both; }
.hero-title-accent { position: relative; color: #76d8ff; animation: titleReveal 900ms 300ms both; }
.hero-title-accent::after { position: absolute; right: 0; bottom: -0.12em; left: 0.08em; height: 2px; content: ""; background: #3979ed; transform-origin: left; animation: lineReveal 680ms 800ms both; }
.hero-subtitle { font-size: clamp(1.4rem, 2.2vw, 2.25rem); font-weight: 300; color: #fff; letter-spacing: -0.02em; margin: 0; }
.hero-subtitle { animation: contentReveal 800ms 480ms both; }
.hero-desc { font-size: clamp(0.85rem, 1.05vw, 1.05rem); color: #a8b9b3; line-height: 1.8; max-width: 520px; margin: 0.2rem 0; animation: contentReveal 800ms 580ms both; }
.hero-buttons { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.4rem; animation: contentReveal 800ms 700ms both; }
.hero-author-row { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.4rem; }
.auth-label { font-size: 0.78rem; color: #64748b; font-weight: 500; }
.auth-name { font-size: 0.88rem; color: #94a3b8; text-decoration: none; font-weight: 500; transition: color 0.2s; }
.auth-name:hover { color: #fff; }
.hero-right { display: flex; align-items: flex-start; justify-content: flex-end; padding: 17vh 7vw 0 0; pointer-events: none; }
.hero-readout { position: relative; width: min(248px, 70%); padding: 16px 17px 14px; overflow: hidden; border: 1px solid rgba(117,204,255,0.28); border-radius: 12px; background: rgba(5,18,43,0.42); box-shadow: 0 20px 60px rgba(0,0,0,0.24); backdrop-filter: blur(15px); animation: readoutEnter 900ms 900ms both; }
.hero-readout::before { position: absolute; inset: -120%; content: ""; background: conic-gradient(from 90deg, transparent 0deg, transparent 276deg, rgba(118,216,255,0.82) 314deg, transparent 342deg); animation: borderSpin 5s linear infinite; }
.hero-readout::after { position: absolute; inset: 1px; z-index: 0; content: ""; border-radius: 11px; background: rgba(5,18,43,0.88); }
.readout-head, .readout-value, .readout-label, .readout-bars, .readout-foot { position: relative; z-index: 1; }
.readout-head, .readout-foot { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.readout-kicker, .readout-status, .readout-label, .readout-foot { color: #8faed1; font-family: 'Google Sans Code', monospace; font-size: 9px; letter-spacing: 0.04em; }
.readout-status { display: inline-flex; align-items: center; gap: 6px; color: #76d8ff; }
.readout-value { margin-top: 20px; color: #f4f8f6; font-family: 'Google Sans Code', monospace; font-size: 31px; font-weight: 600; line-height: 1; }
.readout-label { margin-top: 6px; color: #a8b9b3; }
.readout-bars { display: flex; align-items: end; gap: 5px; height: 49px; margin-top: 17px; padding-bottom: 8px; border-bottom: 1px solid rgba(143,210,193,0.16); }
.readout-bars span { flex: 1; min-width: 4px; border-radius: 2px 2px 0 0; background: linear-gradient(180deg, #8be7ff, #2f78e8); transform-origin: bottom; animation: readoutBars 1.8s ease-in-out infinite alternate; }
.readout-bars span:nth-child(2n) { animation-delay: -0.5s; }.readout-bars span:nth-child(3n) { animation-delay: -1s; }
.readout-foot { margin-top: 10px; }.readout-foot strong { color: #76d8ff; font-family: 'Google Sans Code', monospace; font-size: 12px; font-weight: 600; }
.scene-fallback { position: absolute; right: 13%; top: 44%; z-index: 2; display: flex; flex-direction: column; gap: 0.25rem; color: rgba(255,255,255,0.82); font-family: 'JetBrains Mono', monospace; pointer-events: none; }
.scene-fallback span { color: #76d8ff; font-size: 1.2rem; letter-spacing: 0.04em; }
.scene-fallback small { color: #8faed1; font-size: 0.68rem; letter-spacing: 0.08em; }
.btn { position: relative; display: inline-flex; align-items: center; gap: 0.55rem; padding: 0.7rem 0; border-radius: 8px; font-size: 0.88rem; font-weight: 600; border: none; cursor: pointer; transition: transform 0.3s ease, color 0.3s ease, background 0.3s ease; text-decoration: none; font-family: inherit; width: 200px; justify-content: center; }
.btn b { font-size: 1.05em; font-weight: 500; transition: transform 0.3s ease; }.btn:hover b { transform: translateX(3px); }
.btn-primary { isolation: isolate; overflow: hidden; background: transparent; color: #fff; box-shadow: 0 4px 20px rgba(47,120,232,0.28); }
.btn-primary::before { position: absolute; inset: -130%; z-index: -2; content: ""; background: conic-gradient(from 0deg, transparent 0deg, transparent 280deg, #8be7ff 320deg, transparent 355deg); animation: borderSpin 3.6s linear infinite; }
.btn-primary::after { position: absolute; inset: 1px; z-index: -1; content: ""; border-radius: 7px; background: linear-gradient(135deg, #2f78e8, #174fae); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(47,120,232,0.45); }
.btn-secondary { background: rgba(255,255,255,0.08); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); }
.btn-secondary:hover { background: rgba(255,255,255,0.12); color: #fff; border-color: rgba(255,255,255,0.2); transform: translateY(-2px); }
.metrics-track { position: absolute; bottom: 24px; left: 0; right: 0; z-index: 10; padding: 0 3rem; }
.metrics-bar { display: flex; align-items: center; max-width: 960px; margin: 0 auto; background: rgba(15,23,42,0.35); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(148,163,184,0.2); border-radius: 16px; padding: 1.1rem 0.5rem; }
.m-item { flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; align-items: center; gap: 0.1rem; }
.m-num { font-size: clamp(1.4rem, 2.5vw, 2.8rem); font-weight: 700; letter-spacing: -0.02em; color: #8be7ff; line-height: 1.1; }
.m-item:last-child .m-num, .m-item:last-child .m-num small { color: #76d8ff; }.m-num small { font-size: 0.6em; font-weight: 600; color: #8be7ff; }
.m-lbl { font-size: clamp(0.6rem, 0.8vw, 0.82rem); color: rgba(148,163,184,0.8); font-weight: 500; white-space: nowrap; }
.m-div { width: 1px; height: 34px; background: rgba(148,163,184,0.2); flex-shrink: 0; }
.band-features { min-height: 500px; background: #f8fafc; padding: 5rem 2rem; }
.band-features2 { min-height: 400px; background: #fff; padding: 5rem 2rem; }
.fi { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 30% 70%; gap: 2rem; align-items: start; }
.fl { position: sticky; top: 80px; display: flex; flex-direction: column; gap: 0.8rem; }
.fl-badge { display: inline-flex; align-items: center; gap: 0.45rem; font-size: 0.7rem; font-weight: 600; color: #e56b55; text-transform: uppercase; letter-spacing: 0.08em; }.fl-badge i { width: 18px; height: 2px; background: #e56b55; }
.fl-title { font-size: clamp(1.5rem, 2.5vw, 2.25rem); font-weight: 700; letter-spacing: -0.02em; color: #0f172a; margin: 0; }
.fl-desc { font-size: 0.95rem; color: #64748b; line-height: 1.7; margin: 0; }
.mini-s-wrap { position: relative; width: 100px; height: 100px; margin-top: 0.3rem; }
.mini-s { width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #b2e4d8, #2e8b78 55%, #163f38 100%); box-shadow: inset -20px -20px 60px rgba(0,0,0,0.3), 0 0 40px rgba(46,139,120,0.18); animation: ms 12s linear infinite; }
@keyframes ms { from { transform: rotate(0deg) } 50% { transform: rotate(180deg) scale(1.04) } to { transform: rotate(360deg) } }
@keyframes titleReveal { from { opacity: 0; filter: blur(12px); transform: translateY(18px); } to { opacity: 1; filter: blur(0); transform: translateY(0); } }
@keyframes contentReveal { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes lineReveal { from { opacity: 0; transform: scaleX(0); } to { opacity: 1; transform: scaleX(1); } }
@keyframes readoutEnter { from { opacity: 0; transform: translateY(18px) rotate(2deg); } to { opacity: 1; transform: translateY(0) rotate(0); } }
@keyframes borderSpin { to { transform: rotate(360deg); } }
@keyframes beamDrift { 0%, 100% { opacity: 0.2; } 50% { opacity: 0.8; } }
@keyframes readoutBars { from { transform: scaleY(0.78); opacity: 0.62; } to { transform: scaleY(1); opacity: 1; } }
.mini-s.s2 { background: radial-gradient(circle at 35% 30%, #ffd0c5, #d56b58 55%, #5b2922 100%); box-shadow: inset -20px -20px 60px rgba(0,0,0,0.3), 0 0 40px rgba(229,107,85,0.18); }
.fr { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.fc { padding: 1.5rem; border-radius: 14px; background: #fff; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 1px 4px rgba(0,0,0,0.03); transition: all 0.3s ease; display: flex; flex-direction: column; gap: 0.5rem; }
.fc:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); border-color: rgba(229,107,85,0.24); }
.fc-i { width: 44px; height: 44px; border-radius: 10px; background: linear-gradient(135deg,rgba(229,107,85,0.1),rgba(46,139,120,0.1)); border: 1px solid rgba(229,107,85,0.16); display: flex; align-items: center; justify-content: center; color: #e56b55; }
.fc-i svg { width: 22px; height: 22px; }
.fc h3 { font-size: 1rem; font-weight: 600; color: #0f172a; margin: 0; }
.fc p { font-size: 0.82rem; color: #64748b; line-height: 1.6; margin: 0; flex: 1; }
.fc-tags { display: flex; gap: 0.3rem; flex-wrap: wrap; font-size: 0.68rem; color: #94a3b8; padding: 0.35rem 0.6rem; background: #f8fafc; border-radius: 6px; width: fit-content; }
.band-footer { background: #0f172a; border-top: 1px solid #334155; padding: 2.5rem 2rem; }
.footer-i { max-width: 1000px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; }
.footer-c { display: flex; flex-direction: column; gap: 0.3rem; }
.footer-c-c { text-align: center; }
.footer-c-r { text-align: right; }
.footer-l { font-size: 0.6rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500; margin-bottom: 0.1rem; }
.footer-a { font-size: 0.85rem; color: #94a3b8; text-decoration: none; transition: color 0.2s; }
.footer-a:hover { color: #fff; }
.footer-a-sm { font-size: 0.75rem; }
.footer-t { font-size: 0.85rem; color: #94a3b8; }
.footer-t-sm { font-size: 0.7rem; }
@media (max-width:1100px) { .hero-left { padding-left: 2rem; } .hero-title { font-size: 2.8rem; } .hero-subtitle { font-size: 1.5rem; } .hero-right { padding-right: 3vw; } }
@media (max-width:900px) {
  .nav-inner { padding: 0.7rem 1.25rem; }
  .hero-grid { grid-template-columns: 1fr; height: calc(100vh - 50px); padding-top: 50px; }
  .hero-left { align-items: center; text-align: center; padding: 4rem 1.5rem 6rem; order: 2; }
  .hero-desc { max-width: 100%; } .hero-buttons { align-items: center; } .hero-author-row { justify-content: center; }
  .hero-right { display: none; } .hero-three-bg { opacity: 0.25; } .starfield { opacity: 0.5; }
  .metrics-track { bottom: 16px; padding: 0 1rem; } .metrics-bar { padding: 0.8rem 0; border-radius: 12px; } .m-div { height: 24px; }
  .band-features { padding: 3rem 1.25rem; } .fi { grid-template-columns: 1fr; } .fl { position: static; text-align: center; align-items: center; } .mini-s-wrap { margin: 0 auto; } .fr { grid-template-columns: 1fr 1fr; }
}
@media (max-width:640px) {
  .hero-title { font-size: 2rem; } .hero-subtitle { font-size: 1.2rem; } .hero-badge { font-size: 0.6rem; } .hero-left { padding: 3rem 1rem 5rem; }
  .btn { width: 180px; font-size: 0.8rem; } .metrics-bar { flex-wrap: wrap; padding: 0.6rem 0.5rem; } .m-div { display: none; }
  .m-item { flex-direction: row; gap: 0.3rem; min-width: 30%; justify-content: center; padding: 0.2rem 0; } .m-num { font-size: 1.1rem; } .m-lbl { font-size: 0.6rem; }
  .fr { grid-template-columns: 1fr; } .footer-i { grid-template-columns: 1fr; text-align: center; gap: 1.25rem; } .footer-c-r { text-align: center; }
}
@media (prefers-reduced-motion: reduce) { .fc:hover { transform: none; } .mini-s { animation: none; } .hero-three-bg { display: none; } .scene-fallback { display: flex; } .hero-spotlight, .hero-beams { display: none; } .hero-badge, .hero-title-main, .hero-title-accent, .hero-subtitle, .hero-desc, .hero-buttons, .hero-readout { animation: none; } .hero-title-accent::after, .hero-readout::before, .btn-primary::before, .readout-bars span { animation: none; } }
</style>
