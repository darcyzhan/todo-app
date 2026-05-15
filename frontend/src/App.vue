<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useTasks } from './composables/useTasks'
import { useStats } from './composables/useStats'
import { useAuth } from './composables/useAuth'
import { Icon } from '@iconify/vue'

import CalendarView from './components/CalendarView.vue'
import TaskCard from './components/TaskCard.vue'
import StatsPanel from './components/StatsPanel.vue'
import QuickAdd from './components/QuickAdd.vue'
import TodoForm from './components/TodoForm.vue'

const { tasks, loading, fetchTasks, createTask, updateTask, deleteTask, updateStatus } = useTasks()
const { priorityStats, statusStats, totalTasks, completedRate, maxPriority } = useStats(tasks)
const { isAuthenticated, user, login, register, logout } = useAuth()

const filter = ref('all')
const selectedDate = ref(null)
const showForm = ref(false)
const editingTodo = ref(null)

// Auth form
const authMode = ref('login')
const authNickname = ref('')
const authPassword = ref('')
const authError = ref('')
const authLoading = ref(false)

const filterOptions = [
  { value: 'all', label: '全部', icon: 'mdi:view-grid' },
  { value: 'todo', label: '待办', icon: 'mdi:checkbox-blank-outline' },
  { value: 'in_progress', label: '进行中', icon: 'mdi:progress-clock' },
  { value: 'done', label: '已完成', icon: 'mdi:checkbox-marked-circle' }
]

const filteredTasks = computed(() => {
  let list = tasks.value
  if (filter.value !== 'all') {
    list = list.filter(t => t.status === filter.value)
  }
  if (selectedDate.value) {
    const dateStr = formatDate(selectedDate.value)
    list = list.filter(t => t.due_date && t.due_date.startsWith(dateStr))
  }
  return list
})

function formatDate(d) {
  if (!d) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

async function handleAuth() {
  authError.value = ''
  authLoading.value = true
  try {
    if (authMode.value === 'register') {
      await register(authNickname.value, authPassword.value)
    } else {
      await login(authNickname.value, authPassword.value)
    }
  } catch (e) {
    const msg = e.response?.data?.detail || e.response?.data?.message || e.message || '操作失败'
    authError.value = msg
  } finally {
    authLoading.value = false
  }
}

function handleLogout() {
  logout()
}

async function handleQuickAdd(data) {
  await createTask(data)
}

async function handleFormSubmit(form) {
  if (editingTodo.value) {
    await updateTask(editingTodo.value.id, form)
    editingTodo.value = null
  } else {
    await createTask(form)
  }
  showForm.value = false
}

function handleEdit(todo) {
  editingTodo.value = todo
  showForm.value = true
}

function handleCancelEdit() {
  editingTodo.value = null
  showForm.value = false
}

async function handleDelete(id) {
  if (!confirm('确定要删除该任务吗？')) return
  await deleteTask(id)
}

async function handleDropTask(taskId, dateStr) {
  await updateTask(taskId, { due_date: dateStr })
}

function handleSelectDate(date) {
  if (selectedDate.value && formatDate(selectedDate.value) === formatDate(date)) {
    selectedDate.value = null
  } else {
    selectedDate.value = date
  }
}

function openNewForm() {
  editingTodo.value = null
  showForm.value = true
}

watch(isAuthenticated, (val) => {
  if (val) {
    fetchTasks({ page_size: 100 })
  }
}, { immediate: true })

onMounted(() => {
  if (isAuthenticated.value) {
    fetchTasks({ page_size: 100 })
  }
})
</script>

<template>
  <!-- Login / Register Page -->
  <div v-if="!isAuthenticated" class="auth-page">
    <div class="auth-card">
      <div class="auth-brand">
        <Icon icon="mdi:checkbox-marked-circle-outline" width="40" />
        <h1>TaskFlow</h1>
        <p>智能任务管理</p>
      </div>

      <div class="auth-tabs">
        <button :class="{ active: authMode === 'login' }" @click="authMode = 'login'; authError = ''">登录</button>
        <button :class="{ active: authMode === 'register' }" @click="authMode = 'register'; authError = ''">注册</button>
      </div>

      <form class="auth-form" @submit.prevent="handleAuth">
        <div class="auth-field">
          <label>用户名</label>
          <input v-model="authNickname" type="text" placeholder="输入用户名" required />
        </div>
        <div class="auth-field">
          <label>密码</label>
          <input v-model="authPassword" type="password" placeholder="输入密码" required minlength="4" />
        </div>
        <div v-if="authError" class="auth-error">
          <Icon icon="mdi:alert-circle" width="16" />
          {{ authError }}
        </div>
        <button type="submit" class="auth-submit" :disabled="authLoading">
          <Icon v-if="authLoading" icon="mdi:loading" width="18" class="spin" />
          {{ authMode === 'login' ? '登录' : '注册' }}
        </button>
      </form>
    </div>
  </div>

  <!-- Main App -->
  <div v-else class="app-container">
    <!-- Top Navigation Bar -->
    <header class="top-nav">
      <div class="nav-left">
        <div class="brand">
          <Icon icon="mdi:checkbox-marked-circle-outline" width="24" />
          <span class="brand-text">TaskFlow</span>
        </div>
        <div class="filter-tabs">
          <button
            v-for="opt in filterOptions"
            :key="opt.value"
            :class="{ active: filter === opt.value }"
            @click="filter = opt.value"
          >
            <Icon :icon="opt.icon" width="16" />
            {{ opt.label }}
          </button>
        </div>
      </div>
      <div class="nav-right">
        <div v-if="selectedDate" class="date-badge">
          <Icon icon="mdi:calendar-check" width="14" />
          {{ formatDate(selectedDate) }}
          <button class="clear-date" @click="selectedDate = null">
            <Icon icon="mdi:close-circle" width="14" />
          </button>
        </div>
        <div class="user-badge" v-if="user">
          <Icon icon="mdi:account-circle" width="18" />
          {{ user.nickname }}
        </div>
        <button class="nav-add-btn" @click="openNewForm">
          <Icon icon="mdi:plus" width="18" />
          新建
        </button>
        <button class="nav-logout" @click="handleLogout" title="退出登录">
          <Icon icon="mdi:logout" width="18" />
        </button>
      </div>
    </header>

    <!-- Content Area -->
    <div class="content-area">
      <!-- Upper: Task Cards Section -->
      <section class="tasks-section">
        <div class="section-header">
          <h2>
            <Icon icon="mdi:format-list-checks" width="22" />
            {{ filterOptions.find(o => o.value === filter)?.label || '全部' }}任务
            <span class="task-count">{{ filteredTasks.length }}</span>
          </h2>
        </div>

        <QuickAdd @submit="handleQuickAdd" />

        <div class="tasks-body">
          <div v-if="loading" class="loading">
            <Icon icon="mdi:loading" width="28" class="spin" />
            <span>加载中...</span>
          </div>
          <div v-else-if="filteredTasks.length === 0" class="empty">
            <Icon icon="mdi:checkbox-blank-off-outline" width="52" />
            <p>暂无任务</p>
          </div>
          <div v-else class="task-grid">
            <TaskCard
              v-for="todo in filteredTasks"
              :key="todo.id"
              :todo="todo"
              @toggle="updateStatus(todo.id, $event)"
              @edit="handleEdit(todo)"
              @delete="handleDelete(todo.id)"
            />
          </div>
        </div>
      </section>

      <!-- Lower: Calendar + Stats Section -->
      <section class="calendar-section">
        <div class="calendar-stats-row">
          <CalendarView
            :tasks="tasks"
            :selected-date="selectedDate"
            @drop-task="handleDropTask"
            @select-date="handleSelectDate"
          />
          <StatsPanel
            :priority-stats="priorityStats"
            :status-stats="statusStats"
            :total-tasks="totalTasks"
            :completed-rate="completedRate"
            :max-priority="maxPriority"
          />
        </div>
      </section>
    </div>

    <!-- Edit/Create Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="modal-overlay" @click.self="handleCancelEdit">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ editingTodo ? '编辑任务' : '新建任务' }}</h3>
            <button class="modal-close" @click="handleCancelEdit">
              <Icon icon="mdi:close" width="20" />
            </button>
          </div>
          <TodoForm
            :todo="editingTodo"
            @submit="handleFormSubmit"
            @cancel="handleCancelEdit"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
/* Auth Page */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  padding: 20px;
}

.auth-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 40px;
  width: 400px;
  max-width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.auth-brand {
  text-align: center;
  margin-bottom: 28px;
  color: var(--primary);
}

.auth-brand h1 {
  font-size: 26px;
  font-weight: 700;
  margin: 8px 0 4px;
  color: var(--text-primary);
}

.auth-brand p {
  font-size: 13px;
  color: var(--text-muted);
}

.auth-tabs {
  display: flex;
  border-radius: 10px;
  background: var(--bg-hover);
  padding: 3px;
  margin-bottom: 20px;
}

.auth-tabs button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 8px;
  background: transparent;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.auth-tabs button.active {
  background: var(--bg-card);
  color: var(--primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.auth-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.auth-field input {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-main);
  transition: border-color 0.2s;
}

.auth-field input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.auth-error {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e;
  border-radius: 8px;
  font-size: 13px;
}

.auth-submit {
  padding: 10px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.15s;
  margin-top: 4px;
}

.auth-submit:hover:not(:disabled) {
  background: var(--primary-dark);
}

.auth-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Main App Container */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-main);
}

/* Top Navigation Bar */
.top-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 32px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 28px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--primary);
  font-size: 18px;
  font-weight: 700;
}

.brand-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.filter-tabs {
  display: flex;
  gap: 4px;
  background: var(--bg-hover);
  padding: 3px;
  border-radius: 10px;
}

.filter-tabs button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tabs button:hover {
  color: var(--text-primary);
}

.filter-tabs button.active {
  background: var(--bg-card);
  color: var(--primary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  font-size: 12px;
  color: var(--primary);
}

.clear-date {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--primary);
  display: flex;
  padding: 0;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: var(--text-secondary);
}

.nav-add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 16px;
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.nav-add-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

.nav-logout {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 6px;
  border-radius: 8px;
  display: flex;
  transition: all 0.15s;
}

.nav-logout:hover {
  background: rgba(229, 62, 62, 0.08);
  color: #e53e3e;
}

/* Content Area */
.content-area {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Tasks Section (Upper) */
.tasks-section {
  flex-shrink: 0;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 14px;
}

.task-count {
  background: var(--bg-hover);
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 12px;
}

.tasks-body {
  min-height: 120px;
}

.loading, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px 0;
  color: var(--text-muted);
  font-size: 14px;
}

/* Task Grid - small cards */
.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 10px;
}

/* Calendar Section (Lower) */
.calendar-section {
  flex: 1;
  min-height: 0;
}

.calendar-stats-row {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 16px;
  align-items: start;
}

/* Spin animation */
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: var(--bg-card);
  border-radius: 16px;
  width: 480px;
  max-width: 90vw;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 4px;
  border-radius: 6px;
  display: flex;
  transition: all 0.15s;
}

.modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

/* Responsive */
@media (max-width: 900px) {
  .top-nav {
    padding: 10px 16px;
    flex-wrap: wrap;
    gap: 8px;
  }
  .nav-left { gap: 12px; }
  .filter-tabs { gap: 2px; }
  .filter-tabs button { padding: 5px 10px; font-size: 12px; }
  .content-area { padding: 16px; }
  .task-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
  .calendar-stats-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .brand-text { display: none; }
  .filter-tabs button span { display: none; }
  .user-badge span { display: none; }
  .nav-add-btn span { display: none; }
  .task-grid {
    grid-template-columns: 1fr;
  }
}
</style>
