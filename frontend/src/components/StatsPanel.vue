<script setup>
import { computed } from 'vue'
import { Icon } from '@iconify/vue'

const props = defineProps({
  priorityStats: { type: Object, required: true },
  statusStats: { type: Object, required: true },
  totalTasks: { type: Number, default: 0 },
  completedRate: { type: Number, default: 0 },
  maxPriority: { type: Number, default: 1 }
})

const priorities = computed(() => [
  { key: 'P0', label: '紧急', color: '#e53e3e', count: props.priorityStats.P0 },
  { key: 'P1', label: '高优', color: '#ed8936', count: props.priorityStats.P1 },
  { key: 'P2', label: '中等', color: '#667eea', count: props.priorityStats.P2 },
  { key: 'P3', label: '低优', color: '#a0aec0', count: props.priorityStats.P3 }
])

const statusItems = computed(() => [
  { key: 'todo', label: '待办', color: '#667eea', count: props.statusStats.todo, icon: 'mdi:checkbox-blank-outline' },
  { key: 'in_progress', label: '进行中', color: '#ed8936', count: props.statusStats.in_progress, icon: 'mdi:progress-clock' },
  { key: 'done', label: '已完成', color: '#48bb78', count: props.statusStats.done, icon: 'mdi:checkbox-marked-circle' },
  { key: 'archived', label: '归档', color: '#a0aec0', count: props.statusStats.archived, icon: 'mdi:archive' }
])
</script>

<template>
  <div class="stats-panel">
    <h3 class="stats-title">
      <Icon icon="mdi:chart-bar" width="18" />
      数据统计
    </h3>

    <!-- Summary -->
    <div class="summary-grid">
      <div class="summary-item">
        <span class="summary-value">{{ totalTasks }}</span>
        <span class="summary-label">总任务</span>
      </div>
      <div class="summary-item">
        <span class="summary-value completed">{{ completedRate }}%</span>
        <span class="summary-label">完成率</span>
      </div>
    </div>

    <!-- Priority Distribution -->
    <div class="section">
      <h4 class="section-label">优先级分布</h4>
      <div class="bar-chart">
        <div v-for="p in priorities" :key="p.key" class="bar-row">
          <span class="bar-label">{{ p.label }}</span>
          <div class="bar-track">
            <div
              class="bar-fill"
              :style="{
                width: maxPriority ? (p.count / maxPriority * 100) + '%' : '0%',
                background: p.color
              }"
            ></div>
          </div>
          <span class="bar-count">{{ p.count }}</span>
        </div>
      </div>
    </div>

    <!-- Status Distribution -->
    <div class="section">
      <h4 class="section-label">状态分布</h4>
      <div class="status-list">
        <div v-for="s in statusItems" :key="s.key" class="status-row">
          <Icon :icon="s.icon" :style="{ color: s.color }" width="16" />
          <span class="status-name">{{ s.label }}</span>
          <span class="status-count" :style="{ color: s.color }">{{ s.count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-panel {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}

.stats-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 18px;
}

.summary-item {
  background: var(--bg-hover);
  border-radius: 10px;
  padding: 12px;
  text-align: center;
}

.summary-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: var(--primary);
}

.summary-value.completed {
  color: #48bb78;
}

.summary-label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.section {
  margin-bottom: 16px;
}

.section:last-child {
  margin-bottom: 0;
}

.section-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bar-label {
  font-size: 12px;
  color: var(--text-secondary);
  width: 30px;
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  height: 16px;
  background: var(--bg-hover);
  border-radius: 8px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 8px;
  transition: width 0.4s ease;
  min-width: 0;
}

.bar-count {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  width: 20px;
  text-align: right;
  flex-shrink: 0;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-name {
  flex: 1;
  font-size: 13px;
  color: var(--text-secondary);
}

.status-count {
  font-size: 14px;
  font-weight: 600;
}
</style>
