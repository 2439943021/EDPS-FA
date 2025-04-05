<template>
  <div class="input-container">
    <div class="tip-text">
      <span>（<span style="color: red">*</span>温馨提示：最多只能选择20个PDF文件）</span>
    </div>
    <el-upload
      drag
      class="custom-upload"
      action=""
      :before-upload="beforeUpload"
      :limit="1"
      v-model:file-list="fileList"
    >
      <i class="el-icon-upload">
        <el-icon size="30px"><UploadFilled /></el-icon>
      </i>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击添加文件</em>
      </div>
      <div class="el-upload__tip" slot="tip">
        只能上传pdf文件
      </div>
    </el-upload>
    
    <div>      
      <span style="color: red">*</span><el-text type="danger">模板选择</el-text>
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
        点击上传
      </el-button>
    </div>
    
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as JSZip from "jszip";
import { PostByPdfs, checkAllTemplateByUserId } from "../../api/index";
import { ElMessage } from "element-plus";
import { UploadFilled } from '@element-plus/icons-vue';
// 显示上传文件列表
let fileList: any[] = [];
// 文件数据
const filesArray = ref<{ name: string, content: Blob }[]>([]);
// 用户id
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 用于绑定选中的模板ID
const selectedTemplateId = ref(null);
// 保存大模板信息
const bigTemp = ref<Array<{ id: string; templateName: string }>>([]);
// 获取所有大模板信息
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
  try {
    let processedFilesArray;
    if (isZipFile(file)) {
      processedFilesArray = await readAndUnzip(file);
      console.log('压缩包中的文件数量：', processedFilesArray.length);
    } else {
      processedFilesArray = [{ name: (file as any).name || 'unknown', content: file }];
      console.log('非压缩文件上传');
    }

    processedFilesArray.forEach(file => {
      console.log('文件名：', file.name);
      console.log('文件内容：', file.content);
    });

    filesArray.value = processedFilesArray;

    return Promise.resolve();
  } catch (error) {
    console.error('文件处理失败：', error);
    return Promise.reject();
  }
}

function readAndUnzip(file: Blob): Promise<{ name: string, content: Blob }[]> {
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

function isZipFile(file: Blob): boolean {
  const zipMimeType = 'application/zip';
  const zipExtensions = ['.zip'];

  // 检查 MIME 类型
  if (file.type === zipMimeType) {
    return true;
  }

  // 检查扩展名
  const fileName = (file as any).name || '';
  const fileExtension = fileName.slice(fileName.lastIndexOf('.')).toLowerCase();
  if (zipExtensions.includes(fileExtension)) {
    return true;
  }
  return false;
}


async function handleUpload() {
  if (filesArray.value.length === 0) {
    ElMessage.error('请先选择文件！');
    return;
  }
  try {
    await uploadFile(filesArray.value);
  } catch (error) {
    ElMessage.error('文件上传失败！');
  }
}

async function uploadFile(filesArray: { name: string, content: Blob }[]) {
  if(filesArray.length === 0 || selectedTemplateId.value === null){
    ElMessage.error("请上传文件或选择匹配模板！");
  } else{
    console.log("filesArray", filesArray);
    const formData = new FormData();
    filesArray.forEach(file => {
      formData.append("pdfs", file.content, file.name);
    });
    // formData.append("pdfs", filesArray);
    formData.append("userId", userId);
    formData.append("templateBigId", selectedTemplateId.value as unknown as string);
    formData.append("submitType", "03");
    PostByPdfs(formData);
    ElMessage.success("文件上传成功！");
  }
}
</script>

<style scoped>
.input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: calc(100vh - 50px); /* 设置容器的高度为视口高度减去50px */
}
.custom-upload {
  width: 800px !important; /* 设置宽度为400px */
  /* height: 600px !important; 设置高度为400px */
}
.submit-button {
  width: 300px;
  height: 40px;
  /* margin-top: 10px; 将按钮推到容器的底部 */
  /* margin-bottom: 200px; 设置按钮距离容器底部的距离为300px */
}
.tip-text {
  margin: 10px 550px 10px 0px; /* 上右下左*/
  text-align: left; /* 设置文本左对齐 */
  font-size: 12px; /* 改变字号为12px */
}
</style>
