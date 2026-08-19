import { defineStore } from 'pinia'
import type { ThemeState } from '@/styles/theme'
import { darkPalette, fontFamilyCandidates, lightPalette, shadows } from '@/styles/tokens'

// localStorage 持久化键
const STORAGE_KEY = 'archsuite_theme'

// 主题状态默认值
const defaultState: ThemeState = {
  themeName: 'light',
  primaryColor: '#3457d5',
  fontFamily: fontFamilyCandidates[0].value,
  fontSize: 14,
  borderRadius: 8,
  isDark: false,
  compactness: 1.0,
  contentMaxWidth: 'full'
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
    // 设置界面紧凑度（间距倍数）
    setCompactness(val: number) {
      this.compactness = val
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置内容区最大宽度
    setContentMaxWidth(val: string) {
      this.contentMaxWidth = val
      this.syncRootAttr()
      persist(this.$state)
    },
    // 重置为默认主题
    resetToDefaults() {
      this.$state = { ...defaultState }
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
      const dark = this.isDark
      const pal = dark ? darkPalette : lightPalette
      const sh = dark ? shadows.dark : shadows.light
      root.dataset.theme = dark ? 'dark' : 'light'
      // 用户可调项
      root.style.setProperty('--app-primary', this.primaryColor)
      root.style.setProperty('--app-font-family', this.fontFamily)
      root.style.setProperty('--app-font-size', `${this.fontSize}px`)
      root.style.setProperty('--app-radius', `${this.borderRadius}px`)
      root.style.setProperty('--app-compactness', `${this.compactness}`)
      root.style.setProperty('--app-content-max-width', this.contentMaxWidth)
      // 色板项（跟随亮/暗）
      root.style.setProperty('--app-bg', pal.bodyBackground)
      root.style.setProperty('--app-card-bg', pal.cardBackground)
      root.style.setProperty('--app-text-1', pal.text1)
      root.style.setProperty('--app-text-2', pal.text2)
      root.style.setProperty('--app-text-3', pal.text3)
      root.style.setProperty('--app-divider', pal.dividerColor)
      root.style.setProperty('--app-shadow-sm', sh.sm)
      root.style.setProperty('--app-shadow-md', sh.md)
      root.style.setProperty('--app-shadow-lg', sh.lg)
      // 侧边栏专用令牌（保持深色侧栏风格）
      root.style.setProperty('--app-rail-bg', dark ? '#1a1a1e' : '#1f1f23')
      root.style.setProperty('--app-rail-text', dark ? '#ffffffa6' : '#ffffffa6')
      root.style.setProperty('--app-rail-text-hover', dark ? '#ffffffd9' : '#ffffffd9')
      root.style.setProperty('--app-rail-text-active', '#ffffff')
      root.style.setProperty('--app-rail-border', 'rgba(255, 255, 255, 0.06)')
      root.style.setProperty('--app-rail-hover-bg', 'rgba(255, 255, 255, 0.08)')
    }
  }
})
