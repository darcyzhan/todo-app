<script setup>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const emit = defineEmits(['submit'])

const form = ref({
  title: '',
  priority: 'P2',
  due_date: ''
})

const priorityOptions = [
  { value: 'P0', label: '紧急' },
  { value: 'P1', label: '高' },
  { value: 'P2', label: '中' },
  { value: 'P3', label: '低' }
]

function handleSubmit() {
  if (!form.value.title.trim()) return
  emit('submit', {
    title: form.value.title.trim(),
    priority: form.value.priority,
    due_date: form.value.due_date || null,
    status: 'todo'
  })
  form.value.title = ''
  form.value.priority = 'P2'
  form.value.due_date = ''
}
</script>

<template>
  <form class="quick-add" @submit.prevent="handleSubmit">
    <div class="add-row">
      <Icon icon="mdi:plus-circle" width="22" class="add-icon" />
      <input
        v-model="form.title"
        type="text"
        placeholder="快速添加任务..."
        class="add-input"
      />
      <input
        v-model="form.due_date"
        type="date"
        class="date-input"
        title="截止日期"
      />
      <select v-model="form.priority" class="priority-select" title="优先级">
        <option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <button type="submit" class="submit-btn" title="添加">
        <Icon icon="mdi:send" width="18" />
      </button>
    </div>
  </form>
</template>

<style scoped>
.quick-add {
  margin-bottom: 16px;
}

.add-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-card);
  border-radius: 12px;
  padding: 10px 14px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.add-row:focus-within {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.08);
}

.add-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.add-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 13.5px;
  background: transparent;
  color: var(--text-primary);
  min-width: 0;
}

.add-input::placeholder {
  color: var(--text-muted);
}

.date-input {
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-main);
  cursor: pointer;
  flex-shrink: 0;
}

.priority-select {
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-main);
  cursor: pointer;
  flex-shrink: 0;
}

.submit-btn {
  background: var(--primary);
  border: none;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: all 0.15s;
  flex-shrink: 0;
}

.submit-btn:hover {
  background: var(--primary-dark);
  transform: scale(1.05);
}
</style>
