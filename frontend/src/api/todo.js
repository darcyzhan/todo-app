import axios from 'axios'
import { useAuth } from '../composables/useAuth'

const API_BASE = 'http://localhost:51200/api/v1/tasks'

function authHeaders() {
  const { getAuthHeader } = useAuth()
  return getAuthHeader()
}

export const todoApi = {
  async getAll(params = {}) {
    const { data } = await axios.get(API_BASE, { params, headers: authHeaders() })
    return data
  },

  async getById(id) {
    const { data } = await axios.get(`${API_BASE}/${id}`, { headers: authHeaders() })
    return data
  },

  async create(todo) {
    const { data } = await axios.post(API_BASE, todo, { headers: authHeaders() })
    return data
  },

  async update(id, todo) {
    const { data } = await axios.put(`${API_BASE}/${id}`, todo, { headers: authHeaders() })
    return data
  },

  async delete(id) {
    await axios.delete(`${API_BASE}/${id}`, { headers: authHeaders() })
  },

  async updateStatus(id, status) {
    const { data } = await axios.put(`${API_BASE}/${id}/status`, { status }, { headers: authHeaders() })
    return data
  }
}
