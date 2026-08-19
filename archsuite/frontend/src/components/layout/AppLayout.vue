<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import IconBar, { type ModuleKey } from './IconBar.vue'
import ProjectSwitcher from './ProjectSwitcher.vue'
import PannaAssistant from './PannaAssistant.vue'
import TopBar from './TopBar.vue'
import BottomBar from './BottomBar.vue'
import { useProjectStore } from '@/stores/project'
import { useThemeStore } from '@/stores/theme'
import { useLayoutStore } from '@/stores/layout'
import { useMessage } from 'naive-ui'
import { setLogLevel, getLogLevel, logger } from '@/utils/logger'
import { readSetting } from '@/utils/settings'

// 整体布局：顶部 TopBar + 中栏[左 IconBar | 主内容 | 右 Panna] + 底部 BottomBar
const themeStore = useThemeStore()
const projectStore = useProjectStore()
const layoutStore = useLayoutStore()
const route = useRoute()
const router = useRouter()
const message = useMessage()

// 项目管理弹窗由 TopBar 触发，通过事件传给 IconBar 内的 ProjectSwitcher
const projectManagerOpen = ref(false)

// 当前模块：从路由路径推断
const currentModule = computed<ModuleKey>(() => {
  if (route.path.startsWith('/commerce')) return 'commerce'
  if (route.path.startsWith('/env')) return 'env'
  if (route.path.startsWith('/concept')) return 'concept'
  if (route.path.startsWith('/plan')) return 'plan'
  if (route.path.startsWith('/space')) return 'space'
  if (route.path.startsWith('/settings')) return 'settings'
  return 'project'
})

const currentProjectId = computed(() => projectStore.currentProjectId)

function handleSelectModule(key: ModuleKey) {
  if (key === 'project') router.push('/project')
  else if (key === 'commerce') router.push('/commerce')
  else if (key === 'settings') router.push('/settings')
  else if (key === 'env') router.push('/env')
  else if (key === 'concept') router.push('/concept')
  else if (key === 'plan') router.push('/plan')
  else if (key === 'space') router.push('/space')
}

function handleSelectProject(id: number) {
  projectStore.selectProject(id).catch((e) => {
    message.error(e instanceof Error ? e.message : '切换项目失败')
  })
  projectManagerOpen.value = false
}

async function handleCreateProject(payload: {
  name: string
  code: string
  type?: string
}) {
  try {
    await projectStore.addProject(payload)
    message.success('项目创建成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '创建项目失败')
  }
}

async function handleDeleteProject(id: number) {
  try {
    await projectStore.removeProject(id)
    message.success('项目删除成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除项目失败')
  }
}

// 已加载标记
const loaded = ref(false)

// 自动保存 / 数据刷新 调度器
let autoSaveTimer: number | null = null
let refreshTimer: number | null = null

function setupSchedulers() {
  // 清理旧定时器
  if (autoSaveTimer) window.clearInterval(autoSaveTimer)
  if (refreshTimer) window.clearInterval(refreshTimer)

  const autoSaveSec = Number(readSetting('autoSaveInterval', '0'))
  const refreshSec = Number(readSetting('refreshInterval', '0'))

  // 自动保存：每 N 秒保存当前项目基本信息（无项目则跳过）
  if (autoSaveSec > 0) {
    autoSaveTimer = window.setInterval(() => {
      const pid = projectStore.currentProjectId
      if (!pid || !projectStore.currentProject) return
      // 保存基本信息：复用 store.refreshCurrent 已是最新数据，无需再写
      // 这里仅记录日志，实际保存由用户在编辑 Tab 点击保存触发
      // （避免覆盖未验证表单）
      logger.debug('autosave', `项目 #${pid} 自动保存检查（基本信息由编辑页保存）`)
    }, autoSaveSec * 1000)
  }

  // 数据刷新：每 N 秒重新拉取合同 + 联系人（通过刷新 store 列表）
  if (refreshSec > 0) {
    refreshTimer = window.setInterval(() => {
      const pid = projectStore.currentProjectId
      if (!pid) return
      // 触发项目详情刷新（合同/联系人由各 Tab 自行拉取，这里只刷新项目本体）
      projectStore.refreshCurrent().catch(() => {
        logger.warn('refresh', `项目 #${pid} 数据刷新失败`)
      })
      logger.debug('refresh', `项目 #${pid} 数据刷新触发`)
    }, refreshSec * 1000)
  }
}

onMounted(async () => {
  // 初始化日志级别
  setLogLevel(getLogLevel())
  themeStore.syncRootAttr()
  await projectStore.loadProjects()
  setupSchedulers()
  loaded.value = true
  logger.info('app', 'ArchSuite 前端启动完成')
  // 全局快捷键
  window.addEventListener('keydown', onGlobalKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onGlobalKeydown)
  if (autoSaveTimer) window.clearInterval(autoSaveTimer)
  if (refreshTimer) window.clearInterval(refreshTimer)
})

// 全局快捷键处理
function onGlobalKeydown(e: KeyboardEvent) {
  // 仅 Ctrl/Cmd 组合键
  if (!(e.ctrlKey || e.metaKey)) return
  const key = e.key.toLowerCase()
  if (key === 'k') {
    e.preventDefault()
    projectManagerOpen.value = true
  } else if (key === 'b') {
    e.preventDefault()
    layoutStore.toggleLeftRail()
  } else if (key === 'j') {
    e.preventDefault()
    layoutStore.toggleBottomBar()
  } else if (key === '/') {
    e.preventDefault()
    layoutStore.toggleRightRail()
  } else if (key === ',') {
    e.preventDefault()
    router.push('/settings')
  }
}

// 设置变更时重建调度器
watch(
  () => [readSetting('autoSaveInterval', '0'), readSetting('refreshInterval', '0')],
  () => setupSchedulers()
)

// 路由变化时若无项目，且进入非设置页，自动回退到 /project
watch(
  () => route.path,
  (path) => {
    if (!loaded.value) return
    if (!projectStore.hasProject && !path.startsWith('/settings') && path !== '/project') {
      router.replace('/project')
    }
  }
)
</script>

<template>
  <div class="app-shell">
    <TopBar @open-project-manager="projectManagerOpen = true" />

    <div class="app-body">
      <IconBar
        v-if="layoutStore.leftRailVisible"
        :current-module="currentModule"
        :current-project-id="currentProjectId"
        @select-module="handleSelectModule"
      />
      <main class="app-main">
        <RouterView v-slot="{ Component }">
          <component :is="Component" />
        </RouterView>
      </main>
      <PannaAssistant v-if="layoutStore.rightRailVisible" />
    </div>

    <BottomBar v-if="layoutStore.bottomBarVisible" />

    <!-- 项目管理弹窗（由顶栏触发，独立挂载） -->
    <ProjectSwitcher
      :current-project-id="currentProjectId"
      :hide-trigger="true"
      :force-open="projectManagerOpen"
      @select-project="handleSelectProject"
      @create-project="handleCreateProject"
      @delete-project="handleDeleteProject"
    />
  </div>
</template>

<style scoped lang="scss">
.app-shell {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.app-body {
  flex: 1;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

.app-main {
  flex: 1;
  min-width: 0;
  height: 100%;
  overflow: auto;
  background: var(--app-bg-page);
  // 内边距让内容不贴边、卡片化观感
  padding: 12px 16px;
}
</style>
