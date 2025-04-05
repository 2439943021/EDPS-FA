import { checkVipInfo } from "../api/index";
import { ref } from "vue";
import { ElMessage } from "element-plus";
// 用户信息
let userInfo = ref<{
    id:string,
    upPostCount:number,
    upPostMax:number,
    upTemplateCount:number,
    upTemplateMax:number,
    userId:string,
    vipCreateTime:string,
    vipEndTime:string,
    vipType:string,
    visible:string
  }>();
export async function checkInfo(size:number, userId:number){
    userInfo.value = (await checkVipInfo(userId)).data;
    if(userInfo.value.upPostCount + size <= userInfo.value.upPostMax){
        return true;
    } else {
        ElMessage.error(`上传失败！您当前剩余检测数为：${userInfo.value.upPostMax - userInfo.value.upPostCount}`);
        return false;
    }
}

export async function checkTemp(userId:number){
    userInfo.value = (await checkVipInfo(userId)).data;
    if(userInfo.value.upTemplateCount + 1 <= userInfo.value.upTemplateMax){
        return true;
    } else {
        ElMessage.error('新建失败!您当前可自定义模版剩余数为0!');
        return false;
    }
}