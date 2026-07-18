import axios from "axios"

// 生产环境通过 VITE_API_BASE_URL 环境变量配置后端地址
// 开发环境通过 Vite proxy 代理到 localhost:5000
const http = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
    timeout: 60000
})

export default http
