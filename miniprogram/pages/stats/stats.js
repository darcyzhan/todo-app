import { getDashboard } from '../../services/stats'
import { listTasks } from '../../services/task'

Page({
  data: {
    dashboard: { today_todo: 0, week_done: 0, overdue: 0, in_progress: 0, completion_rate: 0 },
    weeklyData: [0, 0, 0, 0, 0, 0, 0],
    weekLabels: ['一', '二', '三', '四', '五', '六', '日'],
    priorityDist: [],
    recentCompleted: [],
  },

  onShow() { this.loadData() },

  async loadData() {
    try {
      const [dashboard, tasks] = await Promise.all([
        getDashboard(),
        listTasks({ status: 'done', page_size: 10, sort: 'completed_at', order: 'desc' }),
      ])
      // Simulate weekly data
      const weeklyData = [3, 5, 2, 8, 4, 6, dashboard.week_done]
      // Priority distribution
      const allTasks = await listTasks({ page_size: 100 })
      const pDist = [
        { label: '紧急', value: allTasks.items.filter(t => t.priority === 'P0').length, color: '#E17055' },
        { label: '高', value: allTasks.items.filter(t => t.priority === 'P1').length, color: '#FDCB6E' },
        { label: '中', value: allTasks.items.filter(t => t.priority === 'P2').length, color: '#74B9FF' },
        { label: '低', value: allTasks.items.filter(t => t.priority === 'P3').length, color: '#B2BEC3' },
      ].filter(p => p.value > 0)

      this.setData({
        dashboard,
        weeklyData,
        priorityDist: pDist,
        recentCompleted: tasks.items || [],
      })
    } catch (e) { console.error(e) }
  },
})
