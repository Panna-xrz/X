import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// 路由表：模块化结构（IconBar 模式）
// - /project → 项目信息模块（内含 Tab）
// - /commerce → 商务管理模块（内含 Tab） + 合同编辑独立页
// - /settings → 设置页
// - /env /concept /plan /space → 占位页
// - / → 重定向到 /project
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/project'
  },
  // 1. 项目信息
  {
    path: '/project',
    name: 'Project',
    component: () => import('@/views/project/ProjectView.vue'),
    meta: { title: '项目信息' }
  },
  // 2. 商务管理
  {
    path: '/commerce',
    name: 'Commerce',
    component: () => import('@/views/commerce/CommerceView.vue'),
    meta: { title: '商务管理' }
  },
  // 合同编辑器（独立页面）
  {
    path: '/commerce/contract/:id',
    name: 'ContractEditor',
    component: () => import('@/views/commerce/ContractEditor.vue'),
    meta: { title: '合同编辑' }
  },
  // 3. 环境解析（占位）
  {
    path: '/env',
    name: 'Env',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '环境解析', moduleName: '环境解析' }
  },
  // 4. 概念构思（占位）
  {
    path: '/concept',
    name: 'Concept',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '概念构思', moduleName: '概念构思' }
  },
  // 5. 平面构成（占位）
  {
    path: '/plan',
    name: 'Plan',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '平面构成', moduleName: '平面构成' }
  },
  // 6. 空间构成（占位）
  {
    path: '/space',
    name: 'Space',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '空间构成', moduleName: '空间构成' }
  },
  // 7. 设置
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { title: '设置' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
