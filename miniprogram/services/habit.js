import http from './request'

export function createHabit(data) {
  return http.post('/habits', data)
}

export function listHabits() {
  return http.get('/habits')
}

export function getHabit(habitId) {
  return http.get(`/habits/${habitId}`)
}

export function updateHabit(habitId, data) {
  return http.put(`/habits/${habitId}`, data)
}

export function deleteHabit(habitId) {
  return http.delete(`/habits/${habitId}`)
}

export function logHabit(habitId, loggedDate) {
  return http.post(`/habits/${habitId}/log`, null, { params: { logged_date: loggedDate } })
}

export function unlogHabit(habitId, loggedDate) {
  return http.delete(`/habits/${habitId}/log/${loggedDate}`)
}
