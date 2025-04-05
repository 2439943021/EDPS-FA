<template>
    <div class="favorites">
        <el-container>
            <el-aside class="aside">
                <el-menu :default-openeds="['1']" style="width: 200px;background: linear-gradient(to top, #ecf5ff0b, #ffffff00, #ecf5ff00)">
                    <el-sub-menu index="1">
                        <template #title>
                            <el-icon>
                                <el-icon>
                                    <CollectionTag />
                                </el-icon>
                            </el-icon>{{ $t('messages.favoritesList') }}
                        </template>
                        <el-menu-item-group>
                            <el-menu-item @click="handleAddFolder">
                                <el-icon>
                                    <CirclePlusFilled />
                                </el-icon><span>{{ $t('messages.newFavorites') }}</span>
                            </el-menu-item>
                        </el-menu-item-group>
                        <el-menu-item-group v-for="item in collects" :key="item.index">
                            <el-menu-item :index="item.index" @click="swapFavorit(item.classId)"
                                class="split_left_and_right">
                                <div>
                                    <el-tooltip v-if="item.className.length > 5" :content="item.className"
                                        placement="top">
                                        <span class="ellipsis">{{ item.className }}</span>
                                        <!-- <span v-if="lang === 'zh' && item.className === '系统默认收藏夹'" class="ellipsis">{{
                                            $t('messages.favoritesSysName') }}</span>
                                        <span v-else>{{ item.className }}</span> -->
                                    </el-tooltip>
                                    <span v-else class="ellipsis">{{ item.className }}</span>
                                </div>
                                <el-popover placement="bottom" trigger="hover">
                                    <div style="display: flex; flex-direction: column; align-items: center;">
                                        <el-button link @click="modifyFolder(item.className, item.classId)">{{
                                            $t('messages.editMessage')
                                        }}</el-button>
                                        <el-divider />
                                        <el-button link
                                            @click="deleteFavorites(item.className, page.index, page.size)">{{
                                                $t('messages.deleteFavorites') }}</el-button>
                                    </div>
                                    <template #reference>
                                        <el-button link v-show="item.className !== '系统默认收藏夹'">
                                            <el-icon>
                                                <Setting />
                                            </el-icon>
                                        </el-button>
                                    </template>
                                </el-popover>
                            </el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu>
                </el-menu>
            </el-aside>
            <el-main>
                <el-text size="large" tag="b" style="color: #000000; margin-left: 50%; font-size: 20px;">{{ $t('messages.favorites') }}</el-text>
                <el-popconfirm width="250" :icon="InfoFilled" icon-color="#626AEF"
                    :title="$t('messages.batchDownloadTip')" @cancel="onCancel" @confirm="downloads">
                    <template #reference>
                        <el-button style="float: right; font-size: 18px; margin-bottom: 10px;" type="warning" plain
                            :icon="Share">{{
                                $t('messages.button_downloads') }}</el-button>
                    </template>
                    <template #actions="{ confirm, cancel }">
                        <el-button size="small" @click="cancel">否</el-button>
                        <el-button type="danger" size="small" @click="confirm">
                            是
                        </el-button>
                    </template>
                </el-popconfirm>
                <el-table loading.value=false; element-loading-text="Loading..." border :data="tableData" stripe
                    class="custom-table" :header-cell-style="{ color: 'black', background: 'skyblue' }" ref="dataTable"
                    @selection-change="handleSelectionChange">
                    <el-table-column type="selection" align="center" width="55" />
                    <el-table-column :label="$t('messages.index')" align="center" width="70">
                        <template v-slot="scope">
                            {{ (page.index - 1) * page.size + scope.$index + 1 }}
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" align="center" prop="pmcId" label="PMID" width="120" />
                    <el-table-column header-align="center" prop="title" :label="$t('messages.title')" width="260"
                        show-overflow-tooltip />
                    <el-table-column header-align="center" align="center" prop="author" :label="$t('messages.author')"
                        width="100" show-overflow-tooltip />
                    <el-table-column header-align="center" align="center" prop="collectType"
                        :label="$t('messages.collectionMethod')" width="100">
                        <template v-slot="{ row }">
                            {{ collectType(row.collectType) }}
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" prop="content" :label="$t('messages.collectionContent')"
                        show-overflow-tooltip>
                        <template v-slot="scope">
                            <span>
                                {{ scope.row.content.length > 200 ? scope.row.content.slice(0, 200) + '...' :
                                    scope.row.content }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column header-align="center" :label="$t('messages.operation')" width="270">
                        <template v-slot="scoped">
                            <el-button type="primary" link size="small" @click="showContent(scoped.row.content)">{{
                                $t('messages.button_details') }}</el-button>
                            <el-button type="primary" link size="small"
                                @click="showReport(scoped.row.htmlUrl, scoped.row.id)">{{ $t('messages.button_report')
                                }}</el-button>
                            <!-- <el-button link type="primary" size="small"
                                @click="downloadFile(scoped.row.pmcId,
                                    scoped.row.title, scoped.row.content, scoped.row.entity, scoped.row.className)">导出</el-button> -->
                            <el-button link type="primary" size="small" @click="downloadFile(scoped.row)">{{
                                $t('messages.button_download') }}</el-button>
                            <el-button link type="warning" size="small" @click="quitCollect(scoped.row.id, scoped.row.indexId, scoped.row.classId,
                                scoped.row.collectType, scoped.row.content)">{{ $t('messages.button_uncollect')
                                }}</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="page">
                    <!-- <el-text>共{{ page.total }}条</el-text> -->
                    <el-pagination :page-size="page.size" size="large" @current-change="handleCurrentChange" background
                        layout="total, prev, pager, next" :total="page.total" class="el-pagination" />
                </div>
            </el-main>
        </el-container>
    </div>
    <!-- 新建收藏夹对话框 -->
    <el-dialog v-model="addFolder" :title="$t('messages.favoritesInformation')" width="500">
        <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
            <el-form-item :label="$t('messages.favoritesName')" prop="addFolderName">
                <el-input v-model="form.addFolderName" maxlength="20" :placeholder="$t('messages.favoritesName')"
                    show-word-limit @keydown.enter.prevent="addNewFloder" />
            </el-form-item>
        </el-form>
        <div style="text-align: center; margin-top: 50px;">
            <el-button @click="addNewFloder">{{ $t('messages.button_confirm') }}</el-button>
        </div>
    </el-dialog>

    <!-- 编辑收藏夹对话框 -->
    <el-dialog v-model="setFolder" :title="$t('messages.favoritesInformation')" width="500">
        <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
            <el-form-item :label="$t('messages.favoritesName')" prop="addFolderName">
                <el-input v-model="form.addFolderName" maxlength="20" :placeholder="$t('messages.favoritesName')"
                    show-word-limit />
            </el-form-item>
        </el-form>
        <div style="text-align: center; margin-top: 50px;">
            <el-button @click="updateFolderName">{{ $t('messages.button_confirm') }}</el-button>
        </div>
    </el-dialog>
    <!-- 描述框 -->
    <el-dialog v-model="showCollect" :model="content">
        <el-descriptions>
            <el-descriptions-item class-name="content">{{ content }}</el-descriptions-item>
        </el-descriptions>
    </el-dialog>

</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import {
    getUserFavorites, deleteUserFavorites, addUserFavorites,
    getFavoriteMessage, modifyFavorite, favoriteExportExcel, deleteCollection
} from '../../api/index';
import { useUserStore } from '../../store/user';
import { useRouter } from 'vue-router';
import { ElMessage, ElTable } from 'element-plus';
import { CirclePlusFilled, Setting, InfoFilled, Share } from '@element-plus/icons-vue';
import { OutputCollects, Collects, TableData, Favorities } from './types';
import { collectType } from '../../utils/favorities';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
const lang = localStorage.getItem('lang') || 'zh';
// 从pinia中拿到userId
const useStroe = useUserStore();
const userId = useStroe.getInfo().user.userId;
// const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
// 表格数据
const tableData = ref<TableData[]>([])
// 控制table表格
const dataTable = ref<InstanceType<typeof ElTable> | null>(null);
// 用户收藏夹
const collects = ref<Favorities[]>([])
// 新增收藏夹名
const form = ref({
    addFolderName: '',
    classId: 0
});
// 控制新增收藏夹对话框
let addFolder = ref(false);
// 规则校验
const rules = {
    addFolderName: [{ required: true, message: '请填写收藏夹名称', trigger: 'blur' }]
};
// 分页
const page = reactive({
    index: 1,
    size: 10,
    classId: 0,
    total: 0
})
// 加载
let loading = ref(true);
// 控制分页函数
const handleCurrentChange = (val: number) => {
    // console.log('val:', val)
    page.index = val;
    getMessage(page.index, page.size, page.classId);
}
onMounted(async () => {
    await getFavorites();
    getMessage(page.index, page.size, collects.value[0].classId);
    loading.value = false;
})
// 获取用户收藏数据
const getMessage = async (index: number, size: number, classId: number) => {
    const res = (await getFavoriteMessage(index, size, classId)).data;
    tableData.value = res.records;
    page.total = res.total;
    // console.log('page.total:', page.total);

}
// 获取用户收藏夹
const getFavorites = async () => {
    const res = await getUserFavorites(userId);
    // 为每个对象添加一个 index 属性
    collects.value = res.data.map((item: any, idx: number) => ({
        ...item,
        index: String(idx + 1) // 将索引转换为字符串
    }));
    // 给page. classId设置初值
    page.classId = collects.value[0].classId;
}
// 删除收藏夹
const deleteFavorites = (className: string, index: number, size: number) => {
    // console.log("className:", className, "userId", userId);
    deleteUserFavorites(className, userId)
        .then(() => {
            // ElMessage.success('删除成功!');
            ElMessage.success(t('messages.mes_rep_del_suc'));
            // 获取新的收藏夹列表
            getFavorites();
            // 删除原来的收藏夹，将其里面含有的数据移动至默认收藏夹中
            getMessage(index, size, collects.value[0].classId);
        })
        .catch((err) => {
            console.log('发生错误!', err);
        });
}

// 新增
const handleAddFolder = () => {
    addFolder.value = true;
};

// 新增收藏夹
const formRef = ref(null);
const addNewFloder = () => {
    // 1.表单验证
    formRef.value?.validate((valid: boolean) => {
        if (valid) {
            // 2.拿到收藏夹文件名 添加到文件夹列表
            addUserFavorites(form.value.addFolderName, userId)
                .then(async (response) => {
                    if (response.code === 500) {
                        // ElMessage.error('收藏夹重名!');
                        ElMessage.error(t('messages.mes_fav_repeat'));
                    } else {
                        // ElMessage.success('增加成功!');
                        ElMessage.success(t('messages.mes_fav_add'));
                        // 更新收藏夹 
                        getFavorites();
                    }
                });
            // 3.关闭增加收藏夹对话框
            addFolder.value = false;
        } else {
            console.log('表单验证失败');
            return false;
        }
    });
};
// 切换不同的收藏夹
const swapFavorit = async (classId: number) => {
    page.index = 1;
    page.total = 0;
    page.classId = classId;
    console.log("page.classId", page.classId);
    getMessage(page.index, page.size, classId);
}
// 编辑收藏夹信息
const setFolder = ref(false);
const modifyFolder = (className: string, classId: number) => {
    setFolder.value = true;
    form.value.addFolderName = className;
    form.value.classId = classId;
}
// 确认修改
const updateFolderName = () => {
    // 1.表单验证
    formRef.value?.validate((valid: boolean) => {
        if (valid) {
            modifyFavorite(form.value.addFolderName, form.value.classId)
                .then(() => {
                    // ElMessage.success("修改成功!");
                    ElMessage.success(t('messages.mes_fav_modifind'));
                    getFavorites();
                })
                .catch(() => {
                    // ElMessage.success("修改失败!");
                    ElMessage.success(t('messages.mes_fav_modifind_err'));
                });
            // 3.关闭修改收藏夹对话框
            setFolder.value = false;
        } else {
            console.log('表单验证失败');
            return false;
        }
    });
}

// 查看收藏报告
// 设置路由器
const router = useRouter();
const showReport = (htmlUrl: string, reportId: string) => {
    const url = JSON.stringify(htmlUrl);
    const articleId = JSON.stringify(reportId)
    router.push({ name: 'details', query: { url, articleId } });
}

// 导出
const downloadFile = (row: any) => {
    let excelOutput: Collects[] = [];
    excelOutput.push(row);
    // 判断是否有实体
    if (row.entity === null) {
        row.entity = [];
        row.entities = [];
    } else {
        excelOutput[0].entities = JSON.parse(excelOutput[0].entity);
    }
    // 清空数据
    favoriteExportExcel(excelOutput)
        .then(response => {
            // 创建 blob
            let blob = new Blob([response], { type: 'application/vnd.ms-excel' });
            // 创建 href 超链接，点击进行下载
            window.URL = window.URL || window.webkitURL;
            let href = URL.createObjectURL(blob);
            let downA = document.createElement("a");
            downA.href = href;
            downA.download = excelOutput[0].title;
            downA.click();
            // 销毁超连接
            window.URL.revokeObjectURL(href);
        })
        .catch(error => {
            console.error('文件下载失败:', error);
        });
}

// 取消收藏
const quitCollect = (articleId: string, indexId: string, classId: number, collectType: string, content: string) => {
    deleteCollection(userId, articleId, indexId, collectType, content)
        .then(() => {
            // ElMessage.success('取消收藏成功!');
            ElMessage.success(t('messages.mes_fav_quit_collect'));
            getMessage(page.index, page.size, classId);
        });
}

// 查看收藏内容
let content = ref('');
let showCollect = ref(false);
const showContent = (collectValue: string) => {
    showCollect.value = true;
    content.value = collectValue
}
// 批量导出
let multipleSelection = ref<Collects[]>([]);
// 获取所选择行的数据
const handleSelectionChange = (collects: Collects[]) => {
    multipleSelection.value = collects;
    // console.log(multipleSelection.value);    
}
const onCancel = () => {

}
let collectionExcelReqDtoList = ref<OutputCollects[]>([]);
// 批量下载
const downloads = () => {
    // debugger
    // console.log(multipleSelection.value);
    if (multipleSelection.value && multipleSelection.value.length > 0) {
        collectionExcelReqDtoList.value = multipleSelection.value.map(item => {
            const { className, pmcId, title, content, collectType } = item;
            // 使用 JSON.parse 将 entities 转换为对象格式
            let entities = [];
            try {
                entities = item.entity ? JSON.parse(item.entity) : [];
            } catch (error) {
                entities = []; // 解析失败时设置为默认空对象
            }
            return { className, entities, pmcId, title, content, collectType };
        });
        // console.log("collectionExcelReqDtoList:", collectionExcelReqDtoList.value);
        const excelOutput = collectionExcelReqDtoList.value;
        favoriteExportExcel(excelOutput).then(response => {
            // 创建 blob
            let blob = new Blob([response], { type: 'application/vnd.ms-excel' });
            // 创建 href 超链接，点击进行下载
            window.URL = window.URL || window.webkitURL;
            let href = URL.createObjectURL(blob);
            let downA = document.createElement("a");
            downA.href = href;
            downA.download = "批量导出";
            downA.click();
            // 销毁超连接
            window.URL.revokeObjectURL(href);
        })
            .catch(error => {
                console.error('文件下载失败:', error);
            });
    }

};

// 使用计算属性动态切换收藏类型的中英文
// const collectType

</script>

<style scoped>
.favorites {

    height: 90%;
}

.aside {
    width: 200px;
    font-weight: bolder;
    margin-top: 4%;
}

.ellipsis {
    display: inline-block;
    max-width: 10ch;
    /* 限制最多显示5个字符 */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.hover-button {
    display: none;
}

.el-menu-item:hover .hover-button {
    display: inline-flex;
}

.split_left_and_right {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.el-pagination {
    font-size: 17px;
    font-weight: bold;
    margin-top: 5px;
    float: right;
}

.custom-table {
    width: 100%;
    font-family: Arial, sans-serif;
    /* 设置字体 */
    font-size: 15px;
    font-weight: bolder;
    /* 设置字号 */
    color: black;
    /* 设置文字颜色 */
}


.el-main {
    --el-main-padding: 0px;
}

.page {
    display: flex;
    justify-content: flex-end;
}

:deep(.content) {
    font-family: Arial, sans-serif;
    font-size: 15px;
    color: black;
}
</style>