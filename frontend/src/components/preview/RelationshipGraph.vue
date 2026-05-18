<template>
  <div class="relationship-graph">
    <h3>关系图谱</h3>
    <div class="graph-container">
      <svg width="100%" height="300">
        <template v-for="rel in store.relationships" :key="rel.id">
          <line
            :x1="getCharPos(rel.char_a_id).x" :y1="getCharPos(rel.char_a_id).y"
            :x2="getCharPos(rel.char_b_id).x" :y2="getCharPos(rel.char_b_id).y"
            stroke="#4a4a6a" stroke-width="1.5"
          />
          <text
            :x="(getCharPos(rel.char_a_id).x + getCharPos(rel.char_b_id).x) / 2"
            :y="(getCharPos(rel.char_a_id).y + getCharPos(rel.char_b_id).y) / 2 - 5"
            text-anchor="middle" fill="#888" font-size="11"
          >{{ rel.relation_type }}</text>
        </template>
        <template v-for="(pos, id) in positions" :key="id">
          <circle :cx="pos.x" :cy="pos.y" r="20" fill="#7c3aed" opacity=".8" />
          <text :x="pos.x" :y="pos.y + 4" text-anchor="middle" fill="#fff" font-size="12">{{ charNames.get(Number(id)) || '?' }}</text>
        </template>
      </svg>
    </div>
    <div class="rel-list">
      <div v-for="rel in store.relationships" :key="rel.id" class="rel-item">
        <span class="rel-chars">{{ charNames.get(rel.char_a_id) }} ↔ {{ charNames.get(rel.char_b_id) }}</span>
        <span class="rel-type">{{ rel.relation_type }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStoryStore } from '@/stores/story'

const store = useStoryStore()

const charNames = computed(() => {
  const m = new Map<number, string>()
  store.characters.forEach(c => m.set(c.id, c.name))
  return m
})

const positions = computed(() => {
  const chars = store.characters
  const pos: Record<number, { x: number; y: number }> = {}
  const cx = 150, cy = 150, rx = 120, ry = 100
  chars.forEach((c, i) => {
    const angle = (2 * Math.PI * i) / Math.max(chars.length, 1) - Math.PI / 2
    pos[c.id] = { x: cx + rx * Math.cos(angle), y: cy + ry * Math.sin(angle) }
  })
  return pos
})

function getCharPos(id: number) {
  const v = positions.value
  return v[id] ?? { x: 0, y: 0 }
}
</script>

<style scoped>
.relationship-graph {
  margin-top: 24px;
  padding: 16px;
  background: #0f0f23;
  border-radius: 10px;
}
.relationship-graph h3 { font-size: 15px; margin-bottom: 12px; }
.graph-container { display: flex; justify-content: center; }
.rel-list { margin-top: 16px; }
.rel-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid #1a1a2e;
  font-size: 13px;
}
.rel-chars { color: #e0e0e0; }
.rel-type { color: #7c3aed; font-size: 12px; padding: 1px 8px; background: rgba(124,58,237,.1); border-radius: 4px; }
</style>
