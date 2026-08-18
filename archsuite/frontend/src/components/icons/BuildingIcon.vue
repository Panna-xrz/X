<script setup lang="ts">
// 建筑单体图标：独立建筑+层数
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
    <!-- 主体 -->
    <rect x="6" y="3" width="12" height="18" rx="0.5" />
    <!-- 楼层线 -->
    <path d="M6 8h12M6 13h12M6 18h12" />
    <!-- 窗户 -->
    <path d="M9 5v1M12 5v1M15 5v1M9 10v1M12 10v1M15 10v1M9 15v1M12 15v1M15 15v1" />
    <!-- 地面 -->
    <path d="M3 21h18" />
  </svg>
</template>
