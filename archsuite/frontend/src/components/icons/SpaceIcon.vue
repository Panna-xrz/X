<script setup lang="ts">
// 空间构成图标：3D 立方体
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
    <!-- 顶面 -->
    <path d="M12 2l9 5v10l-9 5-9-5V7z" />
    <!-- 内部三个面 -->
    <path d="M12 12l9-5M12 12v10M12 12L3 7" />
    <!-- 隐藏线（虚化） -->
    <path d="M3 17l9-5 9 5" stroke-dasharray="2 2" />
  </svg>
</template>
