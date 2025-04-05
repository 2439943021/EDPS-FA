<template>
  <!-- <div>
    <el-row :gutter="40" v-if="bigTempData" style="margin-left: 0px">
      <el-col :span="8" v-for="(item, index) in bigTempData" :key="index">
        <el-card shadow="always">
          <div>
            <el-text tag="b">{{ item.small_temp_id }}</el-text>
            <el-text tag="b" style="margin-left: 50px;">颜色：</el-text>
            <el-color-picker v-model="item.color" />
            <el-text tag="b" style="margin-left: 50px;"> 类别：{{ item.small_temp_type }}
            </el-text>
            <el-text tag="b" style="margin-left: 50px;">启用：</el-text>
            <el-switch v-model="item.valid" inline-prompt
              style="margin-right: auto;--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" active-text="启用"
              inactive-text="关闭" active-value="1" inactive-value="0" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-button style="float: right; margin-top: 20px; margin-right: 40px;">返回</el-button>
  </div> -->
  <div class="table-container">
    <el-table :data="bigTempData" class="table" :stripe="true">
      <el-table-column prop="small_temp_id" label="名称" width="180" />
      <el-table-column prop="small_temp_type" label="类别" width="180" />
      <el-table-column prop="color" label="颜色">
        <template v-slot="scope">
          <div>
            <el-color-picker v-model="scope.row.color" :disabled="true" />
          </div>
        </template>
      </el-table-column>
      <el-table-column label="启用">
        <template v-slot="scope">
          <div>
            <el-switch v-model="scope.row.valid" inline-prompt :disabled="true"
              style="margin-right: auto;--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949" active-text="启用"
              inactive-text="关闭" active-value="1" inactive-value="0" />
          </div>
        </template>
      </el-table-column>
    </el-table>
    <div class="button-container">
      <el-button type="success" @click="handleGoBack">返回</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  getSmallInfo,
} from "../../api/index";
const route = useRoute();
const router = useRouter();
let bigTempData = ref();
onMounted(async () => {
  const TempId = JSON.parse(route.query.rowData);
  const res = await getSmallInfo(TempId);
  bigTempData.value = res.data.template_big;
  // console.log(bigTempData.value);
})
// 返回按钮
const handleGoBack = () => {
  router.push({name:"ExampleList"});
}
</script>

<style scoped>
.el-card {
  width: 550px;
  margin-top: 40px;
  height: 100px;
}

.table-container {
  margin-left: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button-container {
  margin-right: 45%;
  margin-top:22%;
}
.table {
  width: 50%;
  font-family: Arial, sans-serif;
  font-size: 16px;
  color: black;
}
</style>