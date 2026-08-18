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
  NEmpty
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { getBillings, createBilling } from '@/api/contract'
import type { BillingRecord } from '@/types'

const loading = ref(false)
const dataList = ref<BillingRecord[]>([])

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
const columns = computed<DataTableColumns<BillingRecord>>(() => [
  { title: '收费节点', key: 'node' },
  { title: '合同金额占比', key: 'ratio', width: 120, render: (row) => (row.ratio ?? '-') + '%' },
  {
    title: '金额',
    key: 'amount',
    width: 130,
    render: (row) => `¥ ${(row.amount ?? 0).toLocaleString()}`
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
  }
])

// 新增弹窗
const showModal = ref(false)
const submitting = ref(false)
const formModel = reactive<Partial<BillingRecord>>({
  contractId: '',
  node: '',
  amount: 0,
  ratio: undefined,
  planDate: undefined,
  actualDate: undefined,
  status: 'planned',
  remarks: ''
})

// 加载列表
async function loadList() {
  loading.value = true
  try {
    const res = await getBillings({ page: 1, pageSize: 50 })
    dataList.value = res.list || []
  } catch (e) {
    dataList.value = []
  } finally {
    loading.value = false
  }
}

// 打开新增
function openCreate() {
  Object.assign(formModel, {
    contractId: '',
    node: '',
    amount: 0,
    ratio: undefined,
    planDate: undefined,
    actualDate: undefined,
    status: 'planned',
    remarks: ''
  })
  showModal.value = true
}

// 提交新增
async function submit() {
  if (!formModel.node) {
    return
  }
  submitting.value = true
  try {
    await createBilling(formModel)
    showModal.value = false
    await loadList()
  } catch (e) {
    // 忽略，保持弹窗便于重试
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadList()
})
</script>

<template>
  <NCard title="收费记账" :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
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
    title="新增收费节点"
    style="width: 480px"
    :bordered="false"
  >
    <NForm label-placement="left" label-width="88">
      <NFormItem label="所属合同">
        <NSelect v-model:value="formModel.contractId" :options="[]" placeholder="选择合同" />
      </NFormItem>
      <NFormItem label="收费节点">
        <NInput v-model:value="formModel.node" placeholder="如：设计费-首付款" />
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
