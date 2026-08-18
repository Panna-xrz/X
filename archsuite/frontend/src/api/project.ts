import request from './request'
import type { Project, ProjectExtra, PageResult, AiExtractResult, ApiResponse } from '@/types'

// 获取项目分页列表
export function getProjects(params?: {
  page?: number
  pageSize?: number
  keyword?: string
  status?: string
}): Promise<PageResult<Project>> {
  return request.get<ApiResponse<PageResult<Project>>>('/projects', { params })
    .then((res) => res as unknown as PageResult<Project>)
}

// 创建项目
export function createProject(payload: Partial<Project>): Promise<Project> {
  return request.post<ApiResponse<Project>>('/projects', payload)
    .then((res) => res as unknown as Project)
}

// 获取项目详情
export function getProject(id: string): Promise<Project> {
  return request.get<ApiResponse<Project>>(`/projects/${id}`)
    .then((res) => res as unknown as Project)
}

// 更新项目
export function updateProject(id: string, payload: Partial<Project>): Promise<Project> {
  return request.put<ApiResponse<Project>>(`/projects/${id}`, payload)
    .then((res) => res as unknown as Project)
}

// 删除项目
export function deleteProject(id: string): Promise<void> {
  return request.delete<ApiResponse<void>>(`/projects/${id}`)
    .then(() => undefined)
}

// 获取项目扩展信息
export function getProjectExtra(id: string): Promise<ProjectExtra> {
  return request.get<ApiResponse<ProjectExtra>>(`/projects/${id}/extra`)
    .then((res) => res as unknown as ProjectExtra)
}

// AI 自动提取项目信息（调后端 AI 接口）
export function aiExtractProjectInfo(id: string, payload: { source?: string } = {}): Promise<AiExtractResult> {
  return request.post<ApiResponse<AiExtractResult>>(`/projects/${id}/ai-extract`, payload)
    .then((res) => res as unknown as AiExtractResult)
}
