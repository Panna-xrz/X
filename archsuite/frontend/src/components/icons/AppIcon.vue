<script setup lang="ts">
// 软件图标：建筑剪影（A 字母化建筑：双斜线屋顶 + 三段竖向开窗）
// 与侧栏 ProjectIcon 同源、但更克制，适合顶栏小尺寸
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
    <!-- 屋顶（A 字顶） -->
    <path d="M4 5L12 3L20 5" />
    <!-- 主体外框 -->
    <path d="M6.5 5V20H17.5V5" />
    <!-- 中柱 -->
    <path d="M12 5V20" />
    <!-- 窗格（左中右三段竖向短线） -->
    <path d="M9 9v3M9 14v3M15 9v3M15 14v3" />
  </svg>
</template>
