<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { NTabs, NTabPane, NEmpty, NCard, NSpin } from 'naive-ui'
import { useProjectStore } from '@/stores/project'
import BasicInfoTab from './tabs/BasicInfoTab.vue'
import MetricTab from './tabs/MetricTab.vue'
import SurroundingTab from './tabs/SurroundingTab.vue'
import PhysicalTab from './tabs/PhysicalTab.vue'
import CulturalTab from './tabs/CulturalTab.vue'
import BuildingTab from './tabs/BuildingTab.vue'

// 项目信息主页面：6 个 Tab 子项
const projectStore = useProjectStore()
const activeTab = ref<'basic' | 'metric' | 'surrounding' | 'physical' | 'cultural' | 'building'>('basic')

const currentProjectId = computed(() => projectStore.currentProjectId)
const hasProject = computed(() => projectStore.hasProject)
const projectName = computed(() => projectStore.currentProject?.name || '未选择项目')

// 切换项目时重置 Tab
watch(currentProjectId, () => {
  activeTab.value = 'basic'
})
</script>

<template>
  <div class="project-view">
    <div class="page-header">
      <h2 class="title">项目信息</h2>
      <span v-if="hasProject" class="subtitle">{{ projectName }}</span>
    </div>

    <div v-if="!hasProject" class="empty-state">
      <NCard :bordered="false" size="huge">
        <NEmpty description="请先在左侧选择或新建项目" size="large" />
      </NCard>
    </div>

    <div v-else class="tab-container">
      <NTabs v-model:value="activeTab" type="line" animated>
        <NTabPane name="basic" tab="基本信息">
          <BasicInfoTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="metric" tab="指标信息">
          <MetricTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="surrounding" tab="场地周边">
          <SurroundingTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="physical" tab="物理环境">
          <PhysicalTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="cultural" tab="人文环境">
          <CulturalTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="building" tab="建筑单体">
          <BuildingTab :project-id="currentProjectId!" />
        </NTabPane>
      </NTabs>
    </div>
  </div>
</template>

<style scoped lang="scss">
.project-view {
  padding: 16px 20px;
  min-height: 100vh;
}

.page-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;

  .title {
    font-size: 18px;
    font-weight: 600;
    color: var(--app-text-1);
    margin: 0;
  }

  .subtitle {
    font-size: 13px;
    color: var(--app-text-3);
  }
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 100px);
}

.tab-container {
  background: var(--app-card-bg);
  border-radius: var(--app-radius, 8px);
  padding: 12px 16px;
}
</style>
