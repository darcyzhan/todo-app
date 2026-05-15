const app = getApp()
import { loginWithPassword, register } from '../../services/auth'
import { getDashboard } from '../../services/stats'
import { getUnreadCount } from '../../services/stats'

Page({
  data: {
    userInfo: null,
    isLoggedIn: false,
    stats: null,
    unreadCount: 0,
    showLoginModal: false,
    loginForm: { nickname: '', password: '' },
    isRegister: false,
    menuItems: [
      { icon: '📁', title: '项目管理', url: '/pages/project/project' },
      { icon: '🔥', title: '习惯追踪', url: '/pages/habit/habit' },
      { icon: '🍅', title: '专注模式', url: '/pages/focus/focus' },
      { icon: '🔔', title: '通知中心', url: '/pages/notifications/notifications' },
      { icon: '🔍', title: '搜索', url: '/pages/search/search' },
      { icon: '⚙️', title: '设置', url: '/pages/settings/settings' },
    ],
  },

  onShow() {
    this.checkLogin()
  },

  async checkLogin() {
    if (app.isLoggedIn()) {
      this.setData({ isLoggedIn: true })
      this.loadProfile()
    }
  },

  async loadProfile() {
    try {
      const [stats, unreadResult] = await Promise.all([
        getDashboard(),
        getUnreadCount(),
      ])
      this.setData({ stats, unreadCount: unreadResult.count })
    } catch (e) { console.error(e) }
  },

  onMenuTap(e) {
    const url = e.currentTarget.dataset.url
    if (!this.data.isLoggedIn && url !== '/pages/settings/settings') {
      this.setData({ showLoginModal: true })
      return
    }
    wx.navigateTo({ url })
  },

  onLoginTap() {
    this.setData({ showLoginModal: true, isRegister: false })
  },

  onSwitchToRegister() {
    this.setData({ isRegister: true })
  },

  onSwitchToLogin() {
    this.setData({ isRegister: false })
  },

  onNicknameInput(e) { this.setData({ 'loginForm.nickname': e.detail.value }) },
  onPasswordInput(e) { this.setData({ 'loginForm.password': e.detail.value }) },

  async onLoginSubmit() {
    const { nickname, password } = this.data.loginForm
    if (!nickname || !password) {
      wx.showToast({ title: '请填写完整', icon: 'none' })
      return
    }
    try {
      let result
      if (this.data.isRegister) {
        result = await register(nickname, password)
      } else {
        result = await loginWithPassword(nickname, password)
      }
      app.setToken(result.access_token)
      wx.setStorageSync('refresh_token', result.refresh_token)
      this.setData({ showLoginModal: false, isLoggedIn: true, userInfo: result.user })
      wx.showToast({ title: this.data.isRegister ? '注册成功' : '登录成功', icon: 'success' })
      this.loadProfile()
    } catch (e) {
      wx.showToast({ title: e.message || '操作失败', icon: 'none' })
    }
  },

  onLogout() {
    wx.showModal({
      title: '确认退出',
      content: '退出后需要重新登录',
      success: (res) => {
        if (res.confirm) {
          app.clearToken()
          this.setData({ isLoggedIn: false, userInfo: null, stats: null })
        }
      },
    })
  },

  onCloseModal() {
    this.setData({ showLoginModal: false })
  },
})
