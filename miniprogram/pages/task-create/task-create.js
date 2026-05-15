import { createTask } from '../../services/task'
import { listTags } from '../../services/tag'
import { listProjects } from '../../services/project'
import { parseNaturalLanguage } from '../../utils/date'
import { showToast, vibrateShort } from '../../utils/util'

Page({
  data: {
    title: '',
    description: '',
    priority: 'P2',
    status: 'todo',
    projectId: '',
    dueDate: '',
    dueTime: '',
    energyLevel: '',
    tagIds: [],
    subtasks: [''],
    isRecurring: false,
    recurrenceType: 'daily',
    nlpInput: '',
    showNlp: false,

    // Options
    priorities: [
      { value: 'P0', label: '紧急', color: '#E17055' },
      { value: 'P1', label: '高', color: '#FDCB6E' },
      { value: 'P2', label: '中', color: '#74B9FF' },
      { value: 'P3', label: '低', color: '#B2BEC3' },
    ],
    energyLevels: [
      { value: 'low', label: '低', icon: '🔋' },
      { value: 'medium', label: '中', icon: '🔋🔋' },
      { value: 'high', label: '高', icon: '🔋🔋🔋' },
    ],
    recurrenceTypes: [
      { value: 'daily', label: '每天' },
      { value: 'weekly', label: '每周' },
      { value: 'monthly', label: '每月' },
      { value: 'yearly', label: '每年' },
    ],
    tags: [],
    projects: [],
    showDatePicker: false,
    showTimePicker: false,
    submitting: false,
  },

  onLoad() {
    this.loadOptions()
    const { title, projectId } = this.options || {}
    if (title) this.setData({ title })
    if (projectId) this.setData({ projectId })
  },

  async loadOptions() {
    try {
      const [tags, projects] = await Promise.all([listTags(), listProjects()])
      this.setData({ tags, projects })
    } catch (e) { console.error(e) }
  },

  // NLP input
  onNlpInput(e) {
    this.setData({ nlpInput: e.detail.value })
  },

  onNlpParse() {
    const result = parseNaturalLanguage(this.data.nlpInput)
    this.setData({
      title: result.title,
      priority: result.priority || 'P2',
      dueDate: result.due_date || '',
    })
    showToast('已解析 🎯')
  },

  onToggleNlp() {
    this.setData({ showNlp: !this.data.showNlp })
  },

  // Form inputs
  onTitleInput(e) { this.setData({ title: e.detail.value }) },
  onDescInput(e) { this.setData({ description: e.detail.value }) },

  onPrioritySelect(e) {
    const value = e.currentTarget.dataset.value
    this.setData({ priority: value })
    vibrateShort()
  },

  onEnergySelect(e) {
    const value = e.currentTarget.dataset.value
    this.setData({ energyLevel: this.data.energyLevel === value ? '' : value })
  },

  onProjectSelect(e) {
    const id = e.currentTarget.dataset.id
    this.setData({ projectId: this.data.projectId === id ? '' : id })
  },

  onTagToggle(e) {
    const id = e.currentTarget.dataset.id
    const tagIds = [...this.data.tagIds]
    const idx = tagIds.indexOf(id)
    if (idx > -1) tagIds.splice(idx, 1)
    else tagIds.push(id)
    this.setData({ tagIds })
  },

  onDueDateChange(e) { this.setData({ dueDate: e.detail.value }) },
  onDueTimeChange(e) { this.setData({ dueTime: e.detail.value }) },

  onRecurringToggle() {
    this.setData({ isRecurring: !this.data.isRecurring })
  },

  onRecurrenceType(e) {
    this.setData({ recurrenceType: e.currentTarget.dataset.value })
  },

  // Subtasks
  onSubtaskInput(e) {
    const idx = e.currentTarget.dataset.index
    const subtasks = [...this.data.subtasks]
    subtasks[idx] = e.detail.value
    this.setData({ subtasks })
  },

  onAddSubtask() {
    this.setData({ subtasks: [...this.data.subtasks, ''] })
  },

  onRemoveSubtask(e) {
    const idx = e.currentTarget.dataset.index
    if (this.data.subtasks.length <= 1) return
    const subtasks = [...this.data.subtasks]
    subtasks.splice(idx, 1)
    this.setData({ subtasks })
  },

  // Submit
  async onSubmit() {
    if (!this.data.title.trim()) {
      showToast('请输入任务标题')
      return
    }

    this.setData({ submitting: true })

    try {
      const data = {
        title: this.data.title.trim(),
        description: this.data.description || null,
        priority: this.data.priority,
        status: this.data.status,
        project_id: this.data.projectId || null,
        due_date: this.data.dueDate ? `${this.data.dueDate}T${this.data.dueTime || '23:59'}` : null,
        energy_level: this.data.energyLevel || null,
        tag_ids: this.data.tagIds,
        subtasks: this.data.subtasks.filter(s => s.trim()),
        is_recurring: this.data.isRecurring,
        recurrence_rule: this.data.isRecurring ? { type: this.data.recurrenceType } : null,
      }

      await createTask(data)
      showToast('创建成功 🎉')
      setTimeout(() => wx.navigateBack(), 500)
    } catch (err) {
      showToast('创建失败: ' + (err.message || ''))
    } finally {
      this.setData({ submitting: false })
    }
  },
})
