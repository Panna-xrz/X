import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// 路由表：6 个业务模块
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/project/list'
  },
  // 1. 项目信息
  {
    path: '/project',
    name: 'Project',
    redirect: '/project/list',
    meta: { title: '项目信息' },
    children: [
      {
        path: 'list',
        name: 'ProjectList',
        component: () => import('@/views/project/ProjectList.vue'),
        meta: { title: '项目列表' }
      },
      {
        path: ':id',
        name: 'ProjectDetail',
        component: () => import('@/views/project/ProjectDetail.vue'),
        meta: { title: '项目详情' }
      }
    ]
  },
  // 2. 商务管理
  {
    path: '/commerce',
    name: 'Commerce',
    redirect: '/commerce/contracts',
    meta: { title: '商务管理' },
    children: [
      {
        path: 'contracts',
        name: 'ContractList',
        component: () => import('@/views/commerce/ContractList.vue'),
        meta: { title: '合同列表' }
      },
      {
        path: 'contract/edit/:id?',
        name: 'ContractEditor',
        component: () => import('@/views/commerce/ContractEditor.vue'),
        meta: { title: '合同编辑' }
      },
      {
        path: 'billings',
        name: 'BillingList',
        component: () => import('@/views/commerce/BillingList.vue'),
        meta: { title: '收费记账' }
      }
    ]
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
    path: '/plane',
    name: 'Plane',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '平面构成', moduleName: '平面构成' }
  },
  // 6. 空间构成（占位）
  {
    path: '/space',
    name: 'Space',
    component: () => import('@/views/placeholder/Placeholder.vue'),
    meta: { title: '空间构成', moduleName: '空间构成' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
