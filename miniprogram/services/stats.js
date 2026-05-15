import http from './request'

export function getDashboard() {
  return http.get('/stats/dashboard')
}

export function getNotifications(page = 1) {
  return http.get('/notifications', { page, page_size: 20 })
}

export function getUnreadCount() {
  return http.get('/notifications/unread-count')
}

export function markNotificationRead(notificationId) {
  return http.put(`/notifications/${notificationId}/read`)
}

export function markAllNotificationsRead() {
  return http.put('/notifications/read-all')
}
