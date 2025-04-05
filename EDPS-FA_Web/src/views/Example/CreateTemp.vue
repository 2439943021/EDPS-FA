<template>
  <div>
    <!-- 大模板中的名称、类型、描述 -->
    <el-form 
      label-width="auto"
      style="position: relative;">
      <div style="width: 600px; ">
        <el-form-item style="">
          <template #label>
            <span style="color: red">*</span> <el-text size="large" tag="b">{{ $t('messages.templateName') }}</el-text>
          </template>
          <el-input style="font-size: 20px;" v-model="form.name"/>
        </el-form-item>
        <el-form-item style="width: 600px">
          <template #label>
            <span style="color: red">*</span> <el-text size="large" tag="b">{{ $t('messages.templatType') }}</el-text>
          </template>
          <!-- <el-select v-model="form.type" placeholder="请选择您的模板类型" style="width: 100%">
            <el-option
              v-for="type in templateType"
              :key="type.value"
              :label="getTemplateType(type.value)?.label"
              :value="type.value"
            />
          </el-select> -->
          <el-select :disabled="true" v-model="form.type" placeholder="请选择您的模板类型" style="width: 100%; font-size: 18px;">
            <el-option
              :key="templateType[0].value"
              :label="getTemplateType(templateType[0].value)?.label"
              :value="templateType[0].value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <template #label>
            <span style="color: red">*</span><el-text size="large" tag="b">{{ $t('messages.templateDesc') }}</el-text>
          </template>
          <el-input style="font-size: 20px;" v-model="form.desc" type="textarea" />
        </el-form-item>
      </div>
      <!-- 文件导入小模板 -->
      <el-divider :style="{ borderColor: '#000000', borderWidth: '1px', align:'center', width:'100%',}" />
      <el-form-item size="large" :label="$t('messages.importFile')">
        <el-upload
        action="" 
        :before-upload="beforeUpload"
        :show-file-list="false"
        :http-request="importFileAddbigTemp"
        accept=".xlsx, .xls"
        >
          <el-button type="info" plain :icon="Upload" style="font-size: large;">
            {{ $t('messages.importFile') }}
          </el-button>
        </el-upload>
      </el-form-item>
      <el-button type="warning" size="large" @click="downloadTemp">{{ $t('messages.downloadTemp') }}</el-button>
      <el-divider :style="{ borderColor: '#000000', borderWidth: '1px', align:'center', width:'100%',}" />
    </el-form>
    <!-- 自定义小模版 -->
    <el-text size="large" tag="b" style="color: black;">{{ $t('messages.customTemplate') }}</el-text>
    <el-row :gutter="20" v-if="smallTempData" style="margin-left: 60px">
      <el-col :span="12" v-for="(item, index) in smallTempData" :key="index">
        <div class="card-container">
          <el-card shadow="always">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="width:200px">
                <el-text size="large" tag="b">{{ item.typeName }}</el-text>
              </div>
              <div class="color-picker-container">
                <el-text size="large" tag="b">Color：</el-text>
                <el-color-picker v-model="item.color"/>
                <!-- <ColorPicker v-model="item.color"/> -->
              </div>
              <div>
                <el-text size="large" tag="b">Enable：</el-text>
                <el-switch
                  size="large"
                  v-model="item.valid"
                  inline-prompt
                  style="margin-right: auto;--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                  active-text="On"
                  inactive-text="Off"
                  active-value="1"
                  inactive-value="0"
                />
              </div>
              <el-button 
                type="danger" 
                circle 
                size="small"
                @click="handleDelete(index)"
                ><el-icon><Delete /></el-icon></el-button>
              </div>
            <div >
              <el-table 
                :data="item.data"
                style="width: 100%; font-size: large; font-weight: bolder;"
                height="240"
                border
                highlight-current-row>
                <el-table-column prop="key" :label="$t('messages.matchEntry')" align="center"></el-table-column>
                <el-table-column prop="value" :label="$t('messages.note')" align="center"></el-table-column>
              </el-table>
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col 
      :span="12" 
      style="
      display: flex; align-items: center; 
      justify-content: center; ">
          <el-button @click="openDialogForm" style=" background-color: transparent; width: 100%; height: 270px; font-size: 18px;" :icon="Plus">
            <el-text size="large">{{ $t('messages.button_add') }}</el-text>
          </el-button>
      </el-col>
    
    </el-row>
    
    <div>
      <el-dialog style="font-weight: bolder;" v-model="dialogFormVisible" :title="$t('messages.customSmallTemplate')" width="500">
        <el-form>
          <el-form-item :label="$t('messages.smallTempName')">
            <el-input style="font-size: 18px;" v-model="smallData.typeName" autocomplete="off" />
          </el-form-item>
          <el-form-item :label="$t('messages.smallTempType')">
            <el-radio-group v-model="smallData.type">
              <el-radio :label="'enum'" size="large">{{ $t('messages.smallTempTypeEnumerate') }}</el-radio>
              <el-radio :label="'regex'" size="large">{{ $t('messages.smallTempTypeRegex') }}</el-radio>
            </el-radio-group>
            <el-button type="primary" style="position: absolute; right: 0;" @click="addNewRow">{{ $t('messages.button_add') }}</el-button>
          </el-form-item>
          <el-table :data="smallData.data" border height="200px" style="width: 100%; font-size: large;">
            <el-table-column :label="$t('messages.matchEntry')" align="center" >
              <template #default="{ row }">
                <div v-if="!row.isNew">{{ row.key }}</div>
                <el-input v-else style="font-size: 18px;" v-model="row.key" placeholder="Match input" />
              </template>
            </el-table-column>
            <el-table-column :label="$t('messages.note')" align="center" >
              <template #default="{ row }">
                <div v-if="!row.isNew">{{ row.value }}</div>
                <el-input v-else style="font-size: 18px;" v-model="row.value" placeholder="Enter info" />
              </template>
            </el-table-column>
            <el-table-column :label="$t('messages.operation')" align="center" width="100">
              <template #default="{ row, $index }">
                <el-button v-if="row.isNew" @click="saveNewRow($index)" type="primary"  plain>{{ $t('messages.button_add') }}</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="cancelDialog">{{ $t('messages.button_quit') }}</el-button>
            <!-- <el-button type="primary" @click="addNewRow">新增</el-button> -->
            <el-button type="success" @click="confirmDialog">{{ $t('messages.button_confirm') }}</el-button>
          </div>
        </template>
      </el-dialog>
    </div>
    <el-button style="float: right; font-size: 18px;" type="success" size="large" @click="transformDataToJson">{{ $t('messages.button_confirm') }}</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { smallDataType, addList, BigSmall, templateBig } from "./types"
import { getTemplateType } from "../../utils/Example/tempDescrip";
import { createTempToJson, importFileBigTemp } from "../../api/index";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Upload, Plus } from '@element-plus/icons-vue';
// import ColorPicker from "./ColorPicker.vue";
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
// 用户ID
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 大模板名称、类型、描述
const form = reactive({
  name: "",
  type: "1",
  desc: "",
  userId:""
});
// 大模板类型
const templateType = [
  { label: 'Private', value: '1' },
]
// 初始化新建小模板数据
let smallData = ref<smallDataType>({
  data: [],
  valid: '1',
  typeName: '',
  color: '#11BE05',
  type:'enum'
});

//小模版数据JSON格式
let add_list = Array<addList>() 
// 大模板的名称、描述、类型、用户id
let template_big_info = <BigSmall>({});
// 大模板JSON数据
let template_big = <Array<templateBig>>([]);

let smallTempData = ref<smallDataType[]>([]);

// 控制对话框变量
const dialogFormVisible = ref(false);

// 路由器
const router = useRouter();

// 点击添加模板打开对话框
const openDialogForm = ()=>{
  dialogFormVisible.value = true;
}

// 关闭对话框并且执行确认操作
const confirmDialog = () => {
  // 设置小模版名不能为空
  if(!smallData.value.typeName){
    // ElMessage.error("模版名不能为空！");
    ElMessage.error(t('messages.mes_tmp_creat_no_name'));
  } else {
    dialogFormVisible.value = false;
    if(smallData.value.data.length !== 0){
      smallTempData.value.push(JSON.parse(JSON.stringify(smallData.value))); // 将一个小模版数据加入到小模版数组中
      smallData.value = { // 清空新增的小模版数据，但保持接口结构
        data: [],
        valid: '',
        typeName: '',
        color: '',
        type:'enum'
      };
    }
  }
  // console.log("smallTempData.value",smallTempData.value);
}

// 关闭对话框
const cancelDialog = ()=>{
  dialogFormVisible.value = false;
}

// 点击添加新行按钮
const addNewRow = () => {
  smallData.value.data.unshift({ key: '', value: '', isNew: true });
  // console.log("smallsData.value", smallData.value);
}

// 点击编辑中的添加按钮，添加一对（关键词:相关信息）
const saveNewRow = (index: number) => {
  const newRow = smallData.value.data[index];
  // console.log("newRow", newRow.value);
  newRow.isNew = false;
};

// 删除小模版
const handleDelete = (index: number) =>{
  
  //console.log("smallTempData_before:", smallTempData.value);
  smallTempData.value.splice(index, 1);
  //console.log("smallTempData_after:", smallTempData.value);
}

// 将自定义小模版转化为特定的json数据格式
const transformDataToJson = () => {
  // 系统模板数据
  const system_temp = [
{
  small_temp_id: "genes",
  color: "#FF0000",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "transcript_number",
  color: "#11BE05",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "rgv",
  color: "#0000FF",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "experiment",
  color: "#E7E72D",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "chpo",
  color: "#7B68EE",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "icd10",
  color: "#C86D12",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "species",
  color: "#8FBC8F",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "phenotype",
  color: "#DCB61D",
  valid: "1",
  small_temp_type: "system",
  s_type: "enum"
},
{
  small_temp_id: "HGVS",
  color: "#1EACD3",
  valid: "1",
  small_temp_type: "system",
  s_type: "regex"
},
{
  small_temp_id: "np",
  color: "#CD5C5C",
  valid: "1",
  small_temp_type: "system",
  s_type: "regex"
},
{
  small_temp_id: "fci",
  color: "#DA20D1",
  valid: "1",
  small_temp_type: "system",
  s_type: "regex"
}
  ];
  if(!form.name || !form.type || !form.desc){
    // ElMessage.error("请检查模板名称、模板类型、模板描述是否是否输入完整！");
    ElMessage.error(t('messages.mes_tmp_detection'));
    return 
  }
  // 对大模板中的名称、类型、用户Id、描述赋值
  template_big_info.userId = userId;
  template_big_info.templateName = form.name;
  template_big_info.templateType = form.type;
  template_big_info.templateDescription = form.desc;
  // for(let i = 0;i<system_temp.length;i++){
  //   template_big.push(system_temp[i] as templateBig);
  // }

  for (let i = 0; i < smallTempData.value.length; i++) {
    // 创建小模版数据类型
    const obj1 = {
      // s_type: "enum",
      s_type:smallTempData.value[i].type,
      user_id:userId,
      small_temp_id:userId+'_'+smallTempData.value[i].typeName,
      small_temp_name:smallTempData.value[i].typeName,
      small_temp_type:"usr",
      data: {}
    };
    // 创建大模板中json_data中的小模版
    const obj2 = {
      small_temp_id: userId+'_'+smallTempData.value[i].typeName,
      color: smallTempData.value[i].color,
      valid: smallTempData.value[i].valid,
      small_temp_type: "usr",
      // s_type:"enum"
      s_type:smallTempData.value[i].type
    };
    // 将对象添加到结果数组中
    template_big.push(obj2 as templateBig);
    
    for (let j = 0; j < smallTempData.value[i].data.length; j++) {
      const key = smallTempData.value[i].data[j].key;
      const value = smallTempData.value[i].data[j].value;
      // 使用方括号访问对象的属性，并设置其值
      obj1.data[key] = { info: value };
    }
    // 添加到小模版数据中
    add_list.push(obj1);
  }
  // 组合成后端需要的JSON数据类型
  const JsonData = {
    template_big_info,
    template_big,
    add_list
  }
  // 创建自定义模板
  createTempToJson(JSON.stringify(JsonData))
  .then((res)=>{
    if(res.code === 500){
      // console.log("JsonData:",JSON.stringify(JsonData));
      // 清空数据
      template_big_info = {
        userId:"", 
        templateName: "",
        templateDescription: "",
        templateType: ""
      };
      template_big = [];
      add_list = [];
      ElMessage.error(res.message);
    } else{
      // console.log("JsonData:",JSON.stringify(JsonData));
      // 跳转至我的模板页面
      router.push({name:"ExampleList"});
    }
  });
};

// 文件上传前
const beforeUpload = async (_file:Blob) =>{
  return true;
}

// 文件导入添加大模板
const importFileAddbigTemp = async(options:any) =>{
  // 判断是否输入完整的模板名称、模板类型、模板描述
  if(!form.name || !form.name || !form.name){
    // ElMessage.error("请检查模板名称、模板类型、模板描述是否是否输入完整！");
    ElMessage.error(t('messages.mes_tmp_detection'));
    return ;
  }
  const { file } = options;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("templateName", form.name);
  formData.append("templateType", form.type);
  formData.append("templateDescription", form.desc);
  formData.append("userId", userId);
  try {
    await importFileBigTemp(formData)
    .then((res)=>{
      // 错误判断
      if(res.code !== 0){
        if(Array.isArray(res.data)){
          const elements = res.data.map((element: number) => {
              return element;
          }).join(', ');
          ElMessage.error(`${res.message}，请查看模板中第${elements}张数据表`);
        } else {
          ElMessage.error(res.message);
        }
      } else {
        // ElMessage.success('文件上传成功');
        ElMessage.success(t('messages.message_file_success'));
        router.push({ name: "ExampleList" });
      }
    })
    .catch((err)=>{
      console.log("res", err);
    });
  } catch (error) {
    // ElMessage.error('文件上传失败');
    ElMessage.error(t('messages.mes_pdf_file_err'));
    console.log(error);
  }
}

// 下载模板文件
const downloadTemp = () =>{
  window.location.href = "http://medseeker.genemed.tech/downloads/TempDataExample.xlsx";
} 

</script>

<style scoped>
.card-container{
  margin-top: 10px;
  border-radius:10px;
}
.icon{
  width: 30px;
  height: 30px;
}
.color-picker-container {
  display: flex;
  align-items: center;
}
</style>