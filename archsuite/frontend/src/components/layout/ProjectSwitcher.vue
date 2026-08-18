<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import {
  NPopover,
  NButton,
  NSpace,
  NDivider,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NPopconfirm,
  NEmpty,
  NSpin,
  useMessage
} from 'naive-ui'
import { useProjectStore } from '@/stores/project'
import ProjectIcon from '@/components/icons/ProjectIcon.vue'

// 项目切换器：在图标栏顶部，下拉切换/新建/删除项目
const props = defineProps<{
  currentProjectId: number | null
}>()

const emit = defineEmits<{
  (e: 'selectProject', id: number): void
  (e: 'createProject', payload: { name: string; code: string; client?: string; location?: string; type?: string }): void
  (e: 'deleteProject'): void
}>()

const projectStore = useProjectStore()
const message = useMessage()

// 当前项目名称（截断显示）
const currentName = computed(() => projectStore.currentProject?.name || '选择项目')

// 新建项目弹窗
const showModal = ref(false)
const submitting = ref(false)
const formModel = reactive<{
  name: string
  code: string
  client: string
  location: string
  type: string
}>({
  name: '',
  code: '',
  client: '',
  location: '',
  type: ''
})

const typeOptions = [
  { label: '公共建筑', value: '公共建筑' },
  { label: '住宅', value: '住宅' },
  { label: '商业综合体', value: '商业综合体' },
  { label: '工业建筑', value: '工业建筑' }
]

// 选择项目
function handleSelect(id: number) {
  emit('selectProject', id)
}

// 打开新建弹窗
function openCreate() {
  Object.assign(formModel, { name: '', code: '', client: '', location: '', type: '' })
  showModal.value = true
}

// 提交新建
async function submitCreate() {
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
    const payload = {
      name: formModel.name,
      code: formModel.code,
      client: formModel.client || undefined,
      location: formModel.location || undefined,
      type: formModel.type || undefined
    }
    emit('createProject', payload)
    showModal.value = false
  } catch (e) {
    message.error(e instanceof Error ? e.message : '创建失败')
  } finally {
    submitting.value = false
  }
}

// 删除当前项目
function handleDelete() {
  emit('deleteProject')
}
</script>

<template>
  <div class="project-switcher">
    <NPopover trigger="click" placement="right-start" :width="240">
      <template #trigger>
        <button class="switcher-trigger" :title="currentName">
          <ProjectIcon class="trigger-icon" />
          <span class="switcher-name">{{ currentName }}</span>
        </button>
      </template>

      <div class="switcher-panel">
        <NSpin :show="projectStore.loading">
          <div v-if="projectStore.projects.length" class="project-list">
            <div
              v-for="p in projectStore.projects"
              :key="p.id"
              class="project-item"
              :class="{ active: p.id === props.currentProjectId }"
              @click="handleSelect(p.id)"
            >
              <div class="project-name">{{ p.name }}</div>
              <div class="project-code">{{ p.code }}</div>
            </div>
          </div>
          <NEmpty v-else description="暂无项目" size="small" />
        </NSpin>

        <NDivider style="margin: 8px 0" />
        <NSpace vertical :size="6">
          <NButton block size="small" type="primary" @click="openCreate">
            + 新建项目
          </NButton>
          <NPopconfirm
            v-if="props.currentProjectId"
            placement="right"
            @positive-click="handleDelete"
          >
            <template #trigger>
              <NButton block size="small" type="error" ghost :disabled="!props.currentProjectId">
                删除当前项目
              </NButton>
            </template>
            确认删除当前项目？该操作不可恢复，且会级联删除项目下所有数据。
          </NPopconfirm>
        </NSpace>
      </div>
    </NPopover>

    <NModal
      v-model:show="showModal"
      preset="card"
      title="新建项目"
      style="width: 480px"
      :bordered="false"
    >
      <NForm label-placement="left" label-width="80">
        <NFormItem label="项目名称" required>
          <NInput v-model:value="formModel.name" placeholder="请输入项目名称" />
        </NFormItem>
        <NFormItem label="项目编号" required>
          <NInput v-model:value="formModel.code" placeholder="请输入项目编号" />
        </NFormItem>
        <NFormItem label="委托方">
          <NInput v-model:value="formModel.client" placeholder="请输入委托方" />
        </NFormItem>
        <NFormItem label="项目地址">
          <NInput v-model:value="formModel.location" placeholder="请输入项目地址" />
        </NFormItem>
        <NFormItem label="项目类型">
          <NSelect v-model:value="formModel.type" :options="typeOptions" placeholder="请选择" clearable />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton size="small" @click="showModal = false">取消</NButton>
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
  color: #ffffffa6;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;

  &:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #fff;
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

.switcher-panel {
  padding: 4px 0;
}

.project-list {
  max-height: 320px;
  overflow-y: auto;
}

.project-item {
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: var(--app-bg, #f7f8fa);
  }

  &.active {
    background: rgba(32, 128, 240, 0.12);
  }

  .project-name {
    font-size: 13px;
    font-weight: 500;
  }

  .project-code {
    font-size: 11px;
    color: var(--app-text-3, #a0a0a0);
    margin-top: 2px;
  }
}
</style>
