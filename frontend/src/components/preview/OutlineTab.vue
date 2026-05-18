<template>
  <div class="outline-tab">
    <div class="view-switcher">
      <button
        v-for="v in views"
        :key="v.key"
        class="view-btn"
        :class="{ active: activeView === v.key }"
        @click="activeView = v.key"
      >
        {{ v.label }}
      </button>
    </div>

    <OutlineTree v-if="activeView === 'tree'" />
    <OutlineTimeline v-if="activeView === 'timeline'" />
    <OutlineKanban v-if="activeView === 'kanban'" />

    <div v-if="!store.outline.length" class="empty-outline">
      暂无大纲，在对话中告诉 AI 你想要的故事结构
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStoryStore } from '@/stores/story'
import OutlineTree from './OutlineTree.vue'
import OutlineTimeline from './OutlineTimeline.vue'
import OutlineKanban from './OutlineKanban.vue'

const store = useStoryStore()
const activeView = ref('tree')
const views = [
  { key: 'tree', label: '树状' },
  { key: 'timeline', label: '时间线' },
  { key: 'kanban', label: '看板' },
]
</script>

<style scoped>
.view-switcher {
  display: flex;
  gap: 4px;
  margin-bottom: 16px;
  background: #0f0f23;
  border-radius: 6px;
  padding: 3px;
  width: fit-content;
}
.view-btn {
  padding: 5px 14px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: #888;
  cursor: pointer;
  font-size: 13px;
}
.view-btn.active {
  background: #7c3aed;
  color: #fff;
}
.empty-outline {
  text-align: center;
  color: #666;
  padding: 40px 0;
}
</style>
