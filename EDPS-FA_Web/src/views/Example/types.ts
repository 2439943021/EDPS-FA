export interface smallDataType{
    data:Array<{
        key: string,
        value: string, 
        isNew: Boolean // 增加新的一行
    }>, // 保存 key:value 的数组
    valid:string, // 启用
    typeName:string, // 小模版名称
    color:string, // 颜色
    type:string // 小模版类型
}
//小模版数据JSON格式
export interface addList {
    s_type: string, 
    small_temp_id:string,
    small_temp_name:string,
    data: { [key: string]: { info: string } } 
}
// 大模板的名称、描述、类型、用户id
export interface BigSmall {
    templateName:string,
    templateDescription:string,
    templateType:string,
    userId:string
}

// 大模板JSON数据
export interface templateBig {
    small_temp_id: string,
    color: string,
    valid: string,
    small_temp_type: "user",
    s_type:"enum"
}
