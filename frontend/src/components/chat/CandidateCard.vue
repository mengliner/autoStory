<template>
  <div class="candidate-card">
    <div class="candidate-title">📋 候选版本</div>
    <div class="candidate-versions">
      <div
        v-for="c in candidates"
        :key="c.id"
        class="version-item"
        :class="{ confirmed: c.status === 'confirmed', discarded: c.status === 'discarded' }"
      >
        <span class="version-label">{{ c.version_label || `v${c.id}` }}</span>
        <span class="version-type">({{ c.content_type }})</span>
        <button
          v-if="c.status === 'pending'"
          class="confirm-btn"
          @click="handleConfirm(c.id)"
        >
          确认
        </button>
        <span v-else class="version-status">{{ c.status === 'confirmed' ? '✓' : '✗' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Candidate } from '@/types'
import { useStoryStore } from '@/stores/story'
import { chatSSE } from '@/api/sse'
import { useRoute } from 'vue-router'

const props = defineProps<{ candidates: Candidate[] }>()
const store = useStoryStore()
const route = useRoute()

function handleConfirm(candidateId: number) {
  store.isStreaming = true
  store.addUserMessage(`确认选择候选方案`)
  const msg = `确认选择候选方案 (candidate_id=${candidateId})`

  chatSSE(
    Number(route.params.id),
    msg,
    (delta) => store.appendAssistantText(delta),
    (_data) => {},
    (patch) => store.applyStatePatch(patch),
    (errMsg) => {
      store.addErrorMessage(`确认失败: ${errMsg}`)
      store.isStreaming = false
    },
    () => { store.isStreaming = false }
  )
}
</script>

<style scoped>
.candidate-card {
  margin: 0 0 16px 42px;
  background: #0f0f23;
  border: 1px solid #2a2a4a;
  border-radius: 10px;
  padding: 14px;
}
.candidate-title {
  font-size: 13px;
  color: #888;
  margin-bottom: 10px;
}
.candidate-versions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.version-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #16213e;
  border-radius: 8px;
  border: 1px solid #333;
}
.version-item.confirmed { border-color: #4ade80; opacity: .7; }
.version-item.discarded { border-color: #ef4444; opacity: .5; }
.version-label {
  font-weight: 600;
  font-size: 14px;
  color: #e0e0e0;
}
.version-type { font-size: 12px; color: #888; }
.confirm-btn {
  padding: 2px 10px;
  border: none;
  border-radius: 4px;
  background: #7c3aed;
  color: #fff;
  cursor: pointer;
  font-size: 12px;
}
</style>
