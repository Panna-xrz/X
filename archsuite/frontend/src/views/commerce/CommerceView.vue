<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { NTabs, NTabPane, NEmpty, NCard } from 'naive-ui'
import { useProjectStore } from '@/stores/project'
import ContactTab from './tabs/ContactTab.vue'
import ContractPreviewTab from './tabs/ContractPreviewTab.vue'
import ContractDraftTab from './tabs/ContractDraftTab.vue'
import ContractReviewTab from './tabs/ContractReviewTab.vue'
import ContractManageTab from './tabs/ContractManageTab.vue'

// 商务管理主页面：5 个 Tab 子项
const projectStore = useProjectStore()
const activeTab = ref<'contact' | 'preview' | 'draft' | 'review' | 'manage'>('contact')

const currentProjectId = computed(() => projectStore.currentProjectId)
const hasProject = computed(() => projectStore.hasProject)
const projectName = computed(() => projectStore.currentProject?.name || '未选择项目')

watch(currentProjectId, () => {
  activeTab.value = 'contact'
})
</script>

<template>
  <div class="commerce-view">
    <div class="page-header">
      <h2 class="title">商务管理</h2>
      <span v-if="hasProject" class="subtitle">{{ projectName }}</span>
    </div>

    <div v-if="!hasProject" class="empty-state">
      <NCard :bordered="false" size="huge">
        <NEmpty description="请先在左侧选择或新建项目" size="large" />
      </NCard>
    </div>

    <div v-else class="tab-container">
      <NTabs v-model:value="activeTab" type="line" animated>
        <NTabPane name="contact" tab="联系单">
          <ContactTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="preview" tab="合同预览">
          <ContractPreviewTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="draft" tab="合同草拟">
          <ContractDraftTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="review" tab="合同审查">
          <ContractReviewTab :project-id="currentProjectId!" />
        </NTabPane>
        <NTabPane name="manage" tab="合同管理">
          <ContractManageTab :project-id="currentProjectId!" />
        </NTabPane>
      </NTabs>
    </div>
  </div>
</template>

<style scoped lang="scss">
.commerce-view {
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
