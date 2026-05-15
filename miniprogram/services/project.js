import http from './request'

export function createProject(data) {
  return http.post('/projects', data)
}

export function getProject(projectId) {
  return http.get(`/projects/${projectId}`)
}

export function listProjects() {
  return http.get('/projects')
}

export function updateProject(projectId, data) {
  return http.put(`/projects/${projectId}`, data)
}

export function deleteProject(projectId) {
  return http.delete(`/projects/${projectId}`)
}

export function getProjectStats(projectId) {
  return http.get(`/projects/${projectId}/stats`)
}
