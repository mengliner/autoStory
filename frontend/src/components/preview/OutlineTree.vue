<script lang="ts">
import { computed, ref, defineComponent, h } from 'vue'
import { useStoryStore } from '@/stores/story'
import type { OutlineNode } from '@/types'

export default defineComponent({
  name: 'OutlineTree',
  setup() {
    const store = useStoryStore()

    const rootNodes = computed(() =>
      store.outline.filter(n => !n.parent_id).sort((a, b) => a.sort_order - b.sort_order)
    )

    function getChildren(parentId: number) {
      return store.outline.filter(n => n.parent_id === parentId).sort((a, b) => a.sort_order - b.sort_order)
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const TreeNode: any = defineComponent({
      name: 'TreeNode',
      props: { node: Object as () => OutlineNode, depth: Number },
      setup(props: { node: OutlineNode; depth: number }) {
        const expanded = ref(true)
        const children = computed(() => getChildren(props.node.id))
        const indent = computed(() => `${props.depth * 20}px`)
        const levelIcon = computed(() => {
          switch (props.node.level) {
            case 'volume': return '📘'
            case 'chapter': return '📄'
            case 'section': return '§'
            default: return '•'
          }
        })
        const statusBadge = computed(() => {
          const map: Record<string, string> = {
            outline: '🗒',
            draft: '📝',
            writing: '✍️',
            done: '✅'
          }
          return map[props.node.status] || ''
        })

        return () => h('div', { class: 'tree-node' }, [
          h('div', {
            class: 'node-row',
            style: { paddingLeft: indent.value },
            onClick: () => { expanded.value = !expanded.value }
          }, [
            children.value.length ? h('span', { class: 'toggle' }, expanded.value ? '▾' : '▸') : h('span', { class: 'toggle-placeholder' }),
            h('span', { class: 'node-icon' }, levelIcon.value),
            h('span', { class: 'node-title' }, props.node.title),
            h('span', { class: 'node-status' }, statusBadge.value),
            h('span', { class: 'node-level' }, props.node.level)
          ]),
          props.node.summary && expanded.value ? h('div', { class: 'node-summary', style: { paddingLeft: `calc(${indent.value} + 24px)` } }, props.node.summary.slice(0, 120)) : null,
          expanded.value && children.value.map((child: OutlineNode) =>
            h(TreeNode, { node: child, depth: (props.depth ?? 0) + 1, key: child.id })
          )
        ])
      }
    })

    return () => h('div', { class: 'outline-tree' },
      rootNodes.value.map(node => h(TreeNode, { node, depth: 0, key: node.id }))
    )
  }
})
</script>

<style>
.tree-node { margin-bottom: 2px; }
.node-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background .15s;
}
.node-row:hover { background: rgba(124, 58, 237, .08); }
.toggle { width: 16px; font-size: 12px; color: #888; flex-shrink: 0; }
.toggle-placeholder { width: 16px; flex-shrink: 0; }
.node-icon { flex-shrink: 0; }
.node-title { color: #e0e0e0; }
.node-status { margin-left: auto; font-size: 12px; }
.node-level { font-size: 11px; color: #666; background: #0f0f23; padding: 1px 6px; border-radius: 3px; }
.node-summary { font-size: 13px; color: #888; padding: 2px 0 6px; }
</style>
