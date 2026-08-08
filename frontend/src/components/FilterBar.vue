<template>
  <div class="filter-panel" aria-label="数据筛选">
    <div class="filter-panel-head">
      <div>
        <span class="filter-kicker">Data view</span>
        <strong>筛选条件</strong>
      </div>
      <span class="filter-hint">选择后即时刷新</span>
    </div>
    <div class="filter-row">
      <div class="filter-group">
        <label class="filter-label">情感</label>
        <div class="segmented-control" role="group" aria-label="情感筛选">
          <button
            v-for="opt in sentimentOptions"
            :key="opt.value"
            class="seg-btn"
            type="button"
            :class="{ active: selectedSentiment === opt.value }"
            :aria-pressed="selectedSentiment === opt.value"
            @click="selectSentiment(opt.value)"
          >{{ opt.label }}</button>
        </div>
      </div>
      <div class="filter-group">
        <label class="filter-label">方面</label>
        <div class="segmented-control" role="group" aria-label="方面筛选">
          <button class="seg-btn" type="button" :class="{ active: selectedCategory === 'all' }" :aria-pressed="selectedCategory === 'all'" @click="selectCategory('all')">全部</button>
          <button
            v-for="cat in visibleCategories"
            :key="cat.value"
            class="seg-btn"
            type="button"
            :class="{ active: selectedCategory === cat.value }"
            :aria-pressed="selectedCategory === cat.value"
            @click="selectCategory(cat.value)"
          >{{ cat.label }}</button>
          <button v-if="hiddenCategories.length > 0" class="seg-btn seg-more" type="button" :class="{ active: showMore }" :aria-expanded="showMore" @click="showMore = !showMore">+{{ hiddenCategories.length }}</button>
        </div>
        <div v-if="showMore" class="more-dropdown" role="menu">
          <button v-for="cat in hiddenCategories" :key="cat.value" class="more-item" type="button" role="menuitem" :class="{ active: selectedCategory === cat.value }" @click="selectCategory(cat.value); showMore = false">{{ cat.label }}</button>
        </div>
      </div>
      <div v-if="totalCount > 0" class="filter-count">
        <div class="count-dot" aria-hidden="true"></div>
        <span>{{ totalCount.toLocaleString() }} 条评论</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import http from '../http'
import emitter from '../utils/eventBus'
import { categoryMap } from '../utils/chineseMap'

const props = defineProps<{ sentimentFilter?: string; aspectFilter?: string }>()
const emit = defineEmits(['update:sentimentFilter', 'update:aspectFilter'])

const sentimentOptions = [
  { label: '全部', value: 'all' },
  { label: '正面', value: 'positive' },
  { label: '负面', value: 'negative' },
]

const selectedSentiment = ref('all')
const selectedCategory = ref('all')
const totalCount = ref(0)
const showMore = ref(false)

const categoryOptions = computed(() => Object.entries(categoryMap).map(([value, label]) => ({ value, label })))
const visibleCategories = computed(() => categoryOptions.value.slice(0, 4))
const hiddenCategories = computed(() => categoryOptions.value.slice(4))

function toSentimentValue(value?: string) {
  return value === '正面' || value === 'positive' ? 'positive' : value === '负面' || value === 'negative' ? 'negative' : 'all'
}

function emitChange() {
  const filters = { sentiment: selectedSentiment.value, category: selectedCategory.value }
  emitter.emit('filter-change', filters)
  emit('update:sentimentFilter', selectedSentiment.value === 'all' ? '全部' : selectedSentiment.value === 'positive' ? '正面' : '负面')
  emit('update:aspectFilter', selectedCategory.value === 'all' ? '全部' : selectedCategory.value)
  http.post('/summary', filters).then((response) => { totalCount.value = response.data.total ?? 0 }).catch(() => { totalCount.value = 0 })
}

function selectSentiment(value: string) { selectedSentiment.value = value; emitChange() }
function selectCategory(value: string) { selectedCategory.value = value; emitChange() }

watch(() => props.sentimentFilter, (value) => { selectedSentiment.value = toSentimentValue(value) })
watch(() => props.aspectFilter, (value) => { selectedCategory.value = value && value !== '全部' ? value : 'all' })

onMounted(async () => {
  try {
    const response = await http.post('/summary', { sentiment: selectedSentiment.value, category: selectedCategory.value })
    totalCount.value = response.data.total ?? 0
  } catch { totalCount.value = 0 }
})
</script>

<style scoped>
.filter-panel { padding: 12px 14px 13px; }
.filter-panel-head { display: flex; align-items: center; justify-content: space-between; gap: 24px; margin-bottom: 9px; padding-bottom: 9px; border-bottom: 1px solid var(--line); }
.filter-panel-head > div { display: flex; align-items: baseline; gap: 8px; }
.filter-kicker { color: var(--accent); font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.08em; text-transform: uppercase; }
.filter-panel-head strong { color: var(--ink); font-size: 12px; }
.filter-hint { color: var(--text-faint); font-size: 10px; white-space: nowrap; }
.filter-row { display: flex; align-items: center; flex-wrap: wrap; gap: 14px; }
.filter-group { position: relative; display: flex; align-items: center; gap: 8px; }
.filter-label { color: var(--text-faint); font-size: 10px; font-weight: 700; letter-spacing: 0.06em; }
.segmented-control { display: flex; gap: 2px; padding: 2px; border-radius: 7px; background: var(--canvas-deep); }
.seg-btn { min-height: 27px; padding: 4px 10px; border: 0; border-radius: 5px; background: transparent; color: var(--text-muted); font-size: 11px; font-weight: 600; cursor: pointer; transition: color var(--transition-fast), background var(--transition-fast), transform var(--transition-fast); white-space: nowrap; }
.seg-btn:hover { color: var(--ink); }.seg-btn:active { transform: scale(0.96); }.seg-btn.active { background: var(--panel); color: var(--accent-hover); box-shadow: var(--shadow-sm); }.seg-btn.seg-more { color: var(--accent); }
.more-dropdown { position: absolute; top: calc(100% + 6px); left: 46px; z-index: 20; display: flex; min-width: 140px; max-height: 280px; flex-direction: column; gap: 2px; overflow-y: auto; padding: 4px; border: 1px solid var(--line); border-radius: 7px; background: var(--panel); box-shadow: var(--shadow-md); }
.more-item { padding: 7px 10px; border: 0; border-radius: 5px; background: transparent; color: var(--text-muted); cursor: pointer; font-size: 11px; text-align: left; }.more-item:hover, .more-item.active { background: var(--accent-soft); color: var(--accent-hover); }
.filter-count { display: flex; align-items: center; gap: 6px; color: var(--text-faint); font-family: var(--font-mono); font-size: 10px; white-space: nowrap; }.count-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--positive); }
@media (max-width: 768px) { .filter-panel { padding: 12px; }.filter-panel-head { gap: 12px; }.filter-row { align-items: flex-start; flex-direction: column; }.filter-group { align-items: flex-start; flex-direction: column; gap: 5px; width: 100%; }.segmented-control { max-width: 100%; overflow-x: auto; }.more-dropdown { position: static; width: 100%; max-height: 180px; margin-top: 6px; } }
</style>
