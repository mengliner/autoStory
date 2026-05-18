<template>
  <div class="project-list-page">
    <header class="page-header">
      <h1>📖 我的故事</h1>
      <p class="subtitle">AI 小说创作助手</p>
    </header>

    <div v-if="errorMsg" class="error-banner">{{ errorMsg }}</div>

    <div class="create-bar">
      <input
        v-model="newTitle"
        placeholder="输入新故事标题..."
        @keyup.enter="handleCreate"
        class="create-input"
        maxlength="100"
      />
      <button @click="handleCreate" :disabled="!newTitle.trim() || loading" class="btn btn-primary">
        {{ loading ? '创建中...' : '创建故事' }}
      </button>
    </div>

    <div class="project-grid" v-if="store.projects.length">
      <div
        v-for="project in store.projects"
        :key="project.id"
        class="project-card"
        @click="$router.push(`/story/${project.id}`)"
      >
        <div class="card-header">
          <h2>{{ project.title }}</h2>
          <span class="status-badge" :class="project.status">{{ project.status }}</span>
        </div>
        <p class="card-synopsis">{{ project.synopsis || '暂无简介' }}</p>
        <div class="card-footer">
          <span class="card-date">{{ formatDate(project.updated_at) }}</span>
          <button class="btn-delete" @click.stop="handleDelete(project.id)">删除</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>还没有故事，创建一个开始吧</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useStoryStore } from '@/stores/story'
import { useRouter } from 'vue-router'

const store = useStoryStore()
const router = useRouter()
const newTitle = ref('')

const errorMsg = ref('')
const loading = ref(false)

onMounted(async () => {
  try {
    await store.loadProjects()
  } catch {
    errorMsg.value = '无法连接后端服务，请确认后端已启动 (localhost:8001)'
  }
})

async function handleCreate() {
  if (!newTitle.value.trim()) return
  loading.value = true
  errorMsg.value = ''
  try {
    const p = await store.addProject(newTitle.value.trim())
    newTitle.value = ''
    router.push(`/story/${p.id}`)
  } catch {
    errorMsg.value = '创建失败，请确认后端服务已启动'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: number) {
  if (confirm('确定删除这个故事？')) {
    await store.removeProject(id)
  }
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.project-list-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}
.page-header {
  text-align: center;
  margin-bottom: 32px;
}
.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}
.subtitle {
  color: #888;
  font-size: 16px;
}
.error-banner {
  background: #3b1010;
  border: 1px solid #ef4444;
  color: #fca5a5;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}
.create-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}
.create-input {
  flex: 1;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #333;
  background: #16213e;
  color: #e0e0e0;
  font-size: 16px;
}
.create-input:focus {
  outline: none;
  border-color: #7c3aed;
}
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: opacity .2s;
}
.btn:disabled {
  opacity: .4;
  cursor: not-allowed;
}
.btn-primary {
  background: #7c3aed;
  color: #fff;
}
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.project-card {
  background: #16213e;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: border-color .2s;
}
.project-card:hover {
  border-color: #7c3aed;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.card-header h2 {
  font-size: 20px;
}
.status-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  background: #333;
}
.status-badge.planning { background: #374151; color: #9ca3af; }
.status-badge.writing { background: #1e3a5f; color: #60a5fa; }
.status-badge.done { background: #14532d; color: #4ade80; }
.card-synopsis {
  color: #999;
  font-size: 14px;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-date { font-size: 12px; color: #666; }
.btn-delete {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 13px;
}
.empty-state {
  text-align: center;
  color: #666;
  padding: 60px 0;
}
</style>
