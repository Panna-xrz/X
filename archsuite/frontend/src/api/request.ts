import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

// 创建 axios 实例：统一前缀 /api/v1
const service: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 15000
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

// 响应拦截器：拆包 data，统一错误处理
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const res = response.data
    // 若后端返回 { code, message, data } 结构则按 code 判定
    if (res && typeof res.code === 'number') {
      if (res.code !== 0 && res.code !== 200) {
        console.error('[response business error]', res.message)
        return Promise.reject(new Error(res.message || '业务异常'))
      }
      return res.data as unknown as AxiosResponse
    }
    return res as unknown as AxiosResponse
  },
  (error) => {
    console.error('[response error]', error?.message || error)
    // 统一抛出，调用方可 try/catch
    return Promise.reject(error)
  }
)

export default service
