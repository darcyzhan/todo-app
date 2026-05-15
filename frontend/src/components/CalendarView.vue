<script setup>
import { computed } from 'vue'
import { useCalendar } from '../composables/useCalendar'
import { useDragDrop } from '../composables/useDragDrop'
import { Icon } from '@iconify/vue'

const props = defineProps({
  tasks: { type: Array, default: () => [] },
  selectedDate: { type: Date, default: null }
})

const emit = defineEmits(['drop-task', 'select-date'])

const { calendarDays, weekDays, year, monthName, prevMonth, nextMonth, goToday, isToday, formatDate } = useCalendar()
const { onDragOver, onDragLeave, onDrop, onDragStart, onDragEnd } = useDragDrop()

const isWeekendCol = (idx) => idx === 0 || idx === 6

function getTasksForDate(date) {
  const dateStr = formatDate(date)
  return props.tasks.filter(t => t.due_date && t.due_date.startsWith(dateStr))
}

function handleDrop(e, date) {
  const taskId = onDrop(e, date)
  if (taskId) {
    emit('drop-task', taskId, formatDate(date))
  }
}

function handleDateClick(date) {
  emit('select-date', date)
}
</script>

<template>
  <div class="calendar-panel">
    <div class="calendar-header">
      <h3 class="calendar-title">
        <Icon icon="mdi:calendar-month" width="22" />
        {{ year }}年 {{ monthName }}
      </h3>
      <div class="calendar-nav">
        <button class="nav-btn" @click="prevMonth" title="上个月">
          <Icon icon="mdi:chevron-left" width="20" />
        </button>
        <button class="today-btn" @click="goToday">今天</button>
        <button class="nav-btn" @click="nextMonth" title="下个月">
          <Icon icon="mdi:chevron-right" width="20" />
        </button>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="weekday-row">
        <div
          v-for="(wd, idx) in weekDays"
          :key="wd"
          class="weekday-cell"
          :class="{ 'weekend-col': isWeekendCol(idx) }"
        >
          {{ wd }}
        </div>
      </div>
      <div class="days-grid">
        <div
          v-for="(cell, i) in calendarDays"
          :key="i"
          class="day-cell"
          :class="{
            'other-month': !cell.isCurrentMonth,
            'is-today': isToday(cell.date),
            'is-weekend': cell.isWeekend,
            'is-holiday': !!cell.holiday,
            'has-custom-event': !!cell.customEvent,
            'selected': selectedDate && formatDate(selectedDate) === formatDate(cell.date)
          }"
          @click="handleDateClick(cell.date)"
          @dragover="onDragOver($event, cell.date)"
          @dragleave="onDragLeave"
          @drop="handleDrop($event, cell.date)"
        >
          <div class="day-header">
            <span class="day-number">{{ cell.day }}</span>
            <span
              v-if="cell.holiday"
              class="day-holiday"
              :title="cell.holiday"
            >{{ cell.holiday }}</span>
            <span
              v-else-if="cell.lunarInfo && cell.lunarInfo.isFestival"
              class="day-lunar lunar-festival"
            >{{ cell.lunarInfo.label }}</span>
            <span
              v-else-if="cell.lunarInfo"
              class="day-lunar"
            >{{ cell.lunarInfo.label }}</span>
          </div>

          <!-- 自定义纪念日 -->
          <div
            v-if="cell.customEvent"
            class="custom-event"
            :style="{ color: cell.customEvent.color, background: cell.customEvent.color + '18' }"
          >
            {{ cell.customEvent.label }}
          </div>

          <div class="day-tasks">
            <div
              v-for="task in getTasksForDate(cell.date).slice(0, 2)"
              :key="task.id"
              class="day-task-dot"
              :class="`p-${task.priority}`"
              :title="task.title"
              draggable="true"
              @dragstart="onDragStart($event, task.id)"
              @dragend="onDragEnd"
            >
              {{ task.title.slice(0, 4) }}
            </div>
            <span v-if="getTasksForDate(cell.date).length > 2" class="more-tasks">
              +{{ getTasksForDate(cell.date).length - 2 }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.calendar-panel {
  background: var(--bg-card);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.calendar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.calendar-nav {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-btn {
  background: var(--bg-hover);
  border: none;
  border-radius: 8px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all 0.15s;
}

.nav-btn:hover {
  background: var(--primary);
  color: #fff;
}

.today-btn {
  background: var(--bg-hover);
  border: none;
  border-radius: 8px;
  padding: 5px 14px;
  cursor: pointer;
  font-size: 12px;
  color: var(--primary);
  font-weight: 500;
  transition: all 0.15s;
}

.today-btn:hover {
  background: var(--primary);
  color: #fff;
}

.calendar-grid {
  user-select: none;
}

/* 周表头 */
.weekday-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  margin-bottom: 6px;
}

.weekday-cell {
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  padding: 8px 0;
}

.weekday-cell.weekend-col {
  color: #e53e3e;
}

/* 日期网格 */
.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.day-cell {
  min-height: 64px;
  padding: 4px 3px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.day-cell:hover {
  background: var(--bg-hover);
}

.day-cell.other-month {
  opacity: 0.35;
}

/* 周末背景 */
.day-cell.is-weekend {
  background: rgba(102, 126, 234, 0.04);
}

.day-cell.is-weekend .day-number {
  color: #c53030;
}

.day-cell.other-month.is-weekend .day-number {
  color: #e53e3e;
}

/* 今天 */
.day-cell.is-today {
  background: rgba(102, 126, 234, 0.06);
}

.day-cell.is-today .day-number {
  background: var(--primary);
  color: #fff !important;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

/* 节假日 */
.day-cell.is-holiday {
  background: rgba(229, 62, 62, 0.05);
}

.day-cell.is-holiday .day-number {
  color: #e53e3e;
  font-weight: 600;
}

/* 选中 */
.day-cell.selected {
  background: rgba(102, 126, 234, 0.1);
  box-shadow: inset 0 0 0 1.5px var(--primary);
}

.day-cell.drag-over {
  background: rgba(102, 126, 234, 0.15);
  box-shadow: inset 0 0 0 2px var(--primary);
}

/* 日期头部: 公历 + 农历/节日 */
.day-header {
  display: flex;
  align-items: center;
  gap: 3px;
  margin-bottom: 2px;
  flex-wrap: nowrap;
}

.day-number {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  flex-shrink: 0;
}

.day-lunar {
  font-size: 10px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.day-lunar.lunar-festival {
  color: #ed8936;
  font-weight: 500;
}

.day-holiday {
  font-size: 10px;
  color: #e53e3e;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 自定义纪念日 */
.custom-event {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 4px;
  border-radius: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
  line-height: 1.4;
}

/* 任务点 */
.day-tasks {
  display: flex;
  flex-direction: column;
  gap: 1px;
  overflow: hidden;
  flex: 1;
}

.day-task-dot {
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: grab;
}

.day-task-dot.p-P0 { background: rgba(229,62,62,0.15); color: #e53e3e; }
.day-task-dot.p-P1 { background: rgba(237,137,54,0.15); color: #ed8936; }
.day-task-dot.p-P2 { background: rgba(102,126,234,0.15); color: #667eea; }
.day-task-dot.p-P3 { background: rgba(160,174,192,0.15); color: #718096; }

.more-tasks {
  font-size: 10px;
  color: var(--text-muted);
  padding-left: 5px;
}
</style>
