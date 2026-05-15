import http from './request'

export function createTag(data) {
  return http.post('/tags', data)
}

export function listTags() {
  return http.get('/tags')
}

export function updateTag(tagId, data) {
  return http.put(`/tags/${tagId}`, data)
}

export function deleteTag(tagId) {
  return http.delete(`/tags/${tagId}`)
}
