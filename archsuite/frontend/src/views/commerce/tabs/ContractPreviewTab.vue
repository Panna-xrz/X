<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import {
  NCard,
  NSelect,
  NButton,
  NSpace,
  NEmpty,
  NSpin,
  useMessage
} from 'naive-ui'
import type { SelectOption } from 'naive-ui'
import { getContracts, getContract, downloadContract } from '@/api/contract'
import type { Contract } from '@/types'

// 合同预览 Tab：选择项目下合同 + 下载
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const downloading = ref(false)

const contractList = ref<Contract[]>([])
const selectedId = ref<number | null>(null)
const currentContract = ref<Contract | null>(null)

const contractOptions = computed<SelectOption[]>(() =>
  contractList.value.map((c) => ({
    label: `${c.code || c.id} ${c.name}`,
    value: c.id
  }))
)

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
    return
  }
  loading.value = true
  try {
    currentContract.value = await getContract(selectedId.value)
  } catch (e) {
    currentContract.value = null
    message.error(e instanceof Error ? e.message : '加载合同详情失败')
  } finally {
    loading.value = false
  }
}

async function handleDownload() {
  if (!selectedId.value) {
    message.warning('请先选择合同')
    return
  }
  downloading.value = true
  try {
    const blob = await downloadContract(selectedId.value)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const name = currentContract.value?.name || `contract-${selectedId.value}`
    a.download = `${name}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    message.success('下载成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '下载失败')
  } finally {
    downloading.value = false
  }
}

watch(() => props.projectId, () => {
  selectedId.value = null
  currentContract.value = null
  loadContracts()
}, { immediate: false })

onMounted(() => loadContracts())
</script>

<template>
  <NCard :bordered="false" size="small">
    <template #header>
      <span>合同预览</span>
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
        <NButton size="small" :loading="downloading" :disabled="!selectedId" type="primary" @click="handleDownload">
          下载合同
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
        <pre class="content-text">{{ currentContract.contentText || '（合同正文为空）' }}</pre>
      </div>
      <NEmpty v-else description="请选择合同进行预览" size="large" style="padding: 40px 0" />
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

.content-text {
  font-family: inherit;
  font-size: 13px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--app-text-1);
  background: var(--app-bg, #f7f8fa);
  padding: 16px;
  border-radius: 6px;
  max-height: 560px;
  overflow-y: auto;
  margin: 0;
}
</style>
