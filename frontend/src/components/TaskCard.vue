<script setup>
import { Icon } from '@iconify/vue'
import PriorityBadge from './PriorityBadge.vue'
import { useDragDrop } from '../composables/useDragDrop'

const props = defineProps({
  todo: { type: Object, required: true }
})

const emit = defineEmits(['toggle', 'edit', 'delete'])
const { onDragStart, onDragEnd } = useDragDrop()

const statusIcons = {
  todo: 'mdi:checkbox-blank-outline',
  in_progress: 'mdi:progress-clock',
  done: 'mdi:checkbox-marked-circle',
  archived: 'mdi:archive'
}

const statusLabels = {
  todo: '待办',
  in_progress: '进行中',
  done: '已完成',
  archived: '归档'
}

function toggleStatus() {
  const statusFlow = { todo: 'in_progress', in_progress: 'done', done: 'todo' }
  emit('toggle', statusFlow[props.todo.status] || 'todo')
}
</script>

<template>
  <div
    class="task-card"
    :class="[`priority-${todo.priority}`, `status-${todo.status}`]"
    draggable="true"
    @dragstart="onDragStart($event, todo.id)"
    @dragend="onDragEnd"
  >
    <div class="card-top">
      <div class="card-left">
        <button class="status-btn" @click="toggleStatus" :title="statusLabels[todo.status]">
          <Icon :icon="statusIcons[todo.status] || 'mdi:checkbox-blank-outline'" width="20" />
        </button>
        <span class="task-title" :class="{ 'done': todo.status === 'done' }">
          {{ todo.title }}
        </span>
      </div>
      <PriorityBadge :priority="todo.priority" />
    </div>

    <div class="card-bottom">
      <div class="card-meta">
        <span v-if="todo.due_date" class="due-date">
          <Icon icon="mdi:calendar-clock" width="12" />
          {{ todo.due_date.slice(0, 10) }}
        </span>
        <span class="status-label" :class="todo.status">
          {{ statusLabels[todo.status] }}
        </span>
      </div>
      <div class="card-actions">
        <button class="icon-btn" @click="$emit('edit')" title="编辑">
          <Icon icon="mdi:pencil-outline" width="14" />
        </button>
        <button class="icon-btn delete-btn" @click="$emit('delete')" title="删除">
          <Icon icon="mdi:delete-outline" width="14" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-card {
  background: var(--bg-card);
  border-radius: 12px;
  border-left: 3px solid transparent;
  padding: 12px 14px;
  cursor: grab;
  transition: all 0.2s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-card:hover {
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.12);
  transform: translateY(-2px);
}

.task-card.dragging {
  opacity: 0.5;
  transform: rotate(2deg);
}

.task-card.priority-P0 { border-left-color: #e53e3e; }
.task-card.priority-P1 { border-left-color: #ed8936; }
.task-card.priority-P2 { border-left-color: #667eea; }
.task-card.priority-P3 { border-left-color: #a0aec0; }

.task-card.status-done {
  opacity: 0.55;
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.card-left {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.status-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  color: var(--primary);
  flex-shrink: 0;
  display: flex;
  margin-top: 1px;
  transition: transform 0.15s;
}

.status-btn:hover {
  transform: scale(1.15);
}

.task-title {
  font-size: 13.5px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
  word-break: break-word;
}

.task-title.done {
  text-decoration: line-through;
  color: var(--text-muted);
}

.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.due-date {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: var(--text-muted);
}

.status-label {
  font-size: 10px;
  font-weight: 500;
  padding: 1px 6px;
  border-radius: 4px;
}

.status-label.todo {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.status-label.in_progress {
  background: rgba(237, 137, 54, 0.1);
  color: #ed8936;
}

.status-label.done {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.status-label.archived {
  background: rgba(160, 174, 192, 0.1);
  color: #a0aec0;
}

.card-actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.2s;
}

.task-card:hover .card-actions {
  opacity: 1;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 3px;
  border-radius: 5px;
  color: var(--text-muted);
  display: flex;
  transition: all 0.15s;
}

.icon-btn:hover {
  background: var(--bg-hover);
  color: var(--primary);
}

.delete-btn:hover {
  color: #e53e3e;
  background: rgba(229, 62, 62, 0.08);
}
</style>
