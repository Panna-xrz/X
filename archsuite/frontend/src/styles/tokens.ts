// 设计令牌集中管理：色彩、字体、间距、圆角、阴影等

// 无边框常量：用于覆盖组件边框为透明，体现现代扁平风格
export const BORDER_NONE = '1px solid transparent'

// 亮色色板（精炼靛蓝主色 + 中性灰，规避廉价默认蓝）
export const lightPalette = {
  primary: '#3457d5',
  primaryHover: '#4566e0',
  primaryPressed: '#2a49c0',
  primarySuppl: '#3457d5',
  info: '#3457d5',
  success: '#1f9d6b',
  warning: '#d68a1f',
  error: '#c8344e',
  textBase: '#1f2329',
  text1: '#3b3f45',
  text2: '#6a6f76',
  text3: '#9aa0a8',
  background: '#ffffff',
  bodyBackground: '#f5f6f8',
  cardBackground: '#ffffff',
  modalBackground: '#ffffff',
  popoverBackground: '#ffffff',
  tableHeaderBackground: '#f7f8fa',
  inputBackground: '#ffffff',
  borderColor: 'transparent',
  dividerColor: '#ecedf1'
}

// 暗色色板（同源靛蓝，暗背适配）
export const darkPalette = {
  primary: '#5b78ec',
  primaryHover: '#6f8af0',
  primaryPressed: '#4a66d4',
  primarySuppl: '#5b78ec',
  info: '#5b78ec',
  success: '#3ec98a',
  warning: '#e6a23c',
  error: '#e88a9a',
  textBase: '#ffffffd9',
  text1: '#ffffffc0',
  text2: '#ffffff80',
  text3: '#ffffff52',
  background: '#101014',
  bodyBackground: '#0b0c0f',
  cardBackground: '#16171b',
  modalBackground: '#181a1f',
  popoverBackground: '#1c1d22',
  tableHeaderBackground: '#1e1f24',
  inputBackground: '#1a1b1f',
  borderColor: 'transparent',
  dividerColor: '#26272d'
}

// 字体族候选列表
export const fontFamilyCandidates = [
  { label: '默认系统字体', value: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif' },
  { label: '思源黑体', value: '"Source Han Sans SC", "Noto Sans SC", sans-serif' },
  { label: '等宽字体', value: '"JetBrains Mono", "Fira Code", Consolas, monospace' },
  { label: '微软雅黑', value: '"Microsoft YaHei", "PingFang SC", sans-serif' }
]

// 字号梯度（px）
export const fontSizeScale = {
  xs: 12,
  sm: 13,
  base: 14,
  md: 15,
  lg: 16,
  xl: 18,
  xxl: 22,
  display: 28
}

// 间距梯度（px）
export const spacingScale = {
  xxs: 2,
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48
}

// 圆角梯度（px）
export const borderRadiusScale = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  pill: 999
}

// 阴影
export const shadows = {
  light: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.04)',
    md: '0 2px 8px rgba(0, 0, 0, 0.06)',
    lg: '0 6px 24px rgba(0, 0, 0, 0.08)'
  },
  dark: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.4)',
    md: '0 2px 8px rgba(0, 0, 0, 0.5)',
    lg: '0 6px 24px rgba(0, 0, 0, 0.6)'
  }
}

// 设计令牌聚合导出
export const designTokens = {
  borderNone: BORDER_NONE,
  light: lightPalette,
  dark: darkPalette,
  fontFamilyCandidates,
  fontSize: fontSizeScale,
  spacing: spacingScale,
  borderRadius: borderRadiusScale,
  shadow: shadows
} as const

export type ThemeName = 'light' | 'dark'
