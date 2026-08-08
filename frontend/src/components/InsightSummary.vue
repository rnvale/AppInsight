<template>
  <section class="insight-summary" aria-labelledby="insight-title">
    <div class="insight-copy">
      <div class="insight-eyebrow">Signal readout / {{ sentimentLabel }}</div>
      <h2 id="insight-title" class="insight-title">{{ insightTitle }}</h2>
      <p class="insight-description">{{ insightDescription }}</p>
      <div class="insight-source">基于 {{ fmt(total) }} 条评论 · {{ categoryLabel }} · 可继续下钻</div>
    </div>

    <div class="insight-right">
      <div class="insight-metrics" aria-label="关键指标">
        <div class="insight-metric"><div class="insight-metric-label">正面率</div><div class="insight-metric-value positive">{{ positiveRate }}%</div></div>
        <div class="insight-metric"><div class="insight-metric-label">平均评分</div><div class="insight-metric-value">{{ avgRating }}</div></div>
        <div class="insight-metric"><div class="insight-metric-label">NPS</div><div class="insight-metric-value accent">{{ npsScore }}</div></div>
        <div class="insight-metric"><div class="insight-metric-label">分析维度</div><div class="insight-metric-value">{{ aspectCount }}</div></div>
      </div>
      <div class="insight-links" aria-label="分析入口">
        <button v-for="link in links" :key="link.view" class="insight-link" type="button" @click="$emit('open', link.view)">
          <span class="insight-link-label">{{ link.label }}</span>
          <span class="insight-link-arrow" aria-hidden="true">↗</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  positiveRate: string
  avgRating: string
  npsScore: number
  total: number
  aspectCount: number
  avgLength: string
  sentiment: string
  category: string
}>()

defineEmits<{ (event: 'open', view: string): void }>()

const links = [
  { view: 'sentiment', label: '看情感变化' },
  { view: 'topics', label: '挖掘主题' },
  { view: 'rankings', label: '比较 App' },
  { view: 'explorer', label: '浏览评论' },
]

const fmt = (n: number) => n.toLocaleString()
const sentimentLabel = computed(() => props.sentiment === '全部' ? '全部评论' : `${props.sentiment}评论`)
const categoryLabel = computed(() => props.category === '全部' ? '综合数据集' : props.category)
const insightTitle = computed(() => {
  if (!props.total) return '等待数据进入信号区'
  const rate = Number(props.positiveRate)
  if (rate >= 60) return '整体口碑偏正向，继续定位高潜领域'
  if (rate <= 40) return '负面信号偏高，建议优先检查问题主题'
  return '正负反馈接近，值得继续拆解差异来源'
})
const insightDescription = computed(() => {
  if (!props.total) return '当前筛选没有可用于生成结论的数据，请调整筛选条件或刷新数据。'
  return `当前平均评分为 ${props.avgRating}，NPS 为 ${props.npsScore}。评论平均长度 ${props.avgLength || '0'} 字，先从领域和主题开始下钻，可以更快找到影响口碑的具体信号。`
})
</script>
