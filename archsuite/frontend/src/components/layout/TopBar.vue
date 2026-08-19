<script setup lang="ts">
import { computed } from 'vue'
import { NTooltip } from 'naive-ui'
import AppIcon from '@/components/icons/AppIcon.vue'
import { useLayoutStore } from '@/stores/layout'
import { useProjectStore } from '@/stores/project'

// 顶部状态栏：软件标识 + 项目切换入口 + 布局开关
// 高度尽可能小，单行布局
const layoutStore = useLayoutStore()
const projectStore = useProjectStore()

const projectName = computed(() => projectStore.currentProject?.name || '未选择项目')

const emit = defineEmits<{
  (e: 'openProjectManager'): void
}>()

function onProjectClick() {
  emit('openProjectManager')
}

// 内联布局开关图标（线性 1.6 stroke，与软件图标同源）
</script>

<template>
  <header class="top-bar">
    <!-- 左：软件标识 -->
    <div class="brand">
      <AppIcon class="brand-icon" />
      <span class="brand-name">ArchSuite</span>
    </div>

    <!-- 中：当前项目（点击切换） -->
    <button class="project-pill" @click="onProjectClick">
      <span class="pp-label">项目</span>
      <span class="pp-name" :title="projectName">{{ projectName }}</span>
    </button>

    <!-- 右：布局开关 -->
    <div class="layout-toggles">
      <NTooltip placement="bottom" :delay="200">
        <template #trigger>
          <button
            class="toggle-btn"
            :class="{ active: layoutStore.leftRailVisible }"
            @click="layoutStore.toggleLeftRail()"
          >
            <!-- 左侧栏图标 -->
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="16" rx="1.5" />
              <path d="M9 4v16" />
            </svg>
          </button>
        </template>
        左侧导航栏
      </NTooltip>

      <NTooltip placement="bottom" :delay="200">
        <template #trigger>
          <button
            class="toggle-btn"
            :class="{ active: layoutStore.bottomBarVisible }"
            @click="layoutStore.toggleBottomBar()"
          >
            <!-- 底部栏图标 -->
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="16" rx="1.5" />
              <path d="M3 16h18" />
            </svg>
          </button>
        </template>
        底部状态栏
      </NTooltip>

      <NTooltip placement="bottom" :delay="200">
        <template #trigger>
          <button
            class="toggle-btn"
            :class="{ active: layoutStore.rightRailVisible }"
            @click="layoutStore.toggleRightRail()"
          >
            <!-- 右侧栏图标 -->
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="16" rx="1.5" />
              <path d="M15 4v16" />
            </svg>
          </button>
        </template>
        右侧 Panna 助手
      </NTooltip>
    </div>
  </header>
</template>

<style scoped lang="scss">
.top-bar {
  flex-shrink: 0;
  height: 40px;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 16px;
  background: var(--app-card-bg);
  box-shadow: var(--app-shadow-sm);
  position: relative;
  z-index: 20;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;

  .brand-icon {
    width: 20px;
    height: 20px;
    color: var(--app-primary);
  }

  .brand-name {
    font-size: 1em;
    font-weight: 600;
    color: var(--app-text-1);
    letter-spacing: 0.5px;
  }
}

.project-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  max-width: 320px;
  height: 26px;
  padding: 0 10px;
  border: none;
  background: var(--app-inset-bg);
  border-radius: var(--app-radius);
  color: var(--app-text-2);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: color-mix(in srgb, var(--app-primary) 10%, var(--app-inset-bg));
    color: var(--app-text-1);
  }

  .pp-label {
    font-size: 0.79em;
    color: var(--app-text-3);
  }

  .pp-name {
    font-size: 0.86em;
    font-weight: 500;
    color: var(--app-text-1);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.layout-toggles {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 2px;
}

.toggle-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--app-text-3);
  border-radius: calc(var(--app-radius) - 4px);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: var(--app-inset-bg);
    color: var(--app-text-1);
  }

  &.active {
    color: var(--app-primary);
    background: color-mix(in srgb, var(--app-primary) 12%, transparent);
  }
}
</style>
