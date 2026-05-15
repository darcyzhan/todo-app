import { listTasks } from '../../services/task'
import { getCalendarDays, formatDate, isToday } from '../../utils/date'

Page({
  data: {
    year: new Date().getFullYear(),
    month: new Date().getMonth(),
    calendarDays: [],
    weekHeaders: ['日', '一', '二', '三', '四', '五', '六'],
    selectedDate: formatDate(new Date()),
    tasksByDate: {},
    selectedTasks: [],
    viewMode: 'month', // month, week
  },

  onLoad() { this.generateCalendar() },
  onShow() { this.loadMonthTasks() },

  generateCalendar() {
    const { year, month } = this.data
    const days = getCalendarDays(year, month)
    this.setData({ calendarDays: days })
  },

  async loadMonthTasks() {
    const { year, month } = this.data
    const from = formatDate(new Date(year, month, 1))
    const to = formatDate(new Date(year, month + 1, 0))
    try {
      const result = await listTasks({ due_from: from, due_to: to, page_size: 100 })
      const tasksByDate = {}
      result.items.forEach(task => {
        const date = task.due_date?.split('T')[0]
        if (date) {
          if (!tasksByDate[date]) tasksByDate[date] = []
          tasksByDate[date].push(task)
        }
      })
      this.setData({ tasksByDate })
      if (this.data.selectedDate) this.showDateTasks(this.data.selectedDate)
    } catch (e) { console.error(e) }
  },

  onDayTap(e) {
    const { date } = e.currentTarget.dataset
    if (!date) return
    this.setData({ selectedDate: date })
    this.showDateTasks(date)
  },

  showDateTasks(date) {
    const tasks = this.data.tasksByDate[date] || []
    this.setData({ selectedTasks: tasks })
  },

  onPrevMonth() {
    let { year, month } = this.data
    month--
    if (month < 0) { month = 11; year-- }
    this.setData({ year, month, selectedDate: '' }, () => {
      this.generateCalendar()
      this.loadMonthTasks()
    })
  },

  onNextMonth() {
    let { year, month } = this.data
    month++
    if (month > 11) { month = 0; year++ }
    this.setData({ year, month, selectedDate: '' }, () => {
      this.generateCalendar()
      this.loadMonthTasks()
    })
  },

  onToday() {
    this.setData({
      year: new Date().getFullYear(),
      month: new Date().getMonth(),
      selectedDate: formatDate(new Date()),
    }, () => {
      this.generateCalendar()
      this.loadMonthTasks()
    })
  },

  onCreateTask() {
    const date = this.data.selectedDate || formatDate(new Date())
    wx.navigateTo({ url: `/pages/task-create/task-create?dueDate=${date}` })
  },
})
