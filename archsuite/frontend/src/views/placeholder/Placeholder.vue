<script setup lang="ts">
import { h } from 'vue'
import { NEmpty, NCard } from 'naive-ui'

// 占位组件：接收模块名，居中显示"暂不实现"
const props = defineProps<{
  moduleName?: string
}>()

// 兜底取路由 meta 中的 moduleName
import { useRoute } from 'vue-router'
const route = useRoute()
const name = props.moduleName || (route.meta.moduleName as string) || '未知模块'
</script>

<template>
  <div class="placeholder-page">
    <NCard class="placeholder-card" size="huge" :bordered="false">
      <NEmpty description="" size="large">
        <template #icon>
          <span class="module-emoji">📐</span>
        </template>
        <template #default>
          <div class="content">
            <div class="title">{{ name }}</div>
            <div class="desc">暂不实现（规划中）</div>
          </div>
        </template>
        <template #extra>
          <span class="hint">该模块处于规划阶段，敬请期待后续迭代。</span>
        </template>
      </NEmpty>
    </NCard>
  </div>
</template>

<style scoped lang="scss">
.placeholder-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
}

.placeholder-card {
  width: 100%;
  max-width: 560px;
}

.module-emoji {
  font-size: 48px;
}

.content {
  text-align: center;
  margin-top: 8px;

  .title {
    font-size: 20px;
    font-weight: 600;
    color: var(--app-text-1);
  }

  .desc {
    margin-top: 8px;
    font-size: 14px;
    color: var(--app-text-2);
  }
}

.hint {
  font-size: 12px;
  color: var(--app-text-3);
}
</style>
