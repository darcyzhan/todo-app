import { computed } from 'vue'

export function useStats(tasks) {
  const priorityStats = computed(() => {
    const stats = { P0: 0, P1: 0, P2: 0, P3: 0 }
    if (!tasks || !tasks.value) return stats
    for (const t of tasks.value) {
      if (stats[t.priority] !== undefined) {
        stats[t.priority]++
      }
    }
    return stats
  })

  const statusStats = computed(() => {
    const stats = { todo: 0, in_progress: 0, done: 0, archived: 0 }
    if (!tasks || !tasks.value) return stats
    for (const t of tasks.value) {
      if (stats[t.status] !== undefined) {
        stats[t.status]++
      }
    }
    return stats
  })

  const totalTasks = computed(() => {
    if (!tasks || !tasks.value) return 0
    return tasks.value.length
  })

  const completedRate = computed(() => {
    const total = totalTasks.value
    if (total === 0) return 0
    return Math.round((statusStats.value.done / total) * 100)
  })

  const maxPriority = computed(() => {
    const vals = Object.values(priorityStats.value)
    return Math.max(...vals, 1)
  })

  return {
    priorityStats,
    statusStats,
    totalTasks,
    completedRate,
    maxPriority
  }
}
