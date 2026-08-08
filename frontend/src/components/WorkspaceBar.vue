<template>
  <header class="workspace-bar" aria-label="工作区工具栏">
    <div class="workspace-context">
      <div class="workspace-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 18V9M9 18V6M14 18V3M19 18v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M3 20h18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity=".55"/></svg>
      </div>
      <div class="workspace-copy">
        <div class="workspace-title">{{ pageLabel }}</div>
        <div class="workspace-desc">{{ pageDescription }}</div>
      </div>
    </div>

    <div class="workspace-state">
      <span class="workspace-dataset">{{ datasetLabel }}</span>
      <div class="filter-tokens" v-if="filters.length" aria-label="当前筛选条件">
        <span v-for="filter in filters" :key="filter.label" class="filter-token">
          {{ filter.label }} · {{ filter.value }}
          <button type="button" :aria-label="`清除${filter.label}筛选`" @click="$emit('clear-filter', filter.label)">×</button>
        </span>
      </div>
    </div>

    <div class="workspace-actions">
      <span class="workspace-updated">更新于 {{ updatedAt }}</span>
      <button class="icon-btn" type="button" title="刷新数据" aria-label="刷新数据" @click="$emit('refresh')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 11a8 8 0 0 0-14.9-3M4 5v4h4M4 13a8 8 0 0 0 14.9 3M20 19v-4h-4" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <button class="export-btn" type="button" :disabled="exporting" :aria-busy="exporting" @click="$emit('export')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3v12m0 0 4-4m-4 4-4-4M5 21h14" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <span>{{ exporting ? '生成中' : '导出数据' }}</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  pageLabel: string
  pageDescription: string
  datasetLabel: string
  filters: Array<{ label: string; value: string }>
  updatedAt: string
  exporting: boolean
}>()

defineEmits<{
  (event: 'clear-filter', label: string): void
  (event: 'export'): void
  (event: 'refresh'): void
}>()
</script>
