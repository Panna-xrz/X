<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSpace,
  NSpin,
  useMessage
} from 'naive-ui'
import { getProjectCultural, upsertProjectCultural } from '@/api/project'
import type { ProjectCultural } from '@/types'

// 人文环境 Tab：文化符号、地域建筑、风俗等
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const saving = ref(false)

const formModel = reactive<ProjectCultural>({
  culturalSymbols: '',
  regionalArchitecture: '',
  urbanColorScheme: '',
  localCustoms: '',
  historicalCulture: '',
  remarks: ''
})

async function load() {
  if (!props.projectId) return
  loading.value = true
  try {
    const data = await getProjectCultural(props.projectId)
    Object.assign(formModel, {
      culturalSymbols: data.culturalSymbols,
      regionalArchitecture: data.regionalArchitecture,
      urbanColorScheme: data.urbanColorScheme,
      localCustoms: data.localCustoms,
      historicalCulture: data.historicalCulture,
      remarks: data.remarks
    })
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!props.projectId) return
  saving.value = true
  try {
    await upsertProjectCultural(props.projectId, {
      culturalSymbols: formModel.culturalSymbols || null,
      regionalArchitecture: formModel.regionalArchitecture || null,
      urbanColorScheme: formModel.urbanColorScheme || null,
      localCustoms: formModel.localCustoms || null,
      historicalCulture: formModel.historicalCulture || null,
      remarks: formModel.remarks || null
    })
    message.success('保存成功')
  } catch (e) {
    message.error(e instanceof Error ? e.message : '保存失败')
  } finally {
    saving.value = false
  }
}

watch(() => props.projectId, () => load(), { immediate: false })
onMounted(() => load())
</script>

<template>
  <NCard :bordered="false" size="small">
    <NSpin :show="loading">
      <NForm label-placement="left" label-width="120">
        <NFormItem label="文化符号">
          <NInput v-model:value="formModel.culturalSymbols" type="textarea" :rows="2" placeholder="如：传统纹样、书法、剪纸等" />
        </NFormItem>
        <NFormItem label="地域建筑符号">
          <NInput v-model:value="formModel.regionalArchitecture" type="textarea" :rows="2" placeholder="如：徽派建筑马头墙、四合院" />
        </NFormItem>
        <NFormItem label="城市色彩属性">
          <NInput v-model:value="formModel.urbanColorScheme" type="textarea" :rows="2" placeholder="如：暖灰主调 + 朱砂点缀" />
        </NFormItem>
        <NFormItem label="地域风俗">
          <NInput v-model:value="formModel.localCustoms" type="textarea" :rows="2" placeholder="当地习俗、节庆等" />
        </NFormItem>
        <NFormItem label="地域历史文化">
          <NInput v-model:value="formModel.historicalCulture" type="textarea" :rows="3" placeholder="场地历史沿革、文化脉络" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>

      <NSpace justify="end">
        <NButton :loading="saving" type="primary" @click="save">保存人文环境</NButton>
      </NSpace>
    </NSpin>
  </NCard>
</template>
