<template>
  <div class="message-list" ref="listEl">
    <div v-if="store.chatMessages.length === 0" class="empty-chat">
      <p>开始和 AI 对话，创作你的故事吧 ✍️</p>
      <p class="hint">例如："帮我构思一个修真世界的故事大纲"</p>
    </div>
    <template v-for="(msg, idx) in store.chatMessages" :key="idx">
      <ChatMessage :message="msg" />
      <CandidateCard
        v-if="msg.candidates && msg.candidates.length"
        :candidates="msg.candidates"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useStoryStore } from '@/stores/story'
import ChatMessage from './ChatMessage.vue'
import CandidateCard from './CandidateCard.vue'

const store = useStoryStore()
const listEl = ref<HTMLElement>()

watch(() => store.chatMessages.length, () => {
  nextTick(() => {
    if (listEl.value) {
      listEl.value.scrollTop = listEl.value.scrollHeight
    }
  })
})
</script>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
.empty-chat {
  text-align: center;
  color: #666;
  padding: 80px 20px;
}
.empty-chat p { margin-bottom: 8px; }
.hint { font-size: 14px; color: #555; }
</style>
