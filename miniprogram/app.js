App({
  globalData: {
    userInfo: null,
    token: null,
    baseUrl: 'http://localhost:8000/api/v1',
    theme: 'auto',
  },

  onLaunch() {
    const token = wx.getStorageSync('access_token')
    if (token) {
      this.globalData.token = token
    }
    const theme = wx.getStorageSync('theme')
    if (theme) {
      this.globalData.theme = theme
    }
  },

  isLoggedIn() {
    return !!this.globalData.token
  },

  setToken(token) {
    this.globalData.token = token
    wx.setStorageSync('access_token', token)
  },

  clearToken() {
    this.globalData.token = null
    wx.removeStorageSync('access_token')
  },
})
