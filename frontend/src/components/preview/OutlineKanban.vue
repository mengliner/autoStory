<template>
  <div class="outline-kanban">
    <div
      v-for="col in columns"
      :key="col.status"
      class="kanban-column"
    >
      <div class="kanban-col-header">
        {{ col.label }}
        <span class="count">{{ col.nodes.length }}</span>
      </div>
      <div
        v-for="node in col.nodes"
        :key="node.id"
        class="kanban-card"
      >
        <div class="card-title">{{ node.title }}</div>
        <div class="card-meta">
          <span>{{ node.level }}</span>
          <span v-if="node.summary">{{ node.summary.slice(0, 60) }}</span>
        </div>
      </div>
      <div v-if="!col.nodes.length" class="kanban-empty">无</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()
const columns = computed(() => [
  { status: 'outline', label: '🗒 大纲', nodes: store.outline.filter(n => n.status === 'outline') },
  { status: 'draft', label: '📝 草稿', nodes: store.outline.filter(n => n.status === 'draft') },
  { status: 'writing', label: '✍️ 写作中', nodes: store.outline.filter(n => n.status === 'writing') },
  { status: 'done', label: '✅ 已完成', nodes: store.outline.filter(n => n.status === 'done') },
])
</script>

<style scoped>
.outline-kanban {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.kanban-column {
  background: #0f0f23;
  border-radius: 8px;
  padding: 10px;
}
.kanban-col-header {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
}
.count { font-size: 12px; color: #888; background: #16213e; padding: 1px 6px; border-radius: 8px; }
.kanban-card {
  background: #16213e;
  border-radius: 6px;
  padding: 8px 10px;
  margin-bottom: 6px;
  border: 1px solid #2a2a4a;
}
.card-title { font-size: 13px; color: #e0e0e0; margin-bottom: 4px; }
.card-meta { font-size: 12px; color: #888; display: flex; gap: 8px; }
.kanban-empty { text-align: center; color: #555; font-size: 13px; padding: 12px; }
</style>
