<template>
  <header class="story-header">
    <div class="header-left">
      <router-link to="/" class="home-link">← 返回</router-link>
      <h1 v-if="store.project" class="story-title">{{ store.project.title }}</h1>
    </div>
    <div class="header-actions">
      <span v-if="store.isStreaming" class="streaming-indicator">AI 创作中...</span>
      <router-link :to="`/story/${$route.params.id}/preview`" class="btn btn-outline">
        预览模式
      </router-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()
</script>

<style scoped>
.story-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #0f0f23;
  border-bottom: 1px solid #2a2a4a;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.home-link {
  color: #7c3aed;
  text-decoration: none;
  font-size: 14px;
}
.story-title {
  font-size: 18px;
  color: #e0e0e0;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.streaming-indicator {
  font-size: 13px;
  color: #f59e0b;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
.btn-outline {
  padding: 6px 16px;
  border: 1px solid #7c3aed;
  border-radius: 6px;
  color: #7c3aed;
  text-decoration: none;
  font-size: 14px;
  background: transparent;
  cursor: pointer;
  transition: background .2s;
}
.btn-outline:hover {
  background: rgba(124, 58, 237, .1);
}
</style>
