<script setup lang="ts">
import { computed } from 'vue'
import {
  NConfigProvider,
  NMessageProvider,
  NDialogProvider,
  NLoadingBarProvider,
  darkTheme,
  zhCN,
  dateZhCN
} from 'naive-ui'
import type { GlobalTheme, GlobalThemeOverrides } from 'naive-ui'
import { useThemeStore } from '@/stores/theme'
import { generateThemeOverrides } from '@/styles/theme'
import AppLayout from '@/components/layout/AppLayout.vue'

// 根组件：用 NConfigProvider 注入主题与全局覆盖
const themeStore = useThemeStore()

// 当前主题对象：暗色返回 darkTheme，亮色返回 null
const theme = computed<GlobalTheme | null>(() => (themeStore.isDark ? darkTheme : null))

// 主题覆盖：去边框、统一主色/圆角/字体
const themeOverrides = computed<GlobalThemeOverrides>(() =>
  generateThemeOverrides(themeStore.$state)
)
</script>

<template>
  <NConfigProvider
    :theme="theme"
    :theme-overrides="themeOverrides"
    :locale="zhCN"
    :date-locale="dateZhCN"
  >
    <NLoadingBarProvider>
      <NMessageProvider>
        <NDialogProvider>
          <AppLayout />
        </NDialogProvider>
      </NMessageProvider>
    </NLoadingBarProvider>
  </NConfigProvider>
</template>
