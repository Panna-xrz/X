<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSpace,
  NSwitch,
  NTag,
  NSelect,
  NColorPicker,
  NSlider,
  NAlert,
  useMessage
} from 'naive-ui'
import { useThemeStore } from '@/stores/theme'
import { fontFamilyCandidates, borderRadiusScale } from '@/styles/tokens'

// 设置页：主题切换 / 高德地图 Key / AI 提供商展示
const themeStore = useThemeStore()
const message = useMessage()

// localStorage 键
const AMAP_KEY_STORAGE = 'archsuite_amap_key'
const AI_PROVIDER_STORAGE = 'archsuite_ai_provider'

const amapKey = ref(localStorage.getItem(AMAP_KEY_STORAGE) || '')
const aiProvider = ref(localStorage.getItem(AI_PROVIDER_STORAGE) || 'openai')

const fontOptions = fontFamilyCandidates.map((f) => ({ label: f.label, value: f.value }))

const isDark = computed<boolean>({
  get: () => themeStore.isDark,
  set: (val: boolean) => themeStore.setTheme(val ? 'dark' : 'light')
})

const aiProviderOptions = [
  { label: 'OpenAI（默认）', value: 'openai' },
  { label: 'Anthropic Claude', value: 'anthropic' },
  { label: '通义千问', value: 'qwen' },
  { label: 'DeepSeek', value: 'deepseek' }
]

function saveAmapKey() {
  if (!amapKey.value.trim()) {
    localStorage.removeItem(AMAP_KEY_STORAGE)
    message.success('已清除高德地图 Key（将使用占位符）')
    return
  }
  localStorage.setItem(AMAP_KEY_STORAGE, amapKey.value.trim())
  message.success('高德地图 Key 已保存，刷新地图后生效')
}

function saveAiProvider() {
  localStorage.setItem(AI_PROVIDER_STORAGE, aiProvider.value)
  message.success('AI 提供商已保存')
}
</script>

<template>
  <div class="settings-view">
    <div class="page-header">
      <h2 class="title">设置</h2>
    </div>

    <NCard title="主题设置" :bordered="false" size="small" style="margin-bottom: 16px">
      <NForm label-placement="left" label-width="120">
        <NFormItem label="深色模式">
          <NSwitch v-model:value="isDark" />
        </NFormItem>
        <NFormItem label="主色调">
          <NColorPicker
            :value="themeStore.primaryColor"
            :show-alpha="false"
            @update:value="(v: string) => themeStore.setPrimaryColor(v)"
          />
        </NFormItem>
        <NFormItem label="字体族">
          <NSelect
            :value="themeStore.fontFamily"
            :options="fontOptions"
            @update:value="(v: string) => themeStore.setFontFamily(v)"
          />
        </NFormItem>
        <NFormItem label="字号">
          <div class="slider-row">
            <NSlider
              :value="themeStore.fontSize"
              :min="12"
              :max="18"
              :step="1"
              @update:value="(v: number) => themeStore.setFontSize(v)"
            />
            <span class="slider-value">{{ themeStore.fontSize }}px</span>
          </div>
        </NFormItem>
        <NFormItem label="圆角">
          <div class="slider-row">
            <NSlider
              :value="themeStore.borderRadius"
              :min="borderRadiusScale.none"
              :max="borderRadiusScale.xl"
              :step="1"
              @update:value="(v: number) => themeStore.setBorderRadius(v)"
            />
            <span class="slider-value">{{ themeStore.borderRadius }}px</span>
          </div>
        </NFormItem>
      </NForm>
    </NCard>

    <NCard title="高德地图配置" :bordered="false" size="small" style="margin-bottom: 16px">
      <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
        地图组件将从此处读取 Key。留空则使用占位符 YOUR_AMAP_KEY（地图功能不可用）。
      </NAlert>
      <NForm label-placement="left" label-width="120">
        <NFormItem label="高德 Key">
          <NInput
            v-model:value="amapKey"
            placeholder="如：a1b2c3d4e5f6g7h8i9j0..."
            type="password"
            show-password-on="click"
          />
        </NFormItem>
      </NForm>
      <NSpace justify="end">
        <NButton type="primary" @click="saveAmapKey">保存 Key</NButton>
      </NSpace>
    </NCard>

    <NCard title="AI 提供商" :bordered="false" size="small">
      <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
        AI 提供商为后端配置项，此处仅展示当前生效项。如需切换请联系后端管理员。
      </NAlert>
      <NForm label-placement="left" label-width="120">
        <NFormItem label="当前提供商">
          <NSelect
            v-model:value="aiProvider"
            :options="aiProviderOptions"
            @update:value="saveAiProvider"
          />
        </NFormItem>
        <NFormItem label="生效状态">
          <NTag type="success" size="small" round>已启用</NTag>
        </NFormItem>
      </NForm>
    </NCard>
  </div>
</template>

<style scoped lang="scss">
.settings-view {
  padding: 16px 20px;
  max-width: 720px;
  margin: 0 auto;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 12px;

  .title {
    font-size: 18px;
    font-weight: 600;
    color: var(--app-text-1);
    margin: 0;
  }
}

.slider-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;

  .slider-value {
    font-size: 12px;
    color: var(--app-text-3);
    min-width: 40px;
    text-align: right;
  }
}
</style>
