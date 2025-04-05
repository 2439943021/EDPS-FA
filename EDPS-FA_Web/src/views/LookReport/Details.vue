<template>
  <el-button type="primary" plain @click="returnReportList" link><el-icon><ArrowLeft /></el-icon>{{ $t('messages.returnReportList') }}</el-button>
  <div v-loading="loading" element-loading-text="Loading..." style="height: 1000px;">
    <iframe ref="iframe" id="reportiframe" :src="url" width="100%" style="height: 100%;" frameborder="0"></iframe>
  </div>
  <!-- 对话框 -->
  <el-dialog v-model="collect" width="500" :title="$t('messages.addToFavorites')" append-to-body destroy-on-close center
    @keyup.enter="handleCollect">
    <el-form>
      <el-form-item>
        <el-select v-model="floderName" placeholder="Select" size="large" style="width:200px">
          <el-option v-for="item in favorites" :key="item.classId" :value="item.className" :label="item.className">
            <!-- <span class="ellipsis">{{ item.className }}</span> -->
          </el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <div class="button_center">
      <el-button @click="handleFolder">
        <el-icon>
          <Plus />
        </el-icon>
        {{ $t('messages.newFavorites') }}
      </el-button>
    </div>
    <el-divider />
    <div class="button_center">
      <el-button ref="collectButton" @click="handleCollect">{{ $t('messages.button_collect') }}</el-button>
    </div>
  </el-dialog>

  <!-- 新增收藏夹 -->
  <el-dialog :title="$t('messages.newFavorites')" v-model="addFolder" width="400" @keyup.enter="addNewFloder">
    <el-form :model="form" :rules="rules" ref="formRef">
      <el-form-item :label="$t('messages.favorites')" prop="addFolderName">
        <el-input v-model="form.addFolderName" @keydown.enter.prevent />
      </el-form-item>
    </el-form>
    <div style="text-align: right;">
      <el-button @click="addNewFloder">{{ $t('messages.button_add') }}</el-button>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  getAllUserCollect,
  getUserFavorites,
  collectParagraphInfo,
  deleteCollection,
  addUserFavorites,
} from '../../api/index';
import { ElMessage } from 'element-plus';
import { useUserStore } from '../../store/user';
import { ReceivedFromHtml } from './types';
import { useI18n } from 'vue-i18n';
let lang = localStorage.getItem('lang');
const { t } = useI18n();
// 使用pinia
const useStore = useUserStore();
// const userId = useStore.getInfo().user.userId;
const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// html返回的数据
let receivedFromHtml = reactive(<ReceivedFromHtml>{});
// 文章地址
let url = ref('');
const iframe = ref<HTMLIFrameElement | null>(null);
// 已收藏的文章段落号
let collectedIds = ref();
// 打开收藏夹对话框
let collect = ref(false);
// 打开新增收藏夹对话框
let addFolder = ref(false);
// 默认收藏夹
const floderName = ref('Default System Favorites');
// 收藏夹
let favorites = ref();
// 新增收藏夹名
const form = ref({
  addFolderName: ''
});
// 文章id
const articleId = ref('');
// 路由
const route = useRoute();
// 路由器
const router = useRouter();
// 加载动画
const loading = ref(true)
// 规则校验
const rules = {
  addFolderName: [{ required: true, message: t('messages.createFavoritesTips'), trigger: 'blur' }]
};

// 收藏相关 
const handleContentCollected = async (event: {
  data:
  {
    content: string; pmid: string; pmcid: string; isCollected: boolean;
    paragraphId: string; collectType: string; mouseX: number; mouseY: number; entities: Array<{ name: string, type: string, typeName: string }>
  };
}) => {
  console.log('Received message:', event.data);
  // 从 event.data 解构所需的属性
  receivedFromHtml = { ...event.data }
  // console.log('receivedFromHtml：', receivedFromHtml);
  // debugger
  // 先根据属性判断是根据星星收藏还是光标选中内容的收藏
  if (receivedFromHtml.hasOwnProperty('isCollected')) {
    // 1. 通过 isCollected 判断用户是否收藏
    if (receivedFromHtml.isCollected) {
      collect.value = true;
      // 获取用户收藏夹数组
      const res = await getUserFavorites(userId);
      favorites.value = res.data;
      // 执行收藏操作
    } else {
      // TODO 拿到数据，发送接口，取消收藏
      deleteCollection(userId, articleId.value, receivedFromHtml.paragraphId, receivedFromHtml.collectType)
        .then(() => {
          // ElMessage.success('取消收藏成功!');
          ElMessage.success(t('messages.mes_fav_quit_collect'));
        })
        .catch(() => {
          // ElMessage.error('取消收藏失败!');
          ElMessage.error(t('messages.mes_fav_quit_collect_err'));
        });
    }
  } else if (receivedFromHtml.collectType === 'manu') {
    // 查找已有的选择栏
    const existingToolbar = document.getElementById('toolbar');
    if (existingToolbar) {
      document.body.removeChild(existingToolbar); // 移除已有的选择栏
    }
    // 创建新的选择栏
    // console.log("创建新的选择栏 lang", lang);
    const toolbar = document.createElement('div');
    toolbar.id = 'toolbar'; // 给选择栏一个唯一的 ID
    toolbar.style.position = 'absolute';
    toolbar.style.background = '#F56C6C';
    toolbar.style.border = '1px solid #ccc';
    toolbar.style.padding = '5px';
    toolbar.style.borderRadius = '5px'; // 设置圆角
    toolbar.style.left = `${receivedFromHtml.mouseX}px`;
    toolbar.style.top = `${receivedFromHtml.mouseY + 150}px`;
    watchEffect(() => {
      
      lang = localStorage.getItem('lang');
      if(lang === 'zh'){
        toolbar.innerHTML = '<el-button id="collect-btn" type="primary">收藏</el-button>';
      } else {
        toolbar.innerHTML = '<el-button id="collect-btn" type="primary">Collect</el-button>';
      }
    });
    document.body.appendChild(toolbar);
    // 收藏按钮事件
    document.getElementById('collect-btn')?.addEventListener('click', function () {
      // 执行收藏函数
      handleNotification();
      // 关闭选择栏
      document.body.removeChild(toolbar);
    });
    // 设置定时器，1秒后移除选择栏
    setTimeout(() => {
      if (document.body.contains(toolbar)) {
        document.body.removeChild(toolbar);
      }
    }, 1500);
    // 点击空白区域和鼠标滚轮时移除选择栏
    const removeToolbar = () => {
      if (document.body.contains(toolbar)) {
        document.body.removeChild(toolbar);
      }
      document.removeEventListener('click', removeToolbar);
      document.removeEventListener('wheel', removeToolbar);
    };
    document.addEventListener('click', removeToolbar);
    document.addEventListener('wheel', removeToolbar);
  }
};
// 收藏提示
const handleNotification = async () => {
  // 打开对话框
  collect.value = true;
  // 获取用户收藏夹数组
  const res = await getUserFavorites(userId);
  favorites.value = res.data;
}

// 点击收藏
const handleCollect = () => {
  const collectId = favorites.value.find((ele: { className: string; }) => floderName.value === ele.className)?.classId;
  receivedFromHtml.collectType = receivedFromHtml.collectType === 'manu' ? '选中' : '段落';
  collectParagraphInfo(collectId, userId, articleId.value, receivedFromHtml.content, receivedFromHtml.paragraphId, JSON.stringify(receivedFromHtml.entities), receivedFromHtml.collectType)
    .then(() => {
      // ElMessage.success('收藏成功!');
      ElMessage.success(t('messages.mes_fav_collect_suc'));
    })
    .catch(() => {
      // ElMessage.error('收藏失败!');
      ElMessage.error(t('messages.mes_fav_collect_suc_err'));
    });
  collect.value = false;
}

// 点击新增收藏夹对话框
const handleFolder = (ev: MouseEvent) => {
  addFolder.value = true;
  (ev.currentTarget as HTMLElement).blur(); // 强制失去焦点
}
const formRef = ref(null);
// 新增收藏夹
const addNewFloder = () => {
  // 1. 表单验证
  formRef.value?.validate(async (valid: boolean) => {
    if (valid) {
      // 2. 拿到收藏夹文件名 添加到文件夹列表
      try {
        const response = await addUserFavorites(form.value.addFolderName, userId);

        if (response.code === 500) {
          // ElMessage.error('收藏夹重名!');
          ElMessage.error(t('messages.mes_fav_repeat'));
        } else {
          // ElMessage.success('增加成功!');
          ElMessage.success(t('messages.mes_fav_add'));
          // 将收藏夹替换成新增的
          floderName.value = form.value.addFolderName;
          // 更新收藏夹 
          const res = await getUserFavorites(userId);
          favorites.value = res.data;
          // 3. 关闭增加收藏夹对话框
          addFolder.value = false;
        }
      } catch (error) {
        // ElMessage.error('添加收藏夹失败，请重试。');
        ElMessage.error(t('messages.mes_fav_again_collect'));
      }
    } else {
      console.log('表单验证失败');
      return false;
    }
  });
};

const htmlContent = ref('');
//传给子组件 在组件挂载时添加事件监听器
onMounted(async () => {
  // 先获取 collectedIds 数据
  articleId.value = route.query.articleId ? JSON.parse(route.query.articleId) : '';
  try {
    const res = await getAllUserCollect(userId, articleId.value);
    collectedIds.value = res.data;
  } catch (error) {
    console.error('获取 collectedIds 失败:', error);
  }
  url.value = route.query.url ? JSON.parse(route.query.url) : '';
  // console.log("url.value", url.value);
  // url.value.replace('http://ask.genemed.tech/report/', '/iframe/');
  // console.log("url.value", url.value);
  loading.value = false;
  // 通过 postMessage 传递数据给 iframe
  if (iframe.value) {
    iframe.value.onload = () => {
      try {
        // 使用 JSON.stringify 和 JSON.parse 保证数据可序列化
        const serializedData = JSON.parse(JSON.stringify({ collectedIds: collectedIds.value }));
        // 使用 postMessage 传递数据
        iframe.value!.contentWindow?.postMessage(serializedData, '*');
      } catch (error) {
        console.error('serializedData数组不可序列化!', error);
      }
    };
  }
  window.addEventListener('message', handleContentCollected);
  window.addEventListener('message', function(event) {
    if (event.origin !== 'https://medseeker.genemed.tech') return;
    if (event.data.type === 'REQUEST') {
        // 处理请求并发送响应
        event.source.postMessage({ type: 'RESPONSE', data: 'response data' }, event.origin);
    }
  });
});

// 在组件卸载前移除事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('message', handleContentCollected);
});

// 返回报告列表
const returnReportList = ()=> {
  router.push({name:"result"});
}
</script>

<style scoped>
.button_center {
  text-align: center;
}

.delete-btn {
  margin-left: auto;
}

.ellipsis {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 10ch;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  float: left;
}
</style>