import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getProjects, createProject, deleteProject, getProject } from '@/api/project'
import type { Project } from '@/types'

/**
 * 全局项目状态管理：
 * - 维护项目列表与当前选中项目
 * - 所有页面均基于 currentProjectId 读取/写入子项数据
 * - 选中项目持久化到 localStorage，刷新不丢失
 */
export const useProjectStore = defineStore('project', () => {
  // 项目列表
  const projects = ref<Project[]>([])
  // 当前选中项目 ID
  const currentId = ref<number | null>(null)
  // 当前选中项目对象（懒加载）
  const currentProject = ref<Project | null>(null)
  // 加载状态
  const loading = ref(false)

  // localStorage 持久化键
  const STORAGE_KEY = 'archsuite_current_project_id'

  // 当前项目 ID（只读 computed）
  const currentProjectId = computed(() => currentId.value)

  // 是否已选择项目
  const hasProject = computed(() => currentId.value !== null)

  // 加载项目列表
  async function loadProjects() {
    loading.value = true
    try {
      const res = await getProjects({ page: 1, pageSize: 100 })
      projects.value = res.list || []
      // 若之前选中的项目不在列表中，清空选择
      if (currentId.value && !projects.value.find(p => p.id === currentId.value)) {
        selectProject(null)
      }
      // 若未选中且列表非空，自动选中第一个
      if (!currentId.value && projects.value.length > 0) {
        const saved = localStorage.getItem(STORAGE_KEY)
        const savedId = saved ? Number(saved) : null
        const found = savedId ? projects.value.find(p => p.id === savedId) : null
        selectProject(found ? found.id : projects.value[0].id)
      }
    } catch {
      projects.value = []
    } finally {
      loading.value = false
    }
  }

  // 选中项目（传 null 表示取消选择）
  async function selectProject(id: number | null) {
    currentId.value = id
    if (id !== null) {
      localStorage.setItem(STORAGE_KEY, String(id))
      // 加载项目详情
      try {
        currentProject.value = await getProject(id)
      } catch {
        currentProject.value = null
      }
    } else {
      localStorage.removeItem(STORAGE_KEY)
      currentProject.value = null
    }
  }

  // 新建项目
  async function addProject(payload: { name: string; code: string; client?: string; location?: string; type?: string }) {
    const created = await createProject(payload)
    projects.value.push(created)
    await selectProject(created.id)
    return created
  }

  // 删除当前项目
  async function removeCurrentProject() {
    if (!currentId.value) return
    await deleteProject(currentId.value)
    projects.value = projects.value.filter(p => p.id !== currentId.value)
    // 选中下一个或清空
    const next = projects.value[0]
    await selectProject(next ? next.id : null)
  }

  // 刷新当前项目详情
  async function refreshCurrent() {
    if (!currentId.value) return
    currentProject.value = await getProject(currentId.value)
  }

  return {
    projects,
    currentId,
    currentProject,
    currentProjectId,
    hasProject,
    loading,
    loadProjects,
    selectProject,
    addProject,
    removeCurrentProject,
    refreshCurrent,
  }
})
