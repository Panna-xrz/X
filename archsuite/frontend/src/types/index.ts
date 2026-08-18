// 全局类型定义：与后端 camelCase JSON 契约一一对齐（ID 均为 number）

// 项目状态
export type ProjectStatus = 'draft' | 'planning' | 'in-progress' | 'completed' | 'archived'

// 项目主体信息
export interface Project {
  id: number
  name: string
  code: string // 项目编号
  client: string | null // 委托方
  location: string | null // 项目地址
  type: string | null // 项目类型（公建/住宅/商业等）
  scale: string | null // 建设规模
  startDate: string | null // 开工日期 yyyy-MM-dd
  endDate: string | null // 竣工日期 yyyy-MM-dd
  status: string
  description: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 项目扩展信息（后端为动态键值对）
export interface ProjectExtraItem {
  id: number
  projectId: number
  fieldKey: string
  fieldValue: string | null
  aiSource: string | null
}

export interface ProjectExtraResponse {
  items: ProjectExtraItem[]
  fields: Record<string, string | null>
}

// 合同类型：主合同 / 补充协议
export type ContractType = 'main' | 'supplement'

// 合同主体
export interface Contract {
  id: number
  projectId: number // 关联项目
  code: string // 合同编号
  name: string // 合同名称
  type: ContractType
  partyA: string | null // 甲方
  partyB: string | null // 乙方
  amount: number | null // 合同金额
  signedDate: string | null // 签订日期
  status: string
  contentText: string | null // 合同正文（AI 起草后写回）
  parentContractId: number | null // 补充协议关联的主合同 id
  remarks: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 收费节点（收费记账）
export interface ContractNode {
  id: number
  contractId: number
  name: string // 收费节点名称（如：设计费-首付款）
  ratio: number | null // 占合同金额比例(%)
  amount: number | null // 节点金额
  planDate: string | null // 计划收款日期
  actualDate: string | null // 实际收款日期
  status: string // planned / invoiced / received / overdue
  remarks: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 分页结果（后端 PageResult 契约）
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// 通用包装响应（仅后端异常时出现 {code, message, detail, path}）
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data?: T
  detail?: string | null
}

// AI 提取项目扩展信息结果
export interface AiExtractResult {
  projectId: number
  fields: Record<string, string | null>
  raw: string | null
}

// AI 起草合同正文结果
export interface ContractGenerateResult {
  contractId: number
  content: string
}

// AI 合同审核风险项
export interface ContractRiskItem {
  clause: string | null // 风险条款
  level: string | null // 风险等级：高/中/低
  suggestion: string | null // 改进建议
}

// AI 合同审核结果
export interface ContractReviewResult {
  contractId: number
  risks: ContractRiskItem[]
  raw: string | null // 解析失败时的原文回退
}
