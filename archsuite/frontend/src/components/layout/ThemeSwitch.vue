<script setup lang="ts">
import { computed } from 'vue'
import {
  NButton,
  NPopover,
  NColorPicker,
  NSelect,
  NSlider,
  NSpace,
  NDivider,
  NSwitch
} from 'naive-ui'
import { useThemeStore } from '@/stores/theme'
import { fontFamilyCandidates, borderRadiusScale } from '@/styles/tokens'

// 主题切换：亮/暗按钮 + 气泡内主色/字体/字号/圆角实时调整
const themeStore = useThemeStore()

const isDark = computed<boolean>({
  get: () => themeStore.isDark,
  set: (val: boolean) => themeStore.setTheme(val ? 'dark' : 'light')
})

// 主色选择
function handlePrimaryColor(color: string) {
  themeStore.setPrimaryColor(color)
}

// 字体选择
const fontOptions = fontFamilyCandidates.map((f) => ({ label: f.label, value: f.value }))
function handleFont(value: string) {
  themeStore.setFontFamily(value)
}

// 字号选择
function handleFontSize(value: number) {
  themeStore.setFontSize(value)
}

// 圆角选择
function handleRadius(value: number) {
  themeStore.setBorderRadius(value)
}

// 暗色按钮文字
const darkLabel = computed(() => (themeStore.isDark ? '暗色' : '亮色'))
</script>

<template>
  <NPopover trigger="click" placement="bottom-end" :width="280">
    <template #trigger>
      <NButton size="small" secondary @click="themeStore.toggleDark">
        {{ darkLabel }}
      </NButton>
    </template>

    <NSpace vertical :size="12" style="padding: 4px 0">
      <div class="row">
        <span class="label">暗色模式</span>
        <NSwitch v-model:value="isDark" size="small" />
      </div>

      <NDivider style="margin: 4px 0" />

      <div class="row">
        <span class="label">主色调</span>
        <NColorPicker
          :value="themeStore.primaryColor"
          size="small"
          :show-alpha="false"
          @update:value="handlePrimaryColor"
        />
      </div>

      <div class="row">
        <span class="label">字体族</span>
        <NSelect
          :value="themeStore.fontFamily"
          :options="fontOptions"
          size="small"
          @update:value="handleFont"
        />
      </div>

      <div class="row column">
        <div class="label-row">
          <span class="label">字号</span>
          <span class="value">{{ themeStore.fontSize }}px</span>
        </div>
        <NSlider
          :value="themeStore.fontSize"
          :min="12"
          :max="18"
          :step="1"
          @update:value="handleFontSize"
        />
      </div>

      <div class="row column">
        <div class="label-row">
          <span class="label">圆角</span>
          <span class="value">{{ themeStore.borderRadius }}px</span>
        </div>
        <NSlider
          :value="themeStore.borderRadius"
          :min="borderRadiusScale.none"
          :max="borderRadiusScale.xl"
          :step="1"
          @update:value="handleRadius"
        />
      </div>
    </NSpace>
  </NPopover>
</template>

<style scoped lang="scss">
.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;

  &.column {
    flex-direction: column;
    align-items: stretch;
  }

  .label {
    font-size: 0.93em;
    color: var(--app-text-2);
    white-space: nowrap;
  }

  .label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .value {
      font-size: 0.86em;
      color: var(--app-text-3);
    }
  }
}
</style>
