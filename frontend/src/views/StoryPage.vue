<template>
  <div class="story-page">
    <StoryHeader />
    <div class="story-body">
      <ChatPanel class="chat-panel" />
      <PreviewPanel class="preview-panel" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStoryStore } from '@/stores/story'
import StoryHeader from '@/components/common/StoryHeader.vue'
import ChatPanel from '@/components/chat/ChatPanel.vue'
import PreviewPanel from '@/components/preview/PreviewPanel.vue'

const route = useRoute()
const store = useStoryStore()

onMounted(() => {
  store.loadProject(Number(route.params.id))
})

watch(() => route.params.id, (id) => {
  store.loadProject(Number(id))
})
</script>

<style scoped>
.story-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.story-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.chat-panel {
  width: 40%;
  min-width: 360px;
  border-right: 1px solid #2a2a4a;
}
.preview-panel {
  flex: 1;
  overflow-y: auto;
}
</style>
