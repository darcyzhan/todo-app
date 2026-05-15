/**
 * 日期工具函数
 */

const WEEKDAYS = ['日', '一', '二', '三', '四', '五', '六']
const WEEKDAYS_FULL = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']

export function formatDate(date, format = 'YYYY-MM-DD') {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
}

export function formatRelative(date) {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  return formatDate(date)
}

export function formatDueDate(date) {
  if (!date) return null
  const d = new Date(date)
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const target = new Date(d.getFullYear(), d.getMonth(), d.getDate())
  const diffDays = Math.floor((target - today) / 86400000)

  if (diffDays < 0) return { text: `逾期${Math.abs(diffDays)}天`, status: 'overdue' }
  if (diffDays === 0) return { text: '今天', status: 'today' }
  if (diffDays === 1) return { text: '明天', status: 'soon' }
  if (diffDays <= 7) return { text: `${diffDays}天后`, status: 'soon' }
  return { text: formatDate(date, 'MM-DD'), status: 'normal' }
}

export function isToday(date) {
  if (!date) return false
  const d = new Date(date)
  const now = new Date()
  return d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
}

export function getWeekday(date) {
  if (!date) return ''
  return WEEKDAYS_FULL[new Date(date).getDay()]
}

export function getCalendarDays(year, month) {
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const daysInPrevMonth = new Date(year, month, 0).getDate()

  const days = []

  // Previous month padding
  for (let i = firstDay - 1; i >= 0; i--) {
    days.push({ day: daysInPrevMonth - i, type: 'prev' })
  }

  // Current month
  for (let i = 1; i <= daysInMonth; i++) {
    days.push({
      day: i,
      type: 'current',
      date: formatDate(new Date(year, month, i)),
      isToday: isToday(new Date(year, month, i)),
    })
  }

  // Next month padding
  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    days.push({ day: i, type: 'next' })
  }

  return days
}

export function parseNaturalLanguage(text) {
  const result = { title: text, due_date: null, priority: null, tags: [] }

  // Parse priority
  if (/优先级高|紧急|P0|!!/i.test(text)) {
    result.priority = 'P0'
    result.title = result.title.replace(/优先级高|紧急|P0|!!/gi, '').trim()
  } else if (/优先级中|P1|!/i.test(text)) {
    result.priority = 'P1'
    result.title = result.title.replace(/优先级中|P1|!/g, '').trim()
  }

  // Parse tags
  const tagRegex = /#(\S+)/g
  let match
  while ((match = tagRegex.exec(text)) !== null) {
    result.tags.push(match[1])
  }
  result.title = result.title.replace(/#\S+/g, '').trim()

  // Parse date keywords
  const now = new Date()
  if (/今天/.test(text)) {
    result.due_date = formatDate(now)
    result.title = result.title.replace('今天', '').trim()
  } else if (/明天/.test(text)) {
    result.due_date = formatDate(new Date(now.getTime() + 86400000))
    result.title = result.title.replace('明天', '').trim()
  } else if (/后天/.test(text)) {
    result.due_date = formatDate(new Date(now.getTime() + 86400000 * 2))
    result.title = result.title.replace('后天', '').trim()
  } else if (/下周一/.test(text)) {
    const daysUntilMonday = (8 - now.getDay()) % 7 || 7
    result.due_date = formatDate(new Date(now.getTime() + 86400000 * daysUntilMonday))
    result.title = result.title.replace('下周一', '').trim()
  }

  return result
}
