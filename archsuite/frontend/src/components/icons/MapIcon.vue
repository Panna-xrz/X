<script setup lang="ts">
// 场地周边图标：地图针+周边
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
    <!-- 定位针外圈 -->
    <path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z" />
    <!-- 中心点 -->
    <circle cx="12" cy="10" r="2.5" />
    <!-- 周边环（虚化） -->
    <circle cx="12" cy="10" r="6" stroke-dasharray="2 3" opacity="0.6" />
  </svg>
</template>
