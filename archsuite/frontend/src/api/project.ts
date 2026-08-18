import request from './request'
import type { PageResult, ApiResponse } from '@/types'

// 统一解包辅助：后端返回裸数据体，拦截器已处理异常
function unwrap<T>(p: Promise<{ data: T }>): Promise<T> {
  return p.then((res: any) => res as unknown as T)
}

// ============ 项目 CRUD ============

export function getProjects(params?: { page?: number; pageSize?: number }): Promise<PageResult<import('@/types').Project>> {
  return unwrap(request.get('/projects', { params }))
}

export function createProject(payload: Partial<import('@/types').Project> & { name: string; code: string }): Promise<import('@/types').Project> {
  return unwrap(request.post('/projects', payload))
}

export function getProject(id: number): Promise<import('@/types').Project> {
  return unwrap(request.get(`/projects/${id}`))
}

export function updateProject(id: number, payload: Partial<import('@/types').Project>): Promise<import('@/types').Project> {
  return unwrap(request.put(`/projects/${id}`, payload))
}

export function deleteProject(id: number): Promise<void> {
  return unwrap(request.delete(`/projects/${id}`))
}

// ============ 项目子项 ============

// 指标信息
export function getProjectMetric(id: number): Promise<import('@/types').ProjectMetric> {
  return unwrap(request.get(`/projects/${id}/metric`))
}

export function upsertProjectMetric(id: number, payload: Partial<import('@/types').ProjectMetric>): Promise<import('@/types').ProjectMetric> {
  return unwrap(request.put(`/projects/${id}/metric`, { ...payload, projectId: id }))
}

// 场地周边
export function getProjectSurrounding(id: number): Promise<import('@/types').ProjectSurrounding> {
  return unwrap(request.get(`/projects/${id}/surrounding`))
}

export function upsertProjectSurrounding(id: number, payload: Partial<import('@/types').ProjectSurrounding>): Promise<import('@/types').ProjectSurrounding> {
  return unwrap(request.put(`/projects/${id}/surrounding`, { ...payload, projectId: id }))
}

// 物理环境
export function getProjectPhysical(id: number): Promise<import('@/types').ProjectPhysical> {
  return unwrap(request.get(`/projects/${id}/physical`))
}

export function upsertProjectPhysical(id: number, payload: Partial<import('@/types').ProjectPhysical>): Promise<import('@/types').ProjectPhysical> {
  return unwrap(request.put(`/projects/${id}/physical`, { ...payload, projectId: id }))
}

// 人文环境
export function getProjectCultural(id: number): Promise<import('@/types').ProjectCultural> {
  return unwrap(request.get(`/projects/${id}/cultural`))
}

export function upsertProjectCultural(id: number, payload: Partial<import('@/types').ProjectCultural>): Promise<import('@/types').ProjectCultural> {
  return unwrap(request.put(`/projects/${id}/cultural`, { ...payload, projectId: id }))
}

// 建筑单体
export function getProjectBuildings(id: number): Promise<import('@/types').ProjectBuilding[]> {
  return unwrap(request.get(`/projects/${id}/buildings`))
}

export function createProjectBuilding(projectId: number, payload: Partial<import('@/types').ProjectBuilding> & { name: string }): Promise<import('@/types').ProjectBuilding> {
  return unwrap(request.post(`/projects/${projectId}/buildings`, { ...payload, projectId }))
}

export function updateProjectBuilding(projectId: number, buildingId: number, payload: Partial<import('@/types').ProjectBuilding>): Promise<import('@/types').ProjectBuilding> {
  return unwrap(request.put(`/projects/${projectId}/buildings/${buildingId}`, payload))
}

export function deleteProjectBuilding(projectId: number, buildingId: number): Promise<void> {
  return unwrap(request.delete(`/projects/${projectId}/buildings/${buildingId}`))
}

// 扩展信息 + AI 提取
export function getProjectExtra(id: number): Promise<import('@/types').ProjectExtraResponse> {
  return unwrap(request.get(`/projects/${id}/extra`))
}

export function aiExtractProjectInfo(id: number): Promise<import('@/types').AiExtractResult> {
  return unwrap(request.post(`/projects/${id}/ai-extract`))
}
