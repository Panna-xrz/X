<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  NCard,
  NTabs,
  NTabPane,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NDatePicker,
  NButton,
  NSpace,
  NSpin,
  NDescriptions,
  NDescriptionsItem,
  useMessage
} from 'naive-ui'
import { useRoute } from 'vue-router'
import { getProject, updateProject, getProjectExtra, aiExtractProjectInfo } from '@/api/project'
import type { Project, ProjectExtra, AiExtractResult } from '@/types'

const route = useRoute()
const message = useMessage()

const projectId = computed(() => (route.params.id as string) || '')

const loading = ref(false)
const saving = ref(false)
const aiLoading = ref(false)

// 项目基本信息
const project = reactive<Partial<Project>>({})
// 扩展信息
const extra = reactive<Partial<ProjectExtra>>({})
// AI 提取结果
const aiResult = ref<AiExtractResult | null>(null)

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '规划中', value: 'planning' },
  { label: '进行中', value: 'in-progress' },
  { label: '已完成', value: 'completed' },
  { label: '已归档', value: 'archived' }
]

// 加载详情
async function loadDetail() {
  if (!projectId.value) return
  loading.value = true
  try {
    const data = await getProject(projectId.value)
    Object.assign(project, data)
    try {
      const extraData = await getProjectExtra(projectId.value)
      Object.assign(extra, extraData)
    } catch {
      // 扩展信息可能尚未生成
    }
  } catch (e) {
    message.error('加载项目详情失败')
  } finally {
    loading.value = false
  }
}

// 保存基本信息
async function saveBase() {
  saving.value = true
  try {
    await updateProject(projectId.value, project)
    message.success('保存成功')
  } catch (e) {
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// AI 自动获取项目信息
async function aiExtract() {
  aiLoading.value = true
  try {
    const res = await aiExtractProjectInfo(projectId.value, { source: 'auto' })
    aiResult.value = res
    if (res.fields) {
      Object.assign(project, res.fields)
    }
    message.success(`AI 提取完成（置信度 ${Math.round(res.confidence * 100)}%）`)
  } catch (e) {
    message.error('AI 提取失败，请稍后重试')
  } finally {
    aiLoading.value = false
  }
}

onMounted(() => {
  loadDetail()
})
</script>

<template>
  <NCard :title="`项目详情 - ${project.name || projectId}`" :bordered="false" size="small">
    <NSpin :show="loading">
      <NTabs type="line" animated>
        <!-- 基本信息 -->
        <NTabPane name="base" tab="基本信息">
          <NForm label-placement="left" label-width="100">
            <NFormItem label="项目名称">
              <NInput v-model:value="project.name" placeholder="项目名称" />
            </NFormItem>
            <NFormItem label="项目编号">
              <NInput v-model:value="project.code" placeholder="项目编号" />
            </NFormItem>
            <NFormItem label="委托方">
              <NInput v-model:value="project.client" placeholder="委托方" />
            </NFormItem>
            <NFormItem label="项目类型">
              <NInput v-model:value="project.type" placeholder="项目类型" />
            </NFormItem>
            <NFormItem label="项目地址">
              <NInput v-model:value="project.location" placeholder="项目地址" />
            </NFormItem>
            <NFormItem label="建设规模">
              <NInput v-model:value="project.scale" placeholder="建设规模" />
            </NFormItem>
            <NFormItem label="状态">
              <NSelect v-model:value="project.status" :options="statusOptions" placeholder="状态" />
            </NFormItem>
            <NFormItem label="开工日期">
              <NDatePicker v-model:formatted-value="project.startDate" value-format="yyyy-MM-dd" type="date" clearable />
            </NFormItem>
            <NFormItem label="竣工日期">
              <NDatePicker v-model:formatted-value="project.endDate" value-format="yyyy-MM-dd" type="date" clearable />
            </NFormItem>
            <NFormItem label="备注">
              <NInput v-model:value="project.description" type="textarea" :rows="2" />
            </NFormItem>
          </NForm>
          <NSpace justify="end">
            <NButton type="primary" :loading="saving" @click="saveBase">保存基本信息</NButton>
          </NSpace>
        </NTabPane>

        <!-- 扩展信息 -->
        <NTabPane name="extra" tab="扩展信息">
          <NDescriptions label-placement="left" bordered :column="2">
            <NDescriptionsItem label="用地面积">{{ extra.landArea ?? '-' }} ㎡</NDescriptionsItem>
            <NDescriptionsItem label="建筑面积">{{ extra.buildingArea ?? '-' }} ㎡</NDescriptionsItem>
            <NDescriptionsItem label="地上层数">{{ extra.floorsAbove ?? '-' }}</NDescriptionsItem>
            <NDescriptionsItem label="地下层数">{{ extra.floorsUnder ?? '-' }}</NDescriptionsItem>
            <NDescriptionsItem label="高度限制">{{ extra.heightLimit ?? '-' }} m</NDescriptionsItem>
            <NDescriptionsItem label="绿地率">{{ extra.greenRatio ?? '-' }}</NDescriptionsItem>
            <NDescriptionsItem label="容积率">{{ extra.plotRatio ?? '-' }}</NDescriptionsItem>
            <NDescriptionsItem label="设计阶段">{{ extra.designStage ?? '-' }}</NDescriptionsItem>
            <NDescriptionsItem label="备注" :span="2">{{ extra.remarks ?? '-' }}</NDescriptionsItem>
          </NDescriptions>
        </NTabPane>

        <!-- AI 辅助获取 -->
        <NTabPane name="ai" tab="AI 辅助获取">
          <NSpace vertical :size="16">
            <div class="ai-tip">
              点击下方按钮，由 AI 从上传的资料或现场调研中自动解析并填充项目基本信息。
            </div>
            <NButton type="primary" :loading="aiLoading" @click="aiExtract">
              AI 自动获取
            </NButton>
            <NCard v-if="aiResult" :bordered="false" size="small" title="AI 解析结果">
              <NDescriptions label-placement="left" :column="1" bordered>
                <NDescriptionsItem label="置信度">{{ Math.round(aiResult.confidence * 100) }}%</NDescriptionsItem>
                <NDescriptionsItem label="解析字段">{{ JSON.stringify(aiResult.fields) }}</NDescriptionsItem>
                <NDescriptionsItem v-if="aiResult.raw" label="原始内容">{{ aiResult.raw }}</NDescriptionsItem>
              </NDescriptions>
            </NCard>
          </NSpace>
        </NTabPane>
      </NTabs>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.ai-tip {
  color: var(--app-text-2);
  font-size: 13px;
}
</style>
