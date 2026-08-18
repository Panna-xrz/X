<script setup lang="ts">
import { ref, computed, h, type Component } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { NLayoutSider, NMenu, type MenuOption } from 'naive-ui'

// 简易内联 SVG 图标组件（避免引入额外图标库）
function makeIcon(path: string): Component {
  return () =>
    h(
      'svg',
      {
        viewBox: '0 0 24 24',
        width: '18',
        height: '18',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': '1.8',
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round'
      },
      [h('path', { d: path })]
    )
}

// 侧栏菜单：6 个模块，项目信息与商务管理含子项
const menuOptions = computed<MenuOption[]>(() => [
  {
    label: '项目信息',
    key: 'project-group',
    type: 'group',
    icon: makeIcon('M3 7h18M3 12h18M3 17h18'),
    children: [
      {
        label: () => h(RouterLink, { to: '/project/list' }, { default: () => '项目列表' }),
        key: '/project/list'
      },
      {
        label: () => h(RouterLink, { to: '/project/detail' }, { default: () => '项目详情' }),
        key: '/project/:id'
      }
    ]
  },
  {
    label: '商务管理',
    key: 'commerce-group',
    type: 'group',
    icon: makeIcon('M4 4h16v16H4zM4 9h16M9 9v11'),
    children: [
      {
        label: () => h(RouterLink, { to: '/commerce/contracts' }, { default: () => '合同列表' }),
        key: '/commerce/contracts'
      },
      {
        label: () =>
          h(RouterLink, { to: '/commerce/contract/edit' }, { default: () => '合同编辑' }),
        key: '/commerce/contract/edit'
      },
      {
        label: () => h(RouterLink, { to: '/commerce/billings' }, { default: () => '收费记账' }),
        key: '/commerce/billings'
      }
    ]
  },
  {
    label: '环境解析',
    key: '/env',
    icon: makeIcon('M3 12h4l3 8 4-16 3 8h4')
  },
  {
    label: '概念构思',
    key: '/concept',
    icon: makeIcon('M12 2a7 7 0 100 14 7 7 0 000-14zM12 2v3M12 19v3M2 12h3M19 12h3')
  },
  {
    label: '平面构成',
    key: '/plane',
    icon: makeIcon('M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z')
  },
  {
    label: '空间构成',
    key: '/space',
    icon: makeIcon('M3 3h7v7H3zM14 3l7 0v7h-7zM7 14l7 7 7-7z')
  }
])

const route = useRoute()
const router = useRouter()
const activeKey = ref<string>(route.path)

// 点击菜单项路由跳转（项目详情占位项保持原样）
function handleSelect(key: string) {
  if (key.startsWith('/project/:id')) return
  if (key) router.push(key)
}
</script>

<template>
  <NLayoutSider
    bordered
    :width="220"
    :collapsed-width="64"
    show-trigger
    collapse-mode="width"
    class="app-sidebar"
  >
    <div class="logo">
      <span class="logo-mark">⬢</span>
      <span class="logo-text">ArchSuite</span>
    </div>
    <NMenu
      :options="menuOptions"
      :value="activeKey"
      :default-expanded-keys="['project-group', 'commerce-group']"
      @update:value="handleSelect"
    />
  </NLayoutSider>
</template>

<style scoped lang="scss">
.app-sidebar {
  display: flex;
  flex-direction: column;
}

.logo {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 18px;
  font-weight: 600;
  font-size: 16px;
  letter-spacing: 0.5px;

  .logo-mark {
    font-size: 18px;
    color: var(--app-primary);
  }
}
</style>
