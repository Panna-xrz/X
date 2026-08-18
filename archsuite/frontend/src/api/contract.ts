import request from './request'
import type {
  Contract,
  ContractNode,
  ContractType,
  ContractGenerateResult,
  ContractReviewResult,
  PageResult,
  ApiResponse
} from '@/types'

// 合同可编辑字段
export type ContractPayload = Partial<
  Pick<
    Contract,
    | 'name'
    | 'code'
    | 'type'
    | 'projectId'
    | 'partyA'
    | 'partyB'
    | 'amount'
    | 'signedDate'
    | 'status'
    | 'contentText'
    | 'remarks'
    | 'parentContractId'
  >
>

// 获取合同分页列表（可按项目过滤）
export function getContracts(params?: {
  projectId?: number
  page?: number
  pageSize?: number
}): Promise<PageResult<Contract>> {
  return request
    .get<ApiResponse<PageResult<Contract>>>('/contracts', { params })
    .then((res) => res as unknown as PageResult<Contract>)
}

// 创建合同（name/projectId 必填）
export function createContract(
  payload: ContractPayload & { name: string; projectId: number; type?: ContractType }
): Promise<Contract> {
  return request
    .post<ApiResponse<Contract>>('/contracts', payload)
    .then((res) => res as unknown as Contract)
}

// 获取合同详情
export function getContract(id: number): Promise<Contract> {
  return request
    .get<ApiResponse<Contract>>(`/contracts/${id}`)
    .then((res) => res as unknown as Contract)
}

// 更新合同（仅更新传入字段）
export function updateContract(id: number, payload: ContractPayload): Promise<Contract> {
  return request
    .put<ApiResponse<Contract>>(`/contracts/${id}`, payload)
    .then((res) => res as unknown as Contract)
}

// 删除合同（级联删除收费节点）
export function deleteContract(id: number): Promise<void> {
  return request.delete<ApiResponse<void>>(`/contracts/${id}`).then(() => undefined)
}

// 获取合同的全部收费节点（按计划日期升序）
export function getContractNodes(id: number): Promise<ContractNode[]> {
  return request
    .get<ApiResponse<ContractNode[]>>(`/contracts/${id}/nodes`)
    .then((res) => res as unknown as ContractNode[])
}

// AI 起草合同正文（生成后写回合同 contentText）
export function generateContract(id: number): Promise<ContractGenerateResult> {
  return request
    .post<ApiResponse<ContractGenerateResult>>(`/contracts/${id}/generate`)
    .then((res) => res as unknown as ContractGenerateResult)
}

// AI 审核合同条款风险（返回结构化风险清单）
export function reviewContract(id: number): Promise<ContractReviewResult> {
  return request
    .post<ApiResponse<ContractReviewResult>>(`/contracts/${id}/review`)
    .then((res) => res as unknown as ContractReviewResult)
}

// ===== 收费节点（/nodes）=====

// 获取收费节点分页列表（跨合同，可按 contractId 过滤）
export function getNodes(params?: {
  contractId?: number
  page?: number
  pageSize?: number
}): Promise<PageResult<ContractNode>> {
  return request
    .get<ApiResponse<PageResult<ContractNode>>>('/nodes', { params })
    .then((res) => res as unknown as PageResult<ContractNode>)
}

// 收费节点可编辑字段
export type NodePayload = Partial<
  Pick<ContractNode, 'name' | 'ratio' | 'amount' | 'planDate' | 'actualDate' | 'status' | 'remarks'>
>

// 创建收费节点
export function createNode(
  payload: NodePayload & { name: string; contractId: number }
): Promise<ContractNode> {
  return request
    .post<ApiResponse<ContractNode>>('/nodes', payload)
    .then((res) => res as unknown as ContractNode)
}

// 更新收费节点（仅更新传入字段）
export function updateNode(id: number, payload: NodePayload): Promise<ContractNode> {
  return request
    .put<ApiResponse<ContractNode>>(`/nodes/${id}`, payload)
    .then((res) => res as unknown as ContractNode)
}

// 删除收费节点
export function deleteNode(id: number): Promise<void> {
  return request.delete<ApiResponse<void>>(`/nodes/${id}`).then(() => undefined)
}
