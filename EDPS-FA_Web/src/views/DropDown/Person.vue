<template>
  <div>
    <div class="headImage">
      <!-- <el-avatar :size=200 shape="circle" @error="errorHandler" :src=personInfo.headImg /> -->
      <el-avatar
      v-if="personInfo.headImgurl"
      :size="200"
      shape="circle"
      @error="errorHandler"
      :src="personInfo.headImgurl"
    />
    <el-avatar
      v-else
      :size="200"
      shape="circle"
      :src="defaultAvatar"
    />
    </div>
    <div class="person">
      <el-form :model="personInfo" label-width="auto" style="max-width: 600px;">
        <el-form-item :label="$t('messages.PersonCenter_userId')">
          {{ personInfo.id }}
        </el-form-item>
        <el-form-item :label="$t('messages.PersonCenter_userSex')">
          <!-- {{ personInfo.sex }} -->
            {{ sexType }}
        </el-form-item>
        <el-form-item :label="$t('messages.PersonCenter_userName')">
          {{ personInfo.nickName || 'user' }}
        </el-form-item>
        <!-- <el-form-item :label="$t('messages.PersonCenter_vipType')">
          {{ vipType }}
        </el-form-item>
        <el-form-item :label="$t('messages.PersonCenter_vipOpneTime')">
          {{ personInfo.vipCreateTime }}
        </el-form-item>
        <el-form-item :label="$t('messages.PersonCenter_vipEndTime')">
          {{ personInfo.vipEndTime }}
        </el-form-item> -->
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { PersonInfo } from './types';
import { useUserStore } from '../../store/user';
import { ElMessage } from 'element-plus';
// const userStore = useUserStore();
// let personInfo = reactive({
//   id: Number(''),
//   userOpenId: '',
//   nickName: '',
//   headImg: '',
//   sex: '',
//   createTime: '',
//   updataTime: '',
//   vipId: '',
//   vipCreateTime: '',
//   vipEndTime: '',
//   vipType: '',
// })

import { useI18n } from 'vue-i18n'; 
const { t } = useI18n();
let personInfo = ref(<PersonInfo>{});
// 使用计算属性判断不同的会员类型
const vipType = computed(() => {
  switch (Number(personInfo.value.vipType)) {
      case 0:
        return t('messages.Ordinary_Member');
      case 1:
        return t('messages.Mega_Member');
      case 2:
        return t('messages.Super_Member');
      default:
        return t('messages.Unknown_Member_Type');
  }
})

// 使用计算属性判断性别
const sexType = computed(() => {
  return personInfo.value.sex === '男'
    ? t('messages.sex_man')  // 翻译“男”
    : t('messages.sex_woman'); // 翻译“女”
});

// 保存修改的昵称
const handleSaveName = (name: string) => {
  console.log("修改后的name:", name);
  ElMessage.success("修改成功!");
}
// 头像链接错误时的回调
const errorHandler = () => true;
// 默认头像
const defaultAvatar = "https://medseeker.genemed.tech/ask/report_css/helpimg/defaultAvatar.jpg"
onMounted(() => {
  personInfo.value = JSON.parse(localStorage.getItem('user'));
  // console.log(personInfo.value);
})
</script>

<style>
.person {
  display: inline-block;
  width: 30%;
  align-items: center;
  margin-left: 10%;
}

.headImage {
  display: inline-block;
  margin-left: 50px;
}
</style>