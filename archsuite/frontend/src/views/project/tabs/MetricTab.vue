<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NButton,
  NSpace,
  NSpin,
  useMessage
} from 'naive-ui'
import { getProjectMetric, upsertProjectMetric } from '@/api/project'
import type { ProjectMetric } from '@/types'

// 指标信息 Tab：用地性质、容积率、绿地率等
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const saving = ref(false)

const formModel = reactive<ProjectMetric>({
  landUse: '',
  siteArea: null,
  farAbove: null,
  farUnder: null,
  greenRatio: null,
  buildingDensity: null,
  heightLimit: null,
  totalFloorArea: null,
  aboveFloorArea: null,
  underFloorArea: null,
  parkingAbove: null,
  parkingUnder: null,
  remarks: ''
})

async function load() {
  if (!props.projectId) return
  loading.value = true
  try {
    const data = await getProjectMetric(props.projectId)
    Object.assign(formModel, {
      landUse: data.landUse,
      siteArea: data.siteArea,
      farAbove: data.farAbove,
      farUnder: data.farUnder,
      greenRatio: data.greenRatio,
      buildingDensity: data.buildingDensity,
      heightLimit: data.heightLimit,
      totalFloorArea: data.totalFloorArea,
      aboveFloorArea: data.aboveFloorArea,
      underFloorArea: data.underFloorArea,
      parkingAbove: data.parkingAbove,
      parkingUnder: data.parkingUnder,
      remarks: data.remarks
    })
  } catch (e) {
    // 未创建过 metric，吞掉错误
    Object.assign(formModel, {
      landUse: '',
      siteArea: null,
      farAbove: null,
      farUnder: null,
      greenRatio: null,
      buildingDensity: null,
      heightLimit: null,
      totalFloorArea: null,
      aboveFloorArea: null,
      underFloorArea: null,
      parkingAbove: null,
      parkingUnder: null,
      remarks: ''
    })
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!props.projectId) return
  saving.value = true
  try {
    await upsertProjectMetric(props.projectId, {
      landUse: formModel.landUse || null,
      siteArea: formModel.siteArea,
      farAbove: formModel.farAbove,
      farUnder: formModel.farUnder,
      greenRatio: formModel.greenRatio,
      buildingDensity: formModel.buildingDensity,
      heightLimit: formModel.heightLimit,
      totalFloorArea: formModel.totalFloorArea,
      aboveFloorArea: formModel.aboveFloorArea,
      underFloorArea: formModel.underFloorArea,
      parkingAbove: formModel.parkingAbove,
      parkingUnder: formModel.parkingUnder,
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
        <div class="form-grid">
          <NFormItem label="用地性质">
            <NInput v-model:value="formModel.landUse" placeholder="如：商业用地、住宅用地" />
          </NFormItem>
          <NFormItem label="场地面积（㎡）">
            <NInputNumber v-model:value="formModel.siteArea" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地上容积率">
            <NInputNumber v-model:value="formModel.farAbove" :min="0" :precision="2" :step="0.1" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地下容积率">
            <NInputNumber v-model:value="formModel.farUnder" :min="0" :precision="2" :step="0.1" style="width: 100%" />
          </NFormItem>
          <NFormItem label="绿地率（%）">
            <NInputNumber v-model:value="formModel.greenRatio" :min="0" :max="100" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="建筑密度（%）">
            <NInputNumber v-model:value="formModel.buildingDensity" :min="0" :max="100" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="限高（m）">
            <NInputNumber v-model:value="formModel.heightLimit" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="总建筑面积（㎡）">
            <NInputNumber v-model:value="formModel.totalFloorArea" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地上建筑面积（㎡）">
            <NInputNumber v-model:value="formModel.aboveFloorArea" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地下建筑面积（㎡）">
            <NInputNumber v-model:value="formModel.underFloorArea" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地上停车位">
            <NInputNumber v-model:value="formModel.parkingAbove" :min="0" :precision="0" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地下停车位">
            <NInputNumber v-model:value="formModel.parkingUnder" :min="0" :precision="0" style="width: 100%" />
          </NFormItem>
        </div>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" placeholder="补充说明" />
        </NFormItem>
      </NForm>
      <NSpace justify="end">
        <NButton :loading="saving" type="primary" @click="save">保存指标信息</NButton>
      </NSpace>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 24px;
}
</style>
