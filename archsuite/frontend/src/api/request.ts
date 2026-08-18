import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

// 创建 axios 实例：统一前缀 /api/v1
// 超时设为 120s：AI 起草/审核接口耗时较长
const service: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 120000
})

// 请求拦截器：可附加 token 等
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('archsuite_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('[request error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：直接返回数据本体，统一错误处理
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const res = response.data
    // 成功响应直接是数据本体；若未来后端引入 {code, message, data} 包装则按 code 拆包
    if (res && typeof res === 'object' && typeof res.code === 'number' && res.code !== 200 && res.code !== 0) {
      console.error('[response business error]', res.message)
      return Promise.reject(new Error(res.message || '业务异常'))
    }
    return res as unknown as AxiosResponse
  },
  (error) => {
    // 后端异常格式：{code, message, detail, path}，优先展示后端 message
    const data = error?.response?.data
    const msg = data?.message || error?.message || '网络异常，请稍后重试'
    console.error('[response error]', msg)
    return Promise.reject(new Error(msg))
  }
)

export default service
