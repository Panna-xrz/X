// 全局类型定义：与后端 camelCase JSON 契约一一对齐（ID 均为 number）

// 项目状态
export type ProjectStatus = 'draft' | 'planning' | 'in-progress' | 'completed' | 'archived'

// 项目主体信息
export interface Project {
  id: number
  name: string
  code: string
  client: string | null
  location: string | null
  type: string | null
  scale: string | null
  phase: string | null
  longitude: number | null
  latitude: number | null
  startDate: string | null
  endDate: string | null
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

// 项目指标信息
export interface ProjectMetric {
  id?: number
  projectId?: number
  landUse: string | null
  siteArea: number | null
  farAbove: number | null
  farUnder: number | null
  greenRatio: number | null
  buildingDensity: number | null
  heightLimit: number | null
  totalFloorArea: number | null
  aboveFloorArea: number | null
  underFloorArea: number | null
  parkingAbove: number | null
  parkingUnder: number | null
  remarks: string | null
  createdAt?: string | null
  updatedAt?: string | null
}

// 场地周边
export interface ProjectSurrounding {
  id?: number
  projectId?: number
  longitude: number | null
  latitude: number | null
  within200m: string | null
  within500m: string | null
  within2000m: string | null
  nearbyRoads: string | null
  naturalFeatures: string | null
  transitInfo: string | null
  remarks: string | null
  createdAt?: string | null
  updatedAt?: string | null
}

// 物理环境
export interface ProjectPhysical {
  id?: number
  projectId?: number
  climateZone: string | null
  prevailingWind: string | null
  solarPath: string | null
  annualPrecipitation: number | null
  groundwaterLevel: number | null
  elevation: number | null
  avgAnnualTemp: number | null
  extremeMaxTemp: number | null
  extremeMinTemp: number | null
  remarks: string | null
  createdAt?: string | null
  updatedAt?: string | null
}

// 人文环境
export interface ProjectCultural {
  id?: number
  projectId?: number
  culturalSymbols: string | null
  regionalArchitecture: string | null
  urbanColorScheme: string | null
  localCustoms: string | null
  historicalCulture: string | null
  remarks: string | null
  createdAt?: string | null
  updatedAt?: string | null
}

// 建筑单体
export interface ProjectBuilding {
  id: number
  projectId: number
  code: string
  name: string
  buildingNature: string | null
  buildingFunction: string | null
  floorsAbove: number | null
  floorsUnder: number | null
  height: number | null
  floorArea: number | null
  remarks: string | null
  createdAt?: string | null
  updatedAt?: string | null
}

// 合同类型：主合同 / 补充协议
export type ContractType = 'main' | 'supplement'

// 合同主体
export interface Contract {
  id: number
  projectId: number
  code: string
  name: string
  type: ContractType
  partyA: string | null
  partyB: string | null
  amount: number | null
  signedDate: string | null
  status: string
  contentText: string | null
  parentContractId: number | null
  remarks: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 收费节点
export interface ContractNode {
  id: number
  contractId: number
  name: string
  ratio: number | null
  amount: number | null
  planDate: string | null
  actualDate: string | null
  status: string
  remarks: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 联系单
export type ContactType = 'client' | 'team'

export interface ContactPerson {
  id: number
  projectId: number
  contactType: ContactType
  name: string
  role: string | null
  phone: string | null
  remarks: string | null
  createdAt: string | null
  updatedAt: string | null
}

// 分页结果
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

// 通用响应
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
  clause: string | null
  level: string | null
  suggestion: string | null
}

// AI 合同审核结果
export interface ContractReviewResult {
  contractId: number
  risks: ContractRiskItem[]
  raw: string | null
}
