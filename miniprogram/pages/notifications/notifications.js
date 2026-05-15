import { getNotifications, markNotificationRead, markAllNotificationsRead } from '../../services/stats'

Page({
  data: { notifications: [], page: 1, hasMore: true },
  onShow() { this.load() },
  async load() { try { const r = await getNotifications(this.data.page); this.setData({ notifications: r.items, hasMore: r.items.length >= 20 }) } catch(e){} },
  async onRead(e) { try { await markNotificationRead(e.currentTarget.dataset.id); this.load() } catch(e){} },
  async onReadAll() { try { await markAllNotificationsRead(); this.load() } catch(e){} },
  loadMore() { if (this.data.hasMore) { this.setData({ page: this.data.page + 1 }); this.load() } },
})
