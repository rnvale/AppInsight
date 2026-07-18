<template>
  <div class="landing-magazine">
    <nav class="top-nav">
      <div class="nav-inner">
        <div class="logo-wrap">
          <div class="logo-icon">A</div>
          <span class="logo-text">AppInsight</span>
          <span class="logo-ver">v3.0</span>
        </div>
        <ul class="nav-links">
          <li><button @click="$emit('enter')" class="nav-cta">进入项目 →</button></li>
        </ul>
      </div>
    </nav>

    <section class="band-hero">
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

      <div ref="threeContainer" class="hero-three-bg"></div>

      <div class="hero-grid">
        <div class="hero-left">
          <div class="hero-badge"><span>✦</span><span>通用文本评论情感分析可视化架构</span></div>
          <h1 class="hero-title">AppInsight</h1>
          <h2 class="hero-subtitle">洞察每一句评论</h2>
          <p class="hero-desc">从评论文本到可视化图表，<br>一套可复用的多维评论数据情感分析框架，让数据讲述完整故事。</p>
          <div class="hero-buttons">
            <button @click="$emit('enter')" class="btn btn-primary">探索分析平台 →</button>
            <a href="https://github.com/rnvale/myweb1" class="btn btn-secondary" target="_blank">查看源代码 ▸</a>
          </div>
          <div class="hero-author-row">
            <span class="auth-label">作者</span>
            <a href="https://github.com/rnvale" target="_blank" class="auth-name">Rain Vale</a>
          </div>
        </div>
        <div class="hero-right" aria-hidden="true"></div>
      </div>

      <div class="metrics-track">
        <div class="metrics-bar">
          <div class="m-item">
            <span class="m-num" data-count="12">0</span>
            <span class="m-lbl">可视化图表</span>
          </div>
          <div class="m-div"></div>
          <div class="m-item">
            <span class="m-num" data-count="11321">0</span>
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

    <section class="band-features">
      <div class="fi">
        <div class="fl">
          <div class="fl-badge">✦ 核心能力</div>
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

    <section class="band-features2">
      <div class="fi">
        <div class="fl">
          <div class="fl-badge">✦ 新增能力</div>
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
          <span class="footer-t">AppInsight v3.0</span>
          <span class="footer-t footer-t-sm">情感分析可视化系统</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const emit = defineEmits<{ (e: 'enter'): void }>()
const threeContainer = ref<HTMLDivElement | null>(null)

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
  document.head.appendChild(script)

  function initScene() {
    const THREE = (window as any).THREE
    if (!THREE || !threeContainer.value) return

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

    scene.add(new THREE.AmbientLight(0x475569, 0.7))
    const key = new THREE.DirectionalLight(0xc7d2fe, 0.6)
    key.position.set(4, 6, 5); scene.add(key)
    const back = new THREE.DirectionalLight(0x93c5fd, 0.15)
    back.position.set(-3, -1, -5); scene.add(back)

    const planetGeo = new THREE.IcosahedronGeometry(2.0, 1)
    const posA = planetGeo.attributes.position
    const cols = new Float32Array(posA.count * 3)
    for (let i = 0; i < posA.count; i++) {
      const y = posA.getY(i); const t = (y + 2.0) / 4.0
      const rC = 0.192 + (0.388 - 0.192) * t
      const gC = 0.180 + (0.400 - 0.180) * t
      const bC = 0.506 + (0.945 - 0.506) * t
      cols[i * 3] = rC; cols[i * 3 + 1] = gC; cols[i * 3 + 2] = bC
    }
    planetGeo.setAttribute('color', new THREE.BufferAttribute(cols, 3))

    const planetMat = new THREE.MeshPhongMaterial({
      color: 0x4f46e5, emissive: 0x312e81, emissiveIntensity: 0.08,
      specular: 0x818cf8, shininess: 25, flatShading: true, vertexColors: true,
    })
    const planet = new THREE.Mesh(planetGeo, planetMat)
    planet.position.set(3.0, 0, -1.8); scene.add(planet)

    const wireframe = new THREE.Mesh(new THREE.IcosahedronGeometry(2.1, 1),
      new THREE.MeshBasicMaterial({ color: 0x818cf8, wireframe: true, transparent: true, opacity: 0.1 }))
    wireframe.position.copy(planet.position); scene.add(wireframe)

    const dotGeo = new THREE.BufferGeometry(); const dotPos = new Float32Array(30 * 3)
    for (let i = 0; i < 30; i++) {
      const theta = Math.random() * Math.PI * 2, phi = Math.acos(2 * Math.random() - 1), r = 2.05
      dotPos[i * 3] = Math.sin(phi) * Math.cos(theta) * r
      dotPos[i * 3 + 1] = Math.sin(phi) * Math.sin(theta) * r
      dotPos[i * 3 + 2] = Math.cos(phi) * r
    }
    dotGeo.setAttribute('position', new THREE.BufferAttribute(dotPos, 3))
    const dots = new THREE.Points(dotGeo, new THREE.PointsMaterial({ color: 0xc7d2fe, size: 0.05, transparent: true, opacity: 0.5, sizeAttenuation: true }))
    dots.position.copy(planet.position); scene.add(dots)

    const pivot = new THREE.Group()
    pivot.position.copy(planet.position); scene.add(pivot)
    const rM = new THREE.MeshLambertMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.25, emissive: 0x94a3b8, emissiveIntensity: 0.15 })
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(3.3, 0.012, 8, 80), rM)
    r1.rotation.x = Math.PI / 3; r1.rotation.z = 0.5; pivot.add(r1)
    const rM2 = new THREE.MeshLambertMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.2, emissive: 0x94a3b8, emissiveIntensity: 0.1 })
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(3.7, 0.01, 8, 80), rM2)
    r2.rotation.x = Math.PI / 2.5; r2.rotation.y = 1.3; r2.rotation.z = 0.4; pivot.add(r2)

    const sDefs: any[] = [
      { a: 0, r: 3.3, sp: 0.048, yA: 0.2, yP: 0, ge: new THREE.BoxGeometry(0.32, 0.32, 0.32), co: 0x86efac, sc: 1 },
      { a: 2.2, r: 4.1, sp: 0.032, yA: 0.35, yP: 1.8, ge: new THREE.BoxGeometry(0.24, 0.24, 0.24), co: 0x86efac, sc: 1 },
      { a: 4.8, r: 4.9, sp: 0.022, yA: 0.4, yP: 3.2, ge: new THREE.OctahedronGeometry(0.2), co: 0x86efac, sc: 1 },
      { a: 1.2, r: 3.5, sp: 0.042, yA: 0.15, yP: 1.2, ge: new THREE.BoxGeometry(0.28, 0.28, 0.28), co: 0xfde68a, sc: 1 },
      { a: 5.0, r: 4.5, sp: 0.028, yA: 0.3, yP: 2.8, ge: new THREE.BoxGeometry(0.2, 0.2, 0.2), co: 0xfde68a, sc: 1 },
      { a: 0.8, r: 3.1, sp: 0.055, yA: 0.12, yP: 0.5, ge: new THREE.OctahedronGeometry(0.28), co: 0xa5b4fc, sc: 1 },
      { a: 3.2, r: 3.9, sp: 0.035, yA: 0.25, yP: 2.0, ge: new THREE.OctahedronGeometry(0.22), co: 0xa5b4fc, sc: 1 },
      { a: 6.0, r: 4.7, sp: 0.025, yA: 0.38, yP: 3.5, ge: new THREE.ConeGeometry(0.2, 0.3, 4), co: 0xa5b4fc, sc: 1 },
      { a: 1.6, r: 3.6, sp: 0.045, yA: 0.18, yP: 1.0, ge: new THREE.ConeGeometry(0.22, 0.32, 4), co: 0xa5f3fc, sc: 1 },
      { a: 4.0, r: 4.3, sp: 0.03, yA: 0.28, yP: 2.5, ge: new THREE.ConeGeometry(0.16, 0.06, 3), co: 0xa5f3fc, sc: 1.2 },
      { a: 6.8, r: 5.1, sp: 0.02, yA: 0.42, yP: 4.0, ge: new THREE.IcosahedronGeometry(0.15), co: 0xa5f3fc, sc: 1 },
      { a: 2.6, r: 3.4, sp: 0.04, yA: 0.22, yP: 1.5, ge: new THREE.OctahedronGeometry(0.24), co: 0xc7d2fe, sc: 1 },
      { a: 5.6, r: 4.2, sp: 0.026, yA: 0.32, yP: 3.0, ge: new THREE.TetrahedronGeometry(0.22), co: 0xc7d2fe, sc: 1 },
      { a: 3.4, r: 3.7, sp: 0.038, yA: 0.2, yP: 2.2, ge: new THREE.BoxGeometry(0.18, 0.18, 0.18), co: 0xe2e8f0, sc: 1 },
      { a: 0.4, r: 4.6, sp: 0.024, yA: 0.35, yP: 0.8, ge: new THREE.IcosahedronGeometry(0.16), co: 0xe2e8f0, sc: 1 },
    ]
    const sats: any[] = []
    sDefs.forEach((d, i) => {
      const m = new THREE.Mesh(d.ge, new THREE.MeshLambertMaterial({ color: d.co, emissive: d.co, emissiveIntensity: 0.1, transparent: true, opacity: 0.65 }))
      m.scale.set(d.sc, d.sc, d.sc); m.position.set(Math.cos(d.a) * d.r, 0, Math.sin(d.a) * d.r)
      m.userData = { d, i }; pivot.add(m); sats.push(m)
    })

    const bgGeo = new THREE.BufferGeometry(); const bgP = new Float32Array(60 * 3)
    for (let i = 0; i < 60; i++) { bgP[i * 3] = (Math.random() - 0.5) * 30; bgP[i * 3 + 1] = (Math.random() - 0.5) * 20; bgP[i * 3 + 2] = (Math.random() - 0.5) * 20 - 3 }
    bgGeo.setAttribute('position', new THREE.BufferAttribute(bgP, 3))
    const bgPts = new THREE.Points(bgGeo, new THREE.PointsMaterial({ color: 0xbfdbfe, size: 0.02, transparent: true, opacity: 0.08, sizeAttenuation: true }))
    scene.add(bgPts)

    let rx = 0, ry = 0
    const mm = (e: MouseEvent) => { ry = ((e.clientX / window.innerWidth) * 2 - 1) * 0.05; rx = ((e.clientY / window.innerHeight) * 2 - 1) * 0.03 }
    const tm = (e: TouchEvent) => { if (e.touches.length > 0) { ry = ((e.touches[0].clientX / window.innerWidth) * 2 - 1) * 0.05; rx = ((e.touches[0].clientY / window.innerHeight) * 2 - 1) * 0.03 } }
    document.addEventListener('mousemove', mm); document.addEventListener('touchmove', tm, { passive: true })
    window.addEventListener('resize', () => { const w = container.clientWidth, h = container.clientHeight; if (w > 0 && h > 0) { camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h) } })

    const clock = new (THREE as any).Clock(); let id: number
    function animate() {
      id = requestAnimationFrame(animate); const t = clock.getElapsedTime()
      const pg = planet.parent!; pg.rotation.x += (rx - pg.rotation.x) * 0.012; pg.rotation.y += (ry - pg.rotation.y) * 0.012
      planet.rotation.y += 0.003; planet.rotation.x = Math.sin(t * 0.008) * 0.03
      wireframe.rotation.y += 0.003; wireframe.rotation.x = Math.sin(t * 0.008) * 0.03
      dots.rotation.y += 0.003; dots.rotation.x = Math.sin(t * 0.008) * 0.03
      r1.rotation.z += 0.001; r2.rotation.y += 0.0008
      sats.forEach((s, i) => { const d = sDefs[i]; const a = d.a + t * d.sp; s.position.x = Math.cos(a) * d.r; s.position.z = Math.sin(a) * d.r; s.position.y = Math.sin(a * 1.5 + d.yP + t * 0.12) * d.yA; s.rotation.x = t * 0.3 + i; s.rotation.y = t * 0.5 + i })
      bgPts.rotation.y = t * 0.002; renderer.render(scene, camera)
    }
    animate()
    cleanup = () => {
      document.removeEventListener('mousemove', mm); document.removeEventListener('touchmove', tm)
      cancelAnimationFrame(id); clock.stop()
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement); renderer.dispose()
    }
  }
})
onBeforeUnmount(() => { if (cleanup) cleanup() })
</script>

<style scoped>
.landing-magazine { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Noto Sans SC', sans-serif; color: #0f172a; overflow-x: hidden; }
.top-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 200; backdrop-filter: blur(14px) saturate(1.3); -webkit-backdrop-filter: blur(14px) saturate(1.3); background: rgba(15,23,42,0.55); border-bottom: 1px solid rgba(255,255,255,0.05); }
.nav-inner { display: flex; justify-content: space-between; align-items: center; padding: 0.7rem 2.5rem; max-width: 1400px; margin: 0 auto; }
.logo-wrap { display: flex; align-items: center; gap: 0.6rem; }
.logo-icon { width: 26px; height: 26px; background: linear-gradient(135deg, #0891b2, #d97706); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; font-size: 0.75rem; }
.logo-text { font-size: 1rem; font-weight: 700; letter-spacing: -0.02em; color: #fff; }
.logo-ver { font-size: 0.65rem; font-weight: 500; color: #64748b; }
.nav-cta { padding: 0.4rem 1.1rem; border-radius: 100px; background: linear-gradient(135deg, #0891b2, #2563eb); color: #fff; font-weight: 600; font-size: 0.78rem; cursor: pointer; transition: all 0.2s; border: none; font-family: inherit; }
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(8,145,178,0.3); }
.starfield { position: absolute; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.sf-bg { position: absolute; inset: 0; background: #0f172a; }
.sf-grad { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 0%, #1e293b 0%, #0f172a 50%, #0a0f1a 100%); mix-blend-mode: screen; }
.star { position: absolute; border-radius: 50%; pointer-events: none; }
.nebula { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
.n1 { width: 500px; height: 400px; background: radial-gradient(circle, rgba(59,130,254,0.04), transparent); top: 8%; left: 18%; }
.n2 { width: 450px; height: 380px; background: radial-gradient(circle, rgba(59,130,254,0.03), transparent); bottom: 12%; right: 12%; }
.ground-glow { position: absolute; bottom: 5%; left: 62%; width: 380px; height: 100px; background: radial-gradient(ellipse, rgba(59,130,246,0.06), transparent); filter: blur(60px); transform: translateX(-50%); pointer-events: none; }
.band-hero { position: relative; height: 100vh; min-height: 700px; overflow: hidden; }
.hero-three-bg { position: absolute; inset: 0; z-index: 1; }
.hero-grid { position: relative; z-index: 2; display: grid; grid-template-columns: 60% 40%; height: calc(100vh - 56px); padding-top: 56px; }
.hero-left { display: flex; flex-direction: column; justify-content: center; gap: 0.5rem; padding: 2rem 80px 6rem 48px; }
.hero-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.3rem 0.85rem; border-radius: 100px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); font-size: 0.78rem; font-weight: 500; color: rgba(255,255,255,0.6); width: fit-content; }
.hero-title { font-size: clamp(2.8rem, 4.5vw, 4.5rem); font-weight: 700; letter-spacing: -0.03em; line-height: 1.05; margin: 0; background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: clamp(1.4rem, 2.2vw, 2.25rem); font-weight: 300; color: #fff; letter-spacing: -0.02em; margin: 0; }
.hero-desc { font-size: clamp(0.85rem, 1.05vw, 1.05rem); color: #94a3b8; line-height: 1.8; max-width: 520px; margin: 0.2rem 0; }
.hero-buttons { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.4rem; }
.hero-author-row { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.4rem; }
.auth-label { font-size: 0.78rem; color: #64748b; font-weight: 500; }
.auth-name { font-size: 0.88rem; color: #94a3b8; text-decoration: none; font-weight: 500; transition: color 0.2s; }
.auth-name:hover { color: #fff; }
.hero-right { pointer-events: none; }
.btn { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.7rem 0; border-radius: 100px; font-size: 0.88rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s ease; text-decoration: none; font-family: inherit; width: 200px; justify-content: center; }
.btn-primary { background: linear-gradient(135deg, #0891b2, #2563eb); color: #fff; box-shadow: 0 4px 20px rgba(8,145,178,0.3); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(8,145,178,0.45); }
.btn-secondary { background: rgba(255,255,255,0.08); color: #94a3b8; border: 1px solid rgba(255,255,255,0.1); }
.btn-secondary:hover { background: rgba(255,255,255,0.12); color: #fff; border-color: rgba(255,255,255,0.2); transform: translateY(-2px); }
.metrics-track { position: absolute; bottom: 24px; left: 0; right: 0; z-index: 10; padding: 0 3rem; }
.metrics-bar { display: flex; align-items: center; max-width: 960px; margin: 0 auto; background: rgba(15,23,42,0.35); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(148,163,184,0.2); border-radius: 16px; padding: 1.1rem 0.5rem; }
.m-item { flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; align-items: center; gap: 0.1rem; }
.m-num { font-size: clamp(1.4rem, 2.5vw, 2.8rem); font-weight: 700; letter-spacing: -0.02em; color: #60a5fa; line-height: 1.1; }
.m-num small { font-size: 0.6em; font-weight: 600; color: #60a5fa; }
.m-lbl { font-size: clamp(0.6rem, 0.8vw, 0.82rem); color: rgba(148,163,184,0.8); font-weight: 500; white-space: nowrap; }
.m-div { width: 1px; height: 34px; background: rgba(148,163,184,0.2); flex-shrink: 0; }
.band-features { min-height: 500px; background: #f8fafc; padding: 5rem 2rem; }
.band-features2 { min-height: 400px; background: #fff; padding: 5rem 2rem; }
.fi { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 30% 70%; gap: 2rem; align-items: start; }
.fl { position: sticky; top: 80px; display: flex; flex-direction: column; gap: 0.8rem; }
.fl-badge { font-size: 0.7rem; font-weight: 600; color: #2563eb; text-transform: uppercase; letter-spacing: 0.08em; }
.fl-title { font-size: clamp(1.5rem, 2.5vw, 2.25rem); font-weight: 700; letter-spacing: -0.02em; color: #0f172a; margin: 0; }
.fl-desc { font-size: 0.95rem; color: #64748b; line-height: 1.7; margin: 0; }
.mini-s-wrap { position: relative; width: 100px; height: 100px; margin-top: 0.3rem; }
.mini-s { width: 90px; height: 90px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #60a5fa, #1d4ed8 55%, #1e3a5f 100%); box-shadow: inset -20px -20px 60px rgba(0,0,0,0.3), 0 0 40px rgba(59,130,246,0.2); animation: ms 12s linear infinite; }
@keyframes ms { from { transform: rotate(0deg) } 50% { transform: rotate(180deg) scale(1.04) } to { transform: rotate(360deg) } }
.mini-s.s2 { background: radial-gradient(circle at 35% 30%, #f59e0b, #d97706 55%, #78350f 100%); box-shadow: inset -20px -20px 60px rgba(0,0,0,0.3), 0 0 40px rgba(245,158,11,0.2); }
.fr { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.fc { padding: 1.5rem; border-radius: 14px; background: #fff; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 1px 4px rgba(0,0,0,0.03); transition: all 0.3s ease; display: flex; flex-direction: column; gap: 0.5rem; }
.fc:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.08); border-color: rgba(37,99,235,0.12); }
.fc-i { width: 44px; height: 44px; border-radius: 10px; background: linear-gradient(135deg,rgba(8,145,178,0.08),rgba(37,99,235,0.08)); border: 1px solid rgba(37,99,235,0.1); display: flex; align-items: center; justify-content: center; color: #2563eb; }
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
@media (max-width:1100px) { .hero-left { padding-left: 2rem; } .hero-title { font-size: 2.8rem; } .hero-subtitle { font-size: 1.5rem; } }
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
@media (prefers-reduced-motion: reduce) { .fc:hover { transform: none; } .mini-s { animation: none; } }
</style>
