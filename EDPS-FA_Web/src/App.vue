<template>
  <div id="app">
    <router-view v-if="isLoginPage"></router-view>
    <Home v-else>
      <router-view></router-view>
    </Home>
  </div>
</template>


<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Home from './component/Home.vue';
import { useUserStore } from './store/user';
const route = useRoute();
const isLoginPage = computed(() => route.path === '/login');
// 正式端打包时需要注释下面这条语句
// localStorage.setItem("user", JSON.stringify({id:100005}));
const useStore = useUserStore();
// 从缓存中获取用户信息，放置在pinia中
useStore.setInfo(JSON.parse(localStorage.getItem('user') || '{}').id, JSON.parse(localStorage.getItem('user') || '{}').nickName,
  JSON.parse(localStorage.getItem('user') || '{}').headImgurl, JSON.parse(localStorage.getItem('user') || '{}').sex, JSON.parse(localStorage.getItem('user') || '{}').openId, JSON.parse(localStorage.getItem('user') || '{}').createTime,
  JSON.parse(localStorage.getItem('user') || '{}').updateTime, JSON.parse(localStorage.getItem('user') || '{}').vipId, JSON.parse(localStorage.getItem('user') || '{}').vipCreateTime, JSON.parse(localStorage.getItem('user') || '{}').vipEndTime, JSON.parse(localStorage.getItem('user') || '{}').vipType);
// console.log("pinia的输出:", useStore.getInfo());
</script>

<style>
@import "./assets/css/reset.css";
</style>
