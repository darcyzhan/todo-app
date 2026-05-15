import { listTasks, updateTaskStatus } from '../../services/task'
import { showToast } from '../../utils/util'

Page({
  data: {
    columns: [
      { key: 'todo', title: '待办', icon: '📋', tasks: [] },
      { key: 'in_progress', title: '进行中', icon: '🔥', tasks: [] },
      { key: 'done', title: '已完成', icon: '✅', tasks: [] },
    ],
    loading: true,
    currentProject: '',
  },

  onLoad() { this.loadTasks() },

  async loadTasks() {
    try {
      const result = await listTasks({ page_size: 100 })
      const columns = this.data.columns.map(col => ({
        ...col,
        tasks: result.items.filter(t => t.status === col.key),
      }))
      this.setData({ columns, loading: false })
    } catch (e) { this.setData({ loading: false }) }
  },

  async onMoveTask(e) {
    const { taskId, targetStatus } = e.currentTarget.dataset
    try {
      await updateTaskStatus(taskId, targetStatus)
      showToast('已移动')
      this.loadTasks()
    } catch (e) { showToast('移动失败') }
  },

  onTaskTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/task-detail/task-detail?id=${id}` })
  },

  onMoveRight(e) {
    const { taskId, currentStatus } = e.currentTarget.dataset
    const nextMap = { todo: 'in_progress', in_progress: 'done' }
    if (nextMap[currentStatus]) {
      this.onMoveTask({ currentTarget: { dataset: { taskId, targetStatus: nextMap[currentStatus] } } })
    }
  },

  onMoveLeft(e) {
    const { taskId, currentStatus } = e.currentTarget.dataset
    const prevMap = { in_progress: 'todo', done: 'in_progress' }
    if (prevMap[currentStatus]) {
      this.onMoveTask({ currentTarget: { dataset: { taskId, targetStatus: prevMap[currentStatus] } } })
    }
  },
})
