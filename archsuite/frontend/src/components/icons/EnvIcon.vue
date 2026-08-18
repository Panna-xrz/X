<script setup lang="ts">
// 环境解析图标：地球+定位针
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
    <!-- 地球外圆 -->
    <circle cx="12" cy="12" r="9" />
    <!-- 赤道线 -->
    <path d="M3 12h18" />
    <!-- 经线 -->
    <path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18" />
    <!-- 定位针 -->
    <path d="M19 14l-1.5 4L17 16l-2-0.5L19 14z" fill="currentColor" stroke="none" />
  </svg>
</template>
