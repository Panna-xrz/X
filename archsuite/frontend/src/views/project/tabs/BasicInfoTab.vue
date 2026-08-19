<script setup lang="ts">
import { reactive, ref, watch, onMounted, computed } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NDatePicker,
  NButton,
  NSpace,
  NSpin,
  NTag,
  useMessage
} from 'naive-ui'
import { getProject, updateProject, getProjectExtra, aiExtractProjectInfo } from '@/api/project'
import { getContracts } from '@/api/contract'
import { useProjectStore } from '@/stores/project'
import type { Contract } from '@/types'

// 基本信息 Tab：项目主体字段编辑
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const projectStore = useProjectStore()
const loading = ref(false)
const saving = ref(false)
const aiLoading = ref(false)

const formModel = reactive({
  name: '',
  code: '',
  client: '',
  location: '',
  type: '',
  phase: '',
  startDate: null as string | null,
  endDate: null as string | null,
  description: ''
})

// 项目类型：按《建筑工程设计资质分类标准》GB/T 50360 及《民用建筑设计通则》GB 50352
const typeOptions = [
  { label: '居住建筑', value: '居住建筑' },
  { label: '一般公共建筑', value: '一般公共建筑' },
  { label: '大型公共建筑', value: '大型公共建筑' },
  { label: '工业建筑', value: '工业建筑' },
  { label: '农业建筑', value: '农业建筑' },
  { label: '构筑物', value: '构筑物' }
]

const phaseOptions = [
  { label: '概念设计', value: '概念设计' },
  { label: '方案设计', value: '方案设计' },
  { label: '初步设计', value: '初步设计' },
  { label: '施工图设计', value: '施工图设计' },
  { label: '施工配合', value: '施工配合' },
  { label: '竣工', value: '竣工' }
]

// 合同数据（用于自动识别节点进度）
const contracts = ref<Contract[]>([])

// 节点进度（自动从合同状态聚合，只读）
const progressInfo = computed(() => {
  if (!contracts.value.length) {
    return { text: '未立项', type: 'default' as const }
  }
  const hasSigned = contracts.value.some(c => c.status === 'signed')
  const hasDraft = contracts.value.some(c => c.status === 'draft')
  const hasReviewing = contracts.value.some(c => c.status === 'reviewing')
  const allTerminated = contracts.value.every(c => c.status === 'terminated')

  if (allTerminated) return { text: '已终止', type: 'error' as const }
  if (hasSigned) return { text: '执行中', type: 'success' as const }
  if (hasReviewing) return { text: '审核中', type: 'info' as const }
  if (hasDraft) return { text: '草拟中', type: 'warning' as const }
  return { text: '已立项', type: 'default' as const }
})

// AI 提取结果
const aiFields = ref<Record<string, string | null>>({})

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
      phase: data.phase,
      startDate: data.startDate,
      endDate: data.endDate,
      description: data.description
    })
    // 加载合同以自动识别节点进度
    try {
      const res = await getContracts({ projectId: props.projectId, page: 1, pageSize: 50 })
      contracts.value = res.list || []
    } catch {
      contracts.value = []
    }
    // 加载 AI 提取的扩展字段
    try {
      const extra = await getProjectExtra(props.projectId)
      aiFields.value = extra.fields || {}
    } catch {
      aiFields.value = {}
    }
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
      phase: formModel.phase || null,
      startDate: formModel.startDate,
      endDate: formModel.endDate,
      description: formModel.description || null
    })
    await projectStore.refreshCurrent()
    message.success('保存成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

// AI 提取扩展信息
async function aiExtract() {
  if (!props.projectId) return
  aiLoading.value = true
  try {
    const res = await aiExtractProjectInfo(props.projectId)
    if (Object.keys(res.fields || {}).length) {
      aiFields.value = res.fields
      message.success(`AI 提取完成，共 ${Object.keys(res.fields).length} 个字段`)
    } else {
      message.warning('AI 未能解析出结构化字段')
    }
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 提取失败')
  } finally {
    aiLoading.value = false
  }
}

watch(() => props.projectId, () => loadDetail(), { immediate: false })
onMounted(() => loadDetail())
</script>

<template>
  <NCard :bordered="false" size="small">
    <NSpin :show="loading">
      <!-- 节点进度条（只读，自动识别） -->
      <div class="progress-bar">
        <div class="progress-label">节点进度</div>
        <NTag :type="progressInfo.type" round :bordered="false" size="small">
          {{ progressInfo.text }}
        </NTag>
        <span class="progress-hint">（由合同状态自动识别）</span>
      </div>

      <NForm label-placement="left" label-width="100" :show-require-mark="false" style="margin-top: 16px">
        <div class="form-grid">
          <NFormItem label="项目名称" required>
            <NInput v-model:value="formModel.name" placeholder="请输入项目名称" />
          </NFormItem>
          <NFormItem label="项目编号" required>
            <NInput v-model:value="formModel.code" placeholder="请输入项目编号" />
          </NFormItem>
          <NFormItem label="项目类型">
            <NSelect v-model:value="formModel.type" :options="typeOptions" placeholder="请选择（按国标分类）" clearable />
          </NFormItem>
          <NFormItem label="设计阶段">
            <NSelect v-model:value="formModel.phase" :options="phaseOptions" placeholder="请选择阶段" clearable />
          </NFormItem>
          <NFormItem label="委托方">
            <NInput v-model:value="formModel.client" placeholder="委托甲方单位" />
          </NFormItem>
          <NFormItem label="项目地址">
            <NInput v-model:value="formModel.location" placeholder="项目所在地址" />
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

      <!-- AI 提取的扩展字段（只读展示） -->
      <div v-if="Object.keys(aiFields).length" class="ai-fields">
        <div class="section-title">AI 自动识别字段</div>
        <div class="field-grid">
          <div v-for="(value, key) in aiFields" :key="key" class="field-item">
            <span class="field-key">{{ key }}</span>
            <span class="field-value">{{ value || '-' }}</span>
          </div>
        </div>
      </div>

      <NSpace justify="space-between" style="margin-top: 16px">
        <NButton :loading="aiLoading" @click="aiExtract">AI 自动获取</NButton>
        <NButton :loading="saving" type="primary" @click="save">保存基本信息</NButton>
      </NSpace>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.progress-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: var(--app-bg);
  border-radius: var(--app-radius, 8px);

  .progress-label {
    font-size: 0.93em;
    font-weight: 500;
    color: var(--app-text-1);
  }

  .progress-hint {
    font-size: 0.79em;
    color: var(--app-text-3);
  }
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 24px;
}

.ai-fields {
  margin-top: 20px;
  padding: 12px 16px;
  background: var(--app-bg);
  border-radius: var(--app-radius, 8px);

  .section-title {
    font-size: 0.86em;
    font-weight: 500;
    color: var(--app-text-2);
    margin-bottom: 10px;
  }

  .field-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 24px;
  }

  .field-item {
    display: flex;
    align-items: baseline;
    gap: 8px;
    font-size: 0.86em;

    .field-key {
      color: var(--app-text-3);
      min-width: 80px;
      flex-shrink: 0;
    }

    .field-value {
      color: var(--app-text-1);
    }
  }
}
</style>
