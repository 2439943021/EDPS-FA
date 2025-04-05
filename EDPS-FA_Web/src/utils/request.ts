import axios from "axios"

// 创建 Axios 实例
const instance = axios.create({
  baseURL:import.meta.env.VITE_BASE_URL, // 设置 baseURL
  timeout: 50000 // 设置超时时间
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    // 可以在这里添加请求头、请求参数等
    return config;
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    // 在这里可以对响应结果进行统一处理
    return response.data;
  },
  error => {
    // 对响应错误做点什么
    // 可以在这里处理请求失败的情况
    return Promise.reject(error);
  }
);

// 导出封装后的 Axios 实例
export default instance;