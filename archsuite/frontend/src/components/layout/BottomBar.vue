<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import { NTabs, NTabPane, NEmpty, NTag } from 'naive-ui'
import { useLayoutStore } from '@/stores/layout'
import { useProjectStore } from '@/stores/project'
import {
  useLogEntries,
  connectionStatus,
  lastConnectionAt,
  checkConnection
} from '@/utils/logger'

// 底部状态栏：状态信息 + 点击展开日志抽屉
const layoutStore = useLayoutStore()
const projectStore = useProjectStore()
const entries = useLogEntries()

const drawerOpen = computed(() => layoutStore.logPanelOpen)
const drawerTab = ref<'log' | 'updates' | 'connection'>('log')

// 状态摘要
const connText = computed(() => {
  if (connectionStatus.value === 'ok') return '已连接'
  if (connectionStatus.value === 'fail') return '已断开'
  return '检测中'
})
const connColor = computed(() =>
  connectionStatus.value === 'ok' ? 'success' : connectionStatus.value === 'fail' ? 'error' : 'default'
)
const projectText = computed(() => projectStore.currentProject?.name || '未选择')
const logCount = computed(() => entries.value.length)

function timeStr(ts: number): string {
  const d = new Date(ts)
  return d.toLocaleTimeString('zh-CN', { hour12: false }) + '.' + String(d.getMilliseconds()).padStart(3, '0')
}

function relTime(ts: number | null): string {
  if (!ts) return '-'
  const diff = Date.now() - ts
  if (diff < 60000) return `${Math.floor(diff / 1000)} 秒前`
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  return new Date(ts).toLocaleTimeString('zh-CN', { hour12: false })
}

let pollTimer: number | null = null
onMounted(() => {
  checkConnection()
  pollTimer = window.setInterval(() => checkConnection(), 60000)
})
onBeforeUnmount(() => {
  if (pollTimer) window.clearInterval(pollTimer)
})

function onBarClick() {
  layoutStore.setLogPanelOpen(true)
}
</script>

<template>
  <div class="bottom-wrap">
    <!-- 抽屉（从底部滑出，覆盖状态栏上方） -->
    <transition name="drawer">
      <div v-show="drawerOpen" class="drawer">
        <div class="drawer-header">
          <NTabs v-model:value="drawerTab" type="line" size="small" :pane-style="{ padding: '8px 12px' }">
            <NTabPane name="log" tab="日志">
              <div class="log-list">
                <div v-if="!logCount" class="empty-wrap"><NEmpty description="暂无日志" /></div>
                <div v-for="e in entries" :key="e.id" class="log-row" :class="e.level">
                  <span class="log-ts">{{ timeStr(e.ts) }}</span>
                  <span class="log-level">{{ e.level.toUpperCase() }}</span>
                  <span class="log-cat">[{{ e.category }}]</span>
                  <span class="log-msg">{{ e.message }}</span>
                </div>
              </div>
            </NTabPane>
            <NTabPane name="updates" tab="项目更新记录">
              <div class="empty-wrap"><NEmpty description="项目更新记录（后端待接入）" /></div>
            </NTabPane>
            <NTabPane name="connection" tab="连接状态">
              <div class="conn-grid">
                <div class="conn-item">
                  <span class="conn-k">后端状态</span>
                  <NTag :type="connColor" size="small" round :bordered="false">{{ connText }}</NTag>
                </div>
                <div class="conn-item">
                  <span class="conn-k">最近检测</span>
                  <span class="conn-v">{{ relTime(lastConnectionAt) }}</span>
                </div>
                <div class="conn-item">
                  <span class="conn-k">当前项目</span>
                  <span class="conn-v">{{ projectText }}</span>
                </div>
                <button class="recheck-btn" @click="checkConnection">立即检测</button>
              </div>
            </NTabPane>
          </NTabs>
          <button class="drawer-close" @click="layoutStore.setLogPanelOpen(false)">×</button>
        </div>
      </div>
    </transition>

    <!-- 状态栏本体 -->
    <footer class="bottom-bar" @click="onBarClick">
      <div class="status-group">
        <span class="dot" :class="connectionStatus" />
        <span class="status-text">{{ connText }}</span>
      </div>
      <div class="status-group">
        <span class="status-label">项目</span>
        <span class="status-value">{{ projectText }}</span>
      </div>
      <div class="status-group">
        <span class="status-label">日志</span>
        <span class="status-value">{{ logCount }}</span>
      </div>
      <div class="status-hint">点击查看详情</div>
    </footer>
  </div>
</template>

<style scoped lang="scss">
.bottom-wrap {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 20;
}

.drawer {
  height: 220px;
  background: var(--app-card-bg);
  box-shadow: var(--app-shadow-md);
  border-top: 1px solid transparent;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.drawer-header {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 4px 12px 8px;
  min-height: 0;
}

:deep(.n-tabs) {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

:deep(.n-tab-pane) {
  overflow-y: auto;
  flex: 1;
}

.drawer-close {
  position: absolute;
  top: 6px;
  right: 10px;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--app-text-3);
  font-size: 1.14em;
  cursor: pointer;
  border-radius: calc(var(--app-radius) - 4px);

  &:hover {
    background: var(--app-inset-bg);
    color: var(--app-text-1);
  }
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-family: var(--app-font-family);
}

.log-row {
  display: grid;
  grid-template-columns: 88px 56px 80px 1fr;
  gap: 8px;
  align-items: baseline;
  font-size: 0.79em;
  padding: 2px 4px;
  border-radius: calc(var(--app-radius) - 6px);

  .log-ts { color: var(--app-text-3); font-variant-numeric: tabular-nums; }
  .log-level { color: var(--app-text-3); font-weight: 500; }
  .log-cat { color: var(--app-text-2); }
  .log-msg { color: var(--app-text-1); word-break: break-all; }

  &.error .log-level { color: #c8344e; }
  &.warn .log-level { color: #d68a1f; }
}

.empty-wrap {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.conn-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 4px 4px 8px;
}

.conn-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.86em;

  .conn-k {
    color: var(--app-text-3);
    min-width: 80px;
  }

  .conn-v {
    color: var(--app-text-1);
    font-weight: 500;
  }
}

.recheck-btn {
  align-self: flex-start;
  padding: 4px 12px;
  border: none;
  background: var(--app-inset-bg);
  color: var(--app-text-1);
  border-radius: calc(var(--app-radius) - 2px);
  font-size: 0.79em;
  cursor: pointer;

  &:hover {
    background: color-mix(in srgb, var(--app-primary) 10%, var(--app-inset-bg));
  }
}

.bottom-bar {
  height: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 0 16px;
  background: var(--app-card-bg);
  cursor: pointer;
  user-select: none;
}

.status-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--app-text-3);
  &.ok { background: #1f9d6b; }
  &.fail { background: #c8344e; }
  &.unknown { background: var(--app-text-3); }
}

.status-text {
  font-size: 0.79em;
  color: var(--app-text-2);
}

.status-label {
  font-size: 0.79em;
  color: var(--app-text-3);
}

.status-value {
  font-size: 0.79em;
  color: var(--app-text-1);
  font-weight: 500;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-hint {
  margin-left: auto;
  font-size: 0.72em;
  color: var(--app-text-3);
  opacity: 0.7;
}

.drawer-enter-active,
.drawer-leave-active {
  transition: height 0.25s ease, opacity 0.25s ease;
}
.drawer-enter-from,
.drawer-leave-to {
  height: 0;
  opacity: 0;
}
</style>
