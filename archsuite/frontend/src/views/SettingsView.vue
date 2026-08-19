<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  NTabs,
  NTabPane,
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
  NPopconfirm,
  NDivider,
  useMessage
} from 'naive-ui'
import { useThemeStore } from '@/stores/theme'
import { fontFamilyCandidates, borderRadiusScale } from '@/styles/tokens'

// 设置页：基本设置 / 界面设置 / LLM / 运行时 / 关于 / 清理
const themeStore = useThemeStore()
const message = useMessage()

// localStorage 键
const AMAP_KEY_STORAGE = 'archsuite_amap_key'
const AI_PROVIDER_STORAGE = 'archsuite_ai_provider'
const AI_APIKEY_STORAGE = 'archsuite_ai_apikey'
const AI_BASEURL_STORAGE = 'archsuite_ai_baseurl'
const AI_MODEL_STORAGE = 'archsuite_ai_model'
const SETTINGS_STORAGE = 'archsuite_settings'

// 通用设置读写（聚合到单个 JSON 对象）
function readSetting(key: string, def: string): string {
  try {
    const raw = localStorage.getItem(SETTINGS_STORAGE)
    if (!raw) return def
    const obj = JSON.parse(raw) as Record<string, string>
    return obj[key] ?? def
  } catch {
    return def
  }
}
function writeSetting(key: string, val: string): void {
  let obj: Record<string, string> = {}
  try {
    const raw = localStorage.getItem(SETTINGS_STORAGE)
    if (raw) obj = JSON.parse(raw) as Record<string, string>
  } catch {
    obj = {}
  }
  obj[key] = val
  localStorage.setItem(SETTINGS_STORAGE, JSON.stringify(obj))
}

// ---------- 基本设置 ----------
const defaultPhase = ref(readSetting('defaultPhase', '概念设计'))
const autoSaveInterval = ref(Number(readSetting('autoSaveInterval', '30')))
const refreshInterval = ref(Number(readSetting('refreshInterval', '60')))
const amapKey = ref(localStorage.getItem(AMAP_KEY_STORAGE) || '')

const phaseOptions = [
  { label: '概念设计', value: '概念设计' },
  { label: '方案设计', value: '方案设计' },
  { label: '初步设计', value: '初步设计' },
  { label: '施工图设计', value: '施工图设计' },
  { label: '施工配合', value: '施工配合' },
  { label: '竣工', value: '竣工' }
]

function saveBasicSettings() {
  writeSetting('defaultPhase', defaultPhase.value)
  writeSetting('autoSaveInterval', String(autoSaveInterval.value))
  writeSetting('refreshInterval', String(refreshInterval.value))
  message.success('基本设置已保存')
}

function saveAmapKey() {
  if (!amapKey.value.trim()) {
    localStorage.removeItem(AMAP_KEY_STORAGE)
    message.success('已清除高德地图 Key（将使用占位符）')
    return
  }
  localStorage.setItem(AMAP_KEY_STORAGE, amapKey.value.trim())
  message.success('高德地图 Key 已保存，刷新地图后生效')
}

// ---------- 界面设置 ----------
const isDark = computed<boolean>({
  get: () => themeStore.isDark,
  set: (val: boolean) => themeStore.setTheme(val ? 'dark' : 'light')
})

const presetSwatches = ['#3457d5', '#1f9d6b', '#7b61d6', '#d68a1f', '#c8344e']

const fontOptions = fontFamilyCandidates.map((f) => ({ label: f.label, value: f.value }))

const contentMaxWidthOptions = [
  { label: '满屏', value: 'full' },
  { label: '1280px', value: '1280' },
  { label: '1440px', value: '1440' },
  { label: '1600px', value: '1600' }
]

// ---------- LLM API Key 设置 ----------
const aiProvider = ref(localStorage.getItem(AI_PROVIDER_STORAGE) || 'openai')
const aiApiKey = ref(localStorage.getItem(AI_APIKEY_STORAGE) || '')
const aiBaseUrl = ref(localStorage.getItem(AI_BASEURL_STORAGE) || '')
const aiModel = ref(localStorage.getItem(AI_MODEL_STORAGE) || '')
const llmSaved = ref(false)

watch([aiProvider, aiApiKey, aiBaseUrl, aiModel], () => {
  llmSaved.value = false
})

const aiProviderOptions = [
  { label: 'OpenAI', value: 'openai' },
  { label: 'Anthropic Claude', value: 'anthropic' },
  { label: '通义千问', value: 'qwen' },
  { label: 'DeepSeek', value: 'deepseek' }
]

function saveLlm() {
  localStorage.setItem(AI_PROVIDER_STORAGE, aiProvider.value)
  localStorage.setItem(AI_APIKEY_STORAGE, aiApiKey.value.trim())
  localStorage.setItem(AI_BASEURL_STORAGE, aiBaseUrl.value.trim())
  localStorage.setItem(AI_MODEL_STORAGE, aiModel.value.trim())
  llmSaved.value = true
  message.success('LLM 配置已保存')
}

function testConnection() {
  message.info('连接测试功能开发中，敬请期待')
}

// ---------- 运行时设置 ----------
const requestTimeout = ref(Number(readSetting('requestTimeout', '30')))
const aiTimeout = ref(Number(readSetting('aiTimeout', '120')))
const logLevel = ref(readSetting('logLevel', 'info'))

const logLevelOptions = [
  { label: 'Debug', value: 'debug' },
  { label: 'Info', value: 'info' },
  { label: 'Warn', value: 'warn' },
  { label: 'Error', value: 'error' }
]

function saveRuntimeSettings() {
  writeSetting('requestTimeout', String(requestTimeout.value))
  writeSetting('aiTimeout', String(aiTimeout.value))
  writeSetting('logLevel', logLevel.value)
  message.success('运行时设置已保存')
}

// ---------- 关于 ----------
const aboutInfo = {
  appName: 'ArchSuite 建筑设计管理平台',
  version: '0.1.0',
  techStack: 'Vue 3 + TypeScript + Naive UI + Pinia + Vite',
  license: 'MIT License'
}

// ---------- 清理 ----------
const PROTECTED_KEYS = ['archsuite_theme', 'archsuite_current_project_id']

function clearCache() {
  const keysToRemove: string[] = []
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k && !PROTECTED_KEYS.includes(k)) keysToRemove.push(k)
  }
  keysToRemove.forEach((k) => localStorage.removeItem(k))
  message.success('本地缓存已清除，正在刷新…')
  setTimeout(() => location.reload(), 600)
}

function resetAllSettings() {
  localStorage.clear()
  themeStore.resetToDefaults()
  message.success('所有设置已重置为默认，正在刷新…')
  setTimeout(() => location.reload(), 600)
}

function clearProjectData() {
  localStorage.removeItem('archsuite_current_project_id')
  message.success('本地项目数据已清除，正在刷新…')
  setTimeout(() => location.reload(), 600)
}
</script>

<template>
  <div class="settings-view">
    <div class="page-header">
      <h2 class="title">设置</h2>
    </div>

    <NTabs type="line" animated>
      <!-- 基本设置 -->
      <NTabPane name="basic" tab="基本设置">
        <NCard :bordered="false" size="small">
          <NForm label-placement="left" label-width="140">
            <NFormItem label="默认项目阶段">
              <NSelect v-model:value="defaultPhase" :options="phaseOptions" placeholder="请选择" />
            </NFormItem>
            <NFormItem label="自动保存间隔（秒）">
              <div class="slider-row">
                <NSlider v-model:value="autoSaveInterval" :min="10" :max="300" :step="5" />
                <span class="slider-value">{{ autoSaveInterval }}s</span>
              </div>
            </NFormItem>
            <NFormItem label="数据刷新间隔（秒）">
              <div class="slider-row">
                <NSlider v-model:value="refreshInterval" :min="10" :max="600" :step="10" />
                <span class="slider-value">{{ refreshInterval }}s</span>
              </div>
            </NFormItem>
          </NForm>
          <NSpace justify="end">
            <NButton type="primary" @click="saveBasicSettings">保存基本设置</NButton>
          </NSpace>

          <NDivider style="margin: 16px 0 12px" />
          <div class="sub-title">高德地图 Key</div>
          <NForm label-placement="left" label-width="140">
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
            <NButton @click="saveAmapKey">保存 Key</NButton>
          </NSpace>
        </NCard>
      </NTabPane>

      <!-- 界面设置 -->
      <NTabPane name="ui" tab="界面设置">
        <NCard :bordered="false" size="small">
          <NForm label-placement="left" label-width="140">
            <NFormItem label="深色模式">
              <NSwitch v-model:value="isDark" />
            </NFormItem>
            <NFormItem label="主色调">
              <NColorPicker
                :value="themeStore.primaryColor"
                :show-alpha="false"
                :swatches="presetSwatches"
                @update:value="(v: string) => themeStore.setPrimaryColor(v)"
              />
            </NFormItem>
            <NFormItem label="预设色板">
              <NSpace :size="8">
                <button
                  v-for="c in presetSwatches"
                  :key="c"
                  class="swatch-btn"
                  :style="{ background: c }"
                  :title="c"
                  @click="themeStore.setPrimaryColor(c)"
                />
              </NSpace>
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
            <NFormItem label="界面紧凑度">
              <div class="slider-row">
                <NSlider
                  :value="themeStore.compactness"
                  :min="0.8"
                  :max="1.2"
                  :step="0.05"
                  @update:value="(v: number) => themeStore.setCompactness(v)"
                />
                <span class="slider-value">{{ themeStore.compactness.toFixed(2) }}x</span>
              </div>
            </NFormItem>
            <NFormItem label="内容区最大宽度">
              <NSelect
                :value="themeStore.contentMaxWidth"
                :options="contentMaxWidthOptions"
                @update:value="(v: string) => themeStore.setContentMaxWidth(v)"
              />
            </NFormItem>
          </NForm>
        </NCard>
      </NTabPane>

      <!-- LLM API Key 设置 -->
      <NTabPane name="llm" tab="LLM API Key">
        <NCard :bordered="false" size="small">
          <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
            API Key 仅保存在本地浏览器 localStorage，不会上传服务器。请妥善保管。
          </NAlert>
          <NForm label-placement="left" label-width="140">
            <NFormItem label="AI 提供商">
              <NSelect v-model:value="aiProvider" :options="aiProviderOptions" />
            </NFormItem>
            <NFormItem label="API Key">
              <NInput
                v-model:value="aiApiKey"
                placeholder="sk-..."
                type="password"
                show-password-on="click"
              />
            </NFormItem>
            <NFormItem label="Base URL">
              <NInput
                v-model:value="aiBaseUrl"
                placeholder="可选，用于自定义端点（如 https://api.example.com/v1）"
              />
            </NFormItem>
            <NFormItem label="模型名称">
              <NInput v-model:value="aiModel" placeholder="如 gpt-4o, claude-3-sonnet" />
            </NFormItem>
          </NForm>
          <NSpace justify="end" align="center">
            <NTag v-if="llmSaved" type="success" size="small" round>已保存</NTag>
            <NButton @click="testConnection">测试连接</NButton>
            <NButton type="primary" @click="saveLlm">保存</NButton>
          </NSpace>
        </NCard>
      </NTabPane>

      <!-- 运行时设置 -->
      <NTabPane name="runtime" tab="运行时设置">
        <NCard :bordered="false" size="small">
          <NForm label-placement="left" label-width="140">
            <NFormItem label="请求超时（秒）">
              <div class="slider-row">
                <NSlider v-model:value="requestTimeout" :min="10" :max="120" :step="5" />
                <span class="slider-value">{{ requestTimeout }}s</span>
              </div>
            </NFormItem>
            <NFormItem label="AI 请求超时（秒）">
              <div class="slider-row">
                <NSlider v-model:value="aiTimeout" :min="30" :max="300" :step="10" />
                <span class="slider-value">{{ aiTimeout }}s</span>
              </div>
            </NFormItem>
            <NFormItem label="日志级别">
              <NSelect v-model:value="logLevel" :options="logLevelOptions" />
            </NFormItem>
          </NForm>
          <NSpace justify="end">
            <NButton type="primary" @click="saveRuntimeSettings">保存运行时设置</NButton>
          </NSpace>
        </NCard>
      </NTabPane>

      <!-- 关于 -->
      <NTabPane name="about" tab="关于">
        <NCard :bordered="false" size="small">
          <NForm label-placement="left" label-width="120">
            <NFormItem label="应用名称">
              <span class="about-text">{{ aboutInfo.appName }}</span>
            </NFormItem>
            <NFormItem label="版本号">
              <NTag type="primary" size="small" round>v{{ aboutInfo.version }}</NTag>
            </NFormItem>
            <NFormItem label="技术栈">
              <span class="about-text">{{ aboutInfo.techStack }}</span>
            </NFormItem>
            <NFormItem label="开源许可">
              <span class="about-text">{{ aboutInfo.license }}</span>
            </NFormItem>
          </NForm>
        </NCard>
      </NTabPane>

      <!-- 清理 -->
      <NTabPane name="cleanup" tab="清理">
        <NCard :bordered="false" size="small">
          <NAlert type="warning" :bordered="false" style="margin-bottom: 16px">
            以下操作会修改本地浏览器数据，执行后将自动刷新页面。请谨慎操作。
          </NAlert>
          <NSpace vertical :size="16">
            <div class="cleanup-row">
              <div class="cleanup-info">
                <div class="cleanup-title">清除本地缓存</div>
                <div class="cleanup-desc">清除 localStorage 中除主题与当前项目 ID 外的所有数据。</div>
              </div>
              <NButton @click="clearCache">清除缓存</NButton>
            </div>

            <div class="cleanup-row">
              <div class="cleanup-info">
                <div class="cleanup-title">重置所有设置</div>
                <div class="cleanup-desc">恢复默认主题并清除所有 localStorage 数据。</div>
              </div>
              <NPopconfirm @positive-click="resetAllSettings">
                <template #trigger>
                  <NButton type="warning">重置所有设置</NButton>
                </template>
                确认重置所有设置为默认值？所有本地数据将被清除。
              </NPopconfirm>
            </div>

            <div class="cleanup-row">
              <div class="cleanup-info">
                <div class="cleanup-title danger">清除项目数据</div>
                <div class="cleanup-desc">清除当前项目选择与本地项目数据，下次进入将重新加载。</div>
              </div>
              <NPopconfirm @positive-click="clearProjectData">
                <template #trigger>
                  <NButton type="error">清除项目数据</NButton>
                </template>
                确认清除本地项目数据？此操作不可恢复。
              </NPopconfirm>
            </div>
          </NSpace>
        </NCard>
      </NTabPane>
    </NTabs>
  </div>
</template>

<style scoped lang="scss">
.settings-view {
  padding: 16px 20px;
  max-width: 760px;
  margin: 0 auto;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 12px;

  .title {
    font-size: 1.29em;
    font-weight: 600;
    color: var(--app-text-1);
    margin: 0;
  }
}

.sub-title {
  font-size: 0.93em;
  font-weight: 600;
  color: var(--app-text-2);
  margin-bottom: 8px;
}

.slider-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;

  .slider-value {
    font-size: 0.86em;
    color: var(--app-text-3);
    min-width: 48px;
    text-align: right;
  }
}

.swatch-btn {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  border: 1px solid var(--app-divider);
  cursor: pointer;
  padding: 0;
  transition: transform 0.15s;

  &:hover {
    transform: scale(1.12);
  }
}

.about-text {
  font-size: 0.93em;
  color: var(--app-text-2);
}

.cleanup-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--app-divider);

  &:last-child {
    border-bottom: none;
  }

  .cleanup-info {
    flex: 1;
    min-width: 0;
  }

  .cleanup-title {
    font-size: 1em;
    font-weight: 500;
    color: var(--app-text-1);

    &.danger {
      color: var(--app-error, #c8344e);
    }
  }

  .cleanup-desc {
    font-size: 0.86em;
    color: var(--app-text-3);
    margin-top: 2px;
  }
}
</style>
