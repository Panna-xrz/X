<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue'
import {
  NCard,
  NDataTable,
  NSpace,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NDatePicker,
  NSelect,
  NTag,
  NPopconfirm,
  NEmpty,
  useMessage
} from 'naive-ui'
import type { DataTableColumns, SelectOption } from 'naive-ui'
import { getNodes, createNode, updateNode, deleteNode, getContracts } from '@/api/contract'
import type { ContractNode } from '@/types'

const message = useMessage()

const loading = ref(false)
const dataList = ref<ContractNode[]>([])
const total = ref(0)

// 合同筛选与下拉数据
const contractFilter = ref<number | null>(null)
const contractOptions = ref<SelectOption[]>([])

// 状态映射
const statusMap: Record<string, { label: string; type: 'default' | 'info' | 'success' | 'warning' | 'error' }> = {
  planned: { label: '计划中', type: 'default' },
  invoiced: { label: '已开票', type: 'info' },
  received: { label: '已收款', type: 'success' },
  overdue: { label: '逾期', type: 'error' }
}

const statusOptions = [
  { label: '计划中', value: 'planned' },
  { label: '已开票', value: 'invoiced' },
  { label: '已收款', value: 'received' },
  { label: '逾期', value: 'overdue' }
]

// 表格列
const columns = computed<DataTableColumns<ContractNode>>(() => [
  { title: '收费节点', key: 'name' },
  {
    title: '合同金额占比',
    key: 'ratio',
    width: 120,
    render: (row) => (row.ratio != null ? `${row.ratio}%` : '-')
  },
  {
    title: '金额',
    key: 'amount',
    width: 130,
    render: (row) => (row.amount != null ? `¥ ${row.amount.toLocaleString()}` : '-')
  },
  { title: '计划日期', key: 'planDate', width: 120, render: (row) => row.planDate || '-' },
  { title: '实际日期', key: 'actualDate', width: 120, render: (row) => row.actualDate || '-' },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      const s = statusMap[row.status] || statusMap.planned
      return h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 130,
    render: (row) =>
      h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            { size: 'small', text: true, type: 'primary', onClick: () => openEdit(row) },
            { default: () => '编辑' }
          ),
          h(
            NPopconfirm,
            { onPositiveClick: () => removeNode(row.id) },
            {
              trigger: () =>
                h(
                  NButton,
                  { size: 'small', text: true, type: 'error' },
                  { default: () => '删除' }
                ),
              default: () => '确认删除该收费节点？'
            }
          )
        ]
      })
  }
])

// 新增/编辑弹窗
const showModal = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null) // null 表示新增
const formModel = reactive({
  contractId: null as number | null,
  name: '',
  amount: null as number | null,
  ratio: null as number | null,
  planDate: null as string | null,
  actualDate: null as string | null,
  status: 'planned',
  remarks: ''
})

// 加载合同下拉
async function loadContractOptions() {
  try {
    const res = await getContracts({ page: 1, pageSize: 100 })
    contractOptions.value = (res.list || []).map((c) => ({
      label: `${c.code || c.id} ${c.name}`,
      value: c.id
    }))
  } catch {
    contractOptions.value = []
  }
}

// 加载列表
async function loadList() {
  loading.value = true
  try {
    const params: { page: number; pageSize: number; contractId?: number } = {
      page: 1,
      pageSize: 50
    }
    if (contractFilter.value) params.contractId = contractFilter.value
    const res = await getNodes(params)
    dataList.value = res.list || []
    total.value = res.total || 0
  } catch (e) {
    dataList.value = []
    message.error(e instanceof Error ? e.message : '加载收费节点失败')
  } finally {
    loading.value = false
  }
}

// 打开新增
function openCreate() {
  editingId.value = null
  Object.assign(formModel, {
    contractId: contractFilter.value,
    name: '',
    amount: null,
    ratio: null,
    planDate: null,
    actualDate: null,
    status: 'planned',
    remarks: ''
  })
  showModal.value = true
}

// 打开编辑
function openEdit(row: ContractNode) {
  editingId.value = row.id
  Object.assign(formModel, {
    contractId: row.contractId,
    name: row.name,
    amount: row.amount,
    ratio: row.ratio,
    planDate: row.planDate,
    actualDate: row.actualDate,
    status: row.status,
    remarks: row.remarks || ''
  })
  showModal.value = true
}

// 提交新增/编辑
async function submit() {
  if (!formModel.name) {
    message.warning('请填写收费节点名称')
    return
  }
  if (!formModel.contractId) {
    message.warning('请选择所属合同')
    return
  }
  submitting.value = true
  try {
    const payload = {
      name: formModel.name,
      ratio: formModel.ratio,
      amount: formModel.amount,
      planDate: formModel.planDate,
      actualDate: formModel.actualDate,
      status: formModel.status,
      remarks: formModel.remarks || null
    }
    if (editingId.value) {
      await updateNode(editingId.value, payload)
      message.success('更新成功')
    } else {
      await createNode({ ...payload, contractId: formModel.contractId })
      message.success('新增成功')
    }
    showModal.value = false
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '提交失败')
  } finally {
    submitting.value = false
  }
}

// 删除节点
async function removeNode(id: number) {
  try {
    await deleteNode(id)
    message.success('删除成功')
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

onMounted(() => {
  loadContractOptions()
  loadList()
})
</script>

<template>
  <NCard title="收费记账" :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
        <NSelect
          v-model:value="contractFilter"
          :options="contractOptions"
          placeholder="按合同筛选（全部）"
          clearable
          filterable
          size="small"
          style="width: 240px"
          @update:value="loadList"
        />
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="openCreate">+ 新增收费节点</NButton>
      </NSpace>
    </template>

    <NDataTable :columns="columns" :data="dataList" :loading="loading" :bordered="false">
      <template #empty>
        <NEmpty description="暂无收费节点，请新增" />
      </template>
    </NDataTable>
  </NCard>

  <NModal
    v-model:show="showModal"
    preset="card"
    :title="editingId ? '编辑收费节点' : '新增收费节点'"
    style="width: 480px"
    :bordered="false"
  >
    <NForm label-placement="left" label-width="88">
      <NFormItem label="所属合同" required>
        <NSelect
          v-model:value="formModel.contractId"
          :options="contractOptions"
          placeholder="选择合同"
          filterable
          :disabled="Boolean(editingId)"
        />
      </NFormItem>
      <NFormItem label="收费节点" required>
        <NInput v-model:value="formModel.name" placeholder="如：设计费-首付款" />
      </NFormItem>
      <NFormItem label="占比(%)">
        <NInputNumber v-model:value="formModel.ratio" :min="0" :max="100" style="width: 100%" />
      </NFormItem>
      <NFormItem label="金额">
        <NInputNumber v-model:value="formModel.amount" :min="0" :precision="2" style="width: 100%" />
      </NFormItem>
      <NFormItem label="计划日期">
        <NDatePicker
          v-model:formatted-value="formModel.planDate"
          value-format="yyyy-MM-dd"
          type="date"
          clearable
          style="width: 100%"
        />
      </NFormItem>
      <NFormItem label="实际日期">
        <NDatePicker
          v-model:formatted-value="formModel.actualDate"
          value-format="yyyy-MM-dd"
          type="date"
          clearable
          style="width: 100%"
        />
      </NFormItem>
      <NFormItem label="状态">
        <NSelect v-model:value="formModel.status" :options="statusOptions" />
      </NFormItem>
      <NFormItem label="备注">
        <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
      </NFormItem>
    </NForm>

    <template #footer>
      <NSpace justify="end">
        <NButton size="small" @click="showModal = false">取消</NButton>
        <NButton size="small" type="primary" :loading="submitting" @click="submit">确定</NButton>
      </NSpace>
    </template>
  </NModal>
</template>
