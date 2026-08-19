<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NDatePicker,
  NInputNumber,
  NButton,
  NSpace,
  NSpin,
  useMessage
} from 'naive-ui'
import { getProject, updateProject } from '@/api/project'
import { useProjectStore } from '@/stores/project'
import type { Project } from '@/types'

// 基本信息 Tab：项目主体字段编辑
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const projectStore = useProjectStore()
const loading = ref(false)
const saving = ref(false)

const formModel = reactive<Partial<Project>>({
  name: '',
  code: '',
  client: '',
  location: '',
  type: '',
  scale: '',
  phase: '',
  status: 'draft',
  longitude: null,
  latitude: null,
  startDate: null,
  endDate: null,
  description: ''
})

const typeOptions = [
  { label: '公共建筑', value: '公共建筑' },
  { label: '住宅', value: '住宅' },
  { label: '商业综合体', value: '商业综合体' },
  { label: '工业建筑', value: '工业建筑' },
  { label: '其他', value: '其他' }
]

const phaseOptions = [
  { label: '概念设计', value: '概念设计' },
  { label: '方案设计', value: '方案设计' },
  { label: '初步设计', value: '初步设计' },
  { label: '施工图设计', value: '施工图设计' },
  { label: '施工配合', value: '施工配合' },
  { label: '竣工', value: '竣工' }
]

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '规划中', value: 'planning' },
  { label: '进行中', value: 'in-progress' },
  { label: '已完成', value: 'completed' },
  { label: '已归档', value: 'archived' }
]

async function loadDetail() {
  if (!props.projectId) return
  loading.value = true
  try {
    const data = await getProject(props.projectId)
    Object.assign(formModel, {
      name: data.name,
      code: data.code,
      client: data.client,
      location: data.location,
      type: data.type,
      scale: data.scale,
      phase: data.phase,
      status: data.status,
      longitude: data.longitude,
      latitude: data.latitude,
      startDate: data.startDate,
      endDate: data.endDate,
      description: data.description
    })
  } catch (e) {
    message.error(e instanceof Error ? e.message : '加载项目详情失败')
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!props.projectId) return
  if (!formModel.name) {
    message.warning('请填写项目名称')
    return
  }
  if (!formModel.code) {
    message.warning('请填写项目编号')
    return
  }
  saving.value = true
  try {
    await updateProject(props.projectId, {
      name: formModel.name,
      code: formModel.code,
      client: formModel.client || null,
      location: formModel.location || null,
      type: formModel.type || null,
      scale: formModel.scale || null,
      phase: formModel.phase || null,
      status: formModel.status,
      longitude: formModel.longitude,
      latitude: formModel.latitude,
      startDate: formModel.startDate,
      endDate: formModel.endDate,
      description: formModel.description || null
    })
    // 同步刷新项目列表/当前项目，使侧栏切换器显示最新名称
    await projectStore.refreshCurrent()
    message.success('保存成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

watch(() => props.projectId, () => loadDetail(), { immediate: false })
onMounted(() => loadDetail())
</script>

<template>
  <NCard :bordered="false" size="small">
    <NSpin :show="loading">
      <NForm label-placement="left" label-width="100" :show-require-mark="false">
        <div class="form-grid">
          <NFormItem label="项目名称" required>
            <NInput v-model:value="formModel.name" placeholder="请输入项目名称" />
          </NFormItem>
          <NFormItem label="项目编号" required>
            <NInput v-model:value="formModel.code" placeholder="请输入项目编号" />
          </NFormItem>
          <NFormItem label="委托方">
            <NInput v-model:value="formModel.client" placeholder="请输入委托方" />
          </NFormItem>
          <NFormItem label="项目类型">
            <NSelect v-model:value="formModel.type" :options="typeOptions" placeholder="请选择" clearable />
          </NFormItem>
          <NFormItem label="项目地址">
            <NInput v-model:value="formModel.location" placeholder="请输入项目地址" />
          </NFormItem>
          <NFormItem label="建设规模">
            <NInput v-model:value="formModel.scale" placeholder="如：总建筑面积 50000㎡" />
          </NFormItem>
          <NFormItem label="设计阶段">
            <NSelect v-model:value="formModel.phase" :options="phaseOptions" placeholder="请选择阶段" clearable />
          </NFormItem>
          <NFormItem label="状态">
            <NSelect v-model:value="formModel.status" :options="statusOptions" />
          </NFormItem>
          <NFormItem label="经度">
            <NInputNumber v-model:value="formModel.longitude" :precision="6" :step="0.000001" style="width: 100%" placeholder="经度" />
          </NFormItem>
          <NFormItem label="纬度">
            <NInputNumber v-model:value="formModel.latitude" :precision="6" :step="0.000001" style="width: 100%" placeholder="纬度" />
          </NFormItem>
          <NFormItem label="开工日期">
            <NDatePicker v-model:formatted-value="formModel.startDate" value-format="yyyy-MM-dd" type="date" clearable style="width: 100%" />
          </NFormItem>
          <NFormItem label="竣工日期">
            <NDatePicker v-model:formatted-value="formModel.endDate" value-format="yyyy-MM-dd" type="date" clearable style="width: 100%" />
          </NFormItem>
        </div>
        <NFormItem label="项目描述">
          <NInput v-model:value="formModel.description" type="textarea" :rows="3" placeholder="项目概述/背景描述" />
        </NFormItem>
      </NForm>

      <NSpace justify="end">
        <NButton :loading="saving" type="primary" @click="save">保存基本信息</NButton>
      </NSpace>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 24px;
}
</style>
