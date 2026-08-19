<script setup lang="ts">
import type { Component } from 'vue'
import { computed } from 'vue'
import { NTooltip } from 'naive-ui'
import ProjectIcon from '@/components/icons/ProjectIcon.vue'
import CommerceIcon from '@/components/icons/CommerceIcon.vue'
import EnvIcon from '@/components/icons/EnvIcon.vue'
import ConceptIcon from '@/components/icons/ConceptIcon.vue'
import PlanIcon from '@/components/icons/PlanIcon.vue'
import SpaceIcon from '@/components/icons/SpaceIcon.vue'
import SettingsIcon from '@/components/icons/SettingsIcon.vue'
import ProjectSwitcher from './ProjectSwitcher.vue'

// 模块类型
export type ModuleKey =
  | 'project'
  | 'commerce'
  | 'env'
  | 'concept'
  | 'plan'
  | 'space'
  | 'settings'

defineProps<{
  currentModule: ModuleKey
  currentProjectId: number | null
}>()

const emit = defineEmits<{
  (e: 'selectModule', key: ModuleKey): void
  (e: 'selectProject', id: number): void
  (e: 'createProject', payload: { name: string; code: string; type?: string }): void
  (e: 'deleteProject', id: number): void
}>()

// 模块列表
interface ModuleItem {
  key: ModuleKey
  label: string
  icon: Component
  placeholder?: boolean
}

const modules = computed<ModuleItem[]>(() => [
  { key: 'project', label: '项目信息', icon: ProjectIcon },
  { key: 'commerce', label: '商务管理', icon: CommerceIcon },
  { key: 'env', label: '环境解析', icon: EnvIcon, placeholder: true },
  { key: 'concept', label: '概念构思', icon: ConceptIcon, placeholder: true },
  { key: 'plan', label: '平面构成', icon: PlanIcon, placeholder: true },
  { key: 'space', label: '空间构成', icon: SpaceIcon, placeholder: true }
])

function onSelect(key: ModuleKey) {
  emit('selectModule', key)
}
</script>

<template>
  <aside class="icon-bar">
    <!-- 顶部：项目切换器 -->
    <div class="bar-top">
      <ProjectSwitcher
        :current-project-id="currentProjectId"
        @select-project="(id) => emit('selectProject', id)"
        @create-project="(payload) => emit('createProject', payload)"
        @delete-project="(id) => emit('deleteProject', id)"
      />
    </div>

    <!-- 中间：功能模块图标 -->
    <div class="bar-middle">
      <NTooltip
        v-for="m in modules"
        :key="m.key"
        placement="right"
        :delay="200"
      >
        <template #trigger>
          <button
            class="module-btn"
            :class="{
              active: currentModule === m.key,
              placeholder: m.placeholder
            }"
            @click="onSelect(m.key)"
          >
            <component :is="m.icon" class="module-icon" />
          </button>
        </template>
        {{ m.label }}{{ m.placeholder ? '（规划中）' : '' }}
      </NTooltip>
    </div>

    <!-- 底部：设置按钮 -->
    <div class="bar-bottom">
      <NTooltip placement="right" :delay="200">
        <template #trigger>
          <button
            class="module-btn"
            :class="{ active: currentModule === 'settings' }"
            @click="onSelect('settings')"
          >
            <SettingsIcon class="module-icon" />
          </button>
        </template>
        设置
      </NTooltip>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.icon-bar {
  width: 64px;
  height: 100vh;
  background: var(--app-rail-bg);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  flex-shrink: 0;
  user-select: none;
  position: relative;
  z-index: 20;
}

.bar-top {
  border-bottom: 1px solid var(--app-rail-border);
}

.bar-middle {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 0;
  gap: 4px;
}

.bar-bottom {
  border-top: 1px solid var(--app-rail-border);
  padding: 12px 0;
  display: flex;
  justify-content: center;
}

.module-btn {
  position: relative;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: var(--app-radius);
  color: var(--app-rail-text);
  cursor: pointer;
  transition: background 0.18s, color 0.18s;

  &:hover {
    background: var(--app-rail-hover-bg);
    color: var(--app-rail-text-hover);
  }

  &.active {
    background: color-mix(in srgb, var(--app-primary) 18%, transparent);
    color: var(--app-rail-text-active);

    // 左侧竖线
    &::before {
      content: '';
      position: absolute;
      left: -10px;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 24px;
      background: var(--app-primary, #2080f0);
      border-radius: 2px;
    }
  }

  &.placeholder {
    opacity: 0.5;

    &:hover {
      opacity: 0.8;
    }
  }

  .module-icon {
    width: 22px;
    height: 22px;
  }
}
</style>
