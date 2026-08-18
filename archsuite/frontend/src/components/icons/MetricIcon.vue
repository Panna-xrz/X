<script setup lang="ts">
// 指标图标：图表/柱状图
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
    <!-- 坐标轴 -->
    <path d="M3 3v18h18" />
    <!-- 柱状 -->
    <path d="M7 14v4M11 10v8M15 6v12M19 12v6" />
    <!-- 顶部圆点强调 -->
    <circle cx="7" cy="14" r="0.8" fill="currentColor" stroke="none" />
    <circle cx="11" cy="10" r="0.8" fill="currentColor" stroke="none" />
    <circle cx="15" cy="6" r="0.8" fill="currentColor" stroke="none" />
    <circle cx="19" cy="12" r="0.8" fill="currentColor" stroke="none" />
  </svg>
</template>
