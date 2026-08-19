import type { GlobalThemeOverrides } from 'naive-ui'
import { designTokens, BORDER_NONE } from './tokens'

// 主题 Store 状态结构（与 src/stores/theme.ts 对齐）
export interface ThemeState {
  themeName: 'light' | 'dark'
  primaryColor: string
  fontFamily: string
  fontSize: number
  borderRadius: number
  isDark: boolean
  // 界面紧凑度（间距倍数，0.8 ~ 1.2）
  compactness: number
  // 内容区最大宽度：'full' | '1280' | '1440' | '1600'
  contentMaxWidth: string
}

// 根据主题状态生成 Naive UI 全局主题覆盖
// 1) 覆盖 common：主色、圆角、字号、字体族
// 2) 覆盖 Card/Form/Tag 等组件，体现扁平无边框风格
export function generateThemeOverrides(state: ThemeState): GlobalThemeOverrides {
  const palette = state.isDark ? designTokens.dark : designTokens.light

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
      borderRadiusSmall: `${Math.max(2, state.borderRadius - 2)}px`,
      fontSize: `${state.fontSize}px`,
      fontSizeSmall: `${Math.max(12, state.fontSize - 1)}px`,
      fontFamily: state.fontFamily,
      fontWeight: '400',
      bodyColor: palette.bodyBackground,
      cardColor: palette.cardBackground,
      modalColor: palette.modalBackground,
      popoverColor: palette.popoverBackground,
      textColorBase: palette.textBase,
      textColor1: palette.text1,
      textColor2: palette.text2,
      textColor3: palette.text3,
      borderColor: palette.borderColor,
      dividerColor: palette.dividerColor,
      tableHeaderColor: palette.tableHeaderBackground,
      inputColor: palette.inputBackground
    },
    Card: {
      // 卡片无边框，依赖背景与阴影分层
      borderColor: BORDER_NONE,
      color: palette.cardBackground,
      colorModal: palette.cardBackground,
      colorPopover: palette.cardBackground,
      borderRadius: `${state.borderRadius}px`
    },
    Form: {
      // 表单标签颜色
      labelTextColor: palette.text1
    },
    Tag: {
      // 标签无边框
      border: BORDER_NONE,
      borderRadius: `${state.borderRadius}px`
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
      // 输入框边框弱化处理
      border: `1px solid ${state.isDark ? '#26272d' : '#ecedf1'}`,
      borderHover: state.primaryColor,
      borderFocus: state.primaryColor,
      borderRadius: `${state.borderRadius}px`,
      color: palette.inputBackground
    },
    DataTable: {
      // 数据表格无边框
      borderColor: BORDER_NONE,
      thColor: palette.tableHeaderBackground,
      thColorHover: palette.tableHeaderBackground,
      tdColor: palette.cardBackground,
      tdColorHover: state.isDark ? '#1e1f24' : '#f7f8fa',
      borderRadius: `${state.borderRadius}px`
    },
    Menu: {
      // 菜单无边框
      itemColorActive: state.isDark ? '#1e1f24' : '#eaeefb',
      itemColorActiveHover: state.isDark ? '#1e1f24' : '#eaeefb',
      itemColorActiveCollapsed: state.isDark ? '#1e1f24' : '#eaeefb',
      borderRadius: `${state.borderRadius}px`
    },
    Layout: {
      // 布局背景
      color: palette.bodyBackground,
      headerColor: palette.cardBackground,
      siderColor: palette.cardBackground
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
