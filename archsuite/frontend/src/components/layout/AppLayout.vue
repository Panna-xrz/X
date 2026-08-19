<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import IconBar, { type ModuleKey } from './IconBar.vue'
import { useProjectStore } from '@/stores/project'
import { useThemeStore } from '@/stores/theme'
import { useMessage } from 'naive-ui'

// 整体布局：左侧 IconBar(64px) + 主内容区(flex-1)
const themeStore = useThemeStore()
const projectStore = useProjectStore()
const route = useRoute()
const router = useRouter()
const message = useMessage()

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

// 选择模块：路由跳转
function handleSelectModule(key: ModuleKey) {
  if (key === 'project') router.push('/project')
  else if (key === 'commerce') router.push('/commerce')
  else if (key === 'settings') router.push('/settings')
  else if (key === 'env') router.push('/env')
  else if (key === 'concept') router.push('/concept')
  else if (key === 'plan') router.push('/plan')
  else if (key === 'space') router.push('/space')
}

// 选择项目
function handleSelectProject(id: number) {
  projectStore.selectProject(id).catch((e) => {
    message.error(e instanceof Error ? e.message : '切换项目失败')
  })
}

// 新建项目
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

// 删除指定项目
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

onMounted(async () => {
  themeStore.syncRootAttr()
  await projectStore.loadProjects()
  loaded.value = true
})

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
    <IconBar
      :current-module="currentModule"
      :current-project-id="currentProjectId"
      @select-module="handleSelectModule"
      @select-project="handleSelectProject"
      @create-project="handleCreateProject"
      @delete-project="handleDeleteProject"
    />
    <main class="app-main">
      <RouterView v-slot="{ Component }">
        <component :is="Component" />
      </RouterView>
    </main>
  </div>
</template>

<style scoped lang="scss">
.app-shell {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.app-main {
  flex: 1;
  min-width: 0;
  height: 100vh;
  overflow: auto;
  background: var(--app-bg, #f7f8fa);
}
</style>
