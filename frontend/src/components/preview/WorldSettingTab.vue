<template>
  <div class="settings-tab">
    <div v-if="!store.settings.length" class="empty-tab">暂无世界观设定</div>
    <div v-for="group in groupedSettings" :key="group.category" class="setting-group">
      <h3>{{ group.category }}</h3>
      <div v-for="s in group.items" :key="s.id" class="setting-card">
        <h4>{{ s.title }}</h4>
        <p>{{ s.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()

const groupedSettings = computed(() => {
  const groups = new Map<string, typeof store.settings>()
  store.settings.forEach(s => {
    const cat = s.category || '未分类'
    if (!groups.has(cat)) groups.set(cat, [])
    groups.get(cat)!.push(s)
  })
  return Array.from(groups.entries()).map(([category, items]) => ({ category, items }))
})
</script>

<style scoped>
.setting-group { margin-bottom: 20px; }
.setting-group h3 {
  font-size: 14px;
  color: #7c3aed;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #2a2a4a;
}
.setting-card {
  background: #16213e;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
}
.setting-card h4 { font-size: 14px; margin-bottom: 4px; }
.setting-card p { font-size: 13px; color: #999; line-height: 1.5; }
.empty-tab { text-align: center; color: #666; padding: 40px 0; }
</style>
