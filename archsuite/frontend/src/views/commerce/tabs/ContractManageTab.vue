<script setup lang="ts">
import { h, ref, reactive, computed, watch, onMounted } from 'vue'
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
import type { DataTableColumns, DataTableRowKey } from 'naive-ui'
import { useRouter } from 'vue-router'
import {
  getContracts,
  deleteContract,
  getContractNodes,
  createNode,
  updateNode,
  deleteNode
} from '@/api/contract'
import type { Contract, ContractType, ContractNode } from '@/types'

// 合同管理 Tab：合同列表 + 收费节点管理（展开）
const props = defineProps<{ projectId: number }>()

const router = useRouter()
const message = useMessage()
const loading = ref(false)
const dataList = ref<Contract[]>([])

// 展开的行
const expandedRowKeys = ref<DataTableRowKey[]>([])

// 节点缓存：contractId -> ContractNode[]
const nodesMapValue = ref<Record<number, ContractNode[]>>({})
const nodesLoadingMap = ref<Record<number, boolean>>({})

// 类型 / 状态映射
const typeMap: Record<ContractType, { label: string; type: 'success' | 'warning' }> = {
  main: { label: '主合同', type: 'success' },
  supplement: { label: '补充协议', type: 'warning' }
}

const statusMap: Record<string, { label: string; type: 'default' | 'info' | 'success' | 'warning' | 'error' }> = {
  draft: { label: '草稿', type: 'default' },
  reviewing: { label: '审核中', type: 'info' },
  signed: { label: '已签订', type: 'success' },
  terminated: { label: '已终止', type: 'error' }
}

const nodeStatusMap: Record<string, { label: string; type: 'default' | 'info' | 'success' | 'warning' | 'error' }> = {
  planned: { label: '计划中', type: 'default' },
  invoiced: { label: '已开票', type: 'info' },
  received: { label: '已收款', type: 'success' },
  overdue: { label: '逾期', type: 'error' }
}

const nodeStatusOptions = [
  { label: '计划中', value: 'planned' },
  { label: '已开票', value: 'invoiced' },
  { label: '已收款', value: 'received' },
  { label: '逾期', value: 'overdue' }
]

// 表格列：合同 + 展开（renderExpand）
const columns = computed<DataTableColumns<Contract>>(() => [
  { type: 'expand', expandable: () => true, renderExpand: (row) => renderExpand(row) },
  { title: '编号', key: 'code', width: 140, render: (row) => row.code || '-' },
  { title: '名称', key: 'name' },
  {
    title: '类型',
    key: 'type',
    width: 100,
    render: (row) => {
      const t = typeMap[row.type] || typeMap.main
      return h(NTag, { type: t.type, size: 'small', round: true }, { default: () => t.label })
    }
  },
  {
    title: '金额',
    key: 'amount',
    width: 120,
    render: (row) => (row.amount != null ? `¥ ${row.amount.toLocaleString()}` : '-')
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      const s = statusMap[row.status]
      return s
        ? h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
        : row.status
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 140,
    render: (row) =>
      h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            {
              size: 'small',
              text: true,
              type: 'primary',
              onClick: () => router.push(`/commerce/contract/${row.id}`)
            },
            { default: () => '编辑' }
          ),
          h(
            NPopconfirm,
            { onPositiveClick: () => removeContract(row.id) },
            {
              trigger: () =>
                h(
                  NButton,
                  { size: 'small', text: true, type: 'error' },
                  { default: () => '删除' }
                ),
              default: () => '删除该合同及其全部收费节点？'
            }
          )
        ]
      })
  }
])

// 节点表格列
const nodeColumns: DataTableColumns<ContractNode> = [
  { title: '收费节点', key: 'name' },
  {
    title: '占比',
    key: 'ratio',
    width: 80,
    render: (row) => (row.ratio != null ? `${row.ratio}%` : '-')
  },
  {
    title: '金额',
    key: 'amount',
    width: 120,
    render: (row) => (row.amount != null ? `¥ ${row.amount.toLocaleString()}` : '-')
  },
  { title: '计划日期', key: 'planDate', width: 120, render: (row) => row.planDate || '-' },
  { title: '实际日期', key: 'actualDate', width: 120, render: (row) => row.actualDate || '-' },
  {
    title: '状态',
    key: 'status',
    width: 90,
    render: (row) => {
      const s = nodeStatusMap[row.status] || nodeStatusMap.planned
      return h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 140,
    render: (row) =>
      h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            { size: 'small', text: true, type: 'primary', onClick: () => openEditNode(row) },
            { default: () => '编辑' }
          ),
          h(
            NPopconfirm,
            { onPositiveClick: () => removeNode(row.id, row.contractId) },
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
]

// 渲染展开行：节点列表 + 新增按钮
function renderExpand(row: Contract) {
  const nodes = nodesMapValue.value[row.id] || []
  const nodeLoading = nodesLoadingMap.value[row.id]
  return h('div', { class: 'node-expand' }, [
    h('div', { class: 'node-toolbar' }, [
      h(
        NButton,
        { size: 'small', type: 'primary', onClick: () => openCreateNode(row.id) },
        { default: () => '+ 新增节点' }
      ),
      h(
        NButton,
        { size: 'small', onClick: () => loadNodes(row.id) },
        { default: () => '刷新' }
      )
    ]),
    h(
      NDataTable,
      {
        columns: nodeColumns,
        data: nodes,
        loading: Boolean(nodeLoading),
        bordered: false,
        size: 'small',
        rowKey: (r: ContractNode) => r.id
      },
      {
        empty: () => h(NEmpty, { description: '暂无收费节点', size: 'small' })
      }
    )
  ])
}

// 加载合同列表
async function loadList() {
  if (!props.projectId) return
  loading.value = true
  try {
    const res = await getContracts({ projectId: props.projectId, page: 1, pageSize: 200 })
    dataList.value = res.list || []
  } catch (e) {
    dataList.value = []
    message.error(e instanceof Error ? e.message : '加载合同列表失败')
  } finally {
    loading.value = false
  }
}

// 加载某合同的节点
async function loadNodes(contractId: number) {
  nodesLoadingMap.value[contractId] = true
  try {
    const data = await getContractNodes(contractId)
    nodesMapValue.value[contractId] = data || []
  } catch (e) {
    nodesMapValue.value[contractId] = []
    message.error(e instanceof Error ? e.message : '加载收费节点失败')
  } finally {
    nodesLoadingMap.value[contractId] = false
  }
}

// 行展开变化时加载节点
function handleExpand(keys: DataTableRowKey[]) {
  expandedRowKeys.value = keys
  keys.forEach((k) => {
    if (typeof k === 'number' && !nodesMapValue.value[k]) {
      loadNodes(k)
    }
  })
}

// 删除合同
async function removeContract(id: number) {
  try {
    await deleteContract(id)
    message.success('删除成功')
    delete nodesMapValue.value[id]
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

// ===== 节点新增/编辑弹窗 =====
const showNodeModal = ref(false)
const nodeSubmitting = ref(false)
const editingNodeId = ref<number | null>(null)
const nodeContractId = ref<number | null>(null)
const nodeForm = reactive({
  name: '',
  ratio: null as number | null,
  amount: null as number | null,
  planDate: null as string | null,
  actualDate: null as string | null,
  status: 'planned',
  remarks: ''
})

function openCreateNode(contractId: number) {
  editingNodeId.value = null
  nodeContractId.value = contractId
  Object.assign(nodeForm, {
    name: '',
    ratio: null,
    amount: null,
    planDate: null,
    actualDate: null,
    status: 'planned',
    remarks: ''
  })
  showNodeModal.value = true
}

function openEditNode(row: ContractNode) {
  editingNodeId.value = row.id
  nodeContractId.value = row.contractId
  Object.assign(nodeForm, {
    name: row.name,
    ratio: row.ratio,
    amount: row.amount,
    planDate: row.planDate,
    actualDate: row.actualDate,
    status: row.status,
    remarks: row.remarks || ''
  })
  showNodeModal.value = true
}

async function submitNode() {
  if (!nodeForm.name) {
    message.warning('请填写收费节点名称')
    return
  }
  if (!nodeContractId.value) return
  nodeSubmitting.value = true
  try {
    const payload = {
      name: nodeForm.name,
      ratio: nodeForm.ratio,
      amount: nodeForm.amount,
      planDate: nodeForm.planDate,
      actualDate: nodeForm.actualDate,
      status: nodeForm.status,
      remarks: nodeForm.remarks || null
    }
    if (editingNodeId.value) {
      await updateNode(editingNodeId.value, payload)
      message.success('更新成功')
    } else {
      await createNode({ ...payload, contractId: nodeContractId.value })
      message.success('新增成功')
    }
    showNodeModal.value = false
    await loadNodes(nodeContractId.value)
  } catch (e) {
    message.error(e instanceof Error ? e.message : '提交失败')
  } finally {
    nodeSubmitting.value = false
  }
}

async function removeNode(id: number, contractId: number) {
  try {
    await deleteNode(id)
    message.success('删除成功')
    await loadNodes(contractId)
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

watch(() => props.projectId, () => {
  nodesMapValue.value = {}
  expandedRowKeys.value = []
  loadList()
}, { immediate: false })

onMounted(() => loadList())
</script>

<template>
  <NCard :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="router.push('/commerce/contract/0')">
          + 新增合同
        </NButton>
      </NSpace>
    </template>

    <NDataTable
      :columns="columns"
      :data="dataList"
      :loading="loading"
      :bordered="false"
      :single-line="false"
      :row-key="(row: Contract) => row.id"
      :expanded-row-keys="expandedRowKeys"
      @update:expanded-row-keys="handleExpand"
    >
      <template #empty>
        <NEmpty description="暂无合同，请新增" />
      </template>
    </NDataTable>

    <NModal
      v-model:show="showNodeModal"
      preset="card"
      :title="editingNodeId ? '编辑收费节点' : '新增收费节点'"
      style="width: 460px"
      :bordered="false"
    >
      <NForm label-placement="left" label-width="88">
        <NFormItem label="节点名称" required>
          <NInput v-model:value="nodeForm.name" placeholder="如：设计费-首付款" />
        </NFormItem>
        <div class="form-grid">
          <NFormItem label="占比(%)">
            <NInputNumber v-model:value="nodeForm.ratio" :min="0" :max="100" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="金额">
            <NInputNumber v-model:value="nodeForm.amount" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="计划日期">
            <NDatePicker v-model:formatted-value="nodeForm.planDate" value-format="yyyy-MM-dd" type="date" clearable style="width: 100%" />
          </NFormItem>
          <NFormItem label="实际日期">
            <NDatePicker v-model:formatted-value="nodeForm.actualDate" value-format="yyyy-MM-dd" type="date" clearable style="width: 100%" />
          </NFormItem>
        </div>
        <NFormItem label="状态">
          <NSelect v-model:value="nodeForm.status" :options="nodeStatusOptions" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="nodeForm.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton size="small" @click="showNodeModal = false">取消</NButton>
          <NButton size="small" type="primary" :loading="nodeSubmitting" @click="submitNode">确定</NButton>
        </NSpace>
      </template>
    </NModal>
  </NCard>
</template>

<style scoped lang="scss">
:deep(.node-expand) {
  padding: 8px 0 8px 24px;

  .node-toolbar {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
  }
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 16px;
}
</style>
