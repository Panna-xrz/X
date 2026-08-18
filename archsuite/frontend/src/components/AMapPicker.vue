<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { NButton, NInput, NSpace, useMessage } from 'naive-ui'

// 高德地图选点组件
// - 通过 script 标签动态加载高德 JS API 2.0
// - 支持点击/拖拽标记选点
// - 支持逆地理编码显示地址
// - 高德 Key 从 localStorage 读取（settings 中配置），默认占位符 YOUR_AMAP_KEY
// Props/Emits 支持 v-model 经度 + v-model:lat 纬度

const props = withDefaults(
  defineProps<{
    modelValue: number | null
    latModel: number | null
    height?: number
  }>(),
  {
    height: 360
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: number | null): void
  (e: 'update:latModel', val: number | null): void
}>()

const message = useMessage()

const STORAGE_KEY = 'archsuite_amap_key'

// 读取高德 Key
function getAmapKey(): string {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored && stored.trim()) return stored.trim()
  return 'YOUR_AMAP_KEY'
}

const mapContainer = ref<HTMLDivElement | null>(null)
const searchInput = ref('')
const addressText = ref('')
let mapInstance: any = null
let markerInstance: any = null
let geocoderInstance: any = null
let autoCompleteInstance: any = null
let placeSearchInstance: any = null

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
    const script = document.createElement('script')
    script.id = 'amap-script'
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${encodeURIComponent(key)}&plugin=AMap.Geocoder,AMap.AutoComplete,AMap.PlaceSearch`
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
  if (!searchInput.value.trim() || !autoCompleteInstance || !placeSearchInstance) return
  placeSearchInstance.search(searchInput.value.trim(), (status: string, result: any) => {
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
    mapInstance?.destroy?.()
  } catch (e) {
    // ignore
  }
  mapInstance = null
  markerInstance = null
  geocoderInstance = null
  autoCompleteInstance = null
  placeSearchInstance = null
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
        <NButton size="small" type="primary" @click="searchAddress">搜索定位</NButton>
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
  border-radius: 8px;
  overflow: hidden;
  background: #e8eaf0;
}

.info-bar {
  margin-top: 8px;
  font-size: 13px;
  color: var(--app-text-2);

  .coord b {
    color: var(--app-text-1);
    font-weight: 600;
  }

  .address {
    margin-top: 4px;
    color: var(--app-text-2);
  font-size: 12px;
  }
}
</style>
