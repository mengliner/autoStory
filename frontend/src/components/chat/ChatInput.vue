<template>
  <div class="chat-input-area">
    <textarea
      v-model="message"
      placeholder="描述你想要创作的内容..."
      @keydown.enter.exact.prevent="send"
      :disabled="store.isStreaming"
      rows="2"
      maxlength="8000"
    ></textarea>
    <button
      @click="send"
      :disabled="!message.trim() || store.isStreaming"
      class="send-btn"
    >
      {{ store.isStreaming ? '...' : '发送' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStoryStore } from '@/stores/story'
import { chatSSE } from '@/api/sse'
import { useRoute } from 'vue-router'

const store = useStoryStore()
const route = useRoute()
const message = ref('')

function send() {
  if (!message.value.trim() || store.isStreaming) return
  const msg = message.value.trim()
  message.value = ''
  store.addUserMessage(msg)
  store.isStreaming = true

  chatSSE(
    Number(route.params.id),
    msg,
    (delta) => {
      store.appendAssistantText(delta)
    },
    (data) => {
      if (data.tool === 'save_candidates' && data.result?.success) {
        if (Array.isArray(data.result.data)) {
          store.addAssistantCandidates(data.result.data)
          store.candidates = data.result.data
        }
      }
    },
    (patch) => {
      store.applyStatePatch(patch)
    },
    (errMsg) => {
      store.addErrorMessage(`AI 响应失败: ${errMsg}\n\n请点击重试按钮重新发送。`)
      store.isStreaming = false
    },
    () => {
      store.isStreaming = false
    }
  )
}
</script>

<style scoped>
.chat-input-area {
  padding: 16px;
  border-top: 1px solid #2a2a4a;
  display: flex;
  gap: 8px;
}
textarea {
  flex: 1;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #333;
  background: #16213e;
  color: #e0e0e0;
  font-size: 14px;
  resize: none;
  outline: none;
  font-family: inherit;
}
textarea:focus {
  border-color: #7c3aed;
}
.send-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: #7c3aed;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  align-self: flex-end;
  white-space: nowrap;
}
.send-btn:disabled {
  opacity: .4;
  cursor: not-allowed;
}
</style>
