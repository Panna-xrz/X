<script setup lang="ts">
import { reactive, ref, watch, onMounted, computed } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NButton,
  NSpace,
  NSpin,
  NTag,
  useMessage
} from 'naive-ui'
import { getProjectSurrounding, upsertProjectSurrounding, getProject } from '@/api/project'
import AMapPicker from '@/components/AMapPicker.vue'
import { lngLatToGauss3, gauss3ToLngLat, parseRedLineText } from '@/utils/coord'
import type { ProjectSurrounding } from '@/types'

// 场地周边 Tab：高德地图选点 + CGCS2000 坐标 + 用地红线放线 + 周边信息
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

// CGCS2000 单点 XY（与经纬度联动，自动计算）
const xyInfo = computed(() => {
  if (formModel.longitude == null || formModel.latitude == null) return null
  try {
    return lngLatToGauss3(formModel.longitude, formModel.latitude)
  } catch {
    return null
  }
})

// 用地红线放线：CGCS2000 XY 点 -> 经纬度点 -> 传给地图绘制
const redlineInput = ref('')
const redlinePoints = ref<Array<{ lng: number; lat: number }>>([])
const fileInput = ref<HTMLInputElement | null>(null)

function triggerFile() {
  fileInput.value?.click()
}

function onFile(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    redlineInput.value = String(reader.result || '')
    applyRedline()
  }
  reader.onerror = () => message.error('文件读取失败')
  reader.readAsText(file)
  target.value = ''
}

function applyRedline() {
  const res = parseRedLineText(redlineInput.value)
  if (!res.ok) {
    message.warning(res.message)
    return
  }
  const pts = res.points.map((p) => {
    const ll = gauss3ToLngLat(p.x, p.y, res.zone)
    return { lng: ll.lng, lat: ll.lat }
  })
  redlinePoints.value = pts
  message.success(`已放线 ${pts.length} 个红线点（${res.zone ?? '?'}带）`)
}

function clearRedline() {
  redlinePoints.value = []
  redlineInput.value = ''
}

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
          :redline="redlinePoints"
          @update:model-value="updateLng"
          @update:lat-model="updateLat"
        />
      </div>

      <div class="section">
        <div class="section-title">经纬度与 CGCS2000 坐标</div>
        <NSpace :size="12" align="center" wrap>
          <NInputNumber
            :value="formModel.longitude"
            :precision="6"
            :step="0.000001"
            style="width: 180px"
            placeholder="经度"
            @update:value="(v: number | null) => (formModel.longitude = v)"
          />
          <NInputNumber
            :value="formModel.latitude"
            :precision="6"
            :step="0.000001"
            style="width: 180px"
            placeholder="纬度"
            @update:value="(v: number | null) => (formModel.latitude = v)"
          />
          <NTag v-if="xyInfo" size="small" round :bordered="false" type="info">
            CGCS2000 {{ xyInfo.zone }}带
          </NTag>
        </NSpace>
        <div v-if="xyInfo" class="xy-row">
          <span class="xy-item"><span class="xy-k">X(北)</span><span class="xy-v">{{ xyInfo.X.toFixed(3) }}</span></span>
          <span class="xy-item"><span class="xy-k">Y(东)</span><span class="xy-v">{{ xyInfo.Y.toFixed(3) }}</span></span>
          <span class="xy-hint">中央子午线 {{ xyInfo.L0 }}°（自动按 3 度带选择）</span>
        </div>
      </div>

      <!-- 用地红线放线 -->
      <div class="section">
        <div class="section-title">用地红线放线（CGCS2000 3 度带）</div>
        <div class="redline-toolbar">
          <NButton size="small" @click="triggerFile">上传表格</NButton>
          <input
            ref="fileInput"
            type="file"
            accept=".csv,.txt,.tsv"
            style="display: none"
            @change="onFile"
          />
          <NButton size="small" type="primary" @click="applyRedline">放线</NButton>
          <NButton size="small" quaternary @click="clearRedline">清除</NButton>
          <NTag v-if="redlinePoints.length" size="small" round :bordered="false" type="success">
            已加载 {{ redlinePoints.length }} 点
          </NTag>
        </div>
        <NInput
          v-model:value="redlineInput"
          type="textarea"
          :rows="5"
          placeholder="粘贴或输入红线坐标，每行一个点：序号,X(北),Y(东)&#10;示例：&#10;1,4420000.123,39450000.456&#10;2,4420100.000,39450100.000&#10;支持 CSV / TSV / 空格分隔；Y 含带号将自动识别，否则需自行确保带号一致"
        />
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

.xy-row {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  padding: 8px 12px;
  background: var(--app-inset-bg);
  border-radius: calc(var(--app-radius) - 2px);

  .xy-item {
    display: inline-flex;
    align-items: baseline;
    gap: 6px;
  }

  .xy-k {
    font-size: 0.86em;
    color: var(--app-text-3);
    font-weight: 500;
  }

  .xy-v {
    font-size: 0.93em;
    color: var(--app-text-1);
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }

  .xy-hint {
    font-size: 0.79em;
    color: var(--app-text-3);
    margin-left: auto;
  }
}

.redline-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
</style>
