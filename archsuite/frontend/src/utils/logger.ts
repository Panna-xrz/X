// 前端运行时日志：受设置面板 logLevel 控制
// - 内存环形缓冲（最多 200 条），供底部状态栏日志抽屉查看
// - 同时镜像到 console
import { ref } from 'vue'
import { readSetting } from '@/utils/settings'

export type LogLevel = 'debug' | 'info' | 'warn' | 'error'

export interface LogEntry {
  id: number
  ts: number
  level: LogLevel
  category: string
  message: string
}

const LEVEL_ORDER: Record<LogLevel, number> = { debug: 0, info: 1, warn: 2, error: 3 }
const MAX_ENTRIES = 200

const entries = ref<LogEntry[]>([])
let seq = 0

// 当前生效的日志级别（从设置面板读取，默认 info）
function readLevelFromStorage(): LogLevel {
  const v = readSetting('logLevel', 'info')
  if (v === 'debug' || v === 'info' || v === 'warn' || v === 'error') return v
  return 'info'
}
let currentLevel: LogLevel = readLevelFromStorage()

export function setLogLevel(level: LogLevel) {
  currentLevel = level
}

export function getLogLevel(): LogLevel {
  return currentLevel
}

// 从 localStorage 重新读取级别（设置保存后调用）
export function reloadLogLevel() {
  currentLevel = readLevelFromStorage()
}

function shouldLog(level: LogLevel): boolean {
  return LEVEL_ORDER[level] >= LEVEL_ORDER[currentLevel]
}

function push(level: LogLevel, category: string, message: string) {
  if (!shouldLog(level)) return
  const entry: LogEntry = { id: ++seq, ts: Date.now(), level, category, message }
  entries.value.push(entry)
  if (entries.value.length > MAX_ENTRIES) {
    entries.value.splice(0, entries.value.length - MAX_ENTRIES)
  }
  // 镜像到 console
  const fn = level === 'error' ? console.error : level === 'warn' ? console.warn : level === 'debug' ? console.debug : console.info
  fn(`[${category}] ${message}`)
}

export const logger = {
  debug: (category: string, message: string) => push('debug', category, message),
  info: (category: string, message: string) => push('info', category, message),
  warn: (category: string, message: string) => push('warn', category, message),
  error: (category: string, message: string) => push('error', category, message)
}

export function useLogEntries() {
  return entries
}

// 连接状态：健康检查结果
export const connectionStatus = ref<'unknown' | 'ok' | 'fail'>('unknown')
export const lastConnectionAt = ref<number | null>(null)

export async function checkConnection() {
  try {
    const res = await fetch('/health')
    if (res.ok) {
      connectionStatus.value = 'ok'
      lastConnectionAt.value = Date.now()
      logger.info('conn', '后端健康检查成功')
    } else {
      connectionStatus.value = 'fail'
      logger.warn('conn', `后端健康检查返回 ${res.status}`)
    }
  } catch (e) {
    connectionStatus.value = 'fail'
    logger.error('conn', e instanceof Error ? e.message : '后端不可达')
  }
}
