import { defineStore } from 'pinia'
import type {
  Project, Character, Relationship, OutlineNode, Chapter,
  WorldSetting, Foreshadowing, Candidate, ChatMessage, StatePatch
} from '@/types'
import { fetchProjects, createProject, fetchProjectFullState, deleteProject } from '@/api/sse'

export const useStoryStore = defineStore('story', {
  state: () => ({
    projects: [] as Project[],
    project: null as Project | null,
    characters: [] as Character[],
    relationships: [] as Relationship[],
    outline: [] as OutlineNode[],
    chapters: [] as Chapter[],
    settings: [] as WorldSetting[],
    foreshadowings: [] as Foreshadowing[],
    candidates: [] as Candidate[],
    chatMessages: [] as ChatMessage[],
    connectionStatus: 'connected' as 'connected' | 'reconnecting' | 'disconnected',
    isStreaming: false,
  }),

  actions: {
    async loadProjects() {
      this.projects = await fetchProjects()
    },

    async addProject(title: string, synopsis?: string) {
      const p = await createProject(title, synopsis)
      this.projects.unshift(p)
      return p
    },

    async loadProject(id: number) {
      const state = await fetchProjectFullState(id)
      this.project = state.project
      this.characters = state.characters
      this.relationships = state.relationships
      this.outline = state.outline
      this.chapters = state.chapters
      this.settings = state.settings
      this.foreshadowings = state.foreshadowings
      this.candidates = state.candidates
    },

    async removeProject(id: number) {
      await deleteProject(id)
      this.projects = this.projects.filter(p => p.id !== id)
    },

    addUserMessage(content: string) {
      this.chatMessages.push({ role: 'user', content })
    },

    appendAssistantText(delta: string) {
      const last = this.chatMessages[this.chatMessages.length - 1]
      if (last && last.role === 'assistant') {
        last.content += delta
      } else {
        this.chatMessages.push({ role: 'assistant', content: delta })
      }
    },

    addAssistantCandidates(candidates: Candidate[]) {
      const last = this.chatMessages[this.chatMessages.length - 1]
      if (last && last.role === 'assistant') {
        last.candidates = candidates
      }
    },

    addErrorMessage(message: string) {
      this.chatMessages.push({ role: 'assistant', content: message, isError: true })
    },

    applyStatePatch(patch: StatePatch) {
      const { table, action, data } = patch
      if (action === 'error') return

      switch (table) {
        case 'characters':
          if (action === 'create') this.characters.push(data as Character)
          else if (action === 'update') {
            const idx = this.characters.findIndex(c => c.id === data.id)
            if (idx >= 0) this.characters[idx] = { ...this.characters[idx], ...data }
          }
          break
        case 'outline_nodes':
          if (action === 'create') this.outline.push(data as OutlineNode)
          else if (action === 'update') {
            const idx = this.outline.findIndex(n => n.id === data.id)
            if (idx >= 0) this.outline[idx] = { ...this.outline[idx], ...data }
          }
          break
        case 'chapters':
          if (action === 'create') this.chapters.push(data as Chapter)
          else if (action === 'update') {
            const idx = this.chapters.findIndex(c => c.id === data.id)
            if (idx >= 0) this.chapters[idx] = { ...this.chapters[idx], ...data }
          }
          break
        case 'world_settings':
          if (action === 'create') this.settings.push(data as WorldSetting)
          else if (action === 'update') {
            const idx = this.settings.findIndex(s => s.id === data.id)
            if (idx >= 0) this.settings[idx] = { ...this.settings[idx], ...data }
          }
          break
        case 'character_relationships':
          if (action === 'create') this.relationships.push(data as Relationship)
          else if (action === 'update') {
            const idx = this.relationships.findIndex(r => r.id === data.id)
            if (idx >= 0) this.relationships[idx] = { ...this.relationships[idx], ...data }
          }
          break
        case 'foreshadowings':
          if (action === 'create') this.foreshadowings.push(data as Foreshadowing)
          else if (action === 'update') {
            const idx = this.foreshadowings.findIndex(f => f.id === data.id)
            if (idx >= 0) this.foreshadowings[idx] = { ...this.foreshadowings[idx], ...data }
          }
          break
        case 'candidates':
          if (action === 'create') {
            if (Array.isArray(data)) {
              this.candidates.push(...(data as Candidate[]))
            } else {
              this.candidates.push(data as Candidate)
            }
          } else if (action === 'confirm' || action === 'discard') {
            this.candidates = this.candidates.filter(c => c.id !== data.id)
          }
          break
      }
    },

    clearChat() {
      this.chatMessages = []
    }
  },

  getters: {
    charactersMap: (state) => {
      const map = new Map<number, Character>()
      state.characters.forEach(c => map.set(c.id, c))
      return map
    },
    outlineTree: (state) => {
      return state.outline.filter(n => !n.parent_id)
        .sort((a, b) => a.sort_order - b.sort_order)
    },
    childrenOf: (state) => (parentId: number) => {
      return state.outline.filter(n => n.parent_id === parentId)
        .sort((a, b) => a.sort_order - b.sort_order)
    },
    pendingCandidates: (state) => state.candidates.filter(c => c.status === 'pending'),
    hasStreaming: (state) => state.isStreaming
  }
})
