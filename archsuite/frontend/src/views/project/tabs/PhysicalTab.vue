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
import { getProjectPhysical, upsertProjectPhysical } from '@/api/project'
import type { ProjectPhysical } from '@/types'

// 物理环境 Tab：气候、风向、降水、温度等
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const saving = ref(false)

const formModel = reactive<ProjectPhysical>({
  climateZone: '',
  prevailingWind: '',
  solarPath: '',
  annualPrecipitation: null,
  groundwaterLevel: null,
  elevation: null,
  avgAnnualTemp: null,
  extremeMaxTemp: null,
  extremeMinTemp: null,
  remarks: ''
})

async function load() {
  if (!props.projectId) return
  loading.value = true
  try {
    const data = await getProjectPhysical(props.projectId)
    Object.assign(formModel, {
      climateZone: data.climateZone,
      prevailingWind: data.prevailingWind,
      solarPath: data.solarPath,
      annualPrecipitation: data.annualPrecipitation,
      groundwaterLevel: data.groundwaterLevel,
      elevation: data.elevation,
      avgAnnualTemp: data.avgAnnualTemp,
      extremeMaxTemp: data.extremeMaxTemp,
      extremeMinTemp: data.extremeMinTemp,
      remarks: data.remarks
    })
  } catch {
    // 未创建过，保持空
  } finally {
    loading.value = false
  }
}

async function save() {
  if (!props.projectId) return
  saving.value = true
  try {
    await upsertProjectPhysical(props.projectId, {
      climateZone: formModel.climateZone || null,
      prevailingWind: formModel.prevailingWind || null,
      solarPath: formModel.solarPath || null,
      annualPrecipitation: formModel.annualPrecipitation,
      groundwaterLevel: formModel.groundwaterLevel,
      elevation: formModel.elevation,
      avgAnnualTemp: formModel.avgAnnualTemp,
      extremeMaxTemp: formModel.extremeMaxTemp,
      extremeMinTemp: formModel.extremeMinTemp,
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
          <NFormItem label="气候区">
            <NInput v-model:value="formModel.climateZone" placeholder="如：温带季风气候" />
          </NFormItem>
          <NFormItem label="主导风向">
            <NInput v-model:value="formModel.prevailingWind" placeholder="如：夏季东南风、冬季西北风" />
          </NFormItem>
          <NFormItem label="日照轨迹">
            <NInput v-model:value="formModel.solarPath" placeholder="如：夏至日照 8h / 冬至日照 4h" />
          </NFormItem>
          <NFormItem label="年降水量（mm）">
            <NInputNumber v-model:value="formModel.annualPrecipitation" :min="0" :precision="1" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地下水位（m）">
            <NInputNumber v-model:value="formModel.groundwaterLevel" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="海拔（m）">
            <NInputNumber v-model:value="formModel.elevation" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="年均温（℃）">
            <NInputNumber v-model:value="formModel.avgAnnualTemp" :precision="1" style="width: 100%" />
          </NFormItem>
          <NFormItem label="极端最高温（℃）">
            <NInputNumber v-model:value="formModel.extremeMaxTemp" :precision="1" style="width: 100%" />
          </NFormItem>
          <NFormItem label="极端最低温（℃）">
            <NInputNumber v-model:value="formModel.extremeMinTemp" :precision="1" style="width: 100%" />
          </NFormItem>
        </div>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>

      <NSpace justify="end">
        <NButton :loading="saving" type="primary" @click="save">保存物理环境</NButton>
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
