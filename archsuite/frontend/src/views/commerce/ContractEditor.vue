<script setup lang="ts">
import { h, ref, reactive, onMounted, computed } from 'vue'
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
  NDataTable,
  NTag,
  NAlert,
  useMessage
} from 'naive-ui'
import type { DataTableColumns, SelectOption } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'
import {
  getContract,
  createContract,
  updateContract,
  generateContract,
  reviewContract,
  getContracts
} from '@/api/contract'
import { getProjects } from '@/api/project'
import type {
  Contract,
  ContractType,
  ContractRiskItem
} from '@/types'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const contractId = computed(() => Number(route.params.id) || 0)
const isEdit = computed(() => contractId.value > 0)

const loading = ref(false)
const saving = ref(false)
const genLoading = ref(false)
const reviewLoading = ref(false)

// 合同表单（与后端 ContractPayload 契约对齐）
const formModel = reactive({
  code: '',
  name: '',
  type: 'main' as ContractType,
  projectId: null as number | null,
  partyA: '',
  partyB: '',
  amount: null as number | null,
  status: 'draft',
  signedDate: null as string | null,
  parentContractId: null as number | null,
  remarks: '',
  contentText: ''
})

const typeOptions = [
  { label: '主合同', value: 'main' },
  { label: '补充协议', value: 'supplement' }
]

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '审核中', value: 'reviewing' },
  { label: '已签订', value: 'signed' },
  { label: '已终止', value: 'terminated' }
]

// 关联项目 / 主合同下拉数据
const projectOptions = ref<SelectOption[]>([])
const mainContractOptions = ref<SelectOption[]>([])

// AI 审核结果
const reviewResult = ref<{ risks: ContractRiskItem[]; raw: string | null } | null>(null)

// 风险等级 → 标签颜色
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
      return levelTagMap[level]
        ? h(NTag, { type: levelTagMap[level], size: 'small', round: true }, { default: () => level })
        : level
    }
  },
  { title: '改进建议', key: 'suggestion', render: (row) => row.suggestion || '-' }
]

// 加载关联项目下拉
async function loadProjectOptions() {
  try {
    const res = await getProjects({ page: 1, pageSize: 100 })
    projectOptions.value = (res.list || []).map((p) => ({
      label: `${p.code} ${p.name}`,
      value: p.id
    }))
  } catch {
    projectOptions.value = []
  }
}

// 加载主合同下拉（补充协议可选）
async function loadMainContractOptions() {
  try {
    const res = await getContracts({ page: 1, pageSize: 100 })
    mainContractOptions.value = (res.list || [])
      .filter((c) => c.type === 'main' && c.id !== contractId.value)
      .map((c) => ({
        label: `${c.code} ${c.name}`,
        value: c.id
      }))
  } catch {
    mainContractOptions.value = []
  }
}

// 加载合同详情
async function loadDetail() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const data = await getContract(contractId.value)
    Object.assign(formModel, {
      code: data.code || '',
      name: data.name || '',
      type: data.type,
      projectId: data.projectId,
      partyA: data.partyA || '',
      partyB: data.partyB || '',
      amount: data.amount,
      status: data.status,
      signedDate: data.signedDate,
      parentContractId: data.parentContractId,
      remarks: data.remarks || '',
      contentText: data.contentText || ''
    })
  } catch (e) {
    message.error(e instanceof Error ? e.message : '加载合同详情失败')
  } finally {
    loading.value = false
  }
}

// 校验必填
function validate(): boolean {
  if (!formModel.name) {
    message.warning('请填写合同名称')
    return false
  }
  if (!formModel.projectId) {
    message.warning('请选择关联项目')
    return false
  }
  return true
}

// 保存（新建或更新）
async function submit() {
  if (!validate()) return
  saving.value = true
  try {
    const payload = {
      name: formModel.name,
      code: formModel.code,
      type: formModel.type,
      projectId: formModel.projectId!, // validate() 已确保非空
      partyA: formModel.partyA || null,
      partyB: formModel.partyB || null,
      amount: formModel.amount,
      status: formModel.status,
      signedDate: formModel.signedDate,
      parentContractId: formModel.type === 'supplement' ? formModel.parentContractId : null,
      remarks: formModel.remarks || null,
      contentText: formModel.contentText || null
    }
    if (isEdit.value) {
      await updateContract(contractId.value, payload)
      message.success('保存成功')
    } else {
      const created: Contract = await createContract(payload)
      message.success('创建成功')
      router.replace(`/commerce/contract/${created.id}`)
    }
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

// AI 起草合同正文（仅已保存合同可用）
async function generate() {
  if (!isEdit.value) {
    message.warning('请先保存合同后再起草')
    return
  }
  genLoading.value = true
  try {
    const res = await generateContract(contractId.value)
    formModel.contentText = res.content
    message.success('AI 起草完成，正文已回填，可编辑后保存')
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 起草失败')
  } finally {
    genLoading.value = false
  }
}

// AI 审核合同（需已有正文）
async function review() {
  if (!isEdit.value) {
    message.warning('请先保存合同后再审核')
    return
  }
  if (!formModel.contentText) {
    message.warning('合同尚无正文，请先起草或录入正文')
    return
  }
  reviewLoading.value = true
  try {
    const res = await reviewContract(contractId.value)
    reviewResult.value = { risks: res.risks, raw: res.raw }
    message.success(res.risks.length ? `AI 审核完成，发现 ${res.risks.length} 条风险` : 'AI 审核完成')
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 审核失败')
  } finally {
    reviewLoading.value = false
  }
}

onMounted(() => {
  loadProjectOptions()
  loadMainContractOptions()
  loadDetail()
})
</script>

<template>
  <NCard :title="isEdit ? '合同编辑' : '新增合同'" :bordered="false" size="small">
    <NSpin :show="loading">
      <NForm label-placement="left" label-width="100">
        <NFormItem label="合同名称" required>
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
        <NFormItem label="关联项目" required>
          <NSelect
            v-model:value="formModel.projectId"
            :options="projectOptions"
            placeholder="请选择关联项目"
            filterable
          />
        </NFormItem>
        <NFormItem v-if="formModel.type === 'supplement'" label="主合同">
          <NSelect
            v-model:value="formModel.parentContractId"
            :options="mainContractOptions"
            placeholder="补充协议关联的主合同"
            filterable
            clearable
          />
        </NFormItem>
        <NFormItem label="甲方">
          <NInput v-model:value="formModel.partyA" placeholder="甲方单位" />
        </NFormItem>
        <NFormItem label="乙方">
          <NInput v-model:value="formModel.partyB" placeholder="乙方单位" />
        </NFormItem>
        <NFormItem label="合同金额">
          <NInputNumber
            v-model:value="formModel.amount"
            :min="0"
            :precision="2"
            style="width: 100%"
            placeholder="合同金额"
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
        <NFormItem label="状态">
          <NSelect v-model:value="formModel.status" :options="statusOptions" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>

      <NDivider title="合同正文" title-placement="left">
        <NSpace size="small">
          <NButton size="small" type="primary" :loading="genLoading" @click="generate">
            AI 起草正文
          </NButton>
          <NButton size="small" :loading="reviewLoading" @click="review">
            AI 审核风险
          </NButton>
        </NSpace>
      </NDivider>

      <NInput
        v-model:value="formModel.contentText"
        type="textarea"
        :rows="14"
        placeholder="合同正文（可点击「AI 起草正文」自动生成，支持手动编辑，随保存提交）"
      />

      <NSpace justify="end" style="margin-top: 16px">
        <NButton :loading="saving" type="primary" @click="submit">
          {{ isEdit ? '保存' : '创建' }}
        </NButton>
      </NSpace>

      <!-- AI 审核结果：风险清单 -->
      <div v-if="reviewResult" class="review-result">
        <NDivider title="AI 审核结果" title-placement="left" />
        <template v-if="reviewResult.risks.length">
          <NDataTable
            :columns="riskColumns"
            :data="reviewResult.risks"
            :bordered="false"
            :single-line="false"
          />
        </template>
        <template v-else>
          <NAlert type="success" :bordered="false">
            未发现风险，或 AI 返回了无法结构化解析的结果
          </NAlert>
          <NAlert v-if="reviewResult.raw" type="info" :bordered="false" style="margin-top: 12px" title="原始内容">
            {{ reviewResult.raw }}
          </NAlert>
        </template>
      </div>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.review-result {
  margin-top: 16px;
}
</style>
