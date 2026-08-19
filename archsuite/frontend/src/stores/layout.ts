import { defineStore } from 'pinia'
import { ref } from 'vue'

// 布局 Store：管理左右侧栏与底部日志面板的显隐
// - 持久化到 localStorage，刷新后保持用户偏好
const STORAGE_KEY = 'archsuite_layout'

interface LayoutState {
  leftRailVisible: boolean
  rightRailVisible: boolean
  bottomBarVisible: boolean
  logPanelOpen: boolean
}

const defaultState: LayoutState = {
  leftRailVisible: true,
  rightRailVisible: true,
  bottomBarVisible: true,
  logPanelOpen: false
}

function loadState(): LayoutState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { ...defaultState }
    return { ...defaultState, ...(JSON.parse(raw) as Partial<LayoutState>) }
  } catch {
    return { ...defaultState }
  }
}

function persist(state: LayoutState) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  } catch (e) {
    console.error('[layout persist]', e)
  }
}

export const useLayoutStore = defineStore('layout', () => {
  const loaded = loadState()
  const leftRailVisible = ref(loaded.leftRailVisible)
  const rightRailVisible = ref(loaded.rightRailVisible)
  const bottomBarVisible = ref(loaded.bottomBarVisible)
  const logPanelOpen = ref(loaded.logPanelOpen)

  function sync() {
    persist({
      leftRailVisible: leftRailVisible.value,
      rightRailVisible: rightRailVisible.value,
      bottomBarVisible: bottomBarVisible.value,
      logPanelOpen: logPanelOpen.value
    })
  }

  function toggleLeftRail() {
    leftRailVisible.value = !leftRailVisible.value
    sync()
  }
  function toggleRightRail() {
    rightRailVisible.value = !rightRailVisible.value
    sync()
  }
  function toggleBottomBar() {
    bottomBarVisible.value = !bottomBarVisible.value
    sync()
  }
  function toggleLogPanel() {
    logPanelOpen.value = !logPanelOpen.value
    sync()
  }
  function setLogPanelOpen(v: boolean) {
    logPanelOpen.value = v
    sync()
  }

  return {
    leftRailVisible,
    rightRailVisible,
    bottomBarVisible,
    logPanelOpen,
    toggleLeftRail,
    toggleRightRail,
    toggleBottomBar,
    toggleLogPanel,
    setLogPanelOpen
  }
})
