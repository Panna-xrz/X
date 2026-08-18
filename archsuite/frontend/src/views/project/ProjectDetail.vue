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
  NDataTable,
  NEmpty,
  NAlert,
  useMessage
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { useRoute } from 'vue-router'
import { getProject, updateProject, getProjectExtra, aiExtractProjectInfo } from '@/api/project'
import type { Project, AiExtractResult, ProjectExtraItem } from '@/types'

const route = useRoute()
const message = useMessage()

const projectId = computed(() => Number(route.params.id) || 0)

const loading = ref(false)
const saving = ref(false)
const aiLoading = ref(false)

// 项目基本信息（可编辑字段白名单）
const project = reactive<Partial<Project>>({})
// 扩展信息（后端动态键值对 items）
const extraItems = ref<ProjectExtraItem[]>([])
// AI 提取结果
const aiResult = ref<AiExtractResult | null>(null)

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '规划中', value: 'planning' },
  { label: '进行中', value: 'in-progress' },
  { label: '已完成', value: 'completed' },
  { label: '已归档', value: 'archived' }
]

// 扩展字段键 → 中文标签
const extraLabelMap: Record<string, string> = {
  landArea: '用地面积',
  buildingArea: '建筑面积',
  floorsAbove: '地上层数',
  floorsUnder: '地下层数',
  heightLimit: '高度限制',
  greenRatio: '绿地率',
  plotRatio: '容积率',
  designStage: '设计阶段',
  remarks: '备注'
}

const extraColumns: DataTableColumns<ProjectExtraItem> = [
  {
    title: '字段',
    key: 'fieldKey',
    width: 140,
    render: (row) => extraLabelMap[row.fieldKey] || row.fieldKey
  },
  { title: '值', key: 'fieldValue', render: (row) => row.fieldValue ?? '-' },
  {
    title: '来源',
    key: 'aiSource',
    width: 100,
    render: (row) => row.aiSource || '手动录入'
  }
]

// AI 解析结果表格列
interface FieldRow {
  key: string
  value: string | null
}

const aiFieldColumns: DataTableColumns<FieldRow> = [
  {
    title: '字段',
    key: 'key',
    width: 140,
    render: (row) => extraLabelMap[row.key] || row.key
  },
  { title: '值', key: 'value', render: (row) => row.value ?? '-' }
]

// AI 解析结果转为表格行
const aiFieldRows = computed<FieldRow[]>(() =>
  Object.entries(aiResult.value?.fields || {}).map(([key, value]) => ({ key, value }))
)

// 加载详情与扩展信息
async function loadDetail() {
  if (!projectId.value) return
  loading.value = true
  try {
    const data = await getProject(projectId.value)
    Object.assign(project, data)
    await loadExtra()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '加载项目详情失败')
  } finally {
    loading.value = false
  }
}

// 加载扩展信息（可能尚未生成，不阻塞）
async function loadExtra() {
  try {
    const res = await getProjectExtra(projectId.value)
    extraItems.value = res.items || []
  } catch {
    extraItems.value = []
  }
}

// 保存基本信息（仅提交可编辑字段）
async function saveBase() {
  saving.value = true
  try {
    await updateProject(projectId.value, {
      name: project.name,
      code: project.code,
      client: project.client,
      location: project.location,
      type: project.type,
      scale: project.scale,
      startDate: project.startDate,
      endDate: project.endDate,
      status: project.status,
      description: project.description
    })
    message.success('保存成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

// AI 自动提取项目扩展信息
async function aiExtract() {
  aiLoading.value = true
  try {
    const res = await aiExtractProjectInfo(projectId.value)
    aiResult.value = res
    if (Object.keys(res.fields || {}).length) {
      message.success(`AI 提取完成，共 ${Object.keys(res.fields).length} 个字段`)
      // 提取结果已写入后端，刷新扩展信息展示
      await loadExtra()
    } else {
      message.warning('AI 未能解析出结构化字段，请查看原始内容')
    }
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 提取失败，请稍后重试')
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

        <!-- 扩展信息（动态键值对） -->
        <NTabPane name="extra" tab="扩展信息">
          <NDataTable
            v-if="extraItems.length"
            :columns="extraColumns"
            :data="extraItems"
            :bordered="false"
            :single-line="false"
          />
          <NEmpty v-else description="暂无扩展信息，可通过「AI 辅助获取」自动提取" />
        </NTabPane>

        <!-- AI 辅助获取 -->
        <NTabPane name="ai" tab="AI 辅助获取">
          <NSpace vertical :size="16">
            <div class="ai-tip">
              点击下方按钮，由 AI 根据项目基本信息自动解析用地面积、建筑面积、容积率等扩展字段并保存。
            </div>
            <NButton type="primary" :loading="aiLoading" @click="aiExtract">
              AI 自动获取
            </NButton>
            <NCard v-if="aiResult" :bordered="false" size="small" title="AI 解析结果">
              <NAlert v-if="!aiFieldRows.length" type="warning" :bordered="false">
                未能解析出结构化字段
              </NAlert>
              <NDataTable
                v-else
                :columns="aiFieldColumns"
                :data="aiFieldRows"
                :bordered="false"
                :single-line="false"
              />
              <NAlert
                v-if="aiResult.raw"
                type="info"
                :bordered="false"
                style="margin-top: 12px"
                title="原始内容"
              >
                {{ aiResult.raw }}
              </NAlert>
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
