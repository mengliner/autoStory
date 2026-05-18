export interface Project {
  id: number
  title: string
  synopsis: string | null
  status: 'planning' | 'writing' | 'done'
  created_at: string
  updated_at: string
}

export interface Character {
  id: number
  project_id: number
  name: string
  role: string | null
  personality: string | null
  background: string | null
  attributes: Record<string, any> | null
}

export interface Relationship {
  id: number
  project_id: number
  char_a_id: number
  char_b_id: number
  relation_type: string | null
  description: string | null
}

export interface OutlineNode {
  id: number
  project_id: number
  parent_id: number | null
  title: string
  summary: string | null
  level: 'volume' | 'chapter' | 'section'
  sort_order: number
  status: 'outline' | 'draft' | 'writing' | 'done'
}

export interface Chapter {
  id: number
  project_id: number
  outline_node_id: number | null
  title: string
  content: string | null
  status: 'draft' | 'review' | 'done'
  version: number
}

export interface WorldSetting {
  id: number
  project_id: number
  category: string | null
  title: string
  description: string | null
}

export interface Foreshadowing {
  id: number
  project_id: number
  title: string
  description: string | null
  planted_chapter_id: number | null
  resolved_chapter_id: number | null
  resolved_note: string | null
  status: 'planted' | 'resolved'
}

export interface Candidate {
  id: number
  project_id: number
  session_id: string | null
  version_label: string | null
  content_type: 'outline' | 'chapter' | 'character' | 'setting' | 'foreshadowing'
  payload: any
  status: 'pending' | 'confirmed' | 'discarded'
}

export interface ProjectFullState {
  project: Project
  characters: Character[]
  relationships: Relationship[]
  outline: OutlineNode[]
  chapters: Chapter[]
  settings: WorldSetting[]
  foreshadowings: Foreshadowing[]
  candidates: Candidate[]
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  candidates?: Candidate[]
  isError?: boolean
}

export interface StatePatch {
  table: string
  action: string
  data: any
}

export interface SSETextEvent {
  delta: string
}

export interface SSEToolCallEvent {
  tool: string
  status: string
  input: Record<string, any>
  result: {
    success: boolean
    data: any
    table: string
    action: string
    message?: string
  }
}
