<template>
  <div class="list-comp">
    <div style="display: flex; justify-content: space-between;">
      <div><svg t="1731578748546" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="6313" width="16" height="16">
          <path
            d="M512 85.333333c235.648 0 426.666667 191.018667 426.666667 426.666667s-191.018667 426.666667-426.666667 426.666667S85.333333 747.648 85.333333 512 276.352 85.333333 512 85.333333z m0 170.666667a42.666667 42.666667 0 0 0-42.666667 42.666667v341.333333a42.666667 42.666667 0 0 0 85.333334 0V298.666667a42.666667 42.666667 0 0 0-42.666667-42.666667z m0 554.666667a42.666667 42.666667 0 1 0 0-85.333334 42.666667 42.666667 0 0 0 0 85.333334z"
            fill="#FAAD14" p-id="6314"></path>
        </svg><el-text tag="b" size="large" style="color: black;">{{ $t('messages.templatetip') }}</el-text></div>
      <!-- 这里留一个空白的 div 来占位 -->
      <div style="text-align: center; margin-right: 10%;"> <el-text tag="b" style="color: black; font-size: 20px;">{{ $t('messages.template') }}</el-text> </div>
      <!-- <div style="text-align: center;">
    <el-text style="color: black; font-size: 20px;">{{  $t('messages.template') }}</el-text>
  </div> -->
      <div>
        <el-button @click="toCreateTemp" type="success" style="font-size: 18px; margin-bottom: 10px" :icon="CirclePlus" plain>
          {{ $t('messages.button_add') }}
        </el-button>
      </div>
    </div>
    <el-table :data="tableData" border class="el-table" v-loading="loading"
      :header-cell-style="{ background: 'skyblue', color: 'black' }">
      <el-table-column prop="id" :label="$t('messages.index')" align="center" width="80">
        <template v-slot="scope">
          {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column prop="templateName" :label="$t('messages.templateName')" class="word-wrap-column" align="center"
        show-overflow-tooltip width="200"></el-table-column>
      <el-table-column :label="$t('messages.templatType')" align="center" width="150">
        <template v-slot="{ row }">
          <span>{{ getTemplateType(row.templateType)?.label }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="templateDescription" :label="$t('messages.templateDesc')" class="word-wrap-column"
        align="left" show-overflow-tooltip></el-table-column>
      <el-table-column :label="$t('messages.templateCreateTime')" align="center" width="200">
        <template v-slot="{ row }">
          <template v-if="shuoldShow(row.id)">
            {{ row.createTime.slice(0, -3) }}
          </template>
          <template v-else>
            {{ '-' }}
          </template>
        </template>
      </el-table-column>
      <el-table-column :label="$t('messages.templateUpdataTime')" align="center" width="200">
        <template v-slot="{ row }">
          <template v-if="shuoldShow(row.id)">
            {{ row.createTime.slice(0, -3) }}
          </template>
          <template v-else>
            {{ '-' }}
          </template>
        </template>
      </el-table-column>
      <el-table-column :label="$t('messages.operation')" align="center" width="200">
        <template v-slot="{ row }">
          <span v-if="shuoldShow(row)" @click="editTemp(row.id, row.modelTemplate)" class="text-button primary">{{
            $t('messages.button_edit') }}</span>
          <span v-if=isBigModel(row) @click="copyByBigTemp(row.id, userId)" class="text-button info">{{
            $t('messages.button_copy') }}</span>
          <span v-if="shuoldShow(row) && isBigModel(row)" @click="deleteBigTemp(row.id, userId)"
            class="text-button danger">{{ $t('messages.button_dele') }}</span>
        </template>
      </el-table-column>
    </el-table>
    <div style="display: flex; justify-content: flex-end;">
      <el-pagination class="el-pagination" @current-change="handleCurrentChange" background
        layout="total, prev, pager, next" :total="total">
        <!-- <el-text style="color: black;">共 {{ total }} 条</el-text> -->
      </el-pagination>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import { useRouter } from "vue-router";
import { checkAllTemplate, copyByBigTempId, deleteByUserId } from "../../api/index";
import { CirclePlus } from '@element-plus/icons-vue';
import { getTemplateType } from "../../utils/Example/tempDescrip";
import { ElMessage } from 'element-plus'
import { checkTemp } from "../../utils/checkInfo";
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
let tableData = ref();
const currentPage = ref(1);
const pageSize = 10;
let total = ref(0);
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
const router = useRouter();

// 加载动画
let loading = ref(true);

onBeforeMount(async () => {
  try {
    const res = await checkAllTemplate(currentPage.value, pageSize, userId);
    tableData.value = res.data.records;
    total.value = res.data.total;
    loading.value = false;
  } catch (error) {
    console.log(error);
    loading.value = false;
  }
});

// 分页
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  checkAllTemplate(currentPage.value, pageSize, userId)
    .then((res) => {
      tableData.value = res.data.records;
      total.value = res.data.total;
    })
    .catch((error) => {
      console.log(error)
    })
};

// 点击新增路由跳转到新增模板页面 
async function toCreateTemp() {
  // 判断用户是否还能新建自定义模版
  if (await checkTemp(userId)) {
    router.push({ name: 'createtemp' });
  }
}

// 点击编辑路由跳转到编辑页面
function editTemp(row: any, modelTemplate: string) {
  const rowData = JSON.stringify(row); // 将 row 对象转换为 JSON 字符串
  // console.log(rowData);
  if (modelTemplate === '0') {
    router.push({ name: "edit", query: { rowData } });
  } else {
    router.push({ name: "bigmodeledit", query: { rowData } });
  }

}

// 根据大模板ID拷贝大模板
async function copyByBigTemp(id: any, userId: number) {
  if (!await checkTemp(userId)) {
    return;
  }
  copyByBigTempId(id, userId)
    .then((res) => {
      console.log("res", res)
      const success = res;
      console.log("success", success.data)
      if (res.code === 0) {
        // ElMessage.success("拷贝成功！")
        ElMessage.success(t('messages.mes_tmp_copy'))
        checkAllTemplate(1, pageSize, userId)
          .then((response) => {
            tableData.value = response.data.records;
            total.value = response.data.total;
          })
          .catch((error) => {
            console.log(error)
          })
      } else {
        // ElMessage.error("拷贝失败！")
        ElMessage.error(t('messages.mes_tmp_copy_err'))
      }
    })
    .catch((error) => {
      console.log(error)
    })
}

// 根据大模板id删除
function deleteBigTemp(tempId: string, userId: number) {
  deleteByUserId(tempId, userId)
    .then((res) => {
      if (res.code === 0) {
        // ElMessage.success("删除成功！")
        ElMessage.success(t('messages.mes_rep_del_suc'));
        checkAllTemplate(1, pageSize, userId)
          .then((response) => {
            tableData.value = response.data.records;
            total.value = response.data.total;
          })
          .catch((error) => {
            console.log(error)
          })
      } else {
        // ElMessage.error("删除失败！");
        ElMessage.error(t('messages.mes_rep_del_err'));
      }
    })
    .catch((error) => {
      console.log(error)
    })
}

// 判断是否为系统模版和大模型模版
const shuoldShow = (row: any) => {
  // return row.id !== '002' && row.modelTemplate !== '1';
  if (row.id !== '002') {
    return true;
  }
}
// 判断是否为大模型模版
const isBigModel = (row: any) => {
  if (row.modelTemplate === '0') {
    return true;
  }
}
</script>

<style scoped>
.el-table {
  display: flex;
  justify-content: center;
  align-items: center;
  /* 垂直居中时，设置容器高度 */
  width: 100%;
  font-family: Arial, sans-serif;
  /* 设置字体 */
  font-size: 15px;
  font-weight: bolder;
  /* 设置字号 */
  color: #333;
  /* 设置文字颜色 */
  margin-top: 5px;
  /* 暂时适配手机端，后期需要调整样式 */
  overflow: auto;
  min-width: 1400px;
}

.el-table-column {
  height: 100px;
}

.word-wrap-column {
  white-space: nowrap;
  /* 文本不换行 */
  overflow: hidden;
  /* 超出部分隐藏 */
  text-overflow: ellipsis;
  /* 超出部分以省略号显示 */
}

.el-pagination {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 100%;
  /* 垂直居中时，设置容器高度 */
  margin-top: 5px;
  font-size: 17px;
  font-weight: bold;
  float: right;
}

.text-button {
  cursor: pointer;
  /* padding: 0px 0px; */
  border-radius: 3px;
  display: inline-block;
  margin-right: 5px;
  font-size: 13px;
  transition: color 0.5s;
  transition: transform 0.5s ease;
}

.text-button.primary {
  color: #409EFF;
  /* 修改为你需要的颜色 */
}

.text-button.success {
  color: #67C23A;
  /* 修改为你需要的颜色 */
}

.text-button.info {
  color: #E6A23C;
  /* 修改为你需要的颜色 */
}

.text-button.danger {
  color: #F56C6C;
  /* 修改为你需要的颜色 */
}

.text-button:hover {
  transform: translateY(-5px);
}
</style>