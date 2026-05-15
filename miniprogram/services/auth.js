import http from './request'

export function login(code, nickname, avatarUrl) {
  return http.post('/auth/wechat-login', { code, nickname, avatar_url: avatarUrl })
}

export function register(nickname, password) {
  return http.post(`/auth/register?nickname=${encodeURIComponent(nickname)}&password=${encodeURIComponent(password)}`)
}

export function loginWithPassword(nickname, password) {
  return http.post(`/auth/login?nickname=${encodeURIComponent(nickname)}&password=${encodeURIComponent(password)}`)
}

export function refreshToken(refreshToken) {
  return http.post('/auth/refresh', { refresh_token: refreshToken })
}
