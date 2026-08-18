import { defineStore } from 'pinia'
import type { ThemeState } from '@/styles/theme'
import { fontFamilyCandidates } from '@/styles/tokens'

// localStorage 持久化键
const STORAGE_KEY = 'archsuite_theme'

// 主题状态默认值
const defaultState: ThemeState = {
  themeName: 'light',
  primaryColor: '#2080f0',
  fontFamily: fontFamilyCandidates[0].value,
  fontSize: 14,
  borderRadius: 8,
  isDark: false
}

// 从 localStorage 读取并合并默认值
function loadState(): ThemeState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { ...defaultState }
    const parsed = JSON.parse(raw) as Partial<ThemeState>
    return { ...defaultState, ...parsed }
  } catch {
    return { ...defaultState }
  }
}

// 写入 localStorage
function persist(state: ThemeState): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  } catch (e) {
    console.error('[theme persist]', e)
  }
}

// 主题 Store：支持运行时切换亮/暗、主色、字体族、字号、圆角
export const useThemeStore = defineStore('theme', {
  state: (): ThemeState => loadState(),
  getters: {
    // 是否为暗色
    isDarkMode: (state): boolean => state.isDark
  },
  actions: {
    // 切换主题：light / dark
    setTheme(name: 'light' | 'dark') {
      this.themeName = name
      this.isDark = name === 'dark'
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置主色
    setPrimaryColor(color: string) {
      this.primaryColor = color
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置字体族
    setFontFamily(family: string) {
      this.fontFamily = family
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置字号
    setFontSize(size: number) {
      this.fontSize = size
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置圆角
    setBorderRadius(radius: number) {
      this.borderRadius = radius
      this.syncRootAttr()
      persist(this.$state)
    },
    // 切换亮/暗
    toggleDark() {
      this.setTheme(this.isDark ? 'light' : 'dark')
    },
    // 同步到根元素 CSS 变量与 data-theme 属性，供全局 SCSS 使用
    syncRootAttr() {
      const root = document.documentElement
      root.dataset.theme = this.isDark ? 'dark' : 'light'
      root.style.setProperty('--app-primary', this.primaryColor)
      root.style.setProperty('--app-font-family', this.fontFamily)
      root.style.setProperty('--app-font-size', `${this.fontSize}px`)
      root.style.setProperty('--app-radius', `${this.borderRadius}px`)
    }
  }
})
