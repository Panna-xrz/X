// 设计令牌集中管理：色彩、字体、间距、圆角、阴影等
// 体系说明：
// - 背景按"4 层"组织，避免依赖分割线，用层次差异分层
//   L1 page  : 页面底色（最浅）
//   L2 card  : 主卡片底色
//   L3 panel : 次级面板/卡片内分组/表头底色
//   L4 inset : 内嵌最深（输入框、表格斑马、高亮区）
// - 字号"4 种"梯度，单字体族
//   xs   : 辅助/标签
//   sm   : 次要正文/说明
//   base : 主正文
//   lg   : 区块标题

// 无边框常量：用于覆盖组件边框为透明，体现现代扁平风格
export const BORDER_NONE = '1px solid transparent'

// 亮色色板（精炼靛蓝主色 + 4 层中性灰，规避廉价默认蓝）
export const lightPalette = {
  primary: '#3457d5',
  primaryHover: '#4566e0',
  primaryPressed: '#2a49c0',
  primarySuppl: '#3457d5',
  info: '#3457d5',
  success: '#1f9d6b',
  warning: '#d68a1f',
  error: '#c8344e',
  // 文本
  textBase: '#1f2329',
  text1: '#3b3f45',
  text2: '#6a6f76',
  text3: '#9aa0a8',
  // 4 层背景
  surfacePage: '#f4f5f7',
  surfaceCard: '#ffffff',
  surfacePanel: '#fafbfc',
  surfaceInset: '#eef0f3',
  // 兼容旧字段（指向对应 surface）
  background: '#ffffff',
  bodyBackground: '#f4f5f7',
  cardBackground: '#ffffff',
  modalBackground: '#ffffff',
  popoverBackground: '#ffffff',
  tableHeaderBackground: '#fafbfc',
  inputBackground: '#eef0f3',
  borderColor: 'transparent',
  dividerColor: 'transparent'
}

// 暗色色板（同源靛蓝，4 层暗灰，暗背适配）
export const darkPalette = {
  primary: '#5b78ec',
  primaryHover: '#6f8af0',
  primaryPressed: '#4a66d4',
  primarySuppl: '#5b78ec',
  info: '#5b78ec',
  success: '#3ec98a',
  warning: '#e6a23c',
  error: '#e88a9a',
  // 文本
  textBase: '#ffffffd9',
  text1: '#ffffffc0',
  text2: '#ffffff80',
  text3: '#ffffff52',
  // 4 层背景（暗色由浅到深）
  surfacePage: '#0d0e11',
  surfaceCard: '#16171b',
  surfacePanel: '#1c1d22',
  surfaceInset: '#23252b',
  // 兼容旧字段
  background: '#16171b',
  bodyBackground: '#0d0e11',
  cardBackground: '#16171b',
  modalBackground: '#181a1f',
  popoverBackground: '#1c1d22',
  tableHeaderBackground: '#1c1d22',
  inputBackground: '#23252b',
  borderColor: 'transparent',
  dividerColor: 'transparent'
}

// 字体族候选列表（单一字体族理念：用户在面板选择字体）
export const fontFamilyCandidates = [
  { label: '默认系统字体', value: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif' },
  { label: '思源黑体', value: '"Source Han Sans SC", "Noto Sans SC", sans-serif' },
  { label: '等宽字体', value: '"JetBrains Mono", "Fira Code", Consolas, monospace' },
  { label: '微软雅黑', value: '"Microsoft YaHei", "PingFang SC", sans-serif' }
]

// 字号梯度（px）：4 种核心字号
export const fontSizeScale = {
  xs: 12, // 辅助/标签
  sm: 13, // 次要正文
  base: 14, // 主正文
  lg: 16 // 区块标题
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
  sm: 6,
  md: 10,
  lg: 12,
  xl: 16,
  pill: 999
}

// 阴影
export const shadows = {
  light: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.04)',
    md: '0 2px 8px rgba(0, 0, 0, 0.06)',
    lg: '0 8px 28px rgba(0, 0, 0, 0.10)'
  },
  dark: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.4)',
    md: '0 2px 8px rgba(0, 0, 0, 0.5)',
    lg: '0 8px 28px rgba(0, 0, 0, 0.6)'
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
