<script setup lang="ts">
// 项目信息图标：建筑/楼层组合，体现"项目主体"
</script>

<template>
  <svg
    viewBox="0 0 24 24"
    width="24"
    height="24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.5"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <!-- 左侧高层建筑 -->
    <rect x="3" y="3" width="7" height="18" rx="0.5" />
    <!-- 楼层分隔线 -->
    <path d="M5 7h3M5 11h3M5 15h3" />
    <!-- 右侧低层建筑 -->
    <path d="M14 14h7v7h-7z" />
    <!-- 屋顶斜线 -->
    <path d="M13 14l4-4 4 4" />
    <!-- 地面线 -->
    <path d="M2 21h20" />
  </svg>
</template>
