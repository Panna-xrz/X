<script setup lang="ts">
import { h, ref, computed, watch, onMounted } from 'vue'
import {
  NCard,
  NSelect,
  NButton,
  NSpace,
  NEmpty,
  NSpin,
  NDataTable,
  NTag,
  NInput,
  NAlert,
  useMessage
} from 'naive-ui'
import type { SelectOption, DataTableColumns } from 'naive-ui'
import { getContracts, getContract, reviewContract, updateContract } from '@/api/contract'
import type { Contract, ContractRiskItem } from '@/types'

// 合同审查 Tab：选合同 → AI 审查 → 风险清单
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const reviewing = ref(false)
const saving = ref(false)

const contractList = ref<Contract[]>([])
const selectedId = ref<number | null>(null)
const currentContract = ref<Contract | null>(null)
const editableContent = ref('')

// 审查结果
const risks = ref<ContractRiskItem[]>([])
const rawText = ref<string | null>(null)

const contractOptions = computed<SelectOption[]>(() =>
  contractList.value.map((c) => ({
    label: `${c.code || c.id} ${c.name}`,
    value: c.id
  }))
)

// 风险等级 → 标签颜色（高=红/中=黄/低=蓝）
const levelTagMap: Record<string, 'error' | 'warning' | 'info' | 'default'> = {
  高: 'error',
  中: 'warning',
  低: 'info'
}

const riskColumns: DataTableColumns<ContractRiskItem> = [
  { title: '风险条款', key: 'clause', render: (row) => row.clause || '-' },
  {
    title: '等级',
    key: 'level',
    width: 80,
    render: (row) => {
      const level = row.level || '未知'
      const t = levelTagMap[level]
      return t
        ? h(NTag, { type: t, size: 'small', round: true }, { default: () => level })
        : level
    }
  },
  { title: '改进建议', key: 'suggestion', render: (row) => row.suggestion || '-' }
]

async function loadContracts() {
  if (!props.projectId) return
  loading.value = true
  try {
    const res = await getContracts({ projectId: props.projectId, page: 1, pageSize: 200 })
    contractList.value = res.list || []
    if (!selectedId.value && contractList.value.length) {
      selectedId.value = contractList.value[0].id
      await loadDetail()
    }
  } catch (e) {
    contractList.value = []
    message.error(e instanceof Error ? e.message : '加载合同列表失败')
  } finally {
    loading.value = false
  }
}

async function loadDetail() {
  if (!selectedId.value) {
    currentContract.value = null
    editableContent.value = ''
    return
  }
  loading.value = true
  try {
    const data = await getContract(selectedId.value)
    currentContract.value = data
    editableContent.value = data.contentText || ''
  } catch (e) {
    currentContract.value = null
    editableContent.value = ''
    message.error(e instanceof Error ? e.message : '加载合同详情失败')
  } finally {
    loading.value = false
  }
}

async function runReview() {
  if (!selectedId.value) {
    message.warning('请先选择合同')
    return
  }
  if (!editableContent.value) {
    message.warning('合同正文为空，无法审查')
    return
  }
  reviewing.value = true
  try {
    const res = await reviewContract(selectedId.value)
    risks.value = res.risks || []
    rawText.value = res.raw
    message.success(risks.value.length ? `AI 审查完成，发现 ${risks.value.length} 条风险` : 'AI 审查完成，未发现风险')
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 审查失败')
  } finally {
    reviewing.value = false
  }
}

async function saveContent() {
  if (!selectedId.value) return
  saving.value = true
  try {
    await updateContract(selectedId.value, { contentText: editableContent.value })
    message.success('正文保存成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

watch(() => props.projectId, () => {
  selectedId.value = null
  currentContract.value = null
  editableContent.value = ''
  risks.value = []
  rawText.value = null
  loadContracts()
}, { immediate: false })

onMounted(() => loadContracts())
</script>

<template>
  <NCard :bordered="false" size="small">
    <template #header>
      <span>合同审查</span>
    </template>
    <template #header-extra>
      <NSpace>
        <NSelect
          v-model:value="selectedId"
          :options="contractOptions"
          placeholder="选择合同"
          style="width: 320px"
          filterable
          :loading="loading"
          @update:value="loadDetail"
        />
        <NButton size="small" type="primary" :loading="reviewing" :disabled="!selectedId" @click="runReview">
          AI 审查
        </NButton>
        <NButton size="small" :loading="saving" :disabled="!selectedId" @click="saveContent">
          保存正文
        </NButton>
      </NSpace>
    </template>

    <NSpin :show="loading">
      <div v-if="currentContract">
        <div class="meta-bar">
          <span>编号：{{ currentContract.code || '-' }}</span>
          <span>名称：{{ currentContract.name }}</span>
          <span>状态：{{ currentContract.status }}</span>
        </div>

        <NInput
          v-model:value="editableContent"
          type="textarea"
          :rows="14"
          placeholder="合同正文（可编辑后保存）"
        />

        <!-- AI 审查结果 -->
        <div v-if="reviewing || risks.length || rawText" class="review-result">
          <h4 class="section-title">AI 审查结果</h4>
          <template v-if="risks.length">
            <NDataTable :columns="riskColumns" :data="risks" :bordered="false" :single-line="false" />
          </template>
          <template v-else-if="!reviewing">
            <NAlert type="success" :bordered="false">未发现风险</NAlert>
          </template>
          <NAlert v-if="rawText" type="info" :bordered="false" style="margin-top: 12px" title="原始内容">
            {{ rawText }}
          </NAlert>
        </div>
      </div>
      <NEmpty v-else description="请选择合同进行审查" size="large" style="padding: 40px 0" />
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.meta-bar {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: var(--app-text-2);
  padding: 8px 12px;
  background: var(--app-bg, #f7f8fa);
  border-radius: 6px;
  margin-bottom: 12px;
}

.review-result {
  margin-top: 16px;

  .section-title {
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: var(--app-text-1);
  }
}
</style>
