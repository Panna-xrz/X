<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NRadioGroup,
  NRadioButton,
  NInputNumber,
  NDatePicker,
  NButton,
  NSpace,
  NDivider,
  NUpload,
  NAlert,
  useMessage
} from 'naive-ui'
import type { UploadCustomRequestOptions } from 'naive-ui'
import { createContract, updateContract, generateContract } from '@/api/contract'
import type { ContractType, Contract } from '@/types'

// 合同草拟 Tab：模板模式 / 参考模式
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const draftLoading = ref(false)
const saving = ref(false)

// 模式：template 内置模板 / reference 参考上传
const mode = ref<'template' | 'reference'>('template')

// 模板类型（设计/勘察/咨询）
const templateType = ref<'设计合同' | '勘察合同' | '咨询合同'>('设计合同')

const templateOptions = [
  { label: '设计合同', value: '设计合同' },
  { label: '勘察合同', value: '勘察合同' },
  { label: '咨询合同', value: '咨询合同' }
]

// 参考文本
const referenceText = ref('')

// 表单元数据
const formModel = reactive({
  code: '',
  name: '',
  type: 'main' as ContractType,
  partyA: '',
  partyB: '',
  amount: null as number | null,
  signedDate: null as string | null,
  remarks: '',
  contentText: ''
})

// 已起草的合同 ID（若已通过 AI 起草生成）
const draftedContractId = ref<number | null>(null)

const typeOptions = [
  { label: '主合同', value: 'main' },
  { label: '补充协议', value: 'supplement' }
]

// 参考文件自定义请求：读取文本内容
function handleReferenceUpload({ file, onFinish }: UploadCustomRequestOptions) {
  const f = file.file
  if (!f) {
    message.error('文件读取失败')
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    const text = typeof reader.result === 'string' ? reader.result : ''
    referenceText.value = text
    formModel.contentText = text
    message.success(`已加载参考合同：${f.name}`)
    onFinish()
  }
  reader.onerror = () => {
    message.error('读取参考文件失败')
  }
  reader.readAsText(f)
}

// AI 起草（模板模式）：先创建草稿合同，再调用 generateContract
async function aiDraft() {
  if (!props.projectId) {
    message.warning('请先选择项目')
    return
  }
  if (mode.value === 'reference' && !referenceText.value) {
    message.warning('请先上传或粘贴参考合同文本')
    return
  }
  if (!formModel.name) {
    formModel.name = `${templateType.value}-${new Date().toLocaleDateString()}`
  }
  draftLoading.value = true
  try {
    // 1. 创建草稿合同
    let contractId = draftedContractId.value
    if (!contractId) {
      const created: Contract = await createContract({
        projectId: props.projectId,
        name: formModel.name,
        code: formModel.code || `DRAFT-${Date.now()}`,
        type: formModel.type,
        partyA: formModel.partyA || null,
        partyB: formModel.partyB || null,
        amount: formModel.amount,
        signedDate: formModel.signedDate,
        status: 'draft',
        remarks: formModel.remarks || null,
        contentText: formModel.contentText || null
      })
      contractId = created.id
      draftedContractId.value = contractId
    }

    // 2. 调用 AI 起草
    const res = await generateContract(contractId)
    formModel.contentText = res.content
    message.success('AI 起草完成，正文已回填，可继续编辑后保存')
  } catch (e) {
    message.error(e instanceof Error ? e.message : 'AI 起草失败')
  } finally {
    draftLoading.value = false
  }
}

// 保存为合同：若有 draftedContractId 则更新，否则新建
async function save() {
  if (!props.projectId) {
    message.warning('请先选择项目')
    return
  }
  if (!formModel.name) {
    message.warning('请填写合同名称')
    return
  }
  if (!formModel.contentText) {
    message.warning('合同正文为空，无法保存')
    return
  }
  saving.value = true
  try {
    const payload = {
      name: formModel.name,
      code: formModel.code || undefined,
      type: formModel.type,
      projectId: props.projectId,
      partyA: formModel.partyA || null,
      partyB: formModel.partyB || null,
      amount: formModel.amount,
      signedDate: formModel.signedDate,
      status: 'draft',
      remarks: formModel.remarks || null,
      contentText: formModel.contentText
    }
    if (draftedContractId.value) {
      await updateContract(draftedContractId.value, payload)
      message.success('保存成功')
    } else {
      const created: Contract = await createContract(payload)
      draftedContractId.value = created.id
      message.success('已保存为新合同')
    }
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

// 重置
function reset() {
  draftedContractId.value = null
  Object.assign(formModel, {
    code: '',
    name: '',
    type: 'main',
    partyA: '',
    partyB: '',
    amount: null,
    signedDate: null,
    remarks: '',
    contentText: ''
  })
  referenceText.value = ''
}

watch(() => props.projectId, () => reset(), { immediate: false })
</script>

<template>
  <NCard :bordered="false" size="small">
    <template #header>
      <span>合同草拟</span>
    </template>

    <div class="mode-bar">
      <NRadioGroup v-model:value="mode">
        <NRadioButton value="template">内置模板模式</NRadioButton>
        <NRadioButton value="reference">上传参考模式</NRadioButton>
      </NRadioGroup>
    </div>

    <!-- 模板模式 -->
    <div v-if="mode === 'template'" class="mode-section">
      <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
        选择合同模板类型，点击「AI 起草」，系统将基于项目信息自动生成合同正文，可继续编辑后保存为合同。
      </NAlert>
      <NForm label-placement="left" label-width="100">
        <NFormItem label="模板类型">
          <NSelect v-model:value="templateType" :options="templateOptions" style="width: 200px" />
        </NFormItem>
      </NForm>
    </div>

    <!-- 参考模式 -->
    <div v-else class="mode-section">
      <NAlert type="info" :bordered="false" style="margin-bottom: 12px">
        上传其他项目的合同文本作为参考，AI 基于参考文本 + 当前项目信息生成新合同正文。
      </NAlert>
      <NUpload
        :custom-request="handleReferenceUpload"
        :show-file-list="false"
        accept=".txt,.md,.text"
      >
        <NButton size="small">选择参考文件</NButton>
      </NUpload>
      <NInput
        v-model:value="referenceText"
        type="textarea"
        :rows="4"
        placeholder="也可直接粘贴参考合同正文"
        style="margin-top: 8px"
        @update:value="(v: string) => (formModel.contentText = v)"
      />
    </div>

    <NDivider style="margin: 12px 0" />

    <!-- 元数据表单 -->
    <NForm label-placement="left" label-width="100">
      <div class="form-grid">
        <NFormItem label="合同名称">
          <NInput v-model:value="formModel.name" placeholder="如：XX 项目设计合同" />
        </NFormItem>
        <NFormItem label="合同编号">
          <NInput v-model:value="formModel.code" placeholder="合同编号" />
        </NFormItem>
        <NFormItem label="合同类型">
          <NSelect v-model:value="formModel.type" :options="typeOptions" />
        </NFormItem>
        <NFormItem label="合同金额">
          <NInputNumber v-model:value="formModel.amount" :min="0" :precision="2" style="width: 100%" />
        </NFormItem>
        <NFormItem label="甲方">
          <NInput v-model:value="formModel.partyA" placeholder="甲方单位" />
        </NFormItem>
        <NFormItem label="乙方">
          <NInput v-model:value="formModel.partyB" placeholder="乙方单位" />
        </NFormItem>
        <NFormItem label="签订日期">
          <NDatePicker v-model:formatted-value="formModel.signedDate" value-format="yyyy-MM-dd" type="date" clearable style="width: 100%" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" placeholder="备注" />
        </NFormItem>
      </div>
    </NForm>

    <NSpace style="margin: 12px 0">
      <NButton type="primary" :loading="draftLoading" @click="aiDraft">AI 起草</NButton>
      <NButton @click="reset">重置</NButton>
    </NSpace>

    <NInput
      v-model:value="formModel.contentText"
      type="textarea"
      :rows="14"
      placeholder="合同正文（AI 起草后会回填至此，可手动编辑）"
    />

    <NSpace justify="end" style="margin-top: 16px">
      <NButton type="primary" :loading="saving" @click="save">保存为合同</NButton>
    </NSpace>
  </NCard>
</template>

<style scoped lang="scss">
.mode-bar {
  margin-bottom: 12px;
}

.mode-section {
  padding: 8px 0;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 24px;
}
</style>
