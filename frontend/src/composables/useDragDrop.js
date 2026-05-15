import { ref } from 'vue'

export function useDragDrop() {
  const draggedTaskId = ref(null)
  const dragOverDate = ref(null)

  function onDragStart(e, taskId) {
    draggedTaskId.value = taskId
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('text/plain', taskId)
    e.target.classList.add('dragging')
  }

  function onDragEnd(e) {
    draggedTaskId.value = null
    dragOverDate.value = null
    e.target.classList.remove('dragging')
    // Remove all drag-over classes
    document.querySelectorAll('.drag-over').forEach(el => {
      el.classList.remove('drag-over')
    })
  }

  function onDragOver(e, date) {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
    dragOverDate.value = date
    e.currentTarget.classList.add('drag-over')
  }

  function onDragLeave(e) {
    e.currentTarget.classList.remove('drag-over')
    dragOverDate.value = null
  }

  function onDrop(e, date) {
    e.preventDefault()
    e.currentTarget.classList.remove('drag-over')
    const taskId = draggedTaskId.value || e.dataTransfer.getData('text/plain')
    draggedTaskId.value = null
    dragOverDate.value = null
    return taskId
  }

  return {
    draggedTaskId,
    dragOverDate,
    onDragStart,
    onDragEnd,
    onDragOver,
    onDragLeave,
    onDrop
  }
}
