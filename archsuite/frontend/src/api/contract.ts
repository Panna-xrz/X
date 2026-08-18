import request from './request'
import type { Contract, ContractNode, BillingRecord, PageResult, ContractType, ApiResponse } from '@/types'

// 获取合同列表（按项目）
export function getContracts(params: {
  projectId?: string
  type?: ContractType
  page?: number
  pageSize?: number
}): Promise<PageResult<Contract>> {
  return request.get<ApiResponse<PageResult<Contract>>>('/contracts', { params })
    .then((res) => res as unknown as PageResult<Contract>)
}

// 创建合同
export function createContract(payload: Partial<Contract>): Promise<Contract> {
  return request.post<ApiResponse<Contract>>('/contracts', payload)
    .then((res) => res as unknown as Contract)
}

// 获取合同详情
export function getContract(id: string): Promise<Contract> {
  return request.get<ApiResponse<Contract>>(`/contracts/${id}`)
    .then((res) => res as unknown as Contract)
}

// 更新合同
export function updateContract(id: string, payload: Partial<Contract>): Promise<Contract> {
  return request.put<ApiResponse<Contract>>(`/contracts/${id}`, payload)
    .then((res) => res as unknown as Contract)
}

// 获取合同条款节点树
export function getContractNodes(id: string): Promise<ContractNode[]> {
  return request.get<ApiResponse<ContractNode[]>>(`/contracts/${id}/nodes`)
    .then((res) => res as unknown as ContractNode[])
}

// AI 生成合同（按项目与类型生成初稿）
export function aiGenerateContract(payload: {
  projectId: string
  type: ContractType
  parentContractId?: string
}): Promise<ContractNode[]> {
  return request.post<ApiResponse<ContractNode[]>>('/contracts/ai-generate', payload)
    .then((res) => res as unknown as ContractNode[])
}

// AI 审核合同（返回审核意见）
export function aiReviewContract(id: string): Promise<{ issues: string[]; suggestions: string[] }> {
  return request.post<ApiResponse<{ issues: string[]; suggestions: string[] }>>(`/contracts/${id}/ai-review`)
    .then((res) => res as unknown as { issues: string[]; suggestions: string[] })
}

// 获取收费记账列表
export function getBillings(params: { contractId?: string; page?: number; pageSize?: number }): Promise<PageResult<BillingRecord>> {
  return request.get<ApiResponse<PageResult<BillingRecord>>>('/billings', { params })
    .then((res) => res as unknown as PageResult<BillingRecord>)
}

// 新增收费节点
export function createBilling(payload: Partial<BillingRecord>): Promise<BillingRecord> {
  return request.post<ApiResponse<BillingRecord>>('/billings', payload)
    .then((res) => res as unknown as BillingRecord)
}
