<template>
  <div class="table">
    <!-- 选择器 -->
    <!-- <el-select v-model="selectedState"  style="width: 100px" >
        <el-option
          v-for="stateCode in stateCodes"
          :key="stateCode"
          :label="getStateLabel(stateCode).label"
          :value="stateCode"
          @click="searchPmids"
        >
        </el-option>
      </el-select>
      <el-cascader
      v-model="selectedState"
      :options="cascaderOptions"
      :props="{emitPath:false}"
      style="width: 100px"
      @change="searchPmids"
      ></el-cascader> -->
    <!-- 搜索框 -->
    <div style="margin-bottom: 15px;">
      <el-input v-model="searchPmid" clearable placeholder="Please input PMID" style="width: 300px;"/>
      <el-button type="success" plain style="margin-left: 30px; font-size: 18px;" @click="searchPmids(searchPmid)" :icon="Search">{{
        $t('messages.search') }}</el-button>
      <el-button type="primary" plain style="margin-left: 30px; font-size: 18px;" @click="quitSearchPmids" :icon="Refresh">{{
        $t('messages.reset') }}</el-button>
      <!-- <el-button style="float: right;" @click="downloads">{{ $t('messages.batchDownload') }}</el-button> -->
      <el-popconfirm width="250" :icon="InfoFilled" icon-color="#626AEF" :title="$t('messages.batchDownloadTip')"
        @cancel="onCancel" @confirm="downloads">
        <template #reference>
          <el-button type="warning" plain style="margin-left: 30px; font-size: 18px;" :icon="Share">{{ $t('messages.batchDownload')
            }}</el-button>
        </template>
        <template #actions="{ confirm, cancel }">
          <el-button size="small" @click="cancel">否</el-button>
          <el-button type="danger" size="small" @click="confirm">
            是
          </el-button>
        </template>
      </el-popconfirm>
      <div style="text-align: center; margin-top: 1%;">
    <el-text style="color: black; font-size: 20px;">{{ $t('messages.reportlist_title') }}</el-text>
  </div>
    </div>
    <!-- el-table表格 -->
    <div class="table">
      <el-table :data="tableData" border :row-class-name="setRowHeight" @selection-change="handleSelectionChange"
        ref="dataTable" :header-cell-style="{ background: 'skyblue', color: 'black' }" v-loading="loading" style="color: black; height: 800px;">
        <el-table-column type="selection" width="35%" />
        <el-table-column :label="$t('messages.index')" align="center" width="70%">
          <template v-slot="scope">
            {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column :label="$t('messages.subType')" align="center" width="100%">
          <template v-slot="{ row }">
            <span>{{ getSubmitType(row.submitType)?.label }}</span>
          </template>
        </el-table-column>
        <el-table-column :label="$t('messages.templateTest')" prop="templateBigName" align="center" width="130%"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column prop="pmcId" label="PMID" align="center" width="120%">
          <template v-slot="{ row }">
            <span v-if="row.submitType === '03'">-</span>
            <span v-else>{{ row.pmcId }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" class="word-wrap-column" show-overflow-tooltip>
          <template #header>
            <div style="text-align: center;">{{ $t('messages.title') }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="author" :label="$t('messages.author')" align="center" width="120%"
          show-overflow-tooltip />
        <el-table-column prop="state" :label="$t('messages.status')" align="center" width="130%" show-overflow-tooltip>
          <template v-slot="{ row }">
            <span :style="{ color: getStateLabel(row.state).color }">{{ getStateLabel(row.state).label }}</span>
          </template>
        </el-table-column>
        <!-- <el-table-column prop="state" label="状态" align="center" width="80" show-overflow-tooltip>
            <template v-slot="{ row }">
              <span :style="{ color: getStateLabel(row.state).color }">{{ getStateLabel(row.state).label }}</span>
            </template>
          </el-table-column> -->
        <!-- <el-table-column label="进度" align="center" width="100">
            <template v-slot="{ row }">
               <el-progress
                :percentage="getStateLabel(row.state).progress"
                color="#67C23A"
              ></el-progress> 
              <div class="progress-wrapper" :class="{ rotating: getStateLabel(row.state).progress < 100 }">
                <el-progress :percentage="getStateLabel(row.state).progress" type="circle" :width="20" :stroke-width="3"
                  stroke-linecap="square" :format="format" :indeterminate="false" :duration="1" :striped-flow="true"
                  :color="customColor(row.state)" class="custom-progress" />
              </div>
            </template>
          </el-table-column> -->
        <el-table-column :label="$t('messages.collect')" align="center" width="60%">
          <template v-slot="{ row }">
            <el-text v-if="row.state === '13' || row.state === '23'"><el-icon>
                <Close style="color: black;" />
              </el-icon></el-text>
            <el-text v-else-if="row.state !== '11' && row.state !== '12' && row.state !== '13'"><el-icon>
                <Check style="color: black;" />
              </el-icon></el-text>
          </template>
        </el-table-column>
        <el-table-column :label="$t('messages.analyze')" align="center" width="60%">
          <template v-slot="{ row }">
            <el-text
              v-if="row.state === '13' || row.state === '23' || row.state === '33' || row.state === '43'"><el-icon>
                <Close style="color: black;" />
              </el-icon></el-text>
            <el-text v-else-if="row.state === '51'"><el-icon>
                <Check style="color: black;" />
              </el-icon></el-text>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" :label="$t('messages.submissionTime')" align="center" width="175%">
          <template v-slot="{ row }">
            {{ row.createTime.slice(0, -3) }}
          </template>
        </el-table-column>
        <el-table-column prop="endTime" :label="$t('messages.sompletionTime')" align="center" width="175%">
          <template v-slot="{ row }">
            {{ row.endTime ? row.endTime.slice(0, -3) : '' }}
          </template>
        </el-table-column>

        <el-table-column :label="$t('messages.remainingTime')" align="center" width="85%">
          <template #default="{ row }">
            <!-- {{ getStateTime(row.state).time }} m -->
            <!-- {{ calculateTimeDifference(row.createTime) }} m -->
            <!-- 处于*3 状态 则显示X -->
            <el-text v-if="row.state === '13' || row.state === '23' || row.state === '33' || row.state === '43'">
              <el-icon><Close style="color: black;" /></el-icon></el-text>
            <!-- 未完成则计算剩余时间 -->
            <el-text v-else-if="row.state!=='51'" style="color: black;"> {{ calculateTimeDifference(row.createTime) }} M</el-text>
            <el-text v-else><el-icon><Check style="color: black;" /></el-icon></el-text>
          </template>
        </el-table-column>
        <el-table-column :label="$t('messages.operation')" align="center" width="300%">
          <template v-slot="{ row }">
            <span v-if="row.submitType !== '03'" @click="showArticle(row.pmcId)" class="text-button primary">{{
              $t('messages.button_show') }}</span>
            <span v-if="row.state === '51'" @click="lookReport(row.htmlUrl, row.id)" class="text-button success">{{
              $t('messages.button_report') }}</span>
            <el-tooltip v-if="row.state === '51'" class="box-item" effect="dark" :content="$t('messages.download_tip')"
              placement="top">
              <span @click="downloadReport(row.zipUrl, row.title)" class="text-button info">{{
                $t('messages.button_down') }}</span>
            </el-tooltip>
            <span @click="deleteReport(row.id)" class="text-button danger">{{ $t('messages.button_delete') }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页器 -->
    <div style="display: flex; align-items: center; justify-content: flex-end; gap: 16px;">
      <!-- <el-text style="margin-right: 5px;margin-top: 5px;">共{{ total }}条</el-text> -->
      <el-pagination class="el-pagination" background @size-change="handleSizeChange"
        @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[20, 50, 100]"
        :page-size="pageSize" layout="total, sizes,prev, pager, next, page, jumper" :total="total">
        <!-- <el-text style="color: black; margin-right: 10px;">共 {{ total }} 条</el-text> -->
        <el-select v-model="pageSize" @change="handleSizeChange">
          <el-option v-for="size in [20, 50, 100]" :key="size" :label="`${size}/页`" :value="size" />
        </el-select>
      </el-pagination>
      <!-- <el-pagination class="el-pagination" background @size-change="handleSizeChange"
          @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[20, 50, 100]"
          :page-size="pageSize" layout="slot" :total="total">
          <el-text style="color: black;">前往</el-text>
          <el-input v-model.number="jumpPage" style="width: 40px" @keyup.enter="handleJump" :min="1"
            :max="Math.ceil(total / pageSize)" />
          <el-text style="color: black;">页</el-text>
        </el-pagination> -->
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount,computed, onBeforeUnmount, onMounted, onUnmounted, nextTick } from "vue";
import { getList, postCheckByStateAndPmcId, deleteByPimd } from "../../api/index";
import { getStateLabel, getSubmitType } from "../../utils/getStateLabel";
// import { cascaderOptions }  from "../../utils/cascaderOptions";
import { Search, Refresh, InfoFilled, Share } from '@element-plus/icons-vue';
import { AxiosResponse } from "axios";
import { ElMessage } from "element-plus";
import type { ElTable } from 'element-plus';
import { tableRow } from './types';
import { useRouter } from "vue-router";
import { getStateTime } from './utils.ts';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
let tableData = ref();
const currentPage = ref(1);
const pageSize = ref(20);
let total = ref(0);
const setRowHeight = () => "custom-row-height"; // 返回自定义的类名
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 搜索数据
const searchPmid = ref("");
let selectedState = ref("");
// 路由器
const router = useRouter();
// 根据 stateCode 返回对应的状态
// const stateCodes = ["", "0", "1", "2", "3", "4", "5"];

// 设置定时器
let timerId: number | undefined;

// 选择的行
const selectedRows = ref<Array<tableRow>>([]);

// 控制table表格
const dataTable = ref<InstanceType<typeof ElTable> | null>(null);

// 加载动画
const loading = ref(true);

// 定义获取数据的函数
const fetchData = async () => {
  try {
    let response;
    if (searchPmid.value.length || selectedState.value.length) {
      response = await postCheckByStateAndPmcId(
        searchPmid.value,
        pageSize.value,
        currentPage.value,
        selectedState.value,
        userId
      );
    } else {
      response = await getList(pageSize.value, currentPage.value, userId);
    }
    // response = await getList(pageSize.value, currentPage.value, userId);
    // 取消加载动画
    loading.value = false;
    tableData.value = response.data.records;
    total.value = response.data.total;
    // 保存当前选择的行的 ID
    const selectedIds = selectedRows.value.map(row => row.id);
    nextTick(() => {
      // 确保 tableData 是一个数组
      if (Array.isArray(tableData.value)) {
        // 更新数据后，根据 ID 恢复选择状态
        selectedRows.value = tableData.value.filter(row =>
          selectedIds.includes(row.id)
        );
        // 手动设置选择状态
        if (dataTable.value) {
          dataTable.value.clearSelection(); // 先清空选择
          selectedRows.value.forEach(row => {
            dataTable.value?.toggleRowSelection(row, true);
          });
        }
      }
    });
  } catch (error) {
    // 取消加载动画
    loading.value = false;
    console.log(error);
  }
};

const handleSelectionChange = (val: any) => {
  selectedRows.value = val;
};

// 定义轮询函数
const fetchDataPeriodically = () => {
  // 每10秒轮询一次数据
  timerId = setInterval(() => {
    fetchData();
  }, 4000) as unknown as number;
};

// 在组件挂载前执行的逻辑
onBeforeMount(() => {
  fetchData(); // 首次加载数据
  fetchDataPeriodically(); // 启动定时轮询
});

// 在组件销毁前清除定时器
onBeforeUnmount(() => {
  clearInterval(timerId);
});

// 处理每页展示数量改变的函数
const handleSizeChange = (val: number) => {
  pageSize.value = val;
  fetchData();
};

// 处理当前页数改变的函数
const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchData();
};

// 点击搜索按钮执行的函数
const searchPmids = (pimd:string) => {
  currentPage.value = 1;
  const searchId = pimd;
  // console.log("searchId", searchId);
  postCheckByStateAndPmcId(
    searchId,
    pageSize.value,
    currentPage.value,
    selectedState.value,
    userId
  ).then((response: AxiosResponse<any>) => {
    tableData.value = response.data.records;
    total.value = response.data.total;
  });
};

// 点击取消按钮执行的函数
const quitSearchPmids = () => {
  currentPage.value = 1;
  postCheckByStateAndPmcId("", pageSize.value, currentPage.value, selectedState.value, userId)
    .then((response: AxiosResponse<any>) => {
      searchPmid.value = "";
      tableData.value = response.data.records;
      total.value = response.data.total;
    });
};

// 点击查看原文跳转到原文网站
function showArticle(pmcId: any) {
  const originalUrl = `https://pubmed.ncbi.nlm.nih.gov/${pmcId}/`;
  window.open(originalUrl, '_blank');
}

// 查看渲染的报告
const lookReport = (htmlUrl: string, id: string) => {
  const query = {
    url: JSON.stringify(htmlUrl),
    articleId: JSON.stringify(id)
  }
  const detailsRoute = router.resolve({
    name: 'details',
    query
  })
  if (detailsRoute.href) {
    window.open(detailsRoute.href, '_blank')
  } else {
    console.error('无法解析details路由!');
  }
}

// 下载渲染报告和实体信息
const downloadReport = async (zipUrl: string, title: string) => {
  try {
    // 获取压缩包文件内容
    const response = await fetch(zipUrl);
    // 检查响应是否成功（状态码200-299）
    if (!response.ok) {
      throw new Error(`网络响应不成功: ${response.statusText}`);
    }
    // 将响应内容作为Blob获取
    const blob = await response.blob();
    // 为Blob创建一个对象URL
    const url = URL.createObjectURL(blob);
    // 创建一个链接元素
    const link = document.createElement('a');
    link.href = url;
    if (title.length >= 200) title = title.slice(0, 200)
    link.download = `${title}.zip`; // 设置下载文件名
    // 将链接元素添加到文档中
    document.body.appendChild(link);
    // 程序化地点击链接以触发下载
    link.click();
    // 从文档中移除链接元素
    document.body.removeChild(link);
    // 撤销对象URL
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('下载压缩包文件时出错:', error);
  }
};

// 批量下载提示
const clicked = ref(false)
const onCancel = () => {
  clicked.value = true
}

// 批量下载报告
const downloads = async () => {
  try {
    for (let i = 0; i < selectedRows.value.length; i++) {
      // 判断zipUrl是否为空
      if (!selectedRows.value[i].zipUrl) {
        //console.log("zipUrl:null");
        continue;
      }
      // 获取压缩包文件内容
      const response = await fetch(selectedRows.value[i].zipUrl);
      // 检查响应是否成功（状态码200-299）
      if (!response.ok) {
        throw new Error(`网络响应不成功: ${response.statusText}`);
      }
      // 将响应内容作为Blob获取
      const blob = await response.blob();
      // 为Blob创建一个对象URL
      const url = URL.createObjectURL(blob);
      // 创建一个链接元素
      const link = document.createElement('a');
      link.href = url;
      // 设置下载文件名
      link.download = `${selectedRows.value[i].title}.zip`;
      // 将链接元素添加到文档中
      document.body.appendChild(link);
      // 程序化地点击链接以触发下载
      link.click();
      // 从文档中移除链接元素
      document.body.removeChild(link);
      // 撤销对象URL
      URL.revokeObjectURL(url);
    }
  } catch (error) {
    console.error('下载压缩包文件时出错:', error);
  }
};

// 点击删除按钮根据pmid删除文章
const deleteReport = (id: string) => {
  deleteByPimd(id)
    .then((res) => {
      if (res.code === 0) {
        // ElMessage.success("删除成功！");
        ElMessage.success(t('messages.mes_rep_del_suc'));
        fetchData();
      } else {
        // ElMessage.error("删除失败！");
        ElMessage.error(t('messages.mes_rep_del_err'));
      }
    })
};
// 时间差
const calculateTimeDifference = (createTime:string) => {
  const createTimeDate = new Date(createTime.replace(' ', 'T')).getTime();
  const now = new Date().getTime();
  let pastTime = (now - createTimeDate)/(1000 * 60);
  let proportion = getRandom(9, 11, 2) // 8
  if (pastTime < 1){
    pastTime = 1
  }
  if (pastTime >= proportion){
    pastTime = proportion - 1
  }
  let result = proportion - getRandom(1.3, 1.7, 2) * pastTime
  // let result = proportion - getRandom(0.3, 0.5, 2) * pastTime
  if (result < 1){
    result = 1 - getRandom(0.1, 0.6, 2)
    // result = 1 - getRandom(0.1, 0.3, 2)
  }
  return result.toFixed(2);
}
// 获取随机数的方法：在指定范围内生成随机浮点数
const getRandom = (min: number, max: number, decimalPlaces: number): number => {
  const factor = Math.pow(10, decimalPlaces);
  return Math.floor((Math.random() * (max - min) + min) * factor) / factor;
};

let jumpPage = ref(1);
const handleJump = () => {
  if (jumpPage.value > 0 && jumpPage.value <= Math.ceil(total.value / pageSize.value)) {
    handleCurrentChange(jumpPage.value)
    fetchData();
  } else {
    ElMessage.error("请输入有效页码!");
  }
}
// 重置进度条样式 取消后面的进度
const format = (percentage: any) => (percentage === 100 ? '' : '');
const customColor = (state: string) => {
  const redState = ['13', '23', '33', '43'];
  if (redState.includes(state)) {
    return 'red';
  } else {
    if (getStateLabel(state).progress === 100) {
      return '#67C23A';
    } else {
      return '#409EFF';
    }
  }
}
</script>

<style scoped>
/* .table {
  
} */
.table {
    justify-content: center;
    align-items: center;
    /*垂直居中时，设置容器高度 */
    width: 100%;
    /* 设置字体 */
    font-family: Arial, sans-serif;
    /* 设置字号 */
    font-size: 16px;
    font-weight:bolder;
    color: #333;
    /* 设置文字颜色 */
    margin-top: 5px;
  }
.el-pagination {
  display: flex;
  justify-content: left;
  align-items: center;
  height: 100%;
  /* 垂直居中时，设置容器高度 */
  font-size: 16px;
  font-weight: bolder;
  margin-top: 1%;
  float: right;
  overflow: auto;
}

.word-wrap-column {
  white-space: nowrap;
  /* 文本不换行 */
  overflow: hidden;
  /* 超出部分隐藏 */
  text-overflow: ellipsis;
  /* 超出部分以省略号显示 */
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

.center-header .el-table__header-wrapper th {
  text-align: center !important;
}

.word-wrap-column .cell {
  text-align: left !important;
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

/* 旋转进度条 */
.progress-wrapper {
  display: inline-block;
  position: relative;
}

.rotating .custom-progress {
  animation: spin 2s linear infinite;
}

.jump-input {
  width: 50px;
  text-align: center;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>