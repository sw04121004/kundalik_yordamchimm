// Pure functions for Planner due time calculation, status detection, and notification tracking

/**
 * Returns task trigger timestamp (in local time milliseconds)
 * If task has due_date and due_time, combines them.
 * If task has due_date but NO due_time, defaults to 09:00:00 on that date.
 * If task has no due_date, returns null.
 */
export function getTaskTriggerTimestamp(task, defaultHour = 9, defaultMinute = 0) {
  if (!task || !task.due_date) return null
  const [year, month, day] = task.due_date.split('-').map(Number)
  if (!year || !month || !day) return null

  let hour = defaultHour
  let minute = defaultMinute
  let second = 0

  if (task.due_time) {
    const parts = task.due_time.split(':').map(Number)
    if (!isNaN(parts[0])) hour = parts[0]
    if (!isNaN(parts[1])) minute = parts[1]
    if (!isNaN(parts[2])) second = parts[2]
  }

  const d = new Date(year, month - 1, day, hour, minute, second, 0)
  return d.getTime()
}

/**
 * Returns task status relative to now:
 * 'done' | 'someday' | 'overdue' | 'approaching' | 'future'
 */
export function getTaskStatus(task, nowMs = Date.now()) {
  if (!task) return 'someday'
  if (task.is_done) return 'done'
  const triggerMs = getTaskTriggerTimestamp(task)
  if (!triggerMs) return 'someday'

  const diff = triggerMs - nowMs
  if (diff < 0) return 'overdue'
  if (diff <= 30 * 60 * 1000) return 'approaching' // within 30 mins
  return 'future'
}

/**
 * Checks whether task is due right now (or within the past 12 hours) and not yet done.
 */
export function isTaskDue(task, nowMs = Date.now(), maxPastWindowMs = 12 * 60 * 60 * 1000) {
  if (!task || task.is_done) return false
  const triggerMs = getTaskTriggerTimestamp(task)
  if (!triggerMs) return false
  const diff = nowMs - triggerMs
  return diff >= 0 && diff <= maxPastWindowMs
}

/**
 * Storage helpers for per-user notification tracking.
 * Key format: qulay_notified_<userId>
 * Stored object: { [taskId]: lastNotifiedTriggerMs }
 */
export function getNotifiedStorageKey(userId) {
  return `qulay_notified_${userId || 'guest'}`
}

export function readNotifiedMap(userId) {
  try {
    const raw = localStorage.getItem(getNotifiedStorageKey(userId))
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

export function writeNotifiedMap(userId, map) {
  try {
    localStorage.setItem(getNotifiedStorageKey(userId), JSON.stringify(map))
  } catch {}
}

export function isTaskAlreadyNotified(userId, taskId, triggerMs) {
  const map = readNotifiedMap(userId)
  return map[taskId] === triggerMs
}

export function markTaskNotified(userId, taskId, triggerMs) {
  const map = readNotifiedMap(userId)
  map[taskId] = triggerMs
  writeNotifiedMap(userId, map)
}

export function clearTaskNotified(userId, taskId) {
  const map = readNotifiedMap(userId)
  delete map[taskId]
  writeNotifiedMap(userId, map)
}

export function clearAllNotifiedForUser(userId) {
  try {
    localStorage.removeItem(getNotifiedStorageKey(userId))
  } catch {}
}

/**
 * Self-test assertions for unit verification
 */
export function runReminderSelfTests() {
  const testTaskWithTime = { due_date: '2026-11-18', due_time: '14:30:00', is_done: false }
  const tsWithTime = getTaskTriggerTimestamp(testTaskWithTime)
  const d = new Date(tsWithTime)
  const ok1 = d.getFullYear() === 2026 && d.getMonth() === 10 && d.getDate() === 18 && d.getHours() === 14 && d.getMinutes() === 30

  const testTaskNoTime = { due_date: '2026-11-18', due_time: null, is_done: false }
  const tsNoTime = getTaskTriggerTimestamp(testTaskNoTime)
  const d2 = new Date(tsNoTime)
  const ok2 = d2.getHours() === 9 && d2.getMinutes() === 0

  const testDone = { due_date: '2026-11-18', is_done: true }
  const ok3 = getTaskStatus(testDone) === 'done'

  return ok1 && ok2 && ok3
}
