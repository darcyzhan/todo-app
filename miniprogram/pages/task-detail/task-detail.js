import { getTask, updateTask, updateTaskStatus, deleteTask } from '../../services/task'
import { createSubtask, updateSubtask, deleteSubtask } from '../../services/task'
import { formatRelative, formatDueDate } from '../../utils/date'
import { priorityText, priorityColor, statusText, showToast, vibrateShort } from '../../utils/util'

Page({
  data: {
    task: null,
    loading: true,
    editingSubtaskId: null,
    newSubtaskTitle: '',
    showDeleteConfirm: false,
  },

  onLoad(options) {
    this.taskId = options.id
    this.loadTask()
  },

  async loadTask() {
    try {
      const task = await getTask(this.taskId)
      const dueInfo = formatDueDate(task.due_date)
      this.setData({
        task: {
          ...task,
          priority_text: priorityText(task.priority),
          priority_color: priorityColor(task.priority),
          status_text: statusText(task.status),
          due_info: dueInfo,
          subtask_progress: task.subtasks?.length
            ? `${task.subtasks.filter(s => s.is_completed).length}/${task.subtasks.length}`
            : null,
        },
        loading: false,
      })
    } catch (e) {
      showToast('加载失败')
      this.setData({ loading: false })
    }
  },

  async onToggleStatus() {
    const task = this.data.task
    const newStatus = task.status === 'done' ? 'todo' : 'done'
    try {
      await updateTaskStatus(task.id, newStatus)
      vibrateShort()
      showToast(newStatus === 'done' ? '已完成 🎉' : '已重新打开')
      this.loadTask()
    } catch (e) { showToast('操作失败') }
  },

  async onToggleSubtask(e) {
    const { id, completed } = e.currentTarget.dataset
    try {
      await updateSubtask(id, { is_completed: !completed })
      vibrateShort()
      this.loadTask()
    } catch (e) { showToast('操作失败') }
  },

  onSubtaskInput(e) { this.setData({ newSubtaskTitle: e.detail.value }) },

  async onAddSubtask() {
    if (!this.data.newSubtaskTitle.trim()) return
    try {
      await createSubtask(this.taskId, { title: this.data.newSubtaskTitle.trim() })
      this.setData({ newSubtaskTitle: '' })
      this.loadTask()
    } catch (e) { showToast('添加失败') }
  },

  async onDeleteSubtask(e) {
    const id = e.currentTarget.dataset.id
    try {
      await deleteSubtask(id)
      this.loadTask()
    } catch (e) { showToast('删除失败') }
  },

  onEditTask() {
    wx.navigateTo({ url: `/pages/task-create/task-create?id=${this.taskId}&edit=1` })
  },

  async onDeleteTask() {
    wx.showModal({
      title: '确认删除',
      content: '删除后无法恢复，确定吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await deleteTask(this.taskId)
            showToast('已删除')
            setTimeout(() => wx.navigateBack(), 500)
          } catch (e) { showToast('删除失败') }
        }
      },
    })
  },

  onShare() {
    wx.showShareMenu({ withShareTicket: true })
  },
})
