import type { ProjectFullState, Project } from '@/types'

const BASE = '/api'

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${BASE}/projects`)
  if (!res.ok) throw new Error('Failed to fetch projects')
  return res.json()
}

export async function createProject(title: string, synopsis?: string): Promise<Project> {
  const res = await fetch(`${BASE}/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, synopsis })
  })
  if (!res.ok) throw new Error('Failed to create project')
  return res.json()
}

export async function fetchProjectFullState(id: number): Promise<ProjectFullState> {
  const res = await fetch(`${BASE}/projects/${id}`)
  if (!res.ok) throw new Error('Failed to fetch project')
  return res.json()
}

export async function deleteProject(id: number): Promise<void> {
  const res = await fetch(`${BASE}/projects/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('Failed to delete project')
}

export function chatSSE(
  projectId: number,
  message: string,
  onText: (delta: string) => void,
  onToolCall: (data: any) => void,
  onStatePatch: (data: any) => void,
  onError: (message: string) => void,
  onDone: () => void
): AbortController {
  const controller = new AbortController()

  fetch(`${BASE}/chat/${projectId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
    signal: controller.signal
  }).then(async (response) => {
    if (!response.ok) {
      onError(`HTTP ${response.status}`)
      return
    }
    const reader = response.body?.getReader()
    if (!reader) {
      onError('No response body')
      return
    }
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      let eventType = ''
      for (const line of lines) {
        if (line.startsWith('event: ')) {
          eventType = line.slice(7).trim()
        } else if (line.startsWith('data: ')) {
          const dataStr = line.slice(6)
          try {
            const data = JSON.parse(dataStr)
            if (eventType === 'text') {
              onText(data.delta)
            } else if (eventType === 'tool_call') {
              onToolCall(data)
            } else if (eventType === 'state_patch') {
              onStatePatch(data)
            } else if (eventType === 'error') {
              onError(data.message || 'Unknown error')
            } else if (eventType === 'done') {
              onDone()
            }
          } catch {
            // skip parse errors for partial chunks
          }
        }
      }
    }
    onDone()
  }).catch((err) => {
    if (err.name !== 'AbortError') {
      onError(err.message || 'Connection failed')
    }
  })

  return controller
}
