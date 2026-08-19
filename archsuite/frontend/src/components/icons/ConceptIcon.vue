<script setup lang="ts">
// 概念构思图标：灯泡（顶部圆弧 + 底座 + 螺钉），简洁高级线性风
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
    <!-- 灯泡顶部圆弧 -->
    <path d="M9 13.5a5 5 0 1 1 6 0" />
    <!-- 主体到座 -->
    <path d="M9 13.5v2.5a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-2.5" />
    <!-- 螺钉 -->
    <path d="M10.5 17v1.5M13.5 17v1.5" />
  </svg>
</template>
