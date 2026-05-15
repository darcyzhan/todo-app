const app = getApp()

class Request {
  constructor() {
    this.baseUrl = app.globalData.baseUrl
    this.queue = []
    this.isRefreshing = false
  }

  async request(options) {
    const { url, method = 'GET', data, header = {} } = options

    if (app.globalData.token) {
      header['Authorization'] = `Bearer ${app.globalData.token}`
    }

    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.baseUrl}${url}`,
        method,
        data,
        header: {
          'Content-Type': 'application/json',
          ...header,
        },
        success: (res) => {
          if (res.statusCode === 200 || res.statusCode === 201) {
            resolve(res.data)
          } else if (res.statusCode === 401) {
            this._handleUnauthorized()
            reject(new Error('认证已过期，请重新登录'))
          } else if (res.statusCode === 422) {
            reject(new Error(res.data?.detail?.[0]?.msg || '数据验证失败'))
          } else {
            reject(new Error(res.data?.message || `请求失败 (${res.statusCode})`))
          }
        },
        fail: (err) => {
          reject(new Error(err.errMsg || '网络错误'))
        },
      })
    })
  }

  get(url, params) {
    let queryStr = ''
    if (params) {
      const pairs = Object.entries(params)
        .filter(([, v]) => v !== undefined && v !== null && v !== '')
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      if (pairs.length) queryStr = '?' + pairs.join('&')
    }
    return this.request({ url: url + queryStr })
  }

  post(url, data) {
    return this.request({ url, method: 'POST', data })
  }

  put(url, data) {
    return this.request({ url, method: 'PUT', data })
  }

  delete(url, data) {
    return this.request({ url, method: 'DELETE', data })
  }

  async _handleUnauthorized() {
    app.clearToken()
    wx.showToast({ title: '请重新登录', icon: 'none' })
    setTimeout(() => {
      wx.reLaunch({ url: '/pages/index/index' })
    }, 1500)
  }
}

const http = new Request()
export default http
