import { ref, computed } from 'vue'
import { Solar } from 'lunar-javascript'

// 中国法定节假日 (可按年扩展)
const HOLIDAYS = {
  '2025-01-01': '元旦',
  '2025-01-28': '除夕',
  '2025-01-29': '春节',
  '2025-01-30': '初二',
  '2025-01-31': '初三',
  '2025-02-01': '初四',
  '2025-02-02': '初五',
  '2025-02-03': '初六',
  '2025-02-04': '初七',
  '2025-04-04': '清明',
  '2025-04-05': '清明假',
  '2025-04-06': '清明假',
  '2025-05-01': '劳动节',
  '2025-05-02': '劳动假',
  '2025-05-03': '劳动假',
  '2025-05-04': '劳动假',
  '2025-05-05': '劳动假',
  '2025-05-31': '端午',
  '2025-06-01': '端午假',
  '2025-06-02': '端午假',
  '2025-10-01': '国庆',
  '2025-10-02': '国庆假',
  '2025-10-03': '国庆假',
  '2025-10-04': '国庆假',
  '2025-10-05': '国庆假',
  '2025-10-06': '国庆假',
  '2025-10-07': '国庆假',
  '2025-10-08': '国庆假',
  '2026-01-01': '元旦',
  '2026-02-16': '除夕',
  '2026-02-17': '春节',
  '2026-02-18': '初二',
  '2026-02-19': '初三',
  '2026-02-20': '初四',
  '2026-02-21': '初五',
  '2026-02-22': '初六',
  '2026-02-23': '初七',
  '2026-04-05': '清明',
  '2026-04-06': '清明假',
  '2026-05-01': '劳动节',
  '2026-05-02': '劳动假',
  '2026-05-03': '劳动假',
  '2026-05-04': '劳动假',
  '2026-05-05': '劳动假',
  '2026-06-19': '端午',
  '2026-06-20': '端午假',
  '2026-06-21': '端午假',
  '2026-10-01': '国庆',
  '2026-10-02': '国庆假',
  '2026-10-03': '国庆假',
  '2026-10-04': '国庆假',
  '2026-10-05': '国庆假',
  '2026-10-06': '国庆假',
  '2026-10-07': '国庆假',
  '2026-10-08': '中秋',
}

// 自定义纪念日 (农历) - 农历六月初五 老婆生日
const LUNAR_CUSTOM_EVENTS = [
  { month: 6, day: 5, label: '🎂 老婆生日', color: '#e53e3e' }
]

// 自定义纪念日 (公历)
const SOLAR_CUSTOM_EVENTS = {
  // 示例: '01-01': '结婚纪念日'
}

export function useCalendar() {
  const currentDate = ref(new Date())
  const viewMode = ref('month') // month | week

  const year = computed(() => currentDate.value.getFullYear())
  const month = computed(() => currentDate.value.getMonth())

  const monthName = computed(() => {
    const names = ['一月', '二月', '三月', '四月', '五月', '六月',
                   '七月', '八月', '九月', '十月', '十一月', '十二月']
    return names[month.value]
  })

  const weekDays = ['日', '一', '二', '三', '四', '五', '六']

  const calendarDays = computed(() => {
    const firstDay = new Date(year.value, month.value, 1)
    const lastDay = new Date(year.value, month.value + 1, 0)
    const startPad = firstDay.getDay() // 0=Sun
    const totalDays = lastDay.getDate()

    const days = []

    // Previous month padding
    const prevLastDay = new Date(year.value, month.value, 0).getDate()
    for (let i = startPad - 1; i >= 0; i--) {
      days.push(buildDayCell(new Date(year.value, month.value - 1, prevLastDay - i), false))
    }

    // Current month
    for (let d = 1; d <= totalDays; d++) {
      days.push(buildDayCell(new Date(year.value, month.value, d), true))
    }

    // Next month padding (fill to 42 cells = 6 rows)
    const remaining = 42 - days.length
    for (let i = 1; i <= remaining; i++) {
      days.push(buildDayCell(new Date(year.value, month.value + 1, i), false))
    }

    return days
  })

  function buildDayCell(date, isCurrentMonth) {
    const day = date.getDate()
    const dow = date.getDay() // 0=Sun, 6=Sat
    const isWeekend = dow === 0 || dow === 6
    const dateStr = formatDate(date)

    // 节假日
    const holiday = HOLIDAYS[dateStr] || null

    // 农历信息
    let lunarInfo = null
    let customEvent = null
    try {
      const solar = Solar.fromDate(date)
      const lunar = solar.getLunar()
      const lunarMonth = lunar.getMonth()
      const lunarDay = lunar.getDay()
      const lunarMonthStr = lunar.getMonthInChinese()
      const lunarDayStr = lunar.getDayInChinese()

      // 农历显示：初一时显示月名，其他显示日
      const lunarLabel = lunarDay === 1
        ? `${lunarMonthStr}月`
        : lunarDayStr

      // 检查自定义农历事件
      for (const evt of LUNAR_CUSTOM_EVENTS) {
        if (lunarMonth === evt.month && lunarDay === evt.day) {
          customEvent = { label: evt.label, color: evt.color }
        }
      }

      // 农历节日
      const lunarFestivals = lunar.getFestivals()
      if (lunarFestivals.length > 0 && !holiday) {
        // 农历节日优先级低于公历节日
        lunarInfo = { label: lunarFestivals[0], isFestival: true }
      } else {
        lunarInfo = { label: lunarLabel, isFestival: false }
      }
    } catch (e) {
      lunarInfo = null
    }

    // 公历自定义事件
    const mmdd = `${String(date.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    if (SOLAR_CUSTOM_EVENTS[mmdd] && !customEvent) {
      customEvent = { label: SOLAR_CUSTOM_EVENTS[mmdd], color: '#667eea' }
    }

    return {
      date,
      isCurrentMonth,
      day,
      isWeekend,
      holiday,
      lunarInfo,
      customEvent
    }
  }

  function prevMonth() {
    currentDate.value = new Date(year.value, month.value - 1, 1)
  }

  function nextMonth() {
    currentDate.value = new Date(year.value, month.value + 1, 1)
  }

  function goToday() {
    currentDate.value = new Date()
  }

  function isSameDay(d1, d2) {
    if (!d1 || !d2) return false
    return d1.getFullYear() === d2.getFullYear() &&
           d1.getMonth() === d2.getMonth() &&
           d1.getDate() === d2.getDate()
  }

  function isToday(d) {
    return isSameDay(d, new Date())
  }

  function formatDate(d) {
    if (!d) return ''
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}-${m}-${day}`
  }

  return {
    currentDate,
    viewMode,
    year,
    month,
    monthName,
    calendarDays,
    weekDays,
    prevMonth,
    nextMonth,
    goToday,
    isSameDay,
    isToday,
    formatDate
  }
}
