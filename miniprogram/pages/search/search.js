import { listTasks } from '../../services/task'
import { debounce } from '../../utils/util'

Page({
  data: { query: '', results: [], searching: false },
  onInput(e) { this.setData({ query: e.detail.value }); this.search() },
  search: debounce(async function() {
    if (!this.data.query.trim()) { this.setData({ results: [] }); return }
    this.setData({ searching: true })
    try { const r = await listTasks({ q: this.data.query, page_size: 20 }); this.setData({ results: r.items, searching: false }) } catch(e) { this.setData({ searching: false }) }
  }, 300),
  onTaskTap(e) { wx.navigateTo({ url: `/pages/task-detail/task-detail?id=${e.currentTarget.dataset.id}` }) },
})
