<template>
  <div class="input-container" v-loading="loading">
    <div class="tip-text">
      <span
        >（<span style="color: red">*</span
        >{{ $t('messages.tips2') }} ）</span
      >
      <el-button type="warning" plain  @click="downloadExampleFile">{{$t('messages.downloadTemp')}}</el-button>
    </div>
    <div id="upload">
      <el-upload
        drag
        class="custom-upload"
        :action="uploadUrl()"
        :before-upload="beforeUpload"
        :limit="5"
        v-model:file-list="fileList"
      >
        <i class="el-icon-upload"
          ><el-icon size="30px"><UploadFilled /></el-icon
        ></i>
        <div class="el-upload__text">{{ $t('messages.tips4') }}<em>{{ $t('messages.tips5') }}</em></div>
        <div class="el-upload__tip" slot="tip">{{ $t('messages.tips6') }}</div>
      </el-upload>
      <div class="select-container">
      <span style="color: red">*</span><el-text type="danger" size="large">{{ $t('messages.templateSelection') }}</el-text>
      <el-select
        v-model="selectedTemplateId"
        placeholder="请选择模板"
        size="large"
        style="width: 240px"
      >
        <el-option
          v-for="item in bigTemp"
          :key="item.id"
          :label="item.templateName"
          :value="item.id"
        />
      </el-select>
      <el-button class="submit-button" type="primary" @click="uploadFile()"
      >{{ $t('messages.submit') }}</el-button
    >
    </div>
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { transformExcel } from "../../utils/transformExcel";
import { checkInfo } from "../../utils/checkInfo"
import { PostByExcle, checkAllTemplateByUserId } from "../../api/index";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useI18n } from 'vue-i18n'; 
const { t } = useI18n();
let fileList: any[] = [];
// 用户id
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 用于绑定选中的模板Id 默认系统模板
const selectedTemplateId = ref('002');
// 保存大模板信息
const bigTemp = ref<Array<{ id: string; templateName: string }>>([]);
// 解析excel表中的数据
const formatData = ref([]);
let loading = ref(false);
// 路由跳转
const router = useRouter();
onMounted(async () => {
  try {
    const res = await checkAllTemplateByUserId(userId);
    bigTemp.value = res.data;
    // console.log("bigTemp", bigTemp.value);
  } catch (error) {
    console.log(error);
  }
});

async function beforeUpload(file: Blob) {
  // 1. format excel表格数据
  formatData.value = await transformExcel(file);
  // console.log("formatData", formatData.value);
  fileList.push(file);
}

function uploadUrl() {

}

async function uploadFile() {
  loading.value = true;
  // 1. 检查formatData是否有数据
  if (formatData.value.length && selectedTemplateId.value !== null) {
    // params只能传递字符串，JSON.stringify现转字符串，JSON.parse接收再转回
    let pmcidArray = formatData.value.map((item: { PMID: any }) => String(item.PMID));
    // console.log("pmcidArray", pmcidArray);
    // 判断是否剩余可检测数
    if(await checkInfo(pmcidArray.length, userId)){
      const selected = bigTemp.value.find(item => item.id === selectedTemplateId.value);
      await PostByExcle(pmcidArray, selectedTemplateId.value, selected.templateName,userId);
      ElMessage.success(t('messages.message_success'));
      router.push({name:"result"});
    }
  } else {
    ElMessage.error(t('messages.message_file_error'));
  }
  loading.value = false;
}
// 下载模板文件
function downloadExampleFile() {
  window.location.href = "http://medseeker.genemed.tech/downloads/Example.xlsx";
}
</script>

<style scoped>
/* .input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
} */
.custom-upload {
  width: 800px;
}
.submit-button {
  width: 300px;
  height: 40px;
  font-size: 20px;
}
.tip-text {
  /* margin-right: 290px; */
  margin-right: 25%;
  margin-top: 10px;
  text-align: left; /* 设置文本左对齐 */
  font-size: 18px; /* 改变字号为12px */
}
</style>
