<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import {
  NModal,
  NButton,
  NSpace,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NPopconfirm,
  NEmpty,
  NSpin,
  NTag,
  useMessage
} from 'naive-ui'
import { useProjectStore } from '@/stores/project'
import { getContracts } from '@/api/contract'
import ProjectIcon from '@/components/icons/ProjectIcon.vue'
import type { Contract, Project } from '@/types'

// 项目切换器：点击图标打开居中弹窗，管理历史项目 / 新建 / 删除
const props = defineProps<{
  currentProjectId: number | null
}>()

const emit = defineEmits<{
  (e: 'selectProject', id: number): void
  (e: 'createProject', payload: { name: string; code: string; type?: string }): void
  (e: 'deleteProject', id: number): void
}>()

const projectStore = useProjectStore()
const message = useMessage()

// 主弹窗（项目管理）
const showManager = ref(false)
// 新建项目弹窗
const showCreate = ref(false)
const submitting = ref(false)
const formModel = reactive<{ name: string; code: string; type: string }>({
  name: '',
  code: '',
  type: ''
})

// 项目类型（按《建筑工程设计资质分类》及《民用建筑设计通则》整理）
const typeOptions = [
  { label: '居住建筑', value: '居住建筑' },
  { label: '一般公共建筑', value: '一般公共建筑' },
  { label: '大型公共建筑', value: '大型公共建筑' },
  { label: '工业建筑', value: '工业建筑' },
  { label: '农业建筑', value: '农业建筑' },
  { label: '构筑物', value: '构筑物' }
]

// 合同进度数据（每个项目的合同状态聚合）
const projectContracts = ref<Record<number, Contract[]>>({})

// 当前项目名称（截断显示）
const currentName = computed(() => projectStore.currentProject?.name || '选择项目')

// 获取某个项目的节点进度标签
function getProgressLabel(projectId: number): { text: string; color: 'default' | 'info' | 'success' | 'warning' | 'error' } {
  const contracts = projectContracts.value[projectId]
  if (!contracts || contracts.length === 0) {
    return { text: '未立项', color: 'default' }
  }
  const hasSigned = contracts.some(c => c.status === 'signed')
  const hasDraft = contracts.some(c => c.status === 'draft')
  const hasReviewing = contracts.some(c => c.status === 'reviewing')
  const allTerminated = contracts.every(c => c.status === 'terminated')

  if (allTerminated) return { text: '已终止', color: 'error' }
  if (hasSigned) return { text: '执行中', color: 'success' }
  if (hasReviewing) return { text: '审核中', color: 'info' }
  if (hasDraft) return { text: '草拟中', color: 'warning' }
  return { text: '已立项', color: 'default' }
}

// 加载所有项目的合同数据（弹窗打开时）
async function loadContracts() {
  for (const p of projectStore.projects) {
    try {
      const res = await getContracts({ projectId: p.id, page: 1, pageSize: 50 })
      projectContracts.value[p.id] = res.list || []
    } catch {
      projectContracts.value[p.id] = []
    }
  }
}

// 打开弹窗
async function openManager() {
  showManager.value = true
  await loadContracts()
}

// 选择项目
function handleSelect(id: number) {
  emit('selectProject', id)
  showManager.value = false
}

// 删除项目
function handleDelete(id: number) {
  emit('deleteProject', id)
  delete projectContracts.value[id]
}

// 打开新建弹窗
function openCreate() {
  Object.assign(formModel, { name: '', code: '', type: '' })
  showCreate.value = true
}

// 提交新建
function submitCreate() {
  if (!formModel.name) {
    message.warning('请填写项目名称')
    return
  }
  if (!formModel.code) {
    message.warning('请填写项目编号')
    return
  }
  submitting.value = true
  try {
    emit('createProject', {
      name: formModel.name,
      code: formModel.code,
      type: formModel.type || undefined
    })
    showCreate.value = false
  } catch (e) {
    message.error(e instanceof Error ? e.message : '创建失败')
  } finally {
    submitting.value = false
  }
}

// ---------- 分页 snap 翻页（每页 4 个 = 两排两列） ----------
const PAGE_SIZE = 4
// 单页高度（2 行卡片 + 1 行间距），与下方 .project-page height 保持一致
const PAGE_HEIGHT = 292

const projectPages = computed<Project[][]>(() => {
  const all = projectStore.projects
  const pages: Project[][] = []
  for (let i = 0; i < all.length; i += PAGE_SIZE) {
    pages.push(all.slice(i, i + PAGE_SIZE))
  }
  return pages
})

const pagesRef = ref<HTMLDivElement | null>(null)
const isScrolling = ref(false)

// 滚轮翻页：一次滚动一整页，避免卡片卡在一半
function onWheel(e: WheelEvent) {
  e.preventDefault()
  if (isScrolling.value) return
  const container = pagesRef.value
  if (!container) return
  const dir = e.deltaY > 0 ? 1 : -1
  isScrolling.value = true
  container.scrollBy({ top: dir * PAGE_HEIGHT, behavior: 'smooth' })
  window.setTimeout(() => {
    isScrolling.value = false
  }, 450)
}
</script>

<template>
  <div class="project-switcher">
    <button class="switcher-trigger" :title="currentName" @click="openManager">
      <ProjectIcon class="trigger-icon" />
      <span class="switcher-name">{{ currentName }}</span>
    </button>

    <!-- 项目管理弹窗（居中，启动窗口风格） -->
    <NModal
      v-model:show="showManager"
      :bordered="false"
      :mask-closable="true"
      style="width: 640px; max-width: 90vw"
      class="project-manager-modal"
    >
      <div class="manager-container">
        <!-- 头部 -->
        <div class="manager-header">
          <div class="header-left">
            <div class="header-logo">
              <ProjectIcon class="logo-icon" />
            </div>
            <div class="header-text">
              <div class="header-title">项目管理</div>
              <div class="header-sub">选择、新建或管理你的设计项目</div>
            </div>
          </div>
          <NButton quaternary size="small" @click="showManager = false">×</NButton>
        </div>

        <!-- 项目网格：固定两排两列，snap 翻页，隐藏滚动条 -->
        <NSpin :show="projectStore.loading">
          <div
            v-if="projectStore.projects.length"
            ref="pagesRef"
            class="project-pages"
            @wheel.prevent="onWheel"
          >
            <div
              v-for="(page, pageIdx) in projectPages"
              :key="pageIdx"
              class="project-page"
            >
              <div class="project-grid">
                <div
                  v-for="p in page"
                  :key="p.id"
                  class="project-card"
                  :class="{ active: p.id === props.currentProjectId }"
                  @click="handleSelect(p.id)"
                >
                  <!-- 顶部进度标签 -->
                  <div class="card-top">
                    <NTag
                      :type="getProgressLabel(p.id).color"
                      size="tiny"
                      round
                      :bordered="false"
                    >
                      {{ getProgressLabel(p.id).text }}
                    </NTag>
                    <NPopconfirm
                      placement="bottom-end"
                      @positive-click="handleDelete(p.id)"
                    >
                      <template #trigger>
                        <button class="card-delete" @click.stop>×</button>
                      </template>
                      确认删除项目「{{ p.name }}」？<br />该操作不可恢复，且会级联删除项目下所有数据。
                    </NPopconfirm>
                  </div>

                  <!-- 项目主体 -->
                  <div class="card-body">
                    <div class="card-name">{{ p.name }}</div>
                    <div class="card-code">{{ p.code }}</div>
                  </div>

                  <!-- 底部信息 -->
                  <div class="card-foot">
                    <span class="foot-type">{{ p.type || '未分类' }}</span>
                    <NTag
                      v-if="p.id === props.currentProjectId"
                      type="primary"
                      size="tiny"
                      round
                      :bordered="false"
                    >
                      当前
                    </NTag>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <NEmpty v-else description="暂无项目，请新建" style="padding: 60px 0" />
        </NSpin>

        <!-- 底部操作栏 -->
        <div class="manager-footer">
          <span class="footer-count">共 {{ projectStore.projects.length }} 个项目</span>
          <NSpace :size="12">
            <NButton size="small" @click="showManager = false">关闭</NButton>
            <NButton size="small" type="primary" @click="openCreate">
              + 新建项目
            </NButton>
          </NSpace>
        </div>
      </div>
    </NModal>

    <!-- 新建项目弹窗 -->
    <NModal
      v-model:show="showCreate"
      preset="card"
      title="新建项目"
      style="width: 460px; max-width: 90vw"
      :bordered="false"
    >
      <NForm label-placement="left" label-width="80">
        <NFormItem label="项目名称" required>
          <NInput v-model:value="formModel.name" placeholder="请输入项目名称" />
        </NFormItem>
        <NFormItem label="项目编号" required>
          <NInput v-model:value="formModel.code" placeholder="请输入项目编号" />
        </NFormItem>
        <NFormItem label="项目类型">
          <NSelect
            v-model:value="formModel.type"
            :options="typeOptions"
            placeholder="请选择（按国标分类）"
            clearable
          />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton size="small" @click="showCreate = false">取消</NButton>
          <NButton size="small" type="primary" :loading="submitting" @click="submitCreate">
            确定
          </NButton>
        </NSpace>
      </template>
    </NModal>
  </div>
</template>

<style scoped lang="scss">
.project-switcher {
  width: 100%;
}

// 触发按钮在侧边栏内
.switcher-trigger {
  width: 100%;
  height: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 6px 4px;
  background: transparent;
  border: none;
  color: var(--app-rail-text);
  cursor: pointer;
  transition: background 0.18s, color 0.18s;

  &:hover {
    background: var(--app-rail-hover-bg);
    color: var(--app-rail-text-hover);
  }

  .trigger-icon {
    width: 18px;
    height: 18px;
  }

  .switcher-name {
    font-size: 0.79em;
    line-height: 1.2;
    text-align: center;
    max-width: 52px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

// 弹窗容器（启动窗口风格）
.manager-container {
  background: var(--app-card-bg);
  border-radius: var(--app-radius, 8px);
  box-shadow: var(--app-shadow-lg);
  overflow: hidden;
}

.manager-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--app-divider);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header-logo {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--app-radius, 8px);
    background: color-mix(in srgb, var(--app-primary) 12%, transparent);

    .logo-icon {
      width: 22px;
      height: 22px;
      color: var(--app-primary);
    }
  }

  .header-title {
    font-size: 1.14em;
    font-weight: 600;
    color: var(--app-text-1);
    line-height: 1.3;
  }

  .header-sub {
    font-size: 0.86em;
    color: var(--app-text-3);
    margin-top: 2px;
  }
}

// 项目分页滚动容器：固定高度（两排两列），snap 翻页，隐藏滚动条
.project-pages {
  height: 332px; // 2 行卡片(140×2) + 1 间距(12) + 上下内边距(20×2)
  padding: 20px 24px;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  // 用 page 层背景作为卡片舞台，衬托白卡片（无分割线，靠层次区分）
  background: var(--app-bg-page);
  // 隐藏滚动条
  scrollbar-width: none;
  -ms-overflow-style: none;
  &::-webkit-scrollbar {
    display: none;
  }
}

.project-page {
  scroll-snap-align: start;
  scroll-snap-stop: always;
  height: 292px; // 2 行卡片 + 1 间距，与 PAGE_HEIGHT 常量一致
}

// 项目网格
.project-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  height: 100%;
}

.project-card {
  display: flex;
  flex-direction: column;
  height: 140px;
  padding: 14px 16px;
  border-radius: var(--app-radius);
  // 无边框，靠卡片白底浮于 page 浅灰舞台区分层次
  border: none;
  background: var(--app-card-bg);
  box-shadow: var(--app-shadow-sm);
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  gap: 10px;

  &:hover {
    transform: translateY(-1px);
    box-shadow: var(--app-shadow-md);
  }

  &.active {
    background: color-mix(in srgb, var(--app-primary) 8%, var(--app-card-bg));
    box-shadow: 0 0 0 1.5px var(--app-primary), var(--app-shadow-sm);
  }

  .card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .card-delete {
    width: 20px;
    height: 20px;
    border: none;
    background: transparent;
    color: var(--app-text-3);
    font-size: 1.14em;
    line-height: 1;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.15s;

    &:hover {
      background: color-mix(in srgb, var(--error-color, #c8344e) 12%, transparent);
      color: #c8344e;
    }
  }

  .card-body {
    flex: 1;
  }

  .card-name {
    font-size: 1em;
    font-weight: 500;
    color: var(--app-text-1);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .card-code {
    font-size: 0.86em;
    color: var(--app-text-3);
    margin-top: 4px;
  }

  .card-foot {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .foot-type {
      font-size: 0.79em;
      color: var(--app-text-3);
      padding: 2px 8px;
      border-radius: 4px;
      background: var(--app-bg);
    }
  }
}

.manager-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px 16px;
  border-top: 1px solid var(--app-divider);

  .footer-count {
    font-size: 0.86em;
    color: var(--app-text-3);
  }
}
</style>
