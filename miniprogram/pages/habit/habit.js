import { listHabits, logHabit, unlogHabit, createHabit } from '../../services/habit'
import { showToast } from '../../utils/util'

Page({
  data: {
    habits: [],
    showCreateModal: false,
    newHabit: { title: '', icon: '✅', color: '#6C5CE7', frequency: 'daily' },
    icons: ['✅', '🏃', '📚', '💪', '🧘', '🎵', '💧', '🍎', '💤', '🎯'],
    colors: ['#6C5CE7', '#00B894', '#E17055', '#0984E3', '#FDCB6E', '#A29BFE', '#FD79A8'],
  },

  onShow() { this.loadHabits() },

  async loadHabits() {
    try {
      const habits = await listHabits()
      this.setData({ habits })
    } catch (e) { console.error(e) }
  },

  async onLog(e) {
    const { id } = e.currentTarget.dataset
    try {
      await logHabit(id)
      showToast('打卡成功 🔥')
      this.loadHabits()
    } catch (e) {
      if (e.message?.includes('已打卡')) showToast('今天已打过卡了')
      else showToast('打卡失败')
    }
  },

  async onUnlog(e) {
    const { id, date } = e.currentTarget.dataset
    try {
      await unlogHabit(id, date)
      this.loadHabits()
    } catch (e) { showToast('操作失败') }
  },

  onShowCreate() { this.setData({ showCreateModal: true }) },
  onHideCreate() { this.setData({ showCreateModal: false }) },

  onNewTitleInput(e) {
    this.setData({ 'newHabit.title': e.detail.value })
  },
  onIconSelect(e) {
    this.setData({ 'newHabit.icon': e.currentTarget.dataset.icon })
  },
  onColorSelect(e) {
    this.setData({ 'newHabit.color': e.currentTarget.dataset.color })
  },

  async onCreateHabit() {
    if (!this.data.newHabit.title.trim()) { showToast('请输入习惯名称'); return }
    try {
      await createHabit(this.data.newHabit)
      this.setData({ showCreateModal: false, 'newHabit.title': '' })
      showToast('创建成功')
      this.loadHabits()
    } catch (e) { showToast('创建失败') }
  },

  onGoToHabit(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/habit/habit?id=${id}` })
  },
})
