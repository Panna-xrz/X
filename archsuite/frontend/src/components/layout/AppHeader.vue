<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { NLayoutHeader, NBreadcrumb, NBreadcrumbItem } from 'naive-ui'
import ThemeSwitch from './ThemeSwitch.vue'

// 头部：左侧面包屑（取 matched 路由标题），右侧主题切换
const route = useRoute()

// 面包屑项：从 matched 路由的 meta.title 取
const breadcrumbs = computed(() =>
  route.matched
    .filter((m) => m.meta && m.meta.title)
    .map((m) => ({
      title: m.meta.title as string,
      path: m.path
    }))
)
</script>

<template>
  <NLayoutHeader class="app-header">
    <NBreadcrumb class="breadcrumb">
      <NBreadcrumbItem v-for="item in breadcrumbs" :key="item.path">
        {{ item.title }}
      </NBreadcrumbItem>
    </NBreadcrumb>
    <div class="right">
      <ThemeSwitch />
    </div>
  </NLayoutHeader>
</template>

<style scoped lang="scss">
.app-header {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  box-shadow: var(--app-shadow-sm);
  position: relative;
  z-index: 10;
}

.breadcrumb {
  font-size: 14px;
}

.right {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
