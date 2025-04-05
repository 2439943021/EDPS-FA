import { defineStore } from 'pinia';
export const useUserStore = defineStore('user', {
  state(){
    return {
      userId:Number(''),
      userOpenId:'',
      nickName:'',
      headImg:'',
      sex:'',
      createTime:'',
      updateTime:'',
      vipId:'',
      vipCreateTime:'',
      vipEndTime:'',
      vipType:''
    }
  },
  actions:{
    setInfo(id:number, name:string, img:string, sex:string, openId:string,
      createTime:string, updateTime:string, vipId:string, vipCreateTime:string, vipEndTime:string, vipType:string){
      this.userId = id,
      this.userOpenId = openId,
      this.createTime = createTime,
      this.updateTime = updateTime,
      this.nickName = name,
      this.headImg = img,
      this.sex = sex,
      this.vipId = vipId,
      this.vipCreateTime = vipCreateTime,
      this.vipEndTime = vipEndTime,
      this.vipType = vipType
    },
    getInfo(){
      return {
        user:{
          userId:this.userId,
          userOpenId:this.userOpenId,
          nickName:this.nickName,
          headImg:this.headImg,
          sex:this.sex,
          createTime:this.createTime,
          updataTime:this.updateTime,
          vipId:this.vipId,
          vipCreateTime:this.vipCreateTime,
          vipEndTime:this.vipEndTime,
          vipType:this.vipType
        }
      }
    }
  }
});

