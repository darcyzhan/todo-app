import { ref } from 'vue'
import { todoApi } from '../api/todo'

export function useTasks() {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)
  const total = ref(0)

  async function fetchTasks(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await todoApi.getAll(params)
      tasks.value = result.items || []
      total.value = result.total || 0
    } catch (e) {
      error.value = e.message
      console.error('获取任务失败:', e)
    } finally {
      loading.value = false
    }
  }

  async function createTask(data) {
    try {
      await todoApi.create(data)
      await fetchTasks()
    } catch (e) {
      console.error('创建任务失败:', e)
      throw e
    }
  }

  async function updateTask(id, data) {
    try {
      await todoApi.update(id, data)
      await fetchTasks()
    } catch (e) {
      console.error('更新任务失败:', e)
      throw e
    }
  }

  async function deleteTask(id) {
    try {
      await todoApi.delete(id)
      await fetchTasks()
    } catch (e) {
      console.error('删除任务失败:', e)
      throw e
    }
  }

  async function updateStatus(id, status) {
    try {
      await todoApi.updateStatus(id, status)
      await fetchTasks()
    } catch (e) {
      console.error('更新状态失败:', e)
      throw e
    }
  }

  function getTasksByDate(date) {
    if (!date) return []
    const dateStr = typeof date === 'string' ? date : formatDate(date)
    return tasks.value.filter(t => {
      if (!t.due_date) return false
      return t.due_date.startsWith(dateStr)
    })
  }

  function formatDate(d) {
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}-${m}-${day}`
  }

  return {
    tasks,
    loading,
    error,
    total,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    updateStatus,
    getTasksByDate
  }
}
