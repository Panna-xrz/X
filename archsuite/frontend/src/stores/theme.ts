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
  // 4 种字号
  fontSizeXs: 12,
  fontSizeSm: 13,
  fontSizeBase: 14,
  fontSizeLg: 16,
  fontSize: 14, // legacy
  borderRadius: 12,
  isDark: false,
  compactness: 1.0,
  contentMaxWidth: 'full',
  // 4 层背景：null 表示使用色板默认（切换主题时自动跟随）
  surfacePage: null,
  surfaceCard: null,
  surfacePanel: null,
  surfaceInset: null
}

// 从 localStorage 读取并合并默认值
function loadState(): ThemeState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { ...defaultState }
    const parsed = JSON.parse(raw) as Partial<ThemeState>
    const merged = { ...defaultState, ...parsed }
    // 同步 legacy fontSize -> fontSizeBase
    if (parsed.fontSize != null && parsed.fontSizeBase == null) {
      merged.fontSizeBase = parsed.fontSize
    }
    merged.fontSize = merged.fontSizeBase
    return merged
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

// 主题 Store：支持运行时切换亮/暗、主色、字体族、4 种字号、4 层背景、圆角
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
    // 设置 4 种字号（保持联动：xs < sm < base < lg）
    setFontSizeXs(v: number) {
      this.fontSizeXs = v
      this.syncRootAttr()
      persist(this.$state)
    },
    setFontSizeSm(v: number) {
      this.fontSizeSm = v
      this.syncRootAttr()
      persist(this.$state)
    },
    setFontSizeBase(v: number) {
      this.fontSizeBase = v
      this.fontSize = v // legacy
      this.syncRootAttr()
      persist(this.$state)
    },
    setFontSizeLg(v: number) {
      this.fontSizeLg = v
      this.syncRootAttr()
      persist(this.$state)
    },
    // 设置 4 层背景色（null=恢复色板默认）
    setSurfacePage(c: string | null) {
      this.surfacePage = c
      this.syncRootAttr()
      persist(this.$state)
    },
    setSurfaceCard(c: string | null) {
      this.surfaceCard = c
      this.syncRootAttr()
      persist(this.$state)
    },
    setSurfacePanel(c: string | null) {
      this.surfacePanel = c
      this.syncRootAttr()
      persist(this.$state)
    },
    setSurfaceInset(c: string | null) {
      this.surfaceInset = c
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
      root.style.setProperty('--app-radius', `${this.borderRadius}px`)
      root.style.setProperty('--app-compactness', `${this.compactness}`)
      root.style.setProperty('--app-content-max-width', this.contentMaxWidth)
      // 4 种字号
      root.style.setProperty('--app-font-size', `${this.fontSizeBase}px`)
      root.style.setProperty('--app-font-size-xs', `${this.fontSizeXs}px`)
      root.style.setProperty('--app-font-size-sm', `${this.fontSizeSm}px`)
      root.style.setProperty('--app-font-size-lg', `${this.fontSizeLg}px`)
      // 4 层背景（用户覆盖优先，否则用色板默认）
      const page = this.surfacePage || pal.surfacePage
      const card = this.surfaceCard || pal.surfaceCard
      const panel = this.surfacePanel || pal.surfacePanel
      const inset = this.surfaceInset || pal.surfaceInset
      root.style.setProperty('--app-bg', page)
      root.style.setProperty('--app-bg-page', page)
      root.style.setProperty('--app-card-bg', card)
      root.style.setProperty('--app-panel-bg', panel)
      root.style.setProperty('--app-inset-bg', inset)
      // 文本色（跟随亮/暗）
      root.style.setProperty('--app-text-1', pal.text1)
      root.style.setProperty('--app-text-2', pal.text2)
      root.style.setProperty('--app-text-3', pal.text3)
      // 分割线：透明（用层次差异分层）
      root.style.setProperty('--app-divider', 'transparent')
      // 阴影
      root.style.setProperty('--app-shadow-sm', sh.sm)
      root.style.setProperty('--app-shadow-md', sh.md)
      root.style.setProperty('--app-shadow-lg', sh.lg)
      // 侧边栏（rail）专用令牌：浅色模式浅色、深色模式深色
      // - 底色用 surfaceCard 同色（浅色=白、深色=深灰），与主内容区一致
      // - 文本/悬停/激活态在浅色下用深字（侧栏仍可读），暗色下用浅字
      root.style.setProperty('--app-rail-bg', card)
      root.style.setProperty('--app-rail-border', 'transparent')
      root.style.setProperty('--app-rail-hover-bg', inset)
      if (dark) {
        root.style.setProperty('--app-rail-text', '#ffffffa6')
        root.style.setProperty('--app-rail-text-hover', '#ffffffd9')
        root.style.setProperty('--app-rail-text-active', '#ffffff')
      } else {
        root.style.setProperty('--app-rail-text', '#6a6f76')
        root.style.setProperty('--app-rail-text-hover', '#3b3f45')
        root.style.setProperty('--app-rail-text-active', '#1f2329')
      }
    }
  }
})
