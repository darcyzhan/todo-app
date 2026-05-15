import { listProjects, createProject, deleteProject } from '../../services/project'
import { showToast } from '../../utils/util'

Page({
  data: { projects: [], showCreate: false, newName: '', newIcon: '📋', newColor: '#6C5CE7', colors: ['#6C5CE7','#00B894','#E17055','#0984E3','#FDCB6E','#FD79A8','#A29BFE','#55EFC4'], icons: ['📋','🚀','💼','🎯','📱','🎨','📚','🏠','💪','🎮'] },
  onShow() { this.load() },
  async load() { try { this.setData({ projects: await listProjects() }) } catch(e){} },
  onNameInput(e) { this.setData({ newName: e.detail.value }) },
  onIconSelect(e) { this.setData({ newIcon: e.currentTarget.dataset.icon }) },
  onColorSelect(e) { this.setData({ newColor: e.currentTarget.dataset.color }) },
  onShowCreate() { this.setData({ showCreate: true }) },
  onHideCreate() { this.setData({ showCreate: false }) },
  async onCreate() {
    if (!this.data.newName.trim()) { showToast('请输入项目名'); return }
    try { await createProject({ name: this.data.newName, icon: this.data.newIcon, color: this.data.newColor }); this.setData({ showCreate: false, newName: '' }); showToast('创建成功'); this.load() } catch(e) { showToast('创建失败') }
  },
  async onDelete(e) { const id = e.currentTarget.dataset.id; wx.showModal({ title: '确认删除？', success: async (r) => { if (r.confirm) { await deleteProject(id); this.load() } } }) },
  onProjectTap(e) { wx.navigateTo({ url: `/pages/project/project?id=${e.currentTarget.dataset.id}` }) },
})
