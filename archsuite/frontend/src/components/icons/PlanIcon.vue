<script setup lang="ts">
// 平面构成图标：网格平面图
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
    <!-- 外框 -->
    <rect x="3" y="3" width="18" height="18" rx="0.5" />
    <!-- 网格内部分割 -->
    <path d="M3 9h18M3 15h18M9 3v18M15 3v18" />
    <!-- 中心强调点 -->
    <circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none" />
  </svg>
</template>
