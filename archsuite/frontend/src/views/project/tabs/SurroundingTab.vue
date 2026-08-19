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
import { getProjectSurrounding, upsertProjectSurrounding, getProject } from '@/api/project'
import AMapPicker from '@/components/AMapPicker.vue'
import type { ProjectSurrounding } from '@/types'

// 场地周边 Tab：高德地图选点 + 周边信息
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const saving = ref(false)

const formModel = reactive<ProjectSurrounding>({
  longitude: null,
  latitude: null,
  within200m: '',
  within500m: '',
  within2000m: '',
  nearbyRoads: '',
  naturalFeatures: '',
  transitInfo: '',
  remarks: ''
})

async function load() {
  if (!props.projectId) return
  loading.value = true
  try {
    // 先取项目经纬度作为地图初始位置
    try {
      const project = await getProject(props.projectId)
      if (formModel.longitude == null && project.longitude) {
        formModel.longitude = project.longitude
        formModel.latitude = project.latitude
      }
    } catch {
      // ignore
    }
    const data = await getProjectSurrounding(props.projectId)
    Object.assign(formModel, {
      longitude: data.longitude ?? formModel.longitude,
      latitude: data.latitude ?? formModel.latitude,
      within200m: data.within200m,
      within500m: data.within500m,
      within2000m: data.within2000m,
      nearbyRoads: data.nearbyRoads,
      naturalFeatures: data.naturalFeatures,
      transitInfo: data.transitInfo,
      remarks: data.remarks
    })
  } catch (e) {
    // 首次创建：保持空值
  } finally {
    loading.value = false
  }
}

function updateLng(v: number | null) {
  formModel.longitude = v
}
function updateLat(v: number | null) {
  formModel.latitude = v
}

async function save() {
  if (!props.projectId) return
  saving.value = true
  try {
    await upsertProjectSurrounding(props.projectId, {
      longitude: formModel.longitude,
      latitude: formModel.latitude,
      within200m: formModel.within200m || null,
      within500m: formModel.within500m || null,
      within2000m: formModel.within2000m || null,
      nearbyRoads: formModel.nearbyRoads || null,
      naturalFeatures: formModel.naturalFeatures || null,
      transitInfo: formModel.transitInfo || null,
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
      <div class="section">
        <div class="section-title">场地定位</div>
        <AMapPicker
          :model-value="formModel.longitude"
          :lat-model="formModel.latitude"
          :height="360"
          @update:model-value="updateLng"
          @update:lat-model="updateLat"
        />
      </div>

      <div class="section">
        <div class="section-title">经纬度</div>
        <NSpace :size="12">
          <NInputNumber
            :value="formModel.longitude"
            :precision="6"
            :step="0.000001"
            style="width: 200px"
            placeholder="经度"
            @update:value="(v: number | null) => (formModel.longitude = v)"
          />
          <NInputNumber
            :value="formModel.latitude"
            :precision="6"
            :step="0.000001"
            style="width: 200px"
            placeholder="纬度"
            @update:value="(v: number | null) => (formModel.latitude = v)"
          />
        </NSpace>
      </div>

      <NForm label-placement="left" label-width="120">
        <NFormItem label="200m 范围内">
          <NInput v-model:value="formModel.within200m" type="textarea" :rows="2" placeholder="周边 200m 内的重要地物" />
        </NFormItem>
        <NFormItem label="500m 范围内">
          <NInput v-model:value="formModel.within500m" type="textarea" :rows="2" placeholder="周边 500m 内的重要地物" />
        </NFormItem>
        <NFormItem label="2000m 范围内">
          <NInput v-model:value="formModel.within2000m" type="textarea" :rows="2" placeholder="周边 2000m 内的重要地物" />
        </NFormItem>
        <NFormItem label="临近道路">
          <NInput v-model:value="formModel.nearbyRoads" placeholder="如：城市主干道 XX 路" />
        </NFormItem>
        <NFormItem label="自然景观">
          <NInput v-model:value="formModel.naturalFeatures" type="textarea" :rows="2" placeholder="如：临河、靠山、公园" />
        </NFormItem>
        <NFormItem label="交通信息">
          <NInput v-model:value="formModel.transitInfo" type="textarea" :rows="2" placeholder="地铁/公交/高铁等公共交通信息" />
        </NFormItem>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>

      <NSpace justify="end">
        <NButton :loading="saving" type="primary" @click="save">保存场地周边</NButton>
      </NSpace>
    </NSpin>
  </NCard>
</template>

<style scoped lang="scss">
.section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 0.93em;
  font-weight: 600;
  color: var(--app-text-1);
  margin-bottom: 8px;
}
</style>
