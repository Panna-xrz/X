<script setup lang="ts">
// 设置图标：滑块组（三横线 + 滑点），现代高级线性风
</script>

<template>
  <svg
    viewBox="0 0 24 24"
    width="24"
    height="24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.6"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <!-- 三条滑轨 -->
    <path d="M5 7h14M5 12h14M5 17h14" />
    <!-- 三个滑点（填充） -->
    <circle cx="9" cy="7" r="2.2" fill="currentColor" stroke="none" />
    <circle cx="15" cy="12" r="2.2" fill="currentColor" stroke="none" />
    <circle cx="11" cy="17" r="2.2" fill="currentColor" stroke="none" />
  </svg>
</template>
