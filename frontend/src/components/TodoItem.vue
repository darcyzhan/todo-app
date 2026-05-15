<template>
  <div class="todo-item" :class="{ completed: todo.completed }">
    <div class="todo-content">
      <input
        type="checkbox"
        :checked="todo.completed"
        @change="$emit('toggle')"
      />
      <div class="todo-text">
        <span class="title">{{ todo.title }}</span>
        <span v-if="todo.description" class="description">{{ todo.description }}</span>
      </div>
    </div>
    <div class="todo-actions">
      <button @click="$emit('edit')" class="edit-btn">编辑</button>
      <button @click="$emit('delete')" class="delete-btn">删除</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  todo: { type: Object, required: true }
})

defineEmits(['toggle', 'edit', 'delete'])
</script>

<style scoped>
.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s;
}

.todo-item:hover {
  background: #f0f0f0;
}

.todo-item.completed {
  opacity: 0.6;
}

.todo-item.completed .title {
  text-decoration: line-through;
}

.todo-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  margin-top: 2px;
}

.todo-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title {
  font-weight: 500;
  color: #333;
}

.description {
  font-size: 12px;
  color: #666;
}

.todo-actions {
  display: flex;
  gap: 8px;
}

.edit-btn, .delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.edit-btn {
  background: #e6f7ff;
  color: #1890ff;
}

.delete-btn {
  background: #fff1f0;
  color: #ff4d4f;
}
</style>
