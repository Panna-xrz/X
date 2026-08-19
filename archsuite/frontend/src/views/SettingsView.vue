<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
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
  NUpload,
  useMessage
} from 'naive-ui'
import { useThemeStore } from '@/stores/theme'
import {
  fontFamilyCandidates,
  borderRadiusScale,
  lightPalette,
  darkPalette
} from '@/styles/tokens'
import { writeSetting, readSetting } from '@/utils/settings'
import { reloadLogLevel, logger } from '@/utils/logger'

// 设置页：基本 / 界面 / API-Key / 运行时 / 导入导出 / 快捷键 / 关于 / 清理
const themeStore = useThemeStore()
const message = useMessage()

// localStorage 键
const AMAP_KEY_STORAGE = 'archsuite_amap_key'
const AMAP_SECURITY_STORAGE = 'archsuite_amap_security'
const AI_PROVIDER_STORAGE = 'archsuite_ai_provider'
const AI_APIKEY_STORAGE = 'archsuite_ai_apikey'
const AI_BASEURL_STORAGE = 'archsuite_ai_baseurl'
const AI_MODEL_STORAGE = 'archsuite_ai_model'

// ---------- 基本设置 ----------
const defaultPhase = ref(readSetting('defaultPhase', '概念设计'))
const autoSaveInterval = ref(Number(readSetting('autoSaveInterval', '30')))
const refreshInterval = ref(Number(readSetting('refreshInterval', '60')))

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
  message.success('基本设置已保存，调度器已更新')
}

// ---------- 界面设置 ----------
const isDark = computed<boolean>({
  get: () => themeStore.isDark,
  set: (val: boolean) => themeStore.setTheme(val ? 'dark' : 'light')
})

const presetSwatches = ['#3457d5', '#1f9d6b', '#7b61d6', '#d68a1f', '#c8344e']

const fontOptions = fontFamilyCandidates.map((f) => ({ label: f.label, value: f.value }))

// 当前主题色板默认背景（用于"恢复默认"按钮显示与未自定义时的回退值）
const defaultSurface = computed(() => {
  const pal = themeStore.isDark ? darkPalette : lightPalette
  return {
    surfacePage: pal.surfacePage,
    surfaceCard: pal.surfaceCard,
    surfacePanel: pal.surfacePanel,
    surfaceInset: pal.surfaceInset
  }
})

const contentMaxWidthOptions = [
  { label: '满屏', value: 'full' },
  { label: '1280px', value: '1280' },
  { label: '1440px', value: '1440' },
  { label: '1600px', value: '1600' }
]

// ---------- API-Key（合并高德地图 + LLM） ----------
const amapKey = ref(localStorage.getItem(AMAP_KEY_STORAGE) || '')
const amapSecurity = ref(localStorage.getItem(AMAP_SECURITY_STORAGE) || '')

function saveAmapKey() {
  if (!amapKey.value.trim()) {
    localStorage.removeItem(AMAP_KEY_STORAGE)
    message.success('已清除高德地图 Key（将使用占位符）')
  } else {
    localStorage.setItem(AMAP_KEY_STORAGE, amapKey.value.trim())
    message.success('高德地图 Key 已保存，刷新地图后生效')
  }
  if (amapSecurity.value.trim()) {
    localStorage.setItem(AMAP_SECURITY_STORAGE, amapSecurity.value.trim())
  } else {
    localStorage.removeItem(AMAP_SECURITY_STORAGE)
  }
}

const aiProvider = ref(localStorage.getItem(AI_PROVIDER_STORAGE) || 'openai')
const aiApiKey = ref(localStorage.getItem(AI_APIKEY_STORAGE) || '')
const aiBaseUrl = ref(localStorage.getItem(AI_BASEURL_STORAGE) || '')
const aiModel = ref(localStorage.getItem(AI_MODEL_STORAGE) || '')
const llmSaved = ref(false)
const testing = ref(false)

watch([aiProvider, aiApiKey, aiBaseUrl, aiModel], () => {
  llmSaved.value = false
})

const aiProviderOptions = [
  { label: 'OpenAI', value: 'openai' },
  { label: 'Anthropic Claude', value: 'anthropic' },
  { label: '通义千问', value: 'qwen' },
  { label: 'DeepSeek', value: 'deepseek' }
]

// 默认 Base URL（未填写时按 provider 推断）
const providerDefaultUrl: Record<string, string> = {
  openai: 'https://api.openai.com/v1',
  anthropic: 'https://api.anthropic.com/v1',
  qwen: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  deepseek: 'https://api.deepseek.com/v1'
}

function saveLlm() {
  localStorage.setItem(AI_PROVIDER_STORAGE, aiProvider.value)
  localStorage.setItem(AI_APIKEY_STORAGE, aiApiKey.value.trim())
  localStorage.setItem(AI_BASEURL_STORAGE, aiBaseUrl.value.trim())
  localStorage.setItem(AI_MODEL_STORAGE, aiModel.value.trim())
  llmSaved.value = true
  message.success('LLM 配置已保存')
}

// 真实连接测试：调用 /chat/completions 发一条极短请求
async function testConnection() {
  if (!aiApiKey.value.trim()) {
    message.warning('请先填写 API Key')
    return
  }
  testing.value = true
  try {
    const baseUrl = (aiBaseUrl.value.trim() || providerDefaultUrl[aiProvider.value] || '').replace(/\/$/, '')
    if (!baseUrl) {
      message.error('无法确定 Base URL，请填写')
      return
    }
    const model = aiModel.value.trim() || (aiProvider.value === 'openai' ? 'gpt-4o-mini' : 'claude-3-haiku-20240307')
    const res = await fetch(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${aiApiKey.value.trim()}`,
        ...(aiProvider.value === 'anthropic' ? { 'x-api-key': aiApiKey.value.trim(), 'anthropic-version': '2023-06-01' } : {})
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: 'ping' }],
        max_tokens: 1
      })
    })
    if (res.ok) {
      message.success(`连接成功（${aiProvider.value} / ${model}）`)
      logger.info('llm', `连接测试成功: ${aiProvider.value}/${model}`)
    } else {
      const text = await res.text().catch(() => '')
      message.error(`连接失败：HTTP ${res.status} ${text.slice(0, 120)}`)
      logger.warn('llm', `连接测试失败: HTTP ${res.status}`)
    }
  } catch (e) {
    message.error(e instanceof Error ? e.message : '连接测试失败')
    logger.error('llm', e instanceof Error ? e.message : '连接测试失败')
  } finally {
    testing.value = false
  }
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
  reloadLogLevel()
  message.success('运行时设置已保存')
}

// ---------- 导入/导出 ----------
function exportSettings() {
  const data: Record<string, string> = {}
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k) data[k] = localStorage.getItem(k) || ''
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `archsuite-settings-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
  message.success('设置已导出')
}

function importSettings(file: File) {
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const data = JSON.parse(String(reader.result)) as Record<string, string>
      for (const [k, v] of Object.entries(data)) {
        localStorage.setItem(k, v)
      }
      message.success('设置已导入，正在刷新…')
      setTimeout(() => location.reload(), 600)
    } catch (e) {
      message.error('导入失败：文件格式不正确')
    }
  }
  reader.readAsText(file)
  return false
}

// ---------- 快捷键（查看） ----------
const shortcuts = [
  { key: 'Ctrl + K', desc: '打开项目管理' },
  { key: 'Ctrl + B', desc: '切换左侧栏' },
  { key: 'Ctrl + J', desc: '切换底部状态栏' },
  { key: 'Ctrl + /', desc: '切换右侧 Panna 助手' },
  { key: 'Ctrl + S', desc: '保存当前表单' },
  { key: 'Ctrl + ,', desc: '打开设置' }
]

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

// 启动时同步日志级别
onMounted(() => {
  reloadLogLevel()
})

// 监听设置变更事件（writeSetting 派发），自动重载日志级别
onMounted(() => {
  window.addEventListener('archsuite-settings-changed', () => {
    reloadLogLevel()
  })
})
</script>

<template>
  <div class="settings-view">
    <div class="page-header">
      <h2 class="title">设置</h2>
      <span class="header-sub">配置平台行为、外观与第三方集成</span>
    </div>

    <NTabs type="line" animated>
      <!-- 基本设置 -->
      <NTabPane name="basic" tab="基本">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">项目行为</div>
            <NForm label-placement="left" label-width="140">
              <NFormItem label="默认项目阶段">
                <NSelect v-model:value="defaultPhase" :options="phaseOptions" placeholder="请选择" />
              </NFormItem>
              <NFormItem label="自动保存间隔">
                <div class="slider-row">
                  <NSlider v-model:value="autoSaveInterval" :min="10" :max="300" :step="5" />
                  <span class="slider-value">{{ autoSaveInterval }}s</span>
                </div>
              </NFormItem>
              <NFormItem label="数据刷新间隔">
                <div class="slider-row">
                  <NSlider v-model:value="refreshInterval" :min="10" :max="600" :step="10" />
                  <span class="slider-value">{{ refreshInterval }}s</span>
                </div>
              </NFormItem>
            </NForm>
            <NSpace justify="end">
              <NButton type="primary" @click="saveBasicSettings">保存</NButton>
            </NSpace>
          </NCard>
        </div>
      </NTabPane>

      <!-- 界面设置 -->
      <NTabPane name="ui" tab="界面">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">主题</div>
            <NForm label-placement="left" label-width="120">
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
              <NFormItem label="内容区宽度">
                <NSelect
                  :value="themeStore.contentMaxWidth"
                  :options="contentMaxWidthOptions"
                  @update:value="(v: string) => themeStore.setContentMaxWidth(v)"
                />
              </NFormItem>
            </NForm>
          </NCard>

          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">背景层次</div>
            <NForm label-placement="left" label-width="120">
              <NFormItem label="页面底色 L1">
                <div class="color-row">
                  <NColorPicker :value="themeStore.surfacePage || defaultSurface.surfacePage" :show-alpha="false" @update:value="(v: string) => themeStore.setSurfacePage(v)" />
                  <NButton quaternary size="tiny" @click="themeStore.setSurfacePage(null)">默认</NButton>
                </div>
              </NFormItem>
              <NFormItem label="卡片底色 L2">
                <div class="color-row">
                  <NColorPicker :value="themeStore.surfaceCard || defaultSurface.surfaceCard" :show-alpha="false" @update:value="(v: string) => themeStore.setSurfaceCard(v)" />
                  <NButton quaternary size="tiny" @click="themeStore.setSurfaceCard(null)">默认</NButton>
                </div>
              </NFormItem>
              <NFormItem label="次级面板 L3">
                <div class="color-row">
                  <NColorPicker :value="themeStore.surfacePanel || defaultSurface.surfacePanel" :show-alpha="false" @update:value="(v: string) => themeStore.setSurfacePanel(v)" />
                  <NButton quaternary size="tiny" @click="themeStore.setSurfacePanel(null)">默认</NButton>
                </div>
              </NFormItem>
              <NFormItem label="内嵌区 L4">
                <div class="color-row">
                  <NColorPicker :value="themeStore.surfaceInset || defaultSurface.surfaceInset" :show-alpha="false" @update:value="(v: string) => themeStore.setSurfaceInset(v)" />
                  <NButton quaternary size="tiny" @click="themeStore.setSurfaceInset(null)">默认</NButton>
                </div>
              </NFormItem>
            </NForm>
            <div class="sub-title" style="margin-top: 12px">字号梯度</div>
            <NForm label-placement="left" label-width="120">
              <NFormItem label="辅助 xs">
                <div class="slider-row">
                  <NSlider :value="themeStore.fontSizeXs" :min="10" :max="14" :step="1" @update:value="(v: number) => themeStore.setFontSizeXs(v)" />
                  <span class="slider-value">{{ themeStore.fontSizeXs }}px</span>
                </div>
              </NFormItem>
              <NFormItem label="次要 sm">
                <div class="slider-row">
                  <NSlider :value="themeStore.fontSizeSm" :min="11" :max="15" :step="1" @update:value="(v: number) => themeStore.setFontSizeSm(v)" />
                  <span class="slider-value">{{ themeStore.fontSizeSm }}px</span>
                </div>
              </NFormItem>
              <NFormItem label="主字号 base">
                <div class="slider-row">
                  <NSlider :value="themeStore.fontSizeBase" :min="12" :max="18" :step="1" @update:value="(v: number) => themeStore.setFontSizeBase(v)" />
                  <span class="slider-value">{{ themeStore.fontSizeBase }}px</span>
                </div>
              </NFormItem>
              <NFormItem label="标题 lg">
                <div class="slider-row">
                  <NSlider :value="themeStore.fontSizeLg" :min="14" :max="22" :step="1" @update:value="(v: number) => themeStore.setFontSizeLg(v)" />
                  <span class="slider-value">{{ themeStore.fontSizeLg }}px</span>
                </div>
              </NFormItem>
            </NForm>
          </NCard>
        </div>
      </NTabPane>

      <!-- API-Key（高德地图 + LLM 合并） -->
      <NTabPane name="apikey" tab="API-Key">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">高德地图</div>
            <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
              2021-12-02 后申请的 Key 必须配置安全密钥，否则地图无法加载。
            </NAlert>
            <NForm label-placement="left" label-width="120">
              <NFormItem label="高德 Key">
                <NInput v-model:value="amapKey" placeholder="如：a1b2c3d4e5f6g7h8i9j0..." type="password" show-password-on="click" />
              </NFormItem>
              <NFormItem label="安全密钥">
                <NInput v-model:value="amapSecurity" placeholder="securityJsCode（控制台获取）" type="password" show-password-on="click" />
              </NFormItem>
            </NForm>
            <NSpace justify="end">
              <NButton @click="saveAmapKey">保存</NButton>
            </NSpace>
          </NCard>

          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">LLM 大模型</div>
            <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
              API Key 仅保存在本地浏览器，不上传服务器。
            </NAlert>
            <NForm label-placement="left" label-width="120">
              <NFormItem label="AI 提供商">
                <NSelect v-model:value="aiProvider" :options="aiProviderOptions" />
              </NFormItem>
              <NFormItem label="API Key">
                <NInput v-model:value="aiApiKey" placeholder="sk-..." type="password" show-password-on="click" />
              </NFormItem>
              <NFormItem label="Base URL">
                <NInput v-model:value="aiBaseUrl" :placeholder="`可选，默认 ${providerDefaultUrl[aiProvider] || ''}`" />
              </NFormItem>
              <NFormItem label="模型名称">
                <NInput v-model:value="aiModel" placeholder="如 gpt-4o-mini, claude-3-haiku" />
              </NFormItem>
            </NForm>
            <NSpace justify="end" align="center">
              <NTag v-if="llmSaved" type="success" size="small" round>已保存</NTag>
              <NButton :loading="testing" @click="testConnection">测试连接</NButton>
              <NButton type="primary" @click="saveLlm">保存</NButton>
            </NSpace>
          </NCard>
        </div>
      </NTabPane>

      <!-- 运行时设置 -->
      <NTabPane name="runtime" tab="运行时">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">请求与日志</div>
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
        </div>
      </NTabPane>

      <!-- 导入/导出 -->
      <NTabPane name="io" tab="导入导出">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">配置导入导出</div>
            <div class="io-row">
              <div class="io-info">
                <div class="io-title">导出设置</div>
                <div class="io-desc">将当前所有本地设置（主题、API Key、运行时等）导出为 JSON 文件。</div>
              </div>
              <NButton @click="exportSettings">导出</NButton>
            </div>
            <NDivider style="margin: 12px 0" />
            <div class="io-row">
              <div class="io-info">
                <div class="io-title">导入设置</div>
                <div class="io-desc">从 JSON 文件恢复设置，导入后自动刷新页面。</div>
              </div>
              <NUpload :show-file-list="false" :max="1" accept=".json" :custom-request="(opt: any) => { if (opt.file?.file) importSettings(opt.file.file) }">
                <NButton>选择文件</NButton>
              </NUpload>
            </div>
          </NCard>
        </div>
      </NTabPane>

      <!-- 快捷键 -->
      <NTabPane name="shortcuts" tab="快捷键">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">全局快捷键</div>
            <div class="shortcut-list">
              <div v-for="s in shortcuts" :key="s.key" class="shortcut-row">
                <span class="sc-key">{{ s.key }}</span>
                <span class="sc-desc">{{ s.desc }}</span>
              </div>
            </div>
          </NCard>
        </div>
      </NTabPane>

      <!-- 关于 -->
      <NTabPane name="about" tab="关于">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">应用信息</div>
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
        </div>
      </NTabPane>

      <!-- 清理 -->
      <NTabPane name="cleanup" tab="清理">
        <div class="grid-2col">
          <NCard :bordered="false" size="small" class="settings-card">
            <div class="sub-title">数据清理</div>
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
        </div>
      </NTabPane>
    </NTabs>
  </div>
</template>

<style scoped lang="scss">
.settings-view {
  padding: 12px 16px 24px;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100%;
}

.page-header {
  margin-bottom: 12px;
  display: flex;
  align-items: baseline;
  gap: 12px;

  .title {
    font-size: 1.29em;
    font-weight: 600;
    color: var(--app-text-1);
    margin: 0;
  }

  .header-sub {
    font-size: 0.86em;
    color: var(--app-text-3);
  }
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: start;

  // 单卡时左对齐占满
  > .settings-card:only-child {
    grid-column: 1 / -1;
  }
}

.settings-card {
  background: var(--app-card-bg);
  box-shadow: var(--app-shadow-sm);
  border-radius: var(--app-radius);
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

.color-row {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;

  :deep(.n-color-picker-trigger) {
    flex: 1;
  }
}

.swatch-btn {
  width: 22px;
  height: 22px;
  border-radius: var(--app-radius);
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

.io-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;

  .io-info {
    flex: 1;
    min-width: 0;
  }

  .io-title {
    font-size: 1em;
    font-weight: 500;
    color: var(--app-text-1);
  }

  .io-desc {
    font-size: 0.86em;
    color: var(--app-text-3);
    margin-top: 2px;
  }
}

.shortcut-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.shortcut-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 6px 8px;
  border-radius: calc(var(--app-radius) - 4px);

  &:hover {
    background: var(--app-inset-bg);
  }

  .sc-key {
    font-family: var(--app-font-family);
    font-size: 0.86em;
    font-weight: 500;
    color: var(--app-text-1);
    background: var(--app-inset-bg);
    padding: 2px 8px;
    border-radius: calc(var(--app-radius) - 6px);
    min-width: 96px;
    text-align: center;
  }

  .sc-desc {
    font-size: 0.86em;
    color: var(--app-text-2);
  }
}

.cleanup-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid transparent;

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
