import { listTasks, updateTaskStatus, deleteTask, batchUpdateTasks } from '../../services/task'
import { listTags } from '../../services/tag'
import { listProjects } from '../../services/project'
import { getDashboard } from '../../services/stats'
import { formatRelative, formatDueDate } from '../../utils/date'
import { priorityText, priorityColor, statusText, showToast, vibrateShort } from '../../utils/util'

const app = getApp()

Page({
  data: {
    // View
    viewMode: 'list', // list, kanban, calendar
    viewModes: ['list', 'kanban', 'calendar'],

    // Tasks
    tasks: [],
    filteredTasks: [],
    total: 0,
    page: 1,
    hasMore: false,
    loading: false,
    refreshing: false,

    // Filters
    currentFilter: 'all', // all, today, upcoming, overdue, done
    filters: [
      { key: 'all', label: '全部' },
      { key: 'today', label: '今天' },
      { key: 'upcoming', label: '即将到期' },
      { key: 'overdue', label: '逾期' },
      { key: 'done', label: '已完成' },
    ],
    selectedPriority: '',
    selectedProject: '',
    selectedTag: '',
    searchQuery: '',

    // Tags & Projects
    tags: [],
    projects: [],

    // Dashboard stats
    stats: {
      today_todo: 0,
      week_done: 0,
      overdue: 0,
      in_progress: 0,
      completion_rate: 0,
    },

    // Multi-select
    isMultiSelect: false,
    selectedTaskIds: new Set(),

    // UI
    showFilterPanel: false,
    showCreateModal: false,
  },

  onLoad() {
    this.initPage()
  },

  onShow() {
    this.refreshTasks()
  },

  onPullDownRefresh() {
    this.refreshTasks().then(() => wx.stopPullDownRefresh())
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMoreTasks()
    }
  },

  async initPage() {
    if (!app.isLoggedIn()) {
      this.setData({ showLoginPrompt: true })
      return
    }
    await Promise.all([
      this.loadTasks(),
      this.loadTags(),
      this.loadProjects(),
      this.loadStats(),
    ])
  },

  async refreshTasks() {
    this.setData({ page: 1, tasks: [] })
    await this.loadTasks()
    await this.loadStats()
  },

  async loadTasks() {
    if (this.data.loading) return
    this.setData({ loading: true })

    try {
      const params = { page: this.data.page, page_size: 20, sort: 'due_date', order: 'asc' }

      if (this.data.currentFilter === 'today') {
        const today = new Date().toISOString().split('T')[0]
        params.due_from = today
        params.due_to = today
        params.status = 'todo,in_progress'
      } else if (this.data.currentFilter === 'upcoming') {
        const today = new Date().toISOString().split('T')[0]
        params.due_from = today
        params.status = 'todo,in_progress'
      } else if (this.data.currentFilter === 'overdue') {
        params.status = 'todo,in_progress'
      } else if (this.data.currentFilter === 'done') {
        params.status = 'done'
      }

      if (this.data.selectedPriority) {
        params.priority = this.data.selectedPriority
      }
      if (this.data.selectedProject) {
        params.project_id = this.data.selectedProject
      }
      if (this.data.searchQuery) {
        params.q = this.data.searchQuery
      }

      const result = await listTasks(params)
      const tasks = result.items.map(this._formatTask)

      this.setData({
        tasks: this.data.page === 1 ? tasks : [...this.data.tasks, ...tasks],
        total: result.total,
        hasMore: result.has_more,
        loading: false,
      })
    } catch (err) {
      console.error('加载任务失败:', err)
      this.setData({ loading: false })
    }
  },

  async loadMoreTasks() {
    this.setData({ page: this.data.page + 1 })
    await this.loadTasks()
  },

  async loadTags() {
    try {
      const tags = await listTags()
      this.setData({ tags })
    } catch (e) { console.error(e) }
  },

  async loadProjects() {
    try {
      const projects = await listProjects()
      this.setData({ projects })
    } catch (e) { console.error(e) }
  },

  async loadStats() {
    try {
      const stats = await getDashboard()
      this.setData({ stats })
    } catch (e) { console.error(e) }
  },

  _formatTask(task) {
    const dueInfo = formatDueDate(task.due_date)
    return {
      ...task,
      priority_text: priorityText(task.priority),
      priority_color: priorityColor(task.priority),
      status_text: statusText(task.status),
      due_info: dueInfo,
      subtask_progress: task.subtasks?.length
        ? `${task.subtasks.filter(s => s.is_completed).length}/${task.subtasks.length}`
        : null,
    }
  },

  // === Filter Actions ===
  onFilterTap(e) {
    const key = e.currentTarget.dataset.key
    this.setData({ currentFilter: key, page: 1, tasks: [] })
    this.loadTasks()
  },

  onSearchInput(e) {
    this.setData({ searchQuery: e.detail.value })
  },

  onSearch() {
    this.setData({ page: 1, tasks: [] })
    this.loadTasks()
  },

  onToggleFilterPanel() {
    this.setData({ showFilterPanel: !this.data.showFilterPanel })
  },

  onPriorityFilter(e) {
    const priority = e.currentTarget.dataset.priority
    this.setData({
      selectedPriority: this.data.selectedPriority === priority ? '' : priority,
      page: 1, tasks: [],
    })
    this.loadTasks()
  },

  onProjectFilter(e) {
    const projectId = e.currentTarget.dataset.id
    this.setData({
      selectedProject: this.data.selectedProject === projectId ? '' : projectId,
      page: 1, tasks: [],
    })
    this.loadTasks()
  },

  // === Task Actions ===
  onTaskTap(e) {
    const taskId = e.currentTarget.dataset.id
    if (this.data.isMultiSelect) {
      this.toggleTaskSelection(taskId)
    } else {
      wx.navigateTo({ url: `/pages/task-detail/task-detail?id=${taskId}` })
    }
  },

  onTaskLongPress(e) {
    const taskId = e.currentTarget.dataset.id
    vibrateShort()
    if (!this.data.isMultiSelect) {
      this.setData({ isMultiSelect: true, selectedTaskIds: new Set([taskId]) })
    }
  },

  toggleTaskSelection(taskId) {
    const selected = new Set(this.data.selectedTaskIds)
    if (selected.has(taskId)) {
      selected.delete(taskId)
    } else {
      selected.add(taskId)
    }
    this.setData({ selectedTaskIds: selected })
  },

  exitMultiSelect() {
    this.setData({ isMultiSelect: false, selectedTaskIds: new Set() })
  },

  async onToggleComplete(e) {
    const { id, status } = e.currentTarget.dataset
    const newStatus = status === 'done' ? 'todo' : 'done'
    try {
      await updateTaskStatus(id, newStatus)
      vibrateShort()
      showToast(newStatus === 'done' ? '任务已完成 🎉' : '任务已重新打开')
      this.refreshTasks()
    } catch (err) {
      showToast('操作失败')
    }
  },

  async onSwipeDelete(e) {
    const taskId = e.currentTarget.dataset.id
    try {
      await deleteTask(taskId)
      showToast('已删除')
      this.refreshTasks()
    } catch (err) {
      showToast('删除失败')
    }
  },

  async onBatchDone() {
    const ids = Array.from(this.data.selectedTaskIds)
    if (!ids.length) return
    try {
      await batchUpdateTasks({ task_ids: ids, status: 'done' })
      showToast(`已完成 ${ids.length} 项`)
      this.exitMultiSelect()
      this.refreshTasks()
    } catch (err) {
      showToast('操作失败')
    }
  },

  async onBatchDelete() {
    const ids = Array.from(this.data.selectedTaskIds)
    if (!ids.length) return
    wx.showModal({
      title: '确认删除',
      content: `确定删除选中的 ${ids.length} 项任务吗？`,
      success: async (res) => {
        if (res.confirm) {
          for (const id of ids) {
            await deleteTask(id)
          }
          showToast('已删除')
          this.exitMultiSelect()
          this.refreshTasks()
        }
      },
    })
  },

  // === Navigation ===
  onCreateTask() {
    wx.navigateTo({ url: '/pages/task-create/task-create' })
  },

  onViewModeChange(e) {
    const mode = e.currentTarget.dataset.mode
    if (mode === 'kanban') {
      wx.navigateTo({ url: '/pages/kanban/kanban' })
    } else if (mode === 'calendar') {
      wx.switchTab({ url: '/pages/calendar/calendar' })
    } else {
      this.setData({ viewMode: mode })
    }
  },

  onLogin() {
    wx.navigateTo({ url: '/pages/profile/profile' })
  },
})
