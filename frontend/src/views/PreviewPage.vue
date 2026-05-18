<template>
  <div class="preview-page">
    <button class="back-btn" @click="$router.back()">← 返回</button>
    <div v-if="store.project" class="preview-content">
      <h1>{{ store.project.title }}</h1>
      <p class="synopsis">{{ store.project.synopsis }}</p>
      <section v-if="store.outline.length">
        <h2>大纲</h2>
        <OutlineTree />
      </section>
      <section v-if="store.chapters.length">
        <h2>章节</h2>
        <article v-for="ch in store.chapters" :key="ch.id">
          <h3>{{ ch.title }}</h3>
          <div v-html="ch.content" />
        </article>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStoryStore } from '@/stores/story'
import OutlineTree from '@/components/preview/OutlineTree.vue'

const route = useRoute()
const store = useStoryStore()

onMounted(() => store.loadProject(Number(route.params.id)))
</script>

<style scoped>
.preview-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}
.back-btn {
  background: none;
  border: none;
  color: #7c3aed;
  font-size: 16px;
  cursor: pointer;
  margin-bottom: 24px;
}
.preview-content h1 { font-size: 28px; margin-bottom: 16px; }
.synopsis { color: #999; margin-bottom: 32px; }
</style>
