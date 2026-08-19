<script setup lang="ts">
// 环境解析图标：地球（圆 + 经纬线），简洁高级线性风
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
    <!-- 地球外圆 -->
    <circle cx="12" cy="12" r="8" />
    <!-- 经线 -->
    <path d="M12 4v16" />
    <!-- 纬线（赤道椭圆） -->
    <ellipse cx="12" cy="12" rx="8" ry="3.4" />
  </svg>
</template>
