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
import ProjectIcon from '@/components/icons/ProjectIcon.vue'

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

const typeOptions = [
  { label: '公共建筑', value: '公共建筑' },
  { label: '住宅', value: '住宅' },
  { label: '商业综合体', value: '商业综合体' },
  { label: '工业建筑', value: '工业建筑' }
]

// 当前项目名称（截断显示）
const currentName = computed(() => projectStore.currentProject?.name || '选择项目')

// 选择项目
function handleSelect(id: number) {
  emit('selectProject', id)
  showManager.value = false
}

// 删除项目
function handleDelete(id: number) {
  emit('deleteProject', id)
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
</script>

<template>
  <div class="project-switcher">
    <button class="switcher-trigger" :title="currentName" @click="showManager = true">
      <ProjectIcon class="trigger-icon" />
      <span class="switcher-name">{{ currentName }}</span>
    </button>

    <!-- 项目管理弹窗（居中） -->
    <NModal
      v-model:show="showManager"
      preset="card"
      title="项目管理"
      style="width: 520px; max-width: 90vw"
      :bordered="false"
    >
      <NSpin :show="projectStore.loading">
        <div v-if="projectStore.projects.length" class="project-list">
          <div
            v-for="p in projectStore.projects"
            :key="p.id"
            class="project-item"
            :class="{ active: p.id === props.currentProjectId }"
            @click="handleSelect(p.id)"
          >
            <div class="project-info">
              <div class="project-name">
                <span class="name-text">{{ p.name }}</span>
                <NTag
                  v-if="p.id === props.currentProjectId"
                  type="primary"
                  size="tiny"
                  round
                >
                  当前
                </NTag>
              </div>
              <div class="project-code">{{ p.code }}</div>
            </div>
            <NPopconfirm
              placement="left"
              @positive-click="handleDelete(p.id)"
            >
              <template #trigger>
                <NButton
                  size="tiny"
                  type="error"
                  ghost
                  @click.stop
                >
                  删除
                </NButton>
              </template>
              确认删除项目「{{ p.name }}」？该操作不可恢复，且会级联删除项目下所有数据。
            </NPopconfirm>
          </div>
        </div>
        <NEmpty v-else description="暂无项目" size="small" />
      </NSpin>

      <template #footer>
        <NSpace justify="end">
          <NButton @click="showManager = false">关闭</NButton>
          <NButton type="primary" @click="openCreate">+ 新建项目</NButton>
        </NSpace>
      </template>
    </NModal>

    <!-- 新建项目弹窗（居中） -->
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
            placeholder="请选择"
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

// 触发按钮在侧边栏内，使用 --app-rail-* 令牌
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
    font-size: 11px;
    line-height: 1.2;
    text-align: center;
    max-width: 52px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

// 弹窗内容在主内容区，使用 --app-* 令牌
.project-list {
  max-height: 420px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 4px 0;
}

.project-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--app-divider);
  background: var(--app-card-bg);
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;

  &:hover {
    background: var(--app-bg);
  }

  &.active {
    border-color: var(--app-primary);
    background: color-mix(in srgb, var(--app-primary) 8%, transparent);
  }

  .project-info {
    min-width: 0;
    flex: 1;
  }

  .project-name {
    font-size: 13px;
    font-weight: 500;
    color: var(--app-text-1);
    display: flex;
    align-items: center;
    gap: 6px;

    .name-text {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }

  .project-code {
    font-size: 11px;
    color: var(--app-text-3);
    margin-top: 2px;
  }
}
</style>
