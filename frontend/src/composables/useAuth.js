import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1/auth'

const token = ref(localStorage.getItem('access_token') || '')
const refreshToken = ref(localStorage.getItem('refresh_token') || '')
const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  async function register(nickname, password) {
    const { data } = await axios.post(API_BASE + '/register', null, {
      params: { nickname, password }
    })
    setAuth(data)
    return data
  }

  async function login(nickname, password) {
    const { data } = await axios.post(API_BASE + '/login', null, {
      params: { nickname, password }
    })
    setAuth(data)
    return data
  }

  function setAuth(data) {
    token.value = data.access_token
    refreshToken.value = data.refresh_token
    user.value = data.user
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  function getAuthHeader() {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  return {
    token,
    user,
    isAuthenticated,
    register,
    login,
    logout,
    getAuthHeader
  }
}
