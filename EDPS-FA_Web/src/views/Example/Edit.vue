<template>
  <!-- 暂时适配手机端 style="overflow: auto; min-width: 1400px;" -->
  <div v-loading="loading" style="overflow: auto; min-width: 1400px;">
    <!-- 大模板名称、类型、描述 -->
    <el-form v-if="bigTempData" :model="bigTempData" label-width="auto" style="position: relative;">
      <div style="width: 600px">
        <el-form-item>
          <template #label>
            <span style="color: red">*</span> <el-text size="large" tag="b">{{ $t('messages.templateName') }}</el-text>
          </template>
          <el-input style="font-size: 20px;" v-model="bigTempData.templateName" />
        </el-form-item>
        <el-form-item style="width: 600px">
          <template #label>
            <span style="color: red">*</span> <el-text size="large" tag="b">{{ $t('messages.templatType') }}</el-text>
          </template>
          <el-select :disabled="true" v-model="bigTempData.templateType" placeholder="请选择您的模板类型" style="width: 100%">
            <el-option v-for="type in templateType" :key="type.value" :label="getTemplateType(type.value)?.label"
              :value="type.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <template #label>
            <span style="color: red">*</span> <el-text size="large" tag="b">{{ $t('messages.templateDesc') }}</el-text>
          </template>
          <el-input style="font-size: 20px;" v-model="bigTempData.templateDescription" type="textarea" />
        </el-form-item>
      </div>
      <el-divider :style="{ borderColor: '#000000', borderWidth: '1px', align: 'center', width: '100%', }" />
      <el-form-item :label="$t('messages.importFile')">
        <el-upload style="font-size: 20px;" action="" :before-upload="beforeUpload" :http-request="importFileAddSmallTemp"
          :show-file-list="false" accept=".xlsx, .xls">
          <el-button type="info" plain :icon="Upload">
            {{ $t('messages.importFile') }}
          </el-button>
        </el-upload>
      </el-form-item>
      <el-button type="warning" @click="downloadTemp">{{ $t('messages.downloadTemp') }}</el-button>
      <el-divider :style="{ borderColor: '#000000', borderWidth: '1px', align: 'center', width: '100%', }" />
    </el-form>

    <!-- 小模版表格数据展示 -->
    <el-form>
      <el-form-item>
        <template #label>
          <el-text tag="b"> </el-text>
        </template>
        <div>

        </div>
        <el-row v-if="smallTableData" style="margin-left: 0px">
          <el-col :span="12" v-for="(item, index) in smallTableData" :index="index">
            <div class="card-container">
              <el-card shadow="always">
                <!-- 小模版名称、颜色、启用、删除 -->
                <div style="display: flex; justify-content: center; align-items: center;">
                  <el-text size="large" tag="b">{{ item.small_temp_name }}</el-text>
                  <el-text size="large" tag="b" style="margin-left: 50px;">Color：</el-text>
                  <el-color-picker v-model="item.color" />
                  <el-text size="large" tag="b" style="margin-left: 50px;"> Type：
                    <span v-if="item.s_type === 'enum'">{{ $t('messages.smallTempTypeEnumerate') }}</span>
                    <span v-else-if="item.s_type === 'regex'">{{ $t('messages.smallTempTypeRegex') }}</span>
                  </el-text>
                  <!-- <ColorPicker v-model="item.color"/> -->
                  <el-text size="large" tag="b" style="margin-left: 50px;">Enable：</el-text>
                  <el-switch size="large" v-model="item.valid" inline-prompt
                    style="margin-right: auto;--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                    active-text="On" inactive-text="Off" active-value="1" inactive-value="0" />
                  <el-button :disabled="item.small_temp_type === 'system'" type="danger" circle size="small"
                    @click="handleDelete(item.small_temp_id)">
                    <el-icon>
                      <Delete />
                    </el-icon>
                  </el-button>
                </div>
                <!-- 可以获取更多 -->
                <el-button :disabled="item.small_temp_type === 'system'" type="success"
                  @click="openDialogForm(item.small_temp_id, index, item.small_temp_name)" class="el-table-add-row"
                  style="width: 100%">
                  <span>{{ $t('messages.button_edit') }}</span>
                </el-button>
                <el-table :data="smallsData[index]" class="tb-edit" style="width: 100%; font-size: large; font-weight: bolder;" height="240" border
                  highlight-current-row>
                  <el-table-column class="word-wrap-column" show-overflow-tooltip :label="$t('messages.matchEntry')" prop="key"
                    align="center"></el-table-column>
                  <el-table-column class="word-wrap-column" show-overflow-tooltip :label="$t('messages.note')" prop="value"
                    align="center"></el-table-column>
                </el-table>
                <el-button @click="getMoreSmallInfo(item.small_temp_id)" class="el-table-add-row" style="width: 100%">
                  <span style="font-size: 16px;">{{ $t('messages.getMore') }}</span>
                </el-button>
              </el-card>
            </div>
          </el-col>
          <!-- 添加小模版按钮 -->
          <el-col :span="12" style="
            display: flex; align-items: center; 
            justify-content: center; ">
            <el-button @click="openDialogAddSmallTemp" size="large"
              style=" background-color: transparent; width: 100%; height: 270px; font-size: 18px;" :icon="Plus">
              <!-- <el-icon>
                <Plus />
              </el-icon> -->
              {{ $t('messages.button_add') }}
            </el-button>
          </el-col>
        </el-row>
        <!-- 点击编辑打开对话框 -->
        <el-dialog v-model="dialogFormVisible" width="800px" :style="{ 'height': '480px' }">
          <div style="display: flex; align-items: center;">
            <h4>{{$t('messages.editName')}}：</h4>
            <el-input v-model="newSmallTemp.small_temp_name" autocomplete="off"
              style="width: 400px; margin-right: 10px;" />
            <el-button type="primary" style="margin-left: 30%; margin-bottom: 5px;" @click="addNewRow">{{ $t('messages.button_add') }}</el-button>
          </div>
          <div>
            <el-table :data="editData" border style="width: 100%" height="250">
              <el-table-column class="word-wrap-column" show-overflow-tooltip prop="key" :label="$t('messages.matchEntry')" align="center"
                width="150">
                <template #default="{ row }">
                  <div v-if="!row.isNew">{{ row.key }}</div>
                  <el-input v-else v-model="row.key" placeholder="Match input" />
                </template>
              </el-table-column>
              <el-table-column class="word-wrap-column" show-overflow-tooltip prop="value" :label="$t('messages.note')" align="center">
                <template #default="{ row }">
                  <div v-if="!row.isNew">{{ row.value }}</div>
                  <el-input v-else v-model="row.value" placeholder="Match info" />
                </template>
              </el-table-column>
              <el-table-column :label="$t('messages.operation')" align="center" width="200">
                <template #default="{ row, $index }">
                  <el-button v-if="!row.isNew"
                    @click="deleteKeyValue(row.key, row.value, bigTempData.id, newSmallTemp.small_temp_id)"
                    type="danger" size="small" plain>{{$t('messages.editDelete')}}</el-button>
                  <el-button v-else @click="saveNewRow($index, bigTempData.id, newSmallTemp.small_temp_id)"
                    type="primary" size="small" plain>{{$t('messages.button_add')}}</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <template #footer>
            <div class="dialog-footer">
              <!-- <el-button type="primary" @click="addNewRow">{{$t('messages.button_add')}}</el-button> -->
              <el-button @click="cancelDialog">{{ $t('messages.button_quit') }}</el-button>
              <el-button type="primary"
                @click="confirmDialog(newSmallTemp.small_temp_name, bigTempData.id, newSmallTemp.small_temp_id)">{{ $t('messages.button_confirm') }}</el-button>
            </div>
          </template>
        </el-dialog>

        <!-- 新增小模板对话框 -->
        <el-dialog v-model="dialogCreateSmallTempVisible" :title="$t('messages.customSmallTemplate')" width="500">
          <el-form>
            <el-form-item :label="$t('messages.smallTempName')">
              <el-input v-model="addSmallData.small_temp_name" autocomplete="off" />
            </el-form-item>
            <el-form-item :label="$t('messages.smallTempType')">
              <div>
                <el-radio-group v-model="addSmallData.s_type">
                  <el-radio :label="'enum'" size="large">{{ $t('messages.smallTempTypeEnumerate') }}</el-radio>
                  <el-radio :label="'regex'" size="large">{{ $t('messages.smallTempTypeRegex') }}</el-radio>
                </el-radio-group>
              </div>
              <el-button type="primary" style="position: absolute; right: 0; top: 10;" @click="addSmallNewRow">
                {{ $t('messages.button_add') }}
              </el-button>
            </el-form-item>
            <el-table :data="addSmallData.data" border height="250px" style="width: 100%">
              <el-table-column :label="$t('messages.matchEntry')" align="center">
                <template #default="{ row }">
                  <div v-if="!row.isNew">{{ row.key }}</div>
                  <el-input v-else v-model="row.key" placeholder="Match input" />
                </template>
              </el-table-column>
              <el-table-column :label="$t('messages.note')" align="center">
                <template #default="{ row }">
                  <div v-if="!row.isNew">{{ row.value }}</div>
                  <el-input v-else v-model="row.value" placeholder="Enter info" />
                </template>
              </el-table-column>
              <el-table-column :label="$t('messages.operation')" align="center" width="200">
                <template #default="{ row, $index }">
                  <el-button v-if="row.isNew" @click="saveSmallNewRow($index)" type="primary" size="small"
                    plain>{{ $t('messages.button_add') }}</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="cancelAddSmallDialog">{{ $t('messages.button_quit') }}</el-button>
              <!-- <el-button type="primary" @click="addSmallNewRow">{{ $t('messages.button_add') }}</el-button> -->
              <el-button type="success" @click="confirmSmallTempDialog">{{ $t('messages.button_confirm') }}</el-button>
            </div>
          </template>
        </el-dialog>
      </el-form-item>
    </el-form>
    <el-button style="float: right; font-size: 18px;" size="large" type="success" @click="confirmAndToList(
      bigTempData.id,
      bigTempData.templateName,
      bigTempData.templateType,
      bigTempData.templateDescription)">{{ $t('messages.button_confirm') }}</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter, useRoute } from "vue-router";
import {
  getSmallInfo,
  getMoreSmallById,
  deleteByBigtempidAndSmallid,
  addByBigtempidAndSmallid,
  updateByBigtempidAndSmallid,
  enableSmallTemp,
  enableColor,
  addSmallTemp,
  updateByBigtempId,
  deleteSmallTemp,
  importFileSmallTemp
} from "../../api/index";
import { Upload, Plus, Delete } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
import { getTemplateType } from "../../utils/Example/tempDescrip";
// 加载动画
const loading = ref(true)
// 用户ID
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 大模板相关信息
let bigTempData = ref();
// 小模版表格数据
let smallTableData = ref();
// 小模版格式化处理的数据
let smallsData = ref([]);
// 设置每个表格的页码
const pageNums = ref<{ [key: string]: number }>({});
// 控制编辑按钮打开对话框
let dialogFormVisible = ref(false);
// 设置编辑按钮中的对话框可编辑小模版名称
let newSmallTemp = ref({
  small_temp_id: '',
  small_temp_name: ''
});
// 设置编辑按钮中的对话框可编辑小模版表格数据
let editData = ref();
// 大模板类型
const templateType = [
  { label: 'Basic', value: '0' },
  { label: 'Private', value: '1' },
  { label: 'Public', value: '2' }
]
// 路由跳转
const router = useRouter();
// 用来接收list页面传来的参数bigTempId
const route = useRoute();
//** 新增模板相关数据结构 */
// 控制新增模板按钮打开对话框
let dialogCreateSmallTempVisible = ref(false);
// 
const templateBigTableInfo = ref({
  small_temp_id: '',
  color: '#11BE05',
  valid: '1',
  small_temp_type: 'usr',
  s_type: 'enum'
});

// 
let addSmallData = ref({
  small_temp_id: '',
  small_temp_name: '',
  user_id: '',
  s_type: 'enum',
  data: [],
})

// 
let templateSmallTableInfo = ref({
  small_temp_id: '',
  small_temp_name: '',
  user_id: '',
  s_type: 'enum',
  data: {},
})

// 获取大模板中所有小模版的数据
const fetchData = async () => {
  // console.log("rowData:", route.params);
  const bigTempId = JSON.parse(route.query.rowData);
  const response = await getSmallInfo(bigTempId);
  bigTempData.value = response.data.templateBigData;
  smallTableData.value = response.data.template_big;
  const initialPageNums = {};
  // 将原始数据格式化处理，并且初始化每个表格的当前页码
  for (let i = 0; i < smallTableData.value.length; i++) {
    const res = formatData(smallTableData.value[i].bigTemplateData.data);
    smallsData.value.push(res);
  }
  smallTableData.value.forEach((item: { small_temp_id: string; }) => {
    // 将每个表格的 pageNum 设置为 2
    initialPageNums[item.small_temp_id] = 2;
  });
  pageNums.value = initialPageNums;
}

onMounted(async () => {
  try {
    // 更新渲染所有小模版数据
    fetchData();
    // 加载动画设置未false
    loading.value = false;
  } catch (error) {
    console.error(error);
  }
});

// 将后端数据转换成key:value格式
function formatData(dataList: any) {
  const formattedData: any[] = [];
  function recurse(currentObj: any, parentKey = "") {
    for (const key in currentObj) {
      if (currentObj.hasOwnProperty(key)) {
        const newKey = parentKey ? `${parentKey}` : key; // 保留父键信息
        if (typeof currentObj[key] === "object" && currentObj[key] !== null) {
          // 如果当前属性是一个对象，递归处理
          recurse(currentObj[key], newKey);
        } else {
          // 否则，推入数组
          formattedData.push({
            key: newKey,
            value: formatValue(currentObj[key]),
          });
        }
      }
    }
  }
  recurse(dataList);
  return formattedData;
};
// 后端数据格式化
function formatValue(value: any) {
  if (typeof value === "object") {
    if (Array.isArray(value)) {
      return value.map((item) => renderObject(item)).join();
    } else {
      return renderObject(value);
    }
  }
  return value;
};
// 后端数据格式化
function renderObject(obj: any) {
  let result = "";
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      result += `${obj[key]} `;
    }
  }
  return result;
};

// 点击（...）更多按钮后，根据小模版id查看小模版更多信息
const getMoreSmallInfo = (smallTempId: any) => {
  const pageSize = 5; // 固定的每页大小
  getMoreSmallById(smallTempId, pageNums.value[smallTempId], pageSize)
    .then((moreData) => {
      // 判断moreData.dataList数据是否为空，转换成JSON字符串来判断，JSON.stringify(obj) === '{}'
      // if (JSON.stringify(moreData.data.dataList.data)  === '{}') {
      //   ElMessage.error('暂无更多数据！')
      //   return;
      // }
      // 判断moreData.dataList.data中是否为空对象
      if (Object.entries(moreData.data.dataList.data).length === 0) {
        // ElMessage.error('暂无更多数据！');
        ElMessage.error(t('messages.mes_tmp_more_info'));
        return;
      }
      // 将新获取的数据合并到现有数据中
      const newDataList = formatData(moreData.data.dataList.data);
      const itemIndex = smallTableData.value.findIndex((item: { small_temp_id: any; }) => item.small_temp_id === smallTempId);
      if (itemIndex !== -1) {
        (smallsData.value[itemIndex] as any[]) = (smallsData.value[itemIndex] as any[]).concat(newDataList);
      }
      // 更新当前页数
      pageNums.value[smallTempId] = pageNums.value[smallTempId] + 1; // 更新 pageNum
    })
    .catch((error) => {
      console.error(error);
    });
};

// 点击编辑打开对话框
const openDialogForm = (smallTempId: string, index: number, smallName: string) => {
  dialogFormVisible.value = true;
  // 处理对话框的小模版数据
  newSmallTemp.value.small_temp_id = smallTempId;
  newSmallTemp.value.small_temp_name = smallName;
  // 根据小模版id获得小模版详细信息
  editData.value = smallsData.value[index];
}

// 在编辑对话框中删除按钮
const deleteKeyValue = (oldKey: string, oldValue: string, bigTempId: string, smallTempId: string) => {
  // 在删除中将对话框中的数据删除，同时也要将smallTableData中的数据删除
  editData.value = editData.value.filter((item: { key: string; value: string; }) => item.key !== oldKey && item.value !== oldValue);
  deleteByBigtempidAndSmallid(oldKey, oldValue, bigTempId, smallTempId)
    .then((res) => {
      if (res.code === 0) {
        // ElMessage.success("删除成功！");
        ElMessage.success(t('messages.mes_rep_del_suc'));
      } else {
        // ElMessage.error("删除失败！");
        ElMessage.error(t('messages.mes_rep_del_err'));
      }
    });
}

// 在编辑对话框中点击新增按钮
const addNewRow = () => {
  editData.value.unshift({ key: '', value: '', isNew: true });
}

// 在编辑对话框中点击添加按钮，添加一对（关键词:相关信息）
const saveNewRow = (index: number, bigTempId: string, smallTempId: string) => {
  const newRow = editData.value[index];
  newRow.isNew = false;
  addByBigtempidAndSmallid(newRow.key, newRow.value, bigTempId, smallTempId)
    .then((res) => {
      if (res.code === 0) {
        // ElMessage.success("添加成功！");
        ElMessage.success(t('messages.mes_fav_add'));
      } else {
        // ElMessage.error("添加失败！");
        ElMessage.error(t('messages.mes_fav_add_err'));
      }
    });
}

// 在编辑对话框中点击取消按钮
const cancelDialog = () => {
  dialogFormVisible.value = false;
}

// 在编辑对话框中点击确认按钮
const confirmDialog = async (smallName: string, bigTempId: string, smallTempId: string) => {
  dialogFormVisible.value = false;
  // 设置加载动画
  loading.value = true;
  // 清空数据
  smallTableData.value = [];
  bigTempData.value = {};
  smallsData.value = [];
  try {
    // 更新渲染所有小模版数据
    await updateByBigtempidAndSmallid(smallName, bigTempId, smallTempId);
    fetchData();
    // 取消加载动画
    loading.value = false;
  } catch (error) {
    console.error(error);
  }
}

// 监听小模版的颜色值和valid值 
watch(() => bigTempData.value && smallTableData.value, (newList) => {
  // console.log(newList);
  if (newList) {
    newList.forEach((item: { valid: any; small_temp_id: string; color: any; }) => {
      //监听valid值变化，变化则更新valid
      watch(() => item.valid, (newValid) => {
        enableSmallTemp(bigTempData.value.id, item.small_temp_id, newValid);
      });
      //监听颜色值变化，变化则更新颜色
      watch(() => item.color, (newColor) => {
        enableColor(bigTempData.value.id, item.small_temp_id, newColor)
      });
    });
  }
}, { immediate: true });

// ** 新增模板相关函数*/
// 打开添加模板对话框
const openDialogAddSmallTemp = () => {
  dialogCreateSmallTempVisible.value = true;
}

// 在新建小模板对话框中点击添加按钮，添加一对（关键词:相关信息）
const saveSmallNewRow = (index: number) => {
  const newRow = addSmallData.value.data[index];
  // console.log("newRow", newRow.value);
  newRow.isNew = false;
}

// 在新建小模板对话框中点击添加按钮
const addSmallNewRow = () => {
  addSmallData.value.data.unshift({ key: '', value: '', isNew: true });
}

// 在新建小模板对话框中点击取消按钮
const cancelAddSmallDialog = () => {
  // 清空数据
  addSmallData.value = {
    small_temp_id: '',
    small_temp_name: '',
    user_id: '',
    s_type: 'enum',
    data: []
  };
  dialogCreateSmallTempVisible.value = false;
}

// 在新建小模板对话框中点击确认按钮
const confirmSmallTempDialog = async () => {
  dialogCreateSmallTempVisible.value = false;
  // 设置加载动画
  loading.value = true;
  console.log("addSmallData:", addSmallData.value);
  for (let i = 0; i < addSmallData.value.data.length; i++) {
    const key = addSmallData.value.data[i].key;
    const value = addSmallData.value.data[i].value;
    // 使用方括号访问对象的属性，并设置其值
    templateSmallTableInfo.value.data[key] = { info: value };
  }
  templateSmallTableInfo.value.s_type = "usr";
  templateSmallTableInfo.value.small_temp_name = addSmallData.value.small_temp_name;
  templateSmallTableInfo.value.s_type = addSmallData.value.s_type;
  templateSmallTableInfo.value.small_temp_id = userId + '_' + addSmallData.value.small_temp_name;
  templateSmallTableInfo.value.user_id = userId;
  // console.log("templateSmallTableInfo:", templateSmallTableInfo.value);

  templateBigTableInfo.value.small_temp_id = templateSmallTableInfo.value.small_temp_id;
  templateBigTableInfo.value.s_type = templateSmallTableInfo.value.s_type;
  // 组成相应的JSON数据格式
  const createJsonData = {
    id: bigTempData.value.id,
    templateBigTableInfo: templateBigTableInfo.value,
    templateSmallTableInfo: templateSmallTableInfo.value
  }
  try {
    // 新建小模版
    await addSmallTemp(JSON.stringify(createJsonData))
      .then((res) => {
        // 清空数据
        smallTableData.value = [];
        bigTempData.value = {};
        smallsData.value = [];
        if (res.code === 500) {
          ElMessage.error(res.message);
        }
        fetchData();
        loading.value = false;
      })
    // 清空数据
    addSmallData.value = {
      small_temp_id: '',
      small_temp_name: '',
      user_id: '',
      s_type: 'enum',
      data: []
    };
    smallTableData.value = [];
    bigTempData.value = {};
    smallsData.value = [];
    // 取消加载动画
    loading.value = false;
  } catch (error) {
    console.error(error);
  }

  templateSmallTableInfo.value.data = {};
}
// 点击确认按钮提交大模板相关信息并且返回list页面
const confirmAndToList = (templateId: string, templateName: string, templateType: string, templateDescription: string,) => {
  updateByBigtempId(templateId, templateName, templateType, templateDescription)
  router.push({ name: "ExampleList" });
}

/** 删除小模版*/
const handleDelete = (smallTempId: string) => {
  ElMessageBox.confirm(t('messages.mes_tmp_del_tip'), t('messages.mes_tmp_tips'), {
    confirmButtonText: t('messages.mes_tmp_del_tip_yes'),
    cancelButtonText: t('messages.mes_tmp_del_tip_no'),
    type: 'warning',
  }).then(async () => {
    // 执行删除逻辑
    await deleteSmallTemp(bigTempData.value.id, smallTempId);
    // 设置加载动画
    loading.value = true;
    // 清空数据
    smallTableData.value = [];
    bigTempData.value = {};
    smallsData.value = [];
    // 更新渲染所有小模版数据
    fetchData();
    // 取消加载动画
    loading.value = false;

  }).catch(() => {
    // 取消操作逻辑
  });
};

/** 
 * 导入文件
*/
// 文件上传前
const beforeUpload = (file: Blob) => {
  return true;
}

// 导入文件新建小模版
const importFileAddSmallTemp = (options: any) => {
  // 设置加载动画
  loading.value = true;
  const { file } = options;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('templateBigId', bigTempData.value.id);
  formData.append('userId', userId);
  importFileSmallTemp(formData)
    .then((res) => {
      if (res.code === 0) {
        // 清空数据
        smallTableData.value = [];
        bigTempData.value = {};
        smallsData.value = [];
        // 提示
        // ElMessage.success("上传成功！");
        ElMessage.success(t('messages.message_success'));
        // 更新渲染所有小模版数据
        fetchData();
        // 取消加载动画
        loading.value = false;
      } else {
        if (Array.isArray(res.data)) {
          const items = res.data.map((item: number) => {
            return item;
          }).join(', ');
          ElMessage.error(`${res.message}，请检查模板中第${items}张数据表`);
        } else {
          ElMessage.error(res.message);
        }
        // 取消加载动画
        loading.value = false;
      }
    });

}
// 下载模板文件
const downloadTemp = () => {
  window.location.href = "http://medseeker.genemed.tech/downloads/TempDataExample.xlsx";
} 
</script>

<style scoped>
.tb-edit .el-input {
  display: none;
}

.tb-edit .current-row .el-input {
  display: block;
}

.tb-edit .current-row .el-input+span {
  display: none;
}

.word-wrap-column {
  white-space: nowrap;
  /* 文本不换行 */
  overflow: hidden;
  /* 超出部分隐藏 */
  text-overflow: ellipsis;
  /* 超出部分以省略号显示 */
}

.card-container {
  margin-top: 10px;
  border-radius: 10px;
}
</style>
