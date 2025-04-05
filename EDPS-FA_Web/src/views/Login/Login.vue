<template>
  <!-- 顶部 -->
  <div class="loginhead">
    <img src="http://medseeker.genemed.tech/ask/report_css/logo.jpg" alt=""
      style="width: 200px; margin-top: 2%; margin-left: 2%; background-color: white;">
    <el-dropdown class="selectLang">
      <el-button :circle="true" class="rounded-button">
        <svg t="1727512050798" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="4395" width="32" height="32">
          <path
            d="M534.987755 908.538776l18.808163-1.567347c1.567347 0 3.134694-0.522449 5.22449-0.522449 4.702041-0.522449 9.404082-1.044898 14.106123-2.089796 84.636735-13.061224 162.481633-52.767347 223.085714-115.461225 48.587755-50.155102 82.546939-110.759184 99.787755-176.587755 0-0.522449 0-1.044898 0.522449-1.567347 1.567347-5.22449 2.612245-10.971429 3.657143-16.718367 0-1.044898 0.522449-2.089796 0.522449-3.134694 1.044898-5.22449 2.089796-10.44898 2.612245-15.15102 0-1.567347 0.522449-2.612245 0.522449-4.179592 0.522449-4.702041 1.044898-9.404082 2.089796-14.628572 0-1.567347 0.522449-3.657143 0.522449-5.22449 0.522449-4.702041 1.044898-9.404082 1.044898-14.628571 0-1.567347 0.522449-3.657143 0.522449-5.22449 0.522449-6.791837 0.522449-13.061224 0.522449-19.853061s0-13.583673-0.522449-19.853061c0-1.567347-0.522449-3.657143-0.522449-5.22449-0.522449-4.702041-0.522449-9.926531-1.044898-14.628571 0-1.567347-0.522449-3.657143-0.522449-5.22449-0.522449-4.702041-1.044898-9.404082-2.089796-14.628572 0-1.567347-0.522449-2.612245-0.522449-4.179592-1.044898-5.22449-1.567347-10.44898-2.612245-15.15102 0-1.044898-0.522449-2.089796-0.522449-3.134694-1.044898-5.746939-2.612245-10.971429-3.657143-16.718367 0-0.522449 0-1.044898-0.522449-1.567347-17.240816-65.828571-51.2-126.955102-99.787755-176.587755-61.126531-62.693878-138.44898-102.4-223.085714-115.461225-4.702041-0.522449-9.404082-1.044898-14.106123-2.089796-1.567347 0-3.134694-0.522449-5.22449-0.522449l-18.808163-1.567347h-0.522449c-6.269388-0.522449-13.061224-0.522449-19.330612-0.522448h-10.971429c-6.269388 0-13.061224 0.522449-19.330612 1.044897h-0.522449l-18.808163 1.567347h-1.567347c-5.746939 0.522449-11.493878 1.567347-17.240816 2.612245-1.044898 0-2.612245 0.522449-3.657143 0.522449-4.702041 1.044898-9.926531 1.567347-14.628572 2.612245-2.612245 0.522449-4.702041 1.044898-6.791836 1.567347-3.657143 1.044898-7.314286 1.567347-10.971429 2.612245l-10.971429 3.134694c-2.089796 0.522449-4.179592 1.044898-6.791836 2.089796-5.22449 1.567347-10.44898 3.657143-15.67347 5.22449-0.522449 0-1.044898 0.522449-1.567347 0.522449-55.379592 20.897959-106.057143 53.289796-147.853061 96.653061-48.587755 50.155102-82.546939 110.759184-99.787755 176.587755 0 0.522449 0 1.044898-0.522449 1.567347-1.567347 5.22449-2.612245 10.971429-3.657143 16.718367 0 1.044898-0.522449 2.089796-0.522449 3.134694-1.044898 5.22449-2.089796 10.44898-2.612245 15.15102 0 1.567347-0.522449 2.612245-0.522449 4.179592-0.522449 4.702041-1.044898 9.404082-2.089796 14.628572 0 1.567347-0.522449 3.657143-0.522449 5.22449-0.522449 4.702041-1.044898 9.404082-1.044898 14.628571 0 1.567347-0.522449 3.657143-0.522449 5.22449-1.044898 6.269388-1.044898 13.061224-1.044897 19.853061s0 13.583673 0.522448 19.853061c0 1.567347 0.522449 3.657143 0.522449 5.22449 0.522449 4.702041 0.522449 9.926531 1.044898 14.628571 0 1.567347 0.522449 3.657143 0.522449 5.22449 0.522449 4.702041 1.044898 9.404082 2.089796 14.628572 0 1.567347 0.522449 2.612245 0.522449 4.179592 1.044898 5.22449 1.567347 10.44898 2.612245 15.15102 0 1.044898 0.522449 2.089796 0.522449 3.134694 1.044898 5.746939 2.612245 10.971429 3.657143 16.718367 0 0.522449 0 1.044898 0.522449 1.567347 17.240816 65.828571 51.2 126.955102 99.787755 176.587755 42.318367 43.363265 92.473469 75.755102 147.853061 96.130612 0.522449 0 1.567347 0.522449 2.089796 0.522449 5.22449 2.089796 10.44898 3.657143 15.151021 5.22449 2.089796 0.522449 4.702041 1.567347 6.791836 2.089796l10.971429 3.134694c3.657143 1.044898 7.314286 2.089796 10.971429 2.612245 2.089796 0.522449 4.702041 1.044898 6.791836 1.567347 4.702041 1.044898 9.926531 2.089796 14.628572 2.612245 1.044898 0 2.612245 0.522449 3.657143 0.522449 5.746939 1.044898 11.493878 1.567347 17.240816 2.612245h1.567347l18.808163 1.567347h0.522449c6.269388 0.522449 12.538776 0.522449 19.330612 1.044898h11.493878c6.269388 0 13.061224 0 19.330612-0.522449l0.522449 0.522449z"
            fill="#7BD4EF" p-id="4396"></path>
          <path
            d="M447.216327 859.428571c-3.134694-0.522449-6.269388-1.044898-8.881633-1.567347-4.179592-1.044898-8.881633-2.089796-13.061225-3.134693-1.567347-0.522449-3.134694-1.044898-4.70204-1.044898-3.657143-1.044898-7.836735-2.089796-11.493878-3.134694-1.044898-0.522449-2.089796-0.522449-3.134694-1.044898-49.632653-15.673469-95.085714-42.318367-132.702041-76.8 24.555102-22.987755 52.244898-41.795918 82.546939-56.42449 22.987755 52.767347 55.379592 101.877551 94.563265 144.195918-1.044898-1.044898-2.089796-1.044898-3.134693-1.044898z m-272.718368-242.416326l-4.702041-15.673469c0-0.522449-0.522449-1.044898-0.522449-1.567347-1.044898-4.702041-2.089796-9.926531-3.134693-14.628572 0-1.044898-0.522449-1.567347-0.522449-2.612245-1.044898-4.702041-1.567347-8.881633-2.612245-13.583673 0-1.567347-0.522449-2.612245-0.522449-4.179592l-1.567347-12.538776c0-1.567347-0.522449-3.134694-0.522449-4.70204-0.522449-4.179592-0.522449-8.359184-1.044898-13.061225v-3.134694h154.644898c2.089796 50.155102 10.971429 99.787755 27.689796 146.808164-35.004082 16.718367-66.873469 38.661224-95.608164 65.306122-31.869388-36.04898-56.42449-78.889796-71.57551-126.432653z m-14.106122-140.538776c0-1.567347 0.522449-3.134694 0.522449-4.70204l1.567347-12.538776c0-1.567347 0.522449-2.612245 0.522449-4.179592 0.522449-4.702041 1.567347-8.881633 2.612245-13.583673 0-1.044898 0.522449-2.089796 0.522449-2.612245 1.044898-4.702041 2.089796-9.926531 3.134693-14.628572 0-0.522449 0.522449-1.044898 0.522449-1.567347 1.567347-5.22449 2.612245-10.44898 4.702041-15.673469C189.64898 359.444898 214.204082 316.604082 245.55102 280.032653c28.734694 26.644898 60.604082 48.065306 95.608164 65.306123-16.195918 47.542857-25.6 96.653061-27.689796 146.808163H159.346939v-3.134694c0.522449-4.179592 0.522449-8.359184 1.044898-12.538776z m245.55102-301.453061c1.044898-0.522449 2.089796-0.522449 3.134694-1.044898 4.179592-1.044898 7.836735-2.089796 12.016327-3.657143 1.567347-0.522449 2.612245-1.044898 4.179591-1.044898 4.179592-1.044898 8.881633-2.089796 13.583674-3.134693 3.134694-0.522449 5.746939-1.044898 8.881633-1.567347 1.044898 0 2.089796-0.522449 3.134693-0.522449-40.228571 42.840816-72.097959 91.428571-95.608163 144.718367-29.779592-14.628571-57.469388-33.959184-82.546939-56.42449 38.138776-35.004082 83.069388-61.64898 133.22449-77.322449z m176.587755-8.881632h1.044898c63.738776 13.061224 120.685714 43.363265 167.183674 85.681632-26.122449 24.032653-54.857143 43.363265-86.204082 58.514286-23.510204-54.334694-55.902041-103.967347-96.653061-147.330612 5.22449 1.044898 9.926531 2.089796 14.628571 3.134694z m266.971429 240.848979l4.702041 15.673469c0 0.522449 0.522449 1.044898 0.522449 1.567347 1.044898 4.702041 2.089796 9.926531 3.134693 14.628572 0 1.044898 0.522449 1.567347 0.522449 2.612245 1.044898 4.702041 1.567347 8.881633 2.612245 13.583673 0 1.567347 0.522449 2.612245 0.522449 4.179592l1.567347 12.538776c0 1.567347 0.522449 3.134694 0.522449 4.70204 0.522449 4.179592 0.522449 8.359184 1.044898 13.061225v3.134694H705.306122c-2.089796-49.632653-10.971429-98.220408-26.644898-145.240817 36.571429-17.240816 70.008163-39.706122 99.787756-67.395918 31.346939 36.571429 55.902041 79.412245 71.053061 126.955102z m14.106122 140.538776c0 1.567347-0.522449 3.134694-0.522449 4.70204l-1.567347 12.538776c0 1.567347-0.522449 2.612245-0.522449 4.179592-0.522449 4.702041-1.567347 8.881633-2.612245 13.583673 0 1.044898-0.522449 2.089796-0.522449 2.612245-1.044898 4.702041-2.089796 9.926531-3.134693 14.628572 0 0.522449-0.522449 1.044898-0.522449 1.567347-1.567347 5.22449-2.612245 10.44898-4.702041 15.673469-14.628571 47.542857-39.183673 90.383673-71.053061 126.955102-29.779592-27.689796-63.216327-50.155102-99.787756-67.395918 16.195918-47.020408 25.077551-95.608163 26.644898-145.240817h159.346939v3.134694c-0.522449 4.702041-0.522449 8.881633-1.044898 13.061225z m-221.518367 114.416326c-35.526531-12.538776-72.620408-19.853061-110.759184-21.420408v-108.669388h134.269388c-1.044898 44.408163-9.404082 87.771429-23.510204 130.089796z m-110.236735-169.795918V384c37.616327-2.089796 74.710204-8.881633 110.759184-21.420408 14.106122 41.795918 21.942857 85.681633 24.032653 130.089796h-134.791837z m0-147.330612V182.334694c40.75102 41.273469 73.665306 90.383673 96.653061 143.673469-31.346939 10.44898-63.738776 16.718367-96.653061 18.808164z m-39.706122 0c-34.481633-2.089796-67.918367-8.881633-100.310204-20.89796 24.032653-54.857143 57.991837-104.489796 100.832653-146.808163V344.816327z m-114.938776 15.673469c37.093878 13.583673 75.232653 21.420408 114.938776 22.987755v108.669388H353.17551c1.567347-44.930612 9.926531-88.816327 24.032653-131.657143z m114.938776 171.363265v108.669388c-39.706122 2.089796-77.844898 9.926531-114.938776 22.987755-14.628571-42.318367-22.465306-86.726531-24.555102-131.657143h139.493878z m0 147.330612v167.183674c-42.318367-41.795918-76.8-91.95102-100.310204-146.285714 32.391837-12.016327 65.828571-18.808163 100.310204-20.89796z m39.706122 0c32.914286 1.567347 65.306122 8.359184 96.653061 18.808164-22.987755 53.289796-55.902041 101.877551-96.653061 143.673469V679.183673z m132.702041 33.959184c31.346939 15.15102 60.604082 34.481633 86.204082 58.514286-42.318367 38.661224-93.518367 67.395918-150.465306 82.02449-5.22449 1.567347-10.971429 2.612245-16.195919 3.657143-0.522449 0-1.044898 0-1.044898 0.522448-4.702041 1.044898-9.926531 2.089796-14.628571 2.612245 39.706122-42.840816 72.620408-92.995918 96.130612-147.330612z"
            fill="#DCF8FF" p-id="4397"></path>
        </svg>
        {{ $t('messages.language') }}<el-icon class="el-icon--right"></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item style="font-size: 18px; font-weight: bolder;"
            @click="changeLange('zh')">中文</el-dropdown-item>
          <el-dropdown-item style="font-size: 18px; font-weight: bolder;"
            @click="changeLange('en')">English</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
  <el-divider />
  <!-- 轮播图和二维码 -->
  <div style="display: flex; margin-left: 14%; flex: 1;">
    <!-- 轮播图 -->
    <div class="carousel">
      <el-carousel height="600px" :interval="7000">
        <el-carousel-item v-for="(image, index) in item" :key="index" class="carousel-item">
          <img :src="image" class="carousel-image">
        </el-carousel-item>
      </el-carousel>
    </div>
    <!-- 二维码 -->
    <div style="margin-left: 4%;">
      <el-card class="custom-card">
        <el-tabs v-model="activeName" type="card">
          <el-tab-pane :label="$t('messages.logContent6')" name="second">
            <div class="logincontain">
              <img src="http://medseeker.genemed.tech/ask/report_css/medseeker.jpg" alt=""
                style="width: 300px; margin-top: 10px; margin-left: 20px; margin-bottom: 20px;">
              <el-space direction="vertical" style="margin-top: 20px;">
                <el-button type="primary" @click="foreignUser" size="large"
                style="font-size: larger; font-weight: 20px; color: white; width: 300px;">{{$t('messages.logContent7') }}</el-button>
                <!-- <el-button type="primary" size="large" @click="foreignUser"
                  style="font-size: larger; font-weight: 20px; color: black">{{
                    $t('messages.logContent4') }}</el-button> -->
                <!-- <el-text style="color: black; margin-top: 5%; " size="large" tag="b">{{ $t('messages.logContent3')
                  }}</el-text> -->
                  
              </el-space>
            </div>
          </el-tab-pane>
          <el-tab-pane style="font-size: 20px;" :label="$t('messages.logContent5')" name="first">
            <div class="logincontain">
              <img src="http://medseeker.genemed.tech/ask/report_css/medseeker.jpg" alt=""
                style="width: 300px; margin-top: 10px; margin-left: 20px; margin-bottom: 20px;">
              <QrcodeVue :value="qrCode" :size="200"></QrcodeVue>
              <el-space direction="vertical" style="margin-top: 20px;">
                <el-text style="color: black; font-size: large;" tag="b">{{ $t('messages.logContent1') }}</el-text>
                <!-- <el-text style="color: black; font-size: large;">{{ $t('messages.logContent2') }}</el-text> -->
              </el-space>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>

  <!-- 底部 -->
  <div class="loginfooter">
    <div style="text-align: center; justify-content: center; align-items: center; margin-bottom: 5px; display: flex;">
      <div style="display: flex; align-items: center; gap: 20px;">
        <svg t="1733394761950" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="6789" width="25" height="25">
          <path
            d="M767.818667 409.173333C867.338667 444.266667 938.666667 539.136 938.666667 650.666667c0 42.709333-10.496 83.978667-30.261334 120.842666-1.792 3.338667-4.992 8.928-9.696 16.96l14.613334 53.557334c6.506667 23.893333-15.402667 45.813333-39.296 39.296l-53.642667-14.634667-6.229333 3.669333A254.933333 254.933333 0 0 1 682.666667 906.666667c-77.994667 0-147.84-34.88-194.805334-89.888a352.608 352.608 0 0 1-56.64 4.554666c-63.338667 0-124.266667-16.853333-177.472-48.298666-1.834667-1.088-6.410667-3.733333-13.632-7.893334l-80.544 21.653334c-23.914667 6.432-45.76-15.573333-39.146666-39.434667l21.792-78.752a961.205333 961.205333 0 0 1-15.904-27.317333A336.384 336.384 0 0 1 85.333333 480c0-188.618667 154.965333-341.333333 345.888-341.333333 159.914667 0 297.984 108.010667 335.818667 259.296 0.949333 3.765333 1.173333 7.552 0.778667 11.2z m-68.106667-13.952C662.88 282.037333 555.178667 202.666667 431.221333 202.666667 275.434667 202.666667 149.333333 326.933333 149.333333 480c0 46.272 11.498667 90.837333 33.194667 130.698667 2.88 5.290667 10.176 17.706667 21.621333 36.746666a32 32 0 0 1 3.413334 25.013334l-10.517334 37.994666 39.232-10.549333a32 32 0 0 1 24.234667 3.146667c14.272 8.192 22.773333 13.098667 25.802667 14.890666A283.882667 283.882667 0 0 0 431.221333 757.333333c6.154667 0 12.288-0.192 18.389334-0.576A255.061333 255.061333 0 0 1 426.666667 650.666667c0-141.386667 114.613333-256 256-256 5.728 0 11.413333 0.192 17.045333 0.554666z m133.706667 397.056a32 32 0 0 1 3.338666-24.725333 996.672 996.672 0 0 0 15.242667-26.293333A190.997333 190.997333 0 0 0 874.666667 650.666667c0-106.037333-85.962667-192-192-192s-192 85.962667-192 192 85.962667 192 192 192a190.933333 190.933333 0 0 0 98.570666-27.2c2.208-1.322667 8.288-4.874667 18.517334-10.837334a32 32 0 0 1 24.522666-3.210666l12.565334 3.424-3.424-12.565334zM330.666667 426.666667a42.666667 42.666667 0 1 1 0-85.333334 42.666667 42.666667 0 0 1 0 85.333334z m192 0a42.666667 42.666667 0 1 1 0-85.333334 42.666667 42.666667 0 0 1 0 85.333334z m85.333333 202.666666a32 32 0 1 1 0-64 32 32 0 0 1 0 64z m149.333333 0a32 32 0 1 1 0-64 32 32 0 0 1 0 64z"
            fill="#e6e6e6" p-id="6790"></path>
        </svg>
        <img style="width: 50px;" src="https://medseeker.genemed.tech/ask/report_css/kefu.png" alt="">
      </div>
      <div style="display: flex; align-items: center; gap: 10px; margin-left: 50px;">
        <el-icon :size="25">
          <Message />
        </el-icon>
        <el-text style="color: white;" size="large">3026045936@qq.com</el-text>
      </div>
    </div>
    <div style="text-align: center;">
      <el-text size="large" style="color: white;">
        Copyright©NCRCGD 2023 National Clinical Research Center for Geriatric Disorders, Xiangya Hospital, Central South
        University, Changsha Hunan, P.R. China
      </el-text>
    </div>
    <div style="text-align: center; margin-top: 5px">
      <el-text size="large" style="color: white;">
        Copyright©Hunan University of Technology, Zhuzhou Hunan, P.R. China
      </el-text>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import QrcodeVue from 'qrcode.vue';
import { getQrCode, isScanQrcode } from '../../api/index';
import { useRouter } from 'vue-router';
import { useUserStore } from '../../store/user';
import { useI18n } from "vue-i18n";
import { ElMessage } from "element-plus";
const { t } = useI18n();
// 激活登陆方式
let activeName = ref('second')
// 二维码
const qrCode = ref<string | undefined>();
// 校验用户是否扫码
const wechat_flag = ref<string>('');
// 路由器
const router = useRouter();
// 定时器
let loopTimer: number | null = null;
//轮播图地址
let item = ref(['https://medseeker.genemed.tech/ask/report_css/helpimg/1lunbo.png',
  'https://medseeker.genemed.tech/ask/report_css/helpimg/2lunbo.png',
  'https://medseeker.genemed.tech/ask/report_css/helpimg/3lunbo.png']);
// 使用userStore
const userStore = useUserStore();
// debugger
// 获取二维码
const QrCode = () => {
  // 1.从后端获取二维码
  getQrCode()
    .then((res) => {
      // console.log('res:', res.data.url);
      qrCode.value = res.data.url;
      wechat_flag.value = res.data.code;
    })
    .catch((err) => {
      console.log(err);
    });
  // 2.轮询判断用户是否扫码
  userIsScanQRcodeByLoop();
};

// 判断用户是否扫码
const userIsScanQRcodeByLoop = () => {
  // 1.设置定时器
  loopTimer = window.setInterval(() => {
    // 2.轮询函数
    const p = isScanQrcode(wechat_flag.value);
    // console.log('p:', p);
    p.then((res) => {
      if (res.code === 0) {
        // 用户已扫码，停止轮询
        if (loopTimer !== null) {
          clearInterval(loopTimer);
          loopTimer = null;
        }
        // 3.解构返回的数据
        let { openId, nickName, headImgurl, sex, id, createTime, updateTime } = res.data.user;
        let { vipId, vipCreateTime, vipEndTime, vipType } = res.data.userTypeList[0];
        // 4.将openId、nickName、headImgurl、sex添加到pinia状态管理库
        userStore.setInfo(id, nickName, headImgurl, sex, openId, createTime, updateTime, vipId, vipCreateTime, vipEndTime, vipType);
        // console.log(userStore.userId, userStore.nickName, userStore.headImg, userStore.sex);
        // 5.设置sessionStorage
        let user = {
          id,
          openId,
          nickName,
          headImgurl,
          sex,
          createTime,
          updateTime,
          vipId,
          vipCreateTime,
          vipEndTime,
          vipType
        }
        sessionStorage.setItem("user", JSON.stringify(user));
        // 6.设置localStorage
        localStorage.setItem("isAuthenticated", "1");
        localStorage.setItem("user", JSON.stringify(user));
        console.log(sessionStorage.getItem("user"));
        // 7.路由跳转
        router.push({ name: "redirect" });
      }
    }).catch((err) => {
      console.log(err);
    });
  }, 5000);
};

//如果为国外ip、香港、台湾ip
let ip = ref(false);

// 国外ip、香港ip、台湾ip用户使用
const foreignUser = () => {
  // 注意正式端id100042
  localStorage.setItem("user", JSON.stringify({ id: 100042 }));
  // localStorage.setItem("user", JSON.stringify({ id: 100005 }));
  userStore.setInfo(JSON.parse(localStorage.getItem('user') || '{}').id, JSON.parse(localStorage.getItem('user') || '{}').nickName,
    JSON.parse(localStorage.getItem('user') || '{}').headImgurl, JSON.parse(localStorage.getItem('user') || '{}').sex, JSON.parse(localStorage.getItem('user') || '{}').openId, JSON.parse(localStorage.getItem('user') || '{}').createTime,
    JSON.parse(localStorage.getItem('user') || '{}').updateTime, JSON.parse(localStorage.getItem('user') || '{}').vipId, JSON.parse(localStorage.getItem('user') || '{}').vipCreateTime, JSON.parse(localStorage.getItem('user') || '{}').vipEndTime, JSON.parse(localStorage.getItem('user') || '{}').vipType);
  localStorage.setItem("isAuthenticated", "1")
  router.push({ name: "redirect" });
}

onMounted(() => {
  QrCode();
  // ip判断
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(() => {
      // activeName.value = 'second';
      ip.value = true;
    })
    .catch(() => {
      // activeName.value = 'first';
      ip.value = false;
    });
});

onUnmounted(() => {
  if (loopTimer !== null) {
    clearInterval(loopTimer);
  }
});

// 切换语言
const { locale } = useI18n()
const changeLange = (lang: string) => {
  locale.value = lang;
  localStorage.setItem('lang', lang);
  ElMessage.success(t('messages.mes_login_swaplang'));
}

</script>

<style scoped>
.loginhead {
  margin-left: 2%;
}

.selectLang {
  margin-top: 2%;
  margin-right: 4%;
  float: right;
}

.rounded-button {
  width: 120px;
  height: 40px;
  font-size: large;
  font-weight: bold;
  border-radius: 20px;
  padding: 1px 1px;
}

/* 轮播图 */
.carousel {
  width: 60%;
}

/* 轮播图中的图片 */
.carousel-image {
  max-width: 95%;
  max-height: 95%;
  margin-bottom: 2%;
}

.logincontain {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.logincontain h1 {
  color: gray;
}

.custom-card {
  margin-top: 10%;
  width: 450px;
  height: 475px;
  border-radius: 25px;
}

.loginfooter {
  position: fixed;
  padding-top: 1%;
  padding-bottom: 30px;
  /* 固定定位 */
  bottom: 0;
  /* 距离底部为 0 */
  left: 0;
  /* 距离左侧为 0 */
  width: 100%;
  /* 占满整个宽度 */
  font-size: 14px;
  color: #bbb;
  font-weight: 400;
  box-sizing: border-box;
  background-color: #001428;
  text-align: center;
}

.el-login-footer {
  position: fixed;
  line-height: 1em;
  bottom: 0;
  width: 100%;
  text-align: center;
  background-color: #2e2e40;
  color: #fff;
  font-family: Arial;
  height: 100px;
}

.demonstration {
  color: var(--el-text-color-secondary);
}

.carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

/* 登陆卡片选择器样式 */
.el-menu-selection {
  display: flex;
  justify-content: center;
}
</style>