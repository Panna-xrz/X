<script setup lang="ts">
import { onMounted } from 'vue'
import { NLayout, NLayoutContent } from 'naive-ui'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import { useThemeStore } from '@/stores/theme'

// 整体布局：左侧侧栏 + 右侧（头部 + 内容区）
const themeStore = useThemeStore()

onMounted(() => {
  // 首次挂载时把主题状态同步到根元素 CSS 变量与 data-theme
  themeStore.syncRootAttr()
})
</script>

<template>
  <NLayout has-sider position="absolute">
    <AppSidebar />
    <NLayout>
      <AppHeader />
      <NLayoutContent
        class="app-content"
        :native-scrollbar="false"
        content-style="padding: 16px;"
      >
        <RouterView />
      </NLayoutContent>
    </NLayout>
  </NLayout>
</template>

<style scoped lang="scss">
.app-content {
  min-height: calc(100vh - 56px);
}
</style>
