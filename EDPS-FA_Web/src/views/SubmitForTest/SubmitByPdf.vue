<template  >
  <div class="input-container">
    <div class="tip-text">
      <span>（<span style="color: red">*</span>{{ $t('messages.tips3') }} ）</span>
    </div>
    <el-upload
      drag
      class="custom-upload"
      action=""
      :before-upload="beforeUpload"
      :limit="1"
      :http-request="uploadUrl"
      v-model:file-list="fileList"
    >
      <i class="el-icon-upload">
        <el-icon size="30px"><UploadFilled /></el-icon>
      </i>
      <div class="el-upload__text">{{ $t('messages.tips4') }}<em>{{ $t('messages.tips5') }}</em></div>
      <div class="el-upload__tip" slot="tip">{{ $t('messages.tips7') }}</div>
    </el-upload>

    <div style="margin-right: 200px;">
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
      <el-button class="submit-button" type="primary" @click="handleUpload">
        {{ $t('messages.submit') }}
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as JSZip from "jszip";
import { checkAllTemplateByUserId, getTokenByQiniu, insertPdfToDataBase } from "../../api/index";
import * as qiniu from "qiniu-js";
import { checkInfo } from "../../utils/checkInfo"
import { ElMessage, ElLoading  } from "element-plus";
import { UploadFilled } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { useI18n } from 'vue-i18n'; 
const { t } = useI18n();
// 显示上传文件列表
let fileList = ref([]);
// 文件数据
const filesArray = ref<{ name: string; content: Blob }[]>([]);

// 用户id
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;

// 用于绑定选中的模板Id 默认系统模板
const selectedTemplateId = ref('002');

// 保存大模板信息
const bigTemp = ref<Array<{ id: string; templateName: string }>>([]);

// 路由跳转
const router = useRouter();



// 获取所有大模板信息
onMounted(async () => {
  try {
    const res = await checkAllTemplateByUserId(userId);
    bigTemp.value = res.data;
  } catch (error) {
    console.log(error);
  }
});
// 
function uploadUrl(){

}

// 上传之前的检查
async function beforeUpload(file: Blob) {
  try {
    let processedFilesArray;
    if (isZipFile(file)) {
      processedFilesArray = await readAndUnzip(file);
      if(processedFilesArray.length > 10 || processedFilesArray.reduce((total, file)=>{
        return total + file.content.size;
      }, 0) > 1024*1024*100 || processedFilesArray.some((file)=>file.content.size > 1024*1024*20)){
        // ElMessage.error("压缩包文件数量超过限制、解压文件大于100M、解压后存在有pdf文件大于10M！");
        ElMessage.error(t('messages.message_pdf_file_out_limit'));
        fileList.value = []; // 清空文件列表
        return Promise.reject();
      }
      else {
        filesArray.value = processedFilesArray;
      }
      // console.log("压缩包中的文件数量：", processedFilesArray.length);
    } else {
      processedFilesArray = [{ name: (file as any).name || "unknown", content: file }];
      if(processedFilesArray[0].content.size > 20*1024*1024){
        ElMessage.error(`${processedFilesArray[0].name} more than 10M！`);
        fileList.value = []; // 清空文件列表
        return Promise.reject();
      } else {
        filesArray.value = processedFilesArray;
      }
      // console.log("非压缩文件上传");
    }
    return Promise.resolve();
  } catch (error) {
    // console.error("文件处理失败：", error);
    return Promise.reject();
  }
}

// 读取压缩文件
/*
function readAndUnzip(file: Blob): Promise<{ name: string; content: Blob }[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = async (event) => {
      try {
        const zip = await JSZip.loadAsync(event.target.result);
        const filePromises = Object.keys(zip.files).map(async (fileName) => {
          const fileData = await zip.files[fileName].async("blob");
          return { name: fileName, content: fileData };
        });
        const filesArray = await Promise.all(filePromises);
        resolve(filesArray);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = () => {
      reject(reader.error);
    };
  });
}
*/
// 读取压缩文件
function readAndUnzip(file: Blob): Promise<{ name: string; content: Blob }[]> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = async (event) => {
      try {
        const zip = await JSZip.loadAsync(event.target.result);
        const filesArray = await extractFiles(zip);
        resolve(filesArray);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = () => {
      reject(reader.error);
    };
  });
}

// 递归提取文件
async function extractFiles(zip: JSZip): Promise<{ name: string; content: Blob }[]> {
  const files: { name: string; content: Blob }[] = [];

  for (const fileName in zip.files) {
    const file = zip.files[fileName];
    if (!file.dir) { // 如果不是目录，读取文件
      const fileData = await file.async("blob");
      const baseName = fileName.split('/').pop(); // 获取文件的基本名称
      files.push({ name: baseName, content: fileData });
    }
  }

  return files;
}


// 判断是否为压缩文件
function isZipFile(file: Blob): boolean {
  const zipMimeType = "application/zip";
  const zipExtensions = [".zip"];
  // 检查 MIME 类型
  if (file.type === zipMimeType) {
    return true;
  }
  // 检查扩展名
  const fileName = (file as any).name || "";
  const fileExtension = fileName.slice(fileName.lastIndexOf(".")).toLowerCase();
  if (zipExtensions.includes(fileExtension)) {
    return true;
  }
  return false;
}

// 点击提交检测按钮
async function handleUpload() {
  if (filesArray.value.length === 0) {
    // ElMessage.error("请先上传文件！");
    ElMessage.error(t('messages.message_pdf_upload'));
    return;
  }
  try {
    await uploadFile(filesArray.value);
  } catch (error) {
    // ElMessage.error("文件上传失败！");
    ElMessage.error(t('messages.mes_pdf_file_err'));
  }
}

// 生成 年/月/日 时间格式
function getFormattedDate() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}${month}${day}`;
}

// 生成随机数
function generateRandomNumber(length: number) {
  let result = "";
  for (let i = 0; i < length; i++) {
    result += Math.floor(Math.random() * 10).toString();
  }
  return result;
}

// 文件上传到七牛云前处理文件格式，获取七牛云token
async function uploadFile(filesArray: { name: string; content: Blob }[]) {
  if (selectedTemplateId.value === null) {
    // ElMessage.error("请选择匹配模板！");
    ElMessage.error(t('messages.message_pdf_select_temp'));
  } else {
    // console.log("filesArray", filesArray);
    if(!await checkInfo(filesArray.length, userId)){
      return ;
    }
    // console.log("filesArray", filesArray);
    filesArray = filesArray.map(file => ({
      ...file,
      name: file.name.replace(/\.pdf$/, '')
    }));
    // console.log("filesArray", filesArray);
    // 获取上传token
    const uploadToken = await getTokenByQiniu();
    // console.log("uploadToken", uploadToken);
    const config = {
      useCdnDomain: true,
      region: qiniu.region.z2,
      forceDirect: true,
    };
    const uploadPromises = filesArray.map(file => {
      // 生成时间格式
      const dateStr = getFormattedDate();
      // 生成随机数
      const randomNum = generateRandomNumber(32);
      // 指定文件路径
      const filePath = `pdf/${dateStr}/${randomNum}/${randomNum}`;
      // console.log("filePath", filePath);
      // 上传到七牛云
      return uploadSingleFile(file, uploadToken.data, config, filePath)
        .then(() => {
          const url = 'http://ask.genemed.tech/' + filePath + `_${file.name}`;
          const selected = bigTemp.value.find(item => item.id === selectedTemplateId.value);
          // 将数据插入到数据库中
          return insertPdfToDataBase(userId, selectedTemplateId.value, selected.templateName,file.name, url, randomNum);
        });
    });
    try {
      await Promise.all(uploadPromises);
      // console.log("所有文件上传并插入数据库成功");
      // 所有文件上传并插入数据库成功后导航到result页面
      router.push({ name: "result" });
    } catch (error) {
      // ElMessage.error("文件上传或插入数据库失败，请重试！");
      ElMessage.error(t('messages.message_pdf_error'));
    }
  }
  
};

// 将文件上传到七牛云
const uploadSingleFile = (file: any, uploadToken: string, config: any, filePath: string) => {
  const { name, content } = file;
  const key = `${filePath}_${name}`; // 指定文件路径
  const putExtra = {
    fname: name,
    params: {},
    mimeType: ["application/pdf"], // 可选项，确保只上传PDF文件
  };
  // 加载动画
  const loading = ElLoading.service({
    lock: true,
    text: '正在上传中...',
    background: 'rgba(0, 0, 0, 0.7)',
  });
  const observer = {
    next() {
      // console.log("进度:", res.total.percent);
    },
    error() {
      // console.error("上传失败:", err);
      loading.close();
      ElMessage.error(`文件 ${name} 上传失败！`);
    },
    complete() {
      // console.log("上传成功:", res);
      loading.close();
      ElMessage.success(`文件 ${name} 上传成功！`);
    },
  };
  const observable = qiniu.upload(content, key, uploadToken, putExtra, config);
  return new Promise((resolve, reject) => {
    observable.subscribe({
      next: observer.next,
      error: (err: any) => {
        observer.error();
        reject(err);
      },
      complete: (res: any) => {
        observer.complete();
        resolve(res);
      },
    });
  });
};
</script>

<style scoped>
.custom-upload {
  width: 800px !important;
}
.submit-button {
  width: 300px;
  height: 40px;
  font-size: 20px;
}
.tip-text {
  margin-right: 500px;
  margin-top: 10px;
  text-align: left;
  font-size: 18px;
}
</style>
