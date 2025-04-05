<template>
  <div class="input-container">
    <div class="tip-text">
      <span>（<span style="color: red">*</span>{{ $t('messages.tips1')}}）</span>
      <el-button type="warning" plain @click="exampleInput">{{ $t('messages.clickentersample') }}</el-button>
      <!-- <span>（<span style="color: red">*</span>温馨提示：只能输入10个PMID，每行1个）</span> -->
    </div>
    <el-input v-model="textarea" class="custom-input" :rows="20" type="textarea" placeholder="Please Input PMID" />
    <div class="select-container">
      <span style="color: red;">*</span><el-text type="danger" size="large">{{ $t('messages.templateSelection') }}</el-text>
      <el-select v-model="selectedTemplateId" placeholder="请选择模板" size="large" style="width: 240px">
        <el-option v-for="item in bigTemp" :key="item.id" :label="item.templateName" :value="item.id" />
      </el-select>
      <el-button type="primary" @click="submitForm" class="submit-button">{{ $t('messages.submit') }}</el-button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { PostByPmids, checkAllTemplateByUserId } from "../../api/index";
import { checkInfo } from "../../utils/checkInfo"
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useI18n } from 'vue-i18n'; 
const { t } = useI18n();
//用户id
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 输入框中的数据
const textarea = ref("");
// 用于绑定选中的模板Id 默认系统模板
const selectedTemplateId = ref('002');
// 保存大模板信息
const bigTemp = ref<Array<{ id: string; templateName: string }>>([]);
// 路由跳转
const router = useRouter();

onMounted(async () => {
  try {
    const res = await checkAllTemplateByUserId(userId);
    let { data } = res;
    bigTemp.value = data;
    // console.log("bigTemp", bigTemp.value);
  } catch (error) {
    console.log(error);
  }
});

async function submitForm() {
  // 1.判断输入框是否输入数据
  if (textarea.value.length && selectedTemplateId.value !== null) {
    const lines = textarea.value
      .split("\n")
      .map((line) => line.trim()) // 去除首尾空格
      .filter((line) => line); // 过滤为空的字符串
    // 根据selectedTemplateId查找数组中的大模板名
    const selected = bigTemp.value.find(item => item.id === selectedTemplateId.value);
    // 判断是否剩余可检测数
    if (await checkInfo(lines.length, userId)) {
      PostByPmids(lines, selectedTemplateId.value, selected.templateName, userId);
      ElMessage.success(t('messages.message_file_success'));
      router.push({ name: "result" });
    }
  } else {
    // 3.若未输入数据或选择模板则提示输入
    ElMessage.error(t('messages.message_pmid_template'));
  }
}
// 输入样例函数
const pmids=['38469092', '34247825', '34115115', '27048506'];



let index = 0;
const exampleInput = () =>{
  if (textarea) {
      textarea.value += (textarea.value ? '\n' : '') + pmids[index];
      index = (index + 1) % pmids.length;
  }
};
</script>
 
<style scoped>
.input-container {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
}

.custom-input {
  width: 800px;
  font-size: 20px;
  color: black;
}

.submit-button {
  width: 300px;
  height: 40px;
  font-size: 20px;
}

.tip-text {
  margin: 10px 460px 10px 0px;
  font-size: 18px;
}

.select-container {
  display: flex;
  align-items: center;
  margin-top: 10px;
  margin-right: 200px;
}
</style>
