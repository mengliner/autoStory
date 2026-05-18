<template>
  <div class="chat-message" :class="[message.role, { error: message.isError }]">
    <div class="message-avatar">{{ message.role === 'user' ? '👤' : '🤖' }}</div>
    <div class="message-content">
      <div class="message-text" v-text="message.content"></div>
      <button v-if="message.isError" class="retry-btn">重试</button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: { role: string; content: string; isError?: boolean; candidates?: any[] }
}>()
</script>

<style scoped>
.chat-message {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}
.chat-message.user { flex-direction: row-reverse; }
.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}
.chat-message.user .message-avatar { background: #7c3aed; }
.chat-message.assistant .message-avatar { background: #1e3a5f; }
.message-content {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  line-height: 1.6;
  font-size: 14px;
}
.chat-message.user .message-content {
  background: #7c3aed;
  color: #fff;
  border-bottom-right-radius: 2px;
}
.chat-message.assistant .message-content {
  background: #16213e;
  border-bottom-left-radius: 2px;
}
.chat-message.error .message-content {
  background: #3b1010;
  border: 1px solid #ef4444;
}
.retry-btn {
  margin-top: 8px;
  padding: 4px 12px;
  border: 1px solid #ef4444;
  border-radius: 4px;
  background: transparent;
  color: #ef4444;
  cursor: pointer;
  font-size: 12px;
}
</style>
