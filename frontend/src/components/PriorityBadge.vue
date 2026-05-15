<script setup>
import { Icon } from '@iconify/vue'

defineProps({
  priority: { type: String, required: true }
})

const priorityMap = {
  P0: { label: '紧急', color: '#e53e3e', bg: 'rgba(229,62,62,0.12)' },
  P1: { label: '高', color: '#ed8936', bg: 'rgba(237,137,54,0.12)' },
  P2: { label: '中', color: '#667eea', bg: 'rgba(102,126,234,0.12)' },
  P3: { label: '低', color: '#a0aec0', bg: 'rgba(160,174,192,0.12)' }
}
</script>

<template>
  <span
    class="priority-badge"
    :style="{ color: priorityMap[priority]?.color, background: priorityMap[priority]?.bg }"
  >
    <Icon icon="mdi:flag" width="12" />
    {{ priorityMap[priority]?.label || priority }}
  </span>
</template>

<style scoped>
.priority-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}
</style>
