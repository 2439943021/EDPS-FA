import instance from './request'

// 封装一个发送 GET 请求的方法
export function get(url:any, params:any) {
    return instance.get(url, {params});
}


// 封装一个发送 POST 请求的方法
export function post(url:any, data:any, config?: any) {
    return instance.post(url, data, config);
}

// 封装一个发送 DELETE 请求的方法
export function Delete(url:any, data?:any){
    return instance.delete(url, {data});
}
