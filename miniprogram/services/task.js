import http from './request'

export function createTask(data) {
  return http.post('/tasks', data)
}

export function getTask(taskId) {
  return http.get(`/tasks/${taskId}`)
}

export function listTasks(params) {
  return http.get('/tasks', params)
}

export function updateTask(taskId, data) {
  return http.put(`/tasks/${taskId}`, data)
}

export function updateTaskStatus(taskId, status) {
  return http.put(`/tasks/${taskId}/status`, { status })
}

export function deleteTask(taskId) {
  return http.delete(`/tasks/${taskId}`)
}

export function batchUpdateTasks(data) {
  return http.post('/tasks/batch', data)
}

export function createSubtask(taskId, data) {
  return http.post(`/tasks/${taskId}/subtasks`, data)
}

export function updateSubtask(subtaskId, data) {
  return http.put(`/tasks/subtasks/${subtaskId}`, data)
}

export function deleteSubtask(subtaskId) {
  return http.delete(`/tasks/subtasks/${subtaskId}`)
}
