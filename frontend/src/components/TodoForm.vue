<template>
  <form @submit.prevent="handleSubmit" class="todo-form">
    <div class="form-group">
      <label>标题</label>
      <input
        v-model="form.title"
        type="text"
        placeholder="任务标题"
        required
        maxlength="256"
      />
    </div>

    <div class="form-group">
      <label>描述</label>
      <textarea
        v-model="form.description"
        placeholder="任务描述（可选）"
        maxlength="500"
        rows="3"
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>优先级</label>
        <select v-model="form.priority">
          <option value="P0">P0 紧急</option>
          <option value="P1">P1 高</option>
          <option value="P2">P2 中</option>
          <option value="P3">P3 低</option>
        </select>
      </div>

      <div class="form-group">
        <label>状态</label>
        <select v-model="form.status">
          <option value="todo">待办</option>
          <option value="in_progress">进行中</option>
          <option value="done">已完成</option>
          <option value="archived">归档</option>
        </select>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>开始日期</label>
        <input v-model="form.start_date" type="date" />
      </div>
      <div class="form-group">
        <label>截止日期</label>
        <input v-model="form.due_date" type="date" />
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" class="btn-primary">{{ isEdit ? '更新' : '创建' }}</button>
      <button type="button" class="btn-cancel" @click="$emit('cancel')">取消</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  todo: { type: Object, default: null }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref({
  title: '',
  description: '',
  priority: 'P2',
  status: 'todo',
  start_date: '',
  due_date: ''
})
const isEdit = ref(false)

watch(() => props.todo, (newTodo) => {
  if (newTodo) {
    form.value = {
      title: newTodo.title || '',
      description: newTodo.description || '',
      priority: newTodo.priority || 'P2',
      status: newTodo.status || 'todo',
      start_date: newTodo.start_date ? newTodo.start_date.slice(0, 10) : '',
      due_date: newTodo.due_date ? newTodo.due_date.slice(0, 10) : ''
    }
    isEdit.value = true
  } else {
    form.value = {
      title: '',
      description: '',
      priority: 'P2',
      status: 'todo',
      start_date: '',
      due_date: ''
    }
    isEdit.value = false
  }
}, { immediate: true })

function handleSubmit() {
  if (!form.value.title.trim()) return
  const data = { ...form.value }
  if (!data.start_date) data.start_date = null
  if (!data.due_date) data.due_date = null
  emit('submit', data)
}
</script>

<style scoped>
.todo-form {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.form-group label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 8px 12px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  font-size: 13.5px;
  color: var(--text-primary);
  background: var(--bg-main);
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 60px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: 8px;
}

.btn-primary {
  padding: 8px 24px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

.btn-cancel {
  padding: 8px 24px;
  background: var(--bg-hover);
  color: var(--text-secondary);
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-cancel:hover {
  background: var(--border);
}
</style>
