import request from './request'
import { readSetting } from '@/utils/settings'
import type {
  Contract,
  ContractNode,
  ContractType,
  ContractGenerateResult,
  ContractReviewResult,
  PageResult,
} from '@/types'

function unwrap<T>(p: Promise<any>): Promise<T> {
  return p.then((res: any) => res as unknown as T)
}

// AI 接口超时：由设置面板 aiTimeout 控制（默认 120s）
function aiTimeout(): number {
  const sec = Number(readSetting('aiTimeout', '120'))
  if (!Number.isFinite(sec) || sec <= 0) return 120000
  return sec * 1000
}

// 合同可编辑字段
export type ContractPayload = Partial<
  Pick<
    Contract,
    | 'name' | 'code' | 'type' | 'projectId' | 'partyA' | 'partyB'
    | 'amount' | 'signedDate' | 'status' | 'contentText' | 'remarks' | 'parentContractId'
  >
>

// 合同 CRUD
export function getContracts(params?: { projectId?: number; page?: number; pageSize?: number }): Promise<PageResult<Contract>> {
  return unwrap(request.get('/contracts', { params }))
}

export function createContract(payload: ContractPayload & { name: string; projectId: number; type?: ContractType }): Promise<Contract> {
  return unwrap(request.post('/contracts', payload))
}

export function getContract(id: number): Promise<Contract> {
  return unwrap(request.get(`/contracts/${id}`))
}

export function updateContract(id: number, payload: ContractPayload): Promise<Contract> {
  return unwrap(request.put(`/contracts/${id}`, payload))
}

export function deleteContract(id: number): Promise<void> {
  return unwrap(request.delete(`/contracts/${id}`))
}

// 合同正文生成/审核/下载
export function generateContract(id: number): Promise<ContractGenerateResult> {
  return unwrap(request.post(`/contracts/${id}/generate`, {}, { timeout: aiTimeout() }))
}

export function reviewContract(id: number): Promise<ContractReviewResult> {
  return unwrap(request.post(`/contracts/${id}/review`, {}, { timeout: aiTimeout() }))
}

export function downloadContract(id: number): Promise<Blob> {
  return request.get(`/contracts/${id}/download`, { responseType: 'blob' }).then((res: any) => res as unknown as Blob)
}

// 收费节点
export function getContractNodes(id: number): Promise<ContractNode[]> {
  return unwrap(request.get(`/contracts/${id}/nodes`))
}

export type NodePayload = Partial<Pick<ContractNode, 'name' | 'ratio' | 'amount' | 'planDate' | 'actualDate' | 'status' | 'remarks'>>

export function getNodes(params?: { contractId?: number; page?: number; pageSize?: number }): Promise<PageResult<ContractNode>> {
  return unwrap(request.get('/nodes', { params }))
}

export function createNode(payload: NodePayload & { name: string; contractId: number }): Promise<ContractNode> {
  return unwrap(request.post('/nodes', payload))
}

export function updateNode(id: number, payload: NodePayload): Promise<ContractNode> {
  return unwrap(request.put(`/nodes/${id}`, payload))
}

export function deleteNode(id: number): Promise<void> {
  return unwrap(request.delete(`/nodes/${id}`))
}
