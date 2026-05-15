<template>
  <div class="todo-list">
    <div class="filter-bar">
      <button
        v-for="opt in filterOptions"
        :key="opt.value"
        :class="{ active: currentFilter === opt.value }"
        @click="$emit('filter', opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>

    <div v-if="todos.length === 0" class="empty">
      暂无待办事项
    </div>

    <TodoItem
      v-for="todo in todos"
      :key="todo.id"
      :todo="todo"
      @toggle="$emit('toggle', todo.id)"
      @edit="$emit('edit', todo)"
      @delete="$emit('delete', todo.id)"
    />
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import TodoItem from './TodoItem.vue'

defineProps({
  todos: { type: Array, default: () => [] },
  currentFilter: { type: String, default: 'all' }
})

defineEmits(['filter', 'toggle', 'edit', 'delete'])

const filterOptions = [
  { label: '全部', value: 'all' },
  { label: '待办', value: 'pending' },
  { label: '已完成', value: 'completed' }
]
</script>

<style scoped>
.todo-list {
  margin-top: 20px;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.filter-bar button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-bar button:hover {
  border-color: #42b983;
}

.filter-bar button.active {
  background: #42b983;
  color: white;
  border-color: #42b983;
}

.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>
