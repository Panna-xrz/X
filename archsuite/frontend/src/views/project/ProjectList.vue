<script setup lang="ts">
import { ref, reactive, onMounted, h } from 'vue'
import {
  NCard,
  NButton,
  NDataTable,
  NSpace,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NTag,
  useMessage
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { useRouter } from 'vue-router'
import { getProjects, createProject } from '@/api/project'
import type { Project } from '@/types'

const router = useRouter()
const message = useMessage()

// 列表数据与加载状态
const loading = ref(false)
const dataList = ref<Project[]>([])

// 状态标签颜色映射
const statusMap: Record<string, { label: string; type: 'default' | 'success' | 'warning' | 'info' | 'error' }> = {
  draft: { label: '草稿', type: 'default' },
  planning: { label: '规划中', type: 'info' },
  'in-progress': { label: '进行中', type: 'warning' },
  completed: { label: '已完成', type: 'success' },
  archived: { label: '已归档', type: 'default' }
}

// 表格列定义
const columns: DataTableColumns<Project> = [
  { title: '项目编号', key: 'code', width: 120 },
  { title: '项目名称', key: 'name' },
  { title: '委托方', key: 'client', width: 160 },
  { title: '项目类型', key: 'type', width: 120 },
  { title: '状态', key: 'status', width: 100, render: (row) => {
    const s = statusMap[row.status] || statusMap.draft
    return h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
  }},
  { title: '更新时间', key: 'updatedAt', width: 180 },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    render: (row) =>
      h(
        NButton,
        { size: 'small', text: true, type: 'primary', onClick: () => goDetail(row.id) },
        { default: () => '查看详情' }
      )
  }
]

// 新增弹窗状态
const showModal = ref(false)
const submitting = ref(false)
const formModel = reactive<Partial<Project>>({
  name: '',
  code: '',
  client: '',
  location: '',
  type: '',
  scale: '',
  status: 'draft',
  description: ''
})

const typeOptions = [
  { label: '公共建筑', value: '公共建筑' },
  { label: '住宅', value: '住宅' },
  { label: '商业综合体', value: '商业综合体' },
  { label: '工业建筑', value: '工业建筑' }
]

// 加载项目列表
async function loadList() {
  loading.value = true
  try {
    const res = await getProjects({ page: 1, pageSize: 20 })
    dataList.value = res.list || []
  } catch (e) {
    dataList.value = []
    message.error(e instanceof Error ? e.message : '加载项目列表失败')
  } finally {
    loading.value = false
  }
}

// 跳转详情
function goDetail(id: number) {
  router.push(`/project/${id}`)
}

// 打开新增弹窗
function openCreate() {
  Object.assign(formModel, {
    name: '',
    code: '',
    client: '',
    location: '',
    type: '',
    scale: '',
    status: 'draft',
    description: ''
  })
  showModal.value = true
}

// 提交新增
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
    await createProject(formModel)
    message.success('项目创建成功')
    showModal.value = false
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '创建失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadList()
})
</script>

<template>
  <NCard title="项目列表" :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="openCreate">+ 新增项目</NButton>
      </NSpace>
    </template>

    <NDataTable
      :columns="columns"
      :data="dataList"
      :loading="loading"
      :bordered="false"
      :single-line="false"
      remote
    />
  </NCard>

  <NModal
    v-model:show="showModal"
    preset="card"
    title="新增项目"
    style="width: 520px"
    :bordered="false"
  >
    <NForm label-placement="left" label-width="88">
      <NFormItem label="项目名称">
        <NInput v-model:value="formModel.name" placeholder="请输入项目名称" />
      </NFormItem>
      <NFormItem label="项目编号">
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
      <NFormItem label="备注">
        <NInput v-model:value="formModel.description" type="textarea" :rows="2" placeholder="备注说明" />
      </NFormItem>
    </NForm>

    <template #footer>
      <NSpace justify="end">
        <NButton size="small" @click="showModal = false">取消</NButton>
        <NButton size="small" type="primary" :loading="submitting" @click="submitCreate">确定</NButton>
      </NSpace>
    </template>
  </NModal>
</template>
