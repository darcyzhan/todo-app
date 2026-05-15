/**
 * 通用工具函数
 */

export function generateId() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

export function debounce(fn, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

export function throttle(fn, delay = 300) {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      fn.apply(this, args)
    }
  }
}

export function priorityText(priority) {
  const map = { P0: '紧急', P1: '高', P2: '中', P3: '低' }
  return map[priority] || '中'
}

export function statusText(status) {
  const map = {
    todo: '待办',
    in_progress: '进行中',
    done: '已完成',
    archived: '已归档',
    cancelled: '已取消',
  }
  return map[status] || status
}

export function priorityColor(priority) {
  const map = { P0: '#E17055', P1: '#FDCB6E', P2: '#74B9FF', P3: '#B2BEC3' }
  return map[priority] || '#74B9FF'
}

export function durationText(minutes) {
  if (!minutes) return ''
  if (minutes < 60) return `${minutes}分钟`
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m ? `${h}小时${m}分钟` : `${h}小时`
}

export function showToast(title, icon = 'none', duration = 1500) {
  wx.showToast({ title, icon, duration })
}

export function showLoading(title = '加载中...') {
  wx.showLoading({ title, mask: true })
}

export function hideLoading() {
  wx.hideLoading()
}

export function vibrateShort() {
  wx.vibrateShort({ type: 'light' })
}
