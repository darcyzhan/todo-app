const app = getApp()

Page({
  data: { theme: 'auto', language: 'zh-CN', themes: [{ value: 'auto', label: '跟随系统' }, { value: 'light', label: '浅色模式' }, { value: 'dark', label: '深色模式' }] },
  onLoad() { this.setData({ theme: app.globalData.theme }) },
  onThemeChange(e) {
    const theme = e.currentTarget.dataset.value
    this.setData({ theme })
    app.globalData.theme = theme
    wx.setStorageSync('theme', theme)
  },
  onClearCache() { wx.showModal({ title: '确认清除？', content: '将清除所有本地缓存', success: (r) => { if (r.confirm) { wx.clearStorageSync(); wx.showToast({ title: '已清除' }) } } }) },
  onAbout() { wx.showModal({ title: 'TodoMaster Pro', content: '版本 1.0.0\n智能待办管理小程序', showCancel: false }) },
})
