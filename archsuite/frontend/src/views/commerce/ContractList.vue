<script setup lang="ts">
import { ref, onMounted, computed, h } from 'vue'
import {
  NCard,
  NDataTable,
  NSpace,
  NButton,
  NTag,
  NPopconfirm,
  NEmpty,
  useMessage
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { useRouter } from 'vue-router'
import { getContracts, deleteContract } from '@/api/contract'
import type { Contract, ContractType } from '@/types'

const router = useRouter()
const message = useMessage()

const loading = ref(false)
const dataList = ref<Contract[]>([])

// 合同类型映射
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

// 表格列
const columns = computed<DataTableColumns<Contract>>(() => [
  { title: '合同编号', key: 'code', width: 140, render: (row) => row.code || '-' },
  { title: '合同名称', key: 'name' },
  {
    title: '类型',
    key: 'type',
    width: 110,
    render: (row) => {
      const t = typeMap[row.type] || typeMap.main
      return h(NTag, { type: t.type, size: 'small', round: true }, { default: () => t.label })
    }
  },
  {
    title: '合同金额',
    key: 'amount',
    width: 120,
    render: (row) => (row.amount != null ? `¥ ${row.amount.toLocaleString()}` : '-')
  },
  {
    title: '签订日期',
    key: 'signedDate',
    width: 130,
    render: (row) => row.signedDate || '-'
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
    width: 130,
    render: (row) =>
      h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            {
              size: 'small',
              text: true,
              type: 'primary',
              onClick: () => router.push(`/commerce/contract/edit/${row.id}`)
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

// 加载合同列表
async function loadList() {
  loading.value = true
  try {
    const res = await getContracts({ page: 1, pageSize: 50 })
    dataList.value = res.list || []
  } catch (e) {
    dataList.value = []
    message.error(e instanceof Error ? e.message : '加载合同列表失败')
  } finally {
    loading.value = false
  }
}

// 删除合同
async function removeContract(id: number) {
  try {
    await deleteContract(id)
    message.success('删除成功')
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

onMounted(() => {
  loadList()
})
</script>

<template>
  <NCard title="合同列表" :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="router.push('/commerce/contract/edit')">
          + 新增合同
        </NButton>
      </NSpace>
    </template>

    <NDataTable :columns="columns" :data="dataList" :loading="loading" :bordered="false">
      <template #empty>
        <NEmpty description="暂无合同，请新增" />
      </template>
    </NDataTable>
  </NCard>
</template>
