<script setup lang="ts">
// 物理环境图标：太阳/温度计组合
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
    <!-- 太阳 -->
    <circle cx="7" cy="7" r="3" />
    <!-- 光芒 -->
    <path d="M7 1v2M7 11v2M1 7h2M11 7h2M2.8 2.8l1.4 1.4M9.8 9.8l1.4 1.4M2.8 11.2l1.4-1.4M9.8 4.2l1.4-1.4" />
    <!-- 温度计 -->
    <path d="M17 22a2 2 0 0 0 2-2V8a2 2 0 1 0-4 0v12a2 2 0 0 0 2 2z" />
    <!-- 刻度 -->
    <path d="M16 12h2M16 16h2" />
  </svg>
</template>
