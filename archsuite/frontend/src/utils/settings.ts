// 设置读写工具：聚合到 localStorage 'archsuite_settings' JSON 对象
const SETTINGS_STORAGE = 'archsuite_settings'

export function readSetting(key: string, def: string): string {
  try {
    const raw = localStorage.getItem(SETTINGS_STORAGE)
    if (!raw) return def
    const obj = JSON.parse(raw) as Record<string, string>
    return obj[key] ?? def
  } catch {
    return def
  }
}

export function writeSetting(key: string, val: string): void {
  let obj: Record<string, string> = {}
  try {
    const raw = localStorage.getItem(SETTINGS_STORAGE)
    if (raw) obj = JSON.parse(raw) as Record<string, string>
  } catch {
    obj = {}
  }
  obj[key] = val
  localStorage.setItem(SETTINGS_STORAGE, JSON.stringify(obj))
  // 通知监听者（设置变更触发调度器重建等）
  window.dispatchEvent(new CustomEvent('archsuite-settings-changed', { detail: { key, val } }))
}

export const SETTINGS_STORAGE_KEY = SETTINGS_STORAGE
