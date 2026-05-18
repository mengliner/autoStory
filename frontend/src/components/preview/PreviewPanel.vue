<template>
  <div class="preview-panel">
    <div class="panel-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="panel-content">
      <OutlineTab v-if="activeTab === 'outline'" />
      <CharacterTab v-if="activeTab === 'characters'" />
      <WorldSettingTab v-if="activeTab === 'settings'" />
      <ForeshadowTab v-if="activeTab === 'foreshadowings'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import OutlineTab from './OutlineTab.vue'
import CharacterTab from './CharacterTab.vue'
import WorldSettingTab from './WorldSettingTab.vue'
import ForeshadowTab from './ForeshadowTab.vue'

const activeTab = ref('outline')
const tabs = [
  { key: 'outline', label: '📖 大纲' },
  { key: 'characters', label: '👤 角色' },
  { key: 'settings', label: '🌍 世界观' },
  { key: 'foreshadowings', label: '💡 伏笔' },
]
</script>

<style scoped>
.preview-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #12122a;
}
.panel-tabs {
  display: flex;
  border-bottom: 1px solid #2a2a4a;
  padding: 0 16px;
}
.tab-btn {
  padding: 12px 16px;
  border: none;
  background: none;
  color: #888;
  cursor: pointer;
  font-size: 14px;
  border-bottom: 2px solid transparent;
  transition: all .2s;
}
.tab-btn.active {
  color: #7c3aed;
  border-bottom-color: #7c3aed;
}
.tab-btn:hover { color: #b0b0b0; }
.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
</style>
