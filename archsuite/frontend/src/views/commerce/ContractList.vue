<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue'
import {
  NCard,
  NDataTable,
  NSpace,
  NButton,
  NTag,
  NSelect,
  NEmpty
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { useRouter } from 'vue-router'
import { getContracts } from '@/api/contract'
import type { Contract, ContractType } from '@/types'

const router = useRouter()

const loading = ref(false)
const dataList = ref<Contract[]>([])

// 当前选中的项目
const projectId = ref<string>('')

// 合同类型映射
const typeMap: Record<ContractType, { label: string; type: 'success' | 'warning' }> = {
  main: { label: '主合同', type: 'success' },
  supplement: { label: '补充协议', type: 'warning' }
}

const statusMap: Record<string, string> = {
  draft: '草稿',
  reviewing: '审核中',
  signed: '已签订',
  terminated: '已终止'
}

// 表格列
const columns = computed<DataTableColumns<Contract>>(() => [
  { title: '合同编号', key: 'code', width: 140 },
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
    render: (row) => `¥ ${(row.amount ?? 0).toLocaleString()}`
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
    render: (row) => statusMap[row.status] || row.status
  },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    render: (row) =>
      h(
        NButton,
        {
          size: 'small',
          text: true,
          type: 'primary',
          onClick: () => router.push(`/commerce/contract/edit/${row.id}`)
        },
        { default: () => '编辑' }
      )
  }
])

// 加载合同列表（按项目）
async function loadList() {
  loading.value = true
  try {
    const params: { projectId?: string; page: number; pageSize: number } = {
      page: 1,
      pageSize: 50
    }
    if (projectId.value) params.projectId = projectId.value
    const res = await getContracts(params as { projectId?: string })
    dataList.value = res.list || []
  } catch (e) {
    dataList.value = []
  } finally {
    loading.value = false
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
        <NSelect
          v-model:value="projectId"
          placeholder="筛选项目"
          clearable
          :options="[]"
          size="small"
          style="width: 200px"
        />
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="router.push('/commerce/contract/edit')">
          + 新增合同
        </NButton>
      </NSpace>
    </template>

    <NDataTable
      :columns="columns"
      :data="dataList"
      :loading="loading"
      :bordered="false"
    >
      <template #empty>
        <NEmpty description="暂无合同，请新增主合同或补充协议" />
      </template>
    </NDataTable>
  </NCard>
</template>
