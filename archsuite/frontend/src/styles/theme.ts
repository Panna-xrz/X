import type { GlobalThemeOverrides } from 'naive-ui'
import { designTokens, BORDER_NONE } from './tokens'

// 主题 Store 状态结构（与 src/stores/theme.ts 对齐）
export interface ThemeState {
  themeName: 'light' | 'dark'
  primaryColor: string
  fontFamily: string
  // 4 种字号（用户可在设置面板独立调节）
  fontSizeXs: number // 辅助/标签
  fontSizeSm: number // 次要正文
  fontSizeBase: number // 主正文（= legacy fontSize，向下兼容）
  fontSizeLg: number // 区块标题
  // legacy 兼容字段（指向 fontSizeBase）
  fontSize: number
  borderRadius: number
  isDark: boolean
  // 界面紧凑度（间距倍数，0.8 ~ 1.2）
  compactness: number
  // 内容区最大宽度：'full' | '1280' | '1440' | '1600'
  contentMaxWidth: string
  // 4 层背景色（用户可在设置面板独立调节，覆盖默认色板）
  surfacePage: string | null
  surfaceCard: string | null
  surfacePanel: string | null
  surfaceInset: string | null
}

// 根据主题状态生成 Naive UI 全局主题覆盖
// 1) 覆盖 common：主色、圆角、字号、字体族、4 层背景
// 2) 覆盖 Card/Form/Tag 等组件，体现扁平无边框风格（无分割线，靠层次区分）
export function generateThemeOverrides(state: ThemeState): GlobalThemeOverrides {
  const palette = state.isDark ? designTokens.dark : designTokens.light

  // 解析 4 层背景：用户覆盖优先，否则用色板默认
  const surfacePage = state.surfacePage || palette.surfacePage
  const surfaceCard = state.surfaceCard || palette.surfaceCard
  const surfacePanel = state.surfacePanel || palette.surfacePanel
  const surfaceInset = state.surfaceInset || palette.surfaceInset

  const overrides: GlobalThemeOverrides = {
    common: {
      primaryColor: state.primaryColor,
      primaryColorHover: shade(state.primaryColor, 0.12),
      primaryColorPressed: shade(state.primaryColor, -0.12),
      primaryColorSuppl: state.primaryColor,
      infoColor: state.primaryColor,
      infoColorHover: shade(state.primaryColor, 0.12),
      infoColorPressed: shade(state.primaryColor, -0.12),
      borderRadius: `${state.borderRadius}px`,
      borderRadiusSmall: `${Math.max(4, state.borderRadius - 4)}px`,
      // 4 种字号
      fontSize: `${state.fontSizeBase}px`,
      fontSizeSmall: `${state.fontSizeSm}px`,
      fontSizeTiny: `${state.fontSizeXs}px`,
      fontSizeLarge: `${state.fontSizeLg}px`,
      fontFamily: state.fontFamily,
      fontWeight: '400',
      // 4 层背景映射到 Naive common
      bodyColor: surfacePage,
      cardColor: surfaceCard,
      modalColor: surfaceCard,
      popoverColor: surfacePanel,
      // 文本
      textColorBase: palette.textBase,
      textColor1: palette.text1,
      textColor2: palette.text2,
      textColor3: palette.text3,
      // 边框/分割线：透明（用层次差异分层，不依赖分割线）
      borderColor: 'transparent',
      dividerColor: 'transparent',
      tableHeaderColor: surfacePanel,
      inputColor: surfaceInset
    },
    Card: {
      // 卡片无边框，依赖背景与阴影分层
      borderColor: BORDER_NONE,
      color: surfaceCard,
      colorModal: surfaceCard,
      colorPopover: surfacePanel,
      borderRadius: `${state.borderRadius}px`
    },
    Form: {
      // 表单标签颜色
      labelTextColor: palette.text1
    },
    Tag: {
      // 标签无边框
      border: BORDER_NONE,
      borderRadius: `${Math.max(4, state.borderRadius - 2)}px`
    },
    Button: {
      // 按钮无边框（扁平风）
      border: BORDER_NONE,
      borderHover: BORDER_NONE,
      borderPressed: BORDER_NONE,
      borderFocus: BORDER_NONE,
      borderRadius: `${state.borderRadius}px`
    },
    Input: {
      // 输入框无边框，用内嵌最深层背景区分
      border: '1px solid transparent',
      borderHover: state.primaryColor,
      borderFocus: state.primaryColor,
      borderRadius: `${Math.max(4, state.borderRadius - 2)}px`,
      color: surfaceInset,
      colorFocus: surfaceInset
    },
    DataTable: {
      // 数据表格无边框，表头用 panel 层、斑马用 inset 层
      borderColor: BORDER_NONE,
      thColor: surfacePanel,
      thColorHover: surfacePanel,
      tdColor: surfaceCard,
      tdColorHover: surfaceInset,
      borderRadius: `${state.borderRadius}px`
    },
    Menu: {
      // 菜单无边框
      itemColorActive: state.isDark ? '#23252b' : '#eaeefb',
      itemColorActiveHover: state.isDark ? '#23252b' : '#eaeefb',
      itemColorActiveCollapsed: state.isDark ? '#23252b' : '#eaeefb',
      borderRadius: `${state.borderRadius}px`
    },
    Layout: {
      // 布局背景
      color: surfacePage,
      headerColor: surfaceCard,
      siderColor: surfaceCard
    },
    Modal: {
      // 弹窗无边框
      borderRadius: `${state.borderRadius}px`
    },
    Popover: {
      // 气泡无边框
      borderRadius: `${state.borderRadius}px`
    }
  }

  return overrides
}

// 简易颜色明度调节（不引入额外依赖）
// ratio 为正变亮，为负变暗；范围 -1 ~ 1
function shade(hex: string, ratio: number): string {
  const c = hex.replace('#', '')
  if (c.length !== 6) return hex
  const num = parseInt(c, 16)
  let r = (num >> 16) & 0xff
  let g = (num >> 8) & 0xff
  let b = num & 0xff
  const adj = (v: number) =>
    Math.min(255, Math.max(0, Math.round(ratio >= 0 ? v + (255 - v) * ratio : v * (1 + ratio))))
  r = adj(r)
  g = adj(g)
  b = adj(b)
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`
}
