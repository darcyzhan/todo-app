Page({
  data: {
    mode: 'pomodoro', // pomodoro, custom
    focusDuration: 25, // minutes
    breakDuration: 5,
    longBreakDuration: 15,
    isRunning: false,
    isPaused: false,
    remainingSeconds: 25 * 60,
    totalSeconds: 25 * 60,
    completedPomodoros: 0,
    soundType: 'rain', // rain, wave, cafe, none
    taskId: '',
    taskTitle: '',
  },

  timer: null,

  onLoad(options) {
    if (options.taskId) this.setData({ taskId: options.taskId })
    if (options.taskTitle) this.setData({ taskTitle: options.taskTitle })
  },

  onUnload() { this.stopTimer() },

  onStart() {
    this.setData({ isRunning: true, isPaused: false, remainingSeconds: this.data.focusDuration * 60, totalSeconds: this.data.focusDuration * 60 })
    this.startTimer()
  },

  onPause() {
    this.setData({ isPaused: true })
    clearInterval(this.timer)
  },

  onResume() {
    this.setData({ isPaused: false })
    this.startTimer()
  },

  onStop() {
    this.stopTimer()
    this.setData({ isRunning: false, isPaused: false, remainingSeconds: this.data.focusDuration * 60 })
  },

  startTimer() {
    this.timer = setInterval(() => {
      const remaining = this.data.remainingSeconds - 1
      if (remaining <= 0) {
        this.onPomodoroComplete()
      } else {
        this.setData({ remainingSeconds: remaining })
      }
    }, 1000)
  },

  stopTimer() {
    if (this.timer) { clearInterval(this.timer); this.timer = null }
  },

  onPomodoroComplete() {
    this.stopTimer()
    const completed = this.data.completedPomodoros + 1
    this.setData({ completedPomodoros: completed, isRunning: false })
    wx.vibrateLong()
    wx.showModal({
      title: '🎉 专注完成！',
      content: `你已完成 ${completed} 个番茄钟，休息一下吧`,
      showCancel: false,
    })
  },

  onDurationChange(e) {
    const val = Number(e.detail.value)
    this.setData({ focusDuration: val, remainingSeconds: val * 60, totalSeconds: val * 60 })
  },

  onSoundChange(e) {
    this.setData({ soundType: e.currentTarget.dataset.type })
  },
})
