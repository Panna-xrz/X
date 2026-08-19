<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { NButton, NInput, NSpace, useMessage } from 'naive-ui'
import { lngLatToGauss3 } from '@/utils/coord'

// 高德地图选点组件
// - 通过 script 标签动态加载高德 JS API 2.0
// - 支持点击/拖拽标记选点 + 关键词搜索（AutoComplete 建议 + PlaceSearch 定位）
// - 显示 WGS84 经纬度 + CGCS2000 3 度带 XY
// - 支持外部传入红线点列表，自动绘制用地红线多边形

const props = withDefaults(
  defineProps<{
    modelValue: number | null
    latModel: number | null
    height?: number
    redline?: Array<{ lng: number; lat: number }>
  }>(),
  {
    height: 360,
    redline: () => []
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: number | null): void
  (e: 'update:latModel', val: number | null): void
}>()

const message = useMessage()

const STORAGE_KEY = 'archsuite_amap_key'
const SECURITY_KEY = 'archsuite_amap_security'

// 读取高德 Key
function getAmapKey(): string {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored && stored.trim()) return stored.trim()
  return 'YOUR_AMAP_KEY'
}

// 读取高德安全密钥（2021-12-02 后申请的 Key 必须配置）
function getAmapSecurity(): string {
  const stored = localStorage.getItem(SECURITY_KEY)
  return stored && stored.trim() ? stored.trim() : ''
}

const mapContainer = ref<HTMLDivElement | null>(null)
const searchInput = ref('')
const addressText = ref('')
const searchLoading = ref(false)
let mapInstance: any = null
let markerInstance: any = null
let geocoderInstance: any = null
let autoCompleteInstance: any = null
let placeSearchInstance: any = null
let polygonInstance: any = null

// CGCS2000 3 度带 XY（基于当前经纬度自动计算）
const xyInfo = computed(() => {
  if (props.modelValue == null || props.latModel == null) return null
  try {
    return lngLatToGauss3(props.modelValue, props.latModel)
  } catch {
    return null
  }
})

// 动态加载高德 JS API
function loadAmapScript(): Promise<void> {
  return new Promise((resolve, reject) => {
    if ((window as any).AMap) {
      resolve()
      return
    }
    // 防止重复注入
    if (document.getElementById('amap-script')) {
      const check = setInterval(() => {
        if ((window as any).AMap) {
          clearInterval(check)
          resolve()
        }
      }, 60)
      setTimeout(() => {
        clearInterval(check)
        reject(new Error('高德地图加载超时'))
      }, 15000)
      return
    }
    const key = getAmapKey()
    // 安全密钥：2021-12-02 后申请的 Key 必须在脚本加载前注入
    const security = getAmapSecurity()
    if (security) {
      ;(window as any)._AMapSecurityConfig = { securityJsCode: security }
    }
    const script = document.createElement('script')
    script.id = 'amap-script'
    // 插件包含 Polygon（红线放线需要）
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${encodeURIComponent(key)}&plugin=AMap.Geocoder,AMap.AutoComplete,AMap.PlaceSearch,AMap.Polygon`
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('高德地图加载失败，请检查网络或 Key 配置'))
    document.head.appendChild(script)
  })
}

// 初始化地图
async function initMap() {
  if (!mapContainer.value) return
  try {
    await loadAmapScript()
    const AMapNS = (window as any).AMap
    if (!AMapNS) {
      message.error('高德地图未加载')
      return
    }
    const lng = props.modelValue ?? 116.397428
    const lat = props.latModel ?? 39.90923
    mapInstance = new AMapNS.Map(mapContainer.value, {
      zoom: 14,
      center: [lng, lat],
      viewMode: '2D'
    })
    geocoderInstance = new AMapNS.Geocoder({ extensions: 'all' })
    markerInstance = new AMapNS.Marker({
      position: [lng, lat],
      draggable: true
    })
    markerInstance.setMap(mapInstance)
    // 拖拽结束
    markerInstance.on('dragend', (e: any) => {
      const pos = e.target.getPosition()
      updatePosition(pos.lng, pos.lat)
    })
    // 点击地图设置标记
    mapInstance.on('click', (e: any) => {
      const lng = e.lnglat.getLng()
      const lat = e.lnglat.getLat()
      markerInstance.setPosition([lng, lat])
      updatePosition(lng, lat)
    })
    autoCompleteInstance = new AMapNS.AutoComplete({ city: '全国' })
    placeSearchInstance = new AMapNS.PlaceSearch({ city: '全国', pageSize: 5, extensions: 'base' })
    if (props.modelValue != null && props.latModel != null) {
      reverseGeocode(props.modelValue, props.latModel)
    }
    // 地图就绪后绘制初始红线
    drawRedline()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '地图初始化失败')
  }
}

// 更新位置（通知父组件 + 反查地址）
function updatePosition(lng: number, lat: number) {
  emit('update:modelValue', lng)
  emit('update:latModel', lat)
  reverseGeocode(lng, lat)
}

// 逆地理编码
function reverseGeocode(lng: number, lat: number) {
  if (!geocoderInstance) return
  try {
    geocoderInstance.getAddress([lng, lat], (status: string, result: any) => {
      if (status === 'complete' && result?.regeocode) {
        addressText.value = result.regeocode.formattedAddress || ''
      } else {
        addressText.value = ''
      }
    })
  } catch (e) {
    addressText.value = ''
  }
}

// 关键词搜索定位
function searchAddress() {
  const kw = searchInput.value.trim()
  if (!kw) return
  if (!placeSearchInstance || !mapInstance) {
    message.warning('地图尚未就绪，请稍后再试')
    return
  }
  searchLoading.value = true
  placeSearchInstance.search(kw, (status: string, result: any) => {
    searchLoading.value = false
    if (status === 'complete' && result?.poiList?.pois?.length) {
      const poi = result.poiList.pois[0]
      const lng = poi.location.lng
      const lat = poi.location.lat
      markerInstance?.setPosition([lng, lat])
      mapInstance?.setCenter([lng, lat])
      updatePosition(lng, lat)
    } else {
      message.warning('未检索到相关地点')
    }
  })
}

// 绘制/清除用地红线多边形
function drawRedline() {
  if (!mapInstance || !(window as any).AMap) return
  const AMapNS = (window as any).AMap
  if (polygonInstance) {
    polygonInstance.setMap(null)
    polygonInstance = null
  }
  const pts = props.redline
  if (!pts || pts.length < 3) return
  const path = pts.map((p) => [p.lng, p.lat])
  polygonInstance = new AMapNS.Polygon({
    path,
    fillColor: '#c8344e',
    fillOpacity: 0.12,
    strokeColor: '#c8344e',
    strokeWeight: 2,
    strokeOpacity: 0.9
  })
  polygonInstance.setMap(mapInstance)
  mapInstance.setFitView([polygonInstance])
}

// 外部红线变化时重绘
watch(
  () => props.redline,
  () => drawRedline(),
  { deep: true }
)

// 外部经纬度变化时同步标记
watch(
  () => [props.modelValue, props.latModel],
  ([lng, lat]) => {
    if (mapInstance && markerInstance && lng != null && lat != null) {
      try {
        markerInstance.setPosition([lng, lat])
        mapInstance.setCenter([lng, lat])
      } catch (e) {
        // ignore
      }
    }
  }
)

onMounted(async () => {
  await nextTick()
  await initMap()
})

onBeforeUnmount(() => {
  try {
    polygonInstance?.setMap?.(null)
    mapInstance?.destroy?.()
  } catch (e) {
    // ignore
  }
  mapInstance = null
  markerInstance = null
  geocoderInstance = null
  autoCompleteInstance = null
  placeSearchInstance = null
  polygonInstance = null
})
</script>

<template>
  <div class="amap-picker">
    <div class="search-bar">
      <NSpace :size="6" align="center" wrap>
        <NInput
          v-model:value="searchInput"
          placeholder="搜索地点（如：天安门）"
          size="small"
          style="width: 240px"
          @keyup.enter="searchAddress"
        />
        <NButton size="small" type="primary" :loading="searchLoading" @click="searchAddress">
          搜索定位
        </NButton>
      </NSpace>
    </div>
    <div ref="mapContainer" class="map-canvas" :style="{ height: `${height}px` }" />
    <div class="info-bar">
      <NSpace :size="12" align="center" wrap>
        <span class="coord">
          经度：<b>{{ modelValue ?? '-' }}</b>
        </span>
        <span class="coord">
          纬度：<b>{{ latModel ?? '-' }}</b>
        </span>
        <span v-if="xyInfo" class="coord coord-xy">
          CGCS2000 <span class="xy-tag">{{ xyInfo.zone }}带</span>
          X：<b>{{ xyInfo.X.toFixed(3) }}</b>
          Y：<b>{{ xyInfo.Y.toFixed(3) }}</b>
        </span>
      </NSpace>
      <div v-if="addressText" class="address">地址：{{ addressText }}</div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.amap-picker {
  width: 100%;
}

.search-bar {
  margin-bottom: 8px;
}

.map-canvas {
  width: 100%;
  border-radius: var(--app-radius);
  overflow: hidden;
  background: var(--app-card-bg);
}

.info-bar {
  margin-top: 8px;
  font-size: 0.93em;
  color: var(--app-text-2);

  .coord b {
    color: var(--app-text-1);
    font-weight: 600;
  }

  .coord-xy {
    .xy-tag {
      display: inline-block;
      padding: 1px 6px;
      margin: 0 4px;
      border-radius: var(--app-radius);
      background: color-mix(in srgb, var(--app-primary) 12%, transparent);
      color: var(--app-primary);
      font-size: 0.86em;
    }
  }

  .address {
    margin-top: 4px;
    color: var(--app-text-2);
    font-size: 0.86em;
  }
}
</style>
