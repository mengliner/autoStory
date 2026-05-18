<template>
  <div class="chat-panel">
    <MessageList />
    <ChatInput />
  </div>
</template>

<script setup lang="ts">
import MessageList from './MessageList.vue'
import ChatInput from './ChatInput.vue'
</script>

<style scoped>
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #1a1a2e;
}
</style>
