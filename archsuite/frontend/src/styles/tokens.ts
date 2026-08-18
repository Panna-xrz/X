// 设计令牌集中管理：色彩、字体、间距、圆角、阴影等

// 无边框常量：用于覆盖组件边框为透明，体现现代扁平风格
export const BORDER_NONE = '1px solid transparent'

// 亮色色板
export const lightPalette = {
  primary: '#2080f0',
  primaryHover: '#4098fc',
  primaryPressed: '#0c7df0',
  primarySuppl: '#2080f0',
  info: '#2080f0',
  success: '#18a058',
  warning: '#f0a020',
  error: '#d03050',
  textBase: '#333639',
  text1: '#5a5a5a',
  text2: '#7d7d7d',
  text3: '#a0a0a0',
  background: '#ffffff',
  bodyBackground: '#f7f8fa',
  cardBackground: '#ffffff',
  modalBackground: '#ffffff',
  popoverBackground: '#ffffff',
  tableHeaderBackground: '#fafafa',
  inputBackground: '#ffffff',
  borderColor: 'transparent',
  dividerColor: '#efeff5'
}

// 暗色色板
export const darkPalette = {
  primary: '#2080f0',
  primaryHover: '#4098fc',
  primaryPressed: '#0c7df0',
  primarySuppl: '#2080f0',
  info: '#2080f0',
  success: '#18a058',
  warning: '#f0a020',
  error: '#e88080',
  textBase: '#ffffffd9',
  text1: '#ffffffa6',
  text2: '#ffffff7f',
  text3: '#ffffff52',
  background: '#101014',
  bodyBackground: '#0d0d10',
  cardBackground: '#18181c',
  modalBackground: '#18181c',
  popoverBackground: '#18181c',
  tableHeaderBackground: '#202024',
  inputBackground: '#18181c',
  borderColor: 'transparent',
  dividerColor: '#2c2c30'
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
