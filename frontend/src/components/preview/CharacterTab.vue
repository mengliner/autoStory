<template>
  <div class="character-tab">
    <div class="char-grid">
      <div v-for="char in store.characters" :key="char.id" class="char-card">
        <h3>{{ char.name }}</h3>
        <span class="char-role">{{ char.role || '未设定' }}</span>
        <p v-if="char.personality" class="char-meta">{{ char.personality.slice(0, 80) }}</p>
        <p v-if="char.background" class="char-meta">{{ char.background.slice(0, 80) }}</p>
      </div>
    </div>
    <div v-if="!store.characters.length" class="empty-tab">暂无角色</div>

    <RelationshipGraph v-if="store.relationships.length" />
  </div>
</template>

<script setup lang="ts">
import { useStoryStore } from '@/stores/story'
import RelationshipGraph from './RelationshipGraph.vue'

const store = useStoryStore()
</script>

<style scoped>
.char-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}
.char-card {
  background: #16213e;
  border-radius: 10px;
  padding: 14px;
  border: 1px solid #2a2a4a;
}
.char-card h3 { font-size: 16px; margin-bottom: 4px; }
.char-role {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background: #1e3a5f;
  color: #60a5fa;
  display: inline-block;
  margin-bottom: 8px;
}
.char-meta { font-size: 13px; color: #999; line-height: 1.4; }
.empty-tab { text-align: center; color: #666; padding: 40px 0; }
</style>
