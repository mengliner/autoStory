<template>
  <div class="outline-timeline">
    <div class="timeline-track">
      <div
        v-for="(node, idx) in sortedNodes"
        :key="node.id"
        class="timeline-item"
      >
        <div class="timeline-dot" :class="node.level"></div>
        <div v-if="idx < sortedNodes.length - 1" class="timeline-line"></div>
        <div class="timeline-content">
          <div class="timeline-header">
            <span class="tl-level">{{ node.level }}</span>
            <span class="tl-title">{{ node.title }}</span>
            <span class="tl-status">{{ statusEmoji(node.status) }}</span>
          </div>
          <div v-if="node.summary" class="tl-summary">{{ node.summary.slice(0, 100) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()
const sortedNodes = computed(() =>
  [...store.outline].sort((a, b) => {
    const levelOrder = { volume: 0, chapter: 1, section: 2 }
    return (levelOrder[a.level] - levelOrder[b.level]) || (a.sort_order - b.sort_order)
  })
)

function statusEmoji(s: string) {
  const m: Record<string, string> = { outline: '🗒', draft: '📝', writing: '✍️', done: '✅' }
  return m[s] || ''
}
</script>

<style scoped>
.outline-timeline { padding: 8px 0; }
.timeline-track { position: relative; }
.timeline-item { display: flex; gap: 12px; position: relative; padding-bottom: 20px; }
.timeline-dot {
  width: 12px; height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
  position: relative;
  z-index: 1;
}
.timeline-dot.volume { background: #7c3aed; }
.timeline-dot.chapter { background: #3b82f6; }
.timeline-dot.section { background: #6b7280; }
.timeline-line {
  position: absolute;
  left: 5px;
  top: 18px;
  width: 2px;
  height: calc(100% - 18px);
  background: #2a2a4a;
}
.timeline-content { flex: 1; }
.timeline-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
.tl-level {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 3px;
  background: #0f0f23;
  color: #888;
}
.tl-title { color: #e0e0e0; }
.tl-status { font-size: 12px; }
.tl-summary { font-size: 13px; color: #888; margin-top: 4px; }
</style>
