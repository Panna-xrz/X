// 全局类型定义

// 项目状态
export type ProjectStatus = 'draft' | 'planning' | 'in-progress' | 'completed' | 'archived'

// 项目主体信息
export interface Project {
  id: string
  name: string
  code: string // 项目编号
  client: string // 委托方
  location: string // 项目地址
  type: string // 项目类型（公建/住宅/商业等）
  scale: string // 建设规模
  startDate: string // 开工日期
  endDate: string // 竣工日期
  status: ProjectStatus
  description?: string
  createdAt: string
  updatedAt: string
}

// 项目扩展信息（环境/概念/平面/空间等阶段补充字段）
export interface ProjectExtra {
  projectId: string
  landArea?: number // 用地面积
  buildingArea?: number // 建筑面积
  floorsAbove?: number // 地上层数
  floorsUnder?: number // 地下层数
  heightLimit?: number // 高度限制
  greenRatio?: number // 绿地率
  plotRatio?: number // 容积率
  designStage?: string // 当前设计阶段
  remarks?: string
}

// 合同类型：主合同 / 补充协议
export type ContractType = 'main' | 'supplement'

// 合同主体
export interface Contract {
  id: string
  projectId: string // 关联项目
  code: string // 合同编号
  name: string // 合同名称
  type: ContractType
  party?: string // 乙方
  signedDate?: string // 签订日期
  amount: number // 合同金额
  status: 'draft' | 'reviewing' | 'signed' | 'terminated'
  parentContractId?: string // 补充协议关联的主合同 id
  remarks?: string
  createdAt: string
  updatedAt: string
}

// 合同条款节点（用于编辑器左侧结构化树）
export interface ContractNode {
  id: string
  contractId: string
  title: string
  content: string
  order: number
  children?: ContractNode[]
}

// 收费记账记录
export interface BillingRecord {
  id: string
  contractId: string
  node: string // 收费节点名称（如设计费-首付款）
  amount: number
  ratio?: number // 占合同比例
  planDate?: string // 计划日期
  actualDate?: string // 实际日期
  status: 'planned' | 'invoiced' | 'received' | 'overdue'
  remarks?: string
  createdAt: string
  updatedAt: string
}

// 分页结果
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// 通用后端响应
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

// AI 自动提取结果
export interface AiExtractResult {
  projectId: string
  fields: Partial<Project>
  confidence: number
  raw?: string
}
