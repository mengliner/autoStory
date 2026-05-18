<template>
  <div class="foreshadow-tab">
    <div v-if="!store.foreshadowings.length" class="empty-tab">暂无伏笔</div>
    <div class="foreshadow-stats">
      <span>埋入: {{ planted.length }}</span>
      <span>已回收: {{ resolved.length }}</span>
    </div>
    <div
      v-for="f in store.foreshadowings"
      :key="f.id"
      class="foreshadow-card"
      :class="f.status"
    >
      <div class="f-header">
        <span class="f-status">{{ f.status === 'planted' ? '🌱' : '🎯' }}</span>
        <h4>{{ f.title }}</h4>
      </div>
      <p class="f-desc">{{ f.description }}</p>
      <div class="f-meta">
        <span v-if="f.planted_chapter_id">埋入: 第{{ f.planted_chapter_id }}章</span>
        <span v-if="f.resolved_chapter_id">回收: 第{{ f.resolved_chapter_id }}章</span>
      </div>
      <p v-if="f.resolved_note" class="f-resolution">{{ f.resolved_note }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()
const planted = computed(() => store.foreshadowings.filter(f => f.status === 'planted'))
const resolved = computed(() => store.foreshadowings.filter(f => f.status === 'resolved'))
</script>

<style scoped>
.foreshadow-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  font-size: 13px;
  color: #888;
}
.foreshadow-card {
  background: #16213e;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  border-left: 3px solid #f59e0b;
}
.foreshadow-card.resolved { border-left-color: #4ade80; opacity: .7; }
.f-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.f-header h4 { font-size: 14px; }
.f-status { font-size: 14px; }
.f-desc { font-size: 13px; color: #999; line-height: 1.5; margin-bottom: 6px; }
.f-meta { font-size: 12px; color: #666; display: flex; gap: 12px; }
.f-resolution { font-size: 12px; color: #4ade80; margin-top: 4px; }
.empty-tab { text-align: center; color: #666; padding: 40px 0; }
</style>
