import request from './request'
import type {
  Project,
  ProjectExtraResponse,
  PageResult,
  AiExtractResult,
  ApiResponse
} from '@/types'

// 获取项目分页列表
export function getProjects(params?: {
  page?: number
  pageSize?: number
}): Promise<PageResult<Project>> {
  return request
    .get<ApiResponse<PageResult<Project>>>('/projects', { params })
    .then((res) => res as unknown as PageResult<Project>)
}

// 创建项目
export function createProject(
  payload: Partial<Pick<Project, 'name' | 'code' | 'client' | 'location' | 'type' | 'scale' | 'startDate' | 'endDate' | 'status' | 'description'>>
): Promise<Project> {
  return request
    .post<ApiResponse<Project>>('/projects', payload)
    .then((res) => res as unknown as Project)
}

// 获取项目详情
export function getProject(id: number): Promise<Project> {
  return request
    .get<ApiResponse<Project>>(`/projects/${id}`)
    .then((res) => res as unknown as Project)
}

// 更新项目（仅更新传入字段）
export function updateProject(
  id: number,
  payload: Partial<Pick<Project, 'name' | 'code' | 'client' | 'location' | 'type' | 'scale' | 'startDate' | 'endDate' | 'status' | 'description'>>
): Promise<Project> {
  return request
    .put<ApiResponse<Project>>(`/projects/${id}`, payload)
    .then((res) => res as unknown as Project)
}

// 删除项目
export function deleteProject(id: number): Promise<void> {
  return request.delete<ApiResponse<void>>(`/projects/${id}`).then(() => undefined)
}

// 获取项目扩展信息（动态键值对：items 列表 + fields 对象）
export function getProjectExtra(id: number): Promise<ProjectExtraResponse> {
  return request
    .get<ApiResponse<ProjectExtraResponse>>(`/projects/${id}/extra`)
    .then((res) => res as unknown as ProjectExtraResponse)
}

// AI 自动提取项目扩展信息（结果同时写回后端）
export function aiExtractProjectInfo(id: number): Promise<AiExtractResult> {
  return request
    .post<ApiResponse<AiExtractResult>>(`/projects/${id}/ai-extract`)
    .then((res) => res as unknown as AiExtractResult)
}
