<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NDatePicker,
  NInputNumber,
  NSpace,
  NButton,
  NDivider,
  NSpin,
  NCollapse,
  NCollapseItem,
  useMessage
} from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'
import {
  getContract,
  createContract,
  updateContract,
  aiGenerateContract,
  aiReviewContract
} from '@/api/contract'
import type { Contract, ContractType, ContractNode } from '@/types'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const contractId = computed(() => (route.params.id as string) || '')
const isEdit = computed(() => Boolean(contractId.value))

const loading = ref(false)
const saving = ref(false)
const genLoading = ref(false)
const reviewLoading = ref(false)

// 合同表单
const formModel = reactive<Partial<Contract>>({
  code: '',
  name: '',
  type: 'main',
  projectId: '',
  party: '',
  amount: 0,
  status: 'draft',
  signedDate: undefined,
  parentContractId: '',
  remarks: ''
})

const typeOptions = [
  { label: '主合同', value: 'main' },
  { label: '补充协议', value: 'supplement' }
]

// 条款节点（AI 生成或后端返回）
const nodes = ref<ContractNode[]>([])
// 审核意见
const reviewResult = ref<{ issues: string[]; suggestions: string[] } | null>(null)

// 加载合同详情
async function loadDetail() {
  if (!contractId.value) return
  loading.value = true
  try {
    const data = await getContract(contractId.value)
    Object.assign(formModel, data)
  } catch (e) {
    message.error('加载合同详情失败')
  } finally {
    loading.value = false
  }
}

// 保存（新建或更新）
async function submit() {
  if (!formModel.name) {
    message.warning('请填写合同名称')
    return
  }
  saving.value = true
  try {
    if (isEdit.value) {
      await updateContract(contractId.value, formModel)
      message.success('保存成功')
    } else {
      await createContract(formModel)
      message.success('创建成功')
      router.push('/commerce/contracts')
    }
  } catch (e) {
    message.error('保存失败')
  } finally {
    saving.value = false
  }
}

// AI 起草合同条款
async function generate() {
  if (!formModel.projectId) {
    message.warning('请先选择关联项目')
    return
  }
  if (!formModel.type) {
    message.warning('请选择合同类型')
    return
  }
  genLoading.value = true
  try {
    const res = await aiGenerateContract({
      projectId: formModel.projectId,
      type: formModel.type as ContractType,
      parentContractId: formModel.parentContractId
    })
    nodes.value = res || []
    message.success(`AI 起草完成，共 ${nodes.value.length} 个章节`)
  } catch (e) {
    message.error('AI 起草失败')
  } finally {
    genLoading.value = false
  }
}

// AI 审核合同
async function review() {
  if (!isEdit.value) {
    message.warning('请先保存合同后再审核')
    return
  }
  reviewLoading.value = true
  try {
    const res = await aiReviewContract(contractId.value)
    reviewResult.value = res
    message.success('AI 审核完成')
  } catch (e) {
    message.error('AI 审核失败')
  } finally {
    reviewLoading.value = false
  }
}

onMounted(() => {
  loadDetail()
})
</script>

<template>
  <NCard :title="isEdit ? '合同编辑' : '新增合同'" :bordered="false" size="small">
    <NSpin :show="loading">
      <NForm label-placement="left" label-width="100">
        <NFormItem label="合同名称">
          <NInput v-model:value="formModel.name" placeholder="合同名称" />
        </NFormItem>
        <NFormItem label="合同编号">
          <NInput v-model:value="formModel.code" placeholder="合同编号" />
        </NFormItem>
        <NFormItem label="合同类型">
          <NSelect
            v-model:value="formModel.type"
            :options="typeOptions"
            placeholder="主合同 / 补充协议"
          />
        </NFormItem>
        <NFormItem label="关联项目">
          <NSelect
            v-model:value="formModel.projectId"
            :options="[]"
            placeholder="请选择关联项目"
            filterable
          />
        </NFormItem>
        <NFormItem v-if="formModel.type === 'supplement'" label="主合同">
          <NSelect
            v-model:value="formModel.parentContractId"
            :options="[]"
            placeholder="补充协议关联的主合同"
          />
        </NFormItem>
        <NFormItem label="乙方">
          <NInput v-model:value="formModel.party" placeholder="乙方单位" />
        </NFormItem>
        <NFormItem label="合同金额">
          <NInputNumber
            v-model:value="formModel.amount"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </NFormItem>
        <NFormItem label="签订日期">
          <NDatePicker
            v-model:formatted-value="formModel.signedDate"
            value-format="yyyy-MM-dd"
            type="date"
            clearable
            style="width: 100%"
          />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>

      <NDivider title="AI 辅助" title-placement="left" />

      <NSpace>
        <NButton type="primary" :loading="genLoading" @click="generate">
          AI 起草条款
        </NButton>
        <NButton :loading="reviewLoading" @click="review">
          AI 审核
        </NButton>
        <NButton :loading="saving" type="primary" ghost @click="submit">
          {{ isEdit ? '保存' : '创建' }}
        </NButton>
      </NSpace>

      <!-- AI 起草条款 -->
      <NCollapse v-if="nodes.length" class="nodes" arrow-placement="right">
        <NCollapseItem
          v-for="node in nodes"
          :key="node.id"
          :title="node.title"
          :name="node.id"
        >
          <div class="node-content">{{ node.content }}</div>
        </NCollapseItem>
      </NCollapse>

      <!-- AI 审核结果 -->
      <div v-if="reviewResult" class="review-result">
        <NCard :bordered="false" size="small" title="审核意见">
          <div class="block">
            <div class="block-title">问题</div>
            <ul>
              <li v-for="(item, i) in reviewResult.issues" :key="i">{{ item }}</li>
              <li v-if="!reviewResult.issues.length">无</li>
            </ul>
          </div>
          <div class="block">
            <div class="block-title">建议</div>
            <ul>
              <li v-for="(item, i) in reviewResult.suggestions" :key="i">{{ item }}</li>
              <li v-if="!reviewResult.suggestions.length">无</li>
            </ul>
          </div>
        </NCard>
      </div>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.nodes {
  margin-top: 16px;
}

.node-content {
  color: var(--app-text-2);
  font-size: 13px;
  white-space: pre-wrap;
  padding: 8px 4px;
}

.review-result {
  margin-top: 16px;
}

.block {
  margin-bottom: 12px;

  .block-title {
    font-weight: 600;
    margin-bottom: 6px;
    color: var(--app-text-1);
  }

  ul {
    padding-left: 20px;
    color: var(--app-text-2);
    font-size: 13px;
    line-height: 1.8;
  }
}
</style>
