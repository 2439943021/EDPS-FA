<template>
    <el-container>
        <el-aside width="200px">
            <el-affix :offset="300" style="display: block;">
                <div class="navigation">
                    <el-text style="margin-left: 13%; color: black;" size="large" tag="b">{{ $t('messages.navigation')
                        }}</el-text>
                </div>
                <div>
                    <a @click="scrollTo('SubmitForTesting')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.submit_for_testing') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('SelectSubmitType')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.select_submit_type') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('SelectLiteratureData')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.select_literature_data') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('SelectTemplate')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.select_template') }}</el-button></a>
                </div>
                <div><el-button link type="primary" class="navigation" @click="toHelpPag">
                        {{ $t('messages.return') }}</el-button>
                </div>
            </el-affix>
        </el-aside>
        <div style="width:83%;">
            <h1 class="tutorial" title="SubmitForTesting">{{ $t('messages.detection_detail_title') }}</h1>
            <div class="content-wrapper">
                <el-text class="indented">{{ $t('messages.detection_content1') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help2-1-1.png" alt="">
                </div>
                <el-text class="indented" title="SelectSubmitType" tag="b">{{ $t('messages.detection_content2') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content3') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content4') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content5') }}</el-text>
                <el-text class="indented" title="SelectLiteratureData" tag="b">{{ $t('messages.detection_content6') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content7') }}</el-text>
                
                <el-text class="indented_cir">{{ $t('messages.detection_content8')
                    }}</el-text>
                <el-text class="indented_cir" >{{ $t('messages.detection_content9') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content10') }}</el-text>
                <el-text class="indented" title="SelectTemplate" tag="b">{{ $t('messages.detection_content11') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content12') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.detection_content13') }}</el-text>
            </div>
        </div>
    </el-container>
    <el-backtop :right="100" :bottom="100" class="gotop"></el-backtop>
</template>
<script lang="ts" , setup>
import { useRouter } from 'vue-router';
const url = ['http://medseeker.genemed.tech/ask/report_css/helpimg/help2-2.png'];
const router = useRouter();
// 返回帮助页
const toHelpPag = () => {
    router.push({ name: 'help' });
}
// 滑动到目标元素的函数
const scrollTo = (title: string) => {
    const target = document.querySelector(`[title="${title}"]`);
    if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
};
</script>
<style scoped>
/* 帮助标题 */
.tutorial {
    background-color: #295BA7;
    color: white;
    padding: 10px;
    font-size: 23px;
    font-weight: bolder;
}

/* 帮助内容 */
.indented {
    font-size: 25px;
    text-indent: 2em;
    display: block;
    line-height: 1.8;
    color: black;
}

.indented_cir {
    text-indent: 2em;
    padding-left: 2em;
    display: block;
    line-height: 1.8;
    font-size: 25px;
    color: black;
}
.content-wrapper {
    text-align: left;
    margin-top: 10px;
    line-height: 1.8;
    /* text-indent: 2em; */
    font-family: 'Times New Roman'
}

/* 图片 */
.image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
}

.image-container img {
    width: 70%;
    height: auto;
    border: 2px solid black;
    border-radius: 5px;
    padding: 5px;
}

/* 锚点 */
.navigation {
    font-size: 20px;
    margin-bottom: 20px;
    color: black;
}
/* 回到顶部 */
.gotop{
    color: black;
}
</style>