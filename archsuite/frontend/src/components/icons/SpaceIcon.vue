<script setup lang="ts">
// 空间构成图标：等轴测立方体，简洁高级线性风
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
    <!-- 顶面菱形 -->
    <path d="M12 3l8 5v0l-8 5-8-5z" />
    <!-- 左侧棱 -->
    <path d="M4 8v10l8 5" />
    <!-- 右侧棱 -->
    <path d="M20 8v10l-8 5" />
    <!-- 中心竖线 -->
    <path d="M12 13v10" />
  </svg>
</template>
