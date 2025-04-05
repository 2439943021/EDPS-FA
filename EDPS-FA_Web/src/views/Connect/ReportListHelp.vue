<template>
    <el-container>
        <el-aside width="200px">
            <el-affix :offset="200" style="display: block;">
                <div class="navigation">
                    <el-text style="margin-left: 13%; color: black;" size="large" tag="b">{{ $t('messages.navigation')
                        }}</el-text>
                </div>
                <div>
                    <a @click="scrollTo('ReportLlist')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.reportlist_title') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Quick_Retrieval')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Quick_Retrieval') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Bulk_Operation')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Bulk_Operation') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Template_Information')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Template_Information') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Paper_Information')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Paper_Information') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Status_and_Progress')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Status_and_Progress') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Time_Information')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Time_Information') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('Operation_on_the_Results')"><el-button class="navigation" type="primary" link>{{
                        $t('messages.Operation_on_the_Results') }}</el-button></a>
                </div>
                <div><el-button link type="primary" class="navigation" @click="toHelpPag">
                        {{ $t('messages.return') }}</el-button>
                </div>
            </el-affix>
        </el-aside>
        <div style="width:83%;">
            <h1 class="tutorial" title="ReportLlist">{{ $t('messages.reportlist_title') }}</h1>
            <div class="content-wrapper">
                <el-text class="indented">{{ $t('messages.reportlist_content1') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-1.png" alt="">
                </div>
                <el-text class="indented" title="Quick_Retrieval" tag="b">{{ $t('messages.reportlist_content2') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content3') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content4') }}</el-text>
                <el-text class="indented" title="Bulk_Operation" tag="b">{{ $t('messages.reportlist_content5') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content6') }}</el-text>
                <el-text class="indented" title="Template_Information" tag="b">{{ $t('messages.reportlist_content7') }}</el-text>
                
                <el-text class="indented_cir">{{ $t('messages.reportlist_content8')
                    }}</el-text>
                <el-text class="indented" title="Paper_Information" tag="b">{{ $t('messages.reportlist_content9') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content10') }}</el-text>
                <el-text class="indented" title="Status_and_Progress" tag="b">{{ $t('messages.reportlist_content11') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content12') }}</el-text>
                <el-text class="indented" title="Time_Information" tag="b">{{ $t('messages.reportlist_content13') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content14') }}</el-text>
                <el-text class="indented" title="Operation_on_the_Results" tag="b">{{ $t('messages.reportlist_content15') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.reportlist_content16') }}</el-text>
                <el-text class="indented_cir" style="text-indent: 4em;">{{ $t('messages.reportlist_content17') }}</el-text>
                <el-text class="indented_cir" style="text-indent: 4em;">{{ $t('messages.reportlist_content18') }}</el-text>
                <el-text class="indented_cir" style="text-indent: 4em;">{{ $t('messages.reportlist_content19') }}</el-text>
                <el-text class="indented_cir" style="text-indent: 4em;">{{ $t('messages.reportlist_content20') }}</el-text>
                <el-text class="indented_cir" style="text-indent: 4em;">{{ $t('messages.reportlist_content21') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-2.png" alt="">
                </div>
                <el-text class="indented" style="text-indent: 4em;">{{ $t('messages.reportlist_content22') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-3.png" alt="">
                </div>
                <el-text class="indented" style="text-indent: 4em;">{{ $t('messages.reportlist_content23') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-4.png" alt="">
                </div>
                <el-text class="indented" style="text-indent: 4em;">{{ $t('messages.reportlist_content24') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-5.png" alt="">
                </div>
                <el-text class="indented" style="text-indent: 4em;">{{ $t('messages.reportlist_content25') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-6.png" alt="">
                </div>
                <el-text class="indented" style="text-indent: 4em;">{{ $t('messages.reportlist_content26') }}</el-text>
            </div>
        </div>
    </el-container>
    <el-backtop :right="100" :bottom="100" class="gotop"></el-backtop>
</template>
<script lang="ts", setup>
import { useRouter } from 'vue-router';
const url = ['http://medseeker.genemed.tech/ask/report_css/helpimg/help3-2.png'];
const router = useRouter();
const toHelpPag = () => {
    router.push({name:'help'});
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
    text-indent: 2em;
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