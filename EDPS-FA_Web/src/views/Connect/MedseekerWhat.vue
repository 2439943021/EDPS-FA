<template>
    <el-container>
        <el-aside width="200px">
            <el-affix :offset="380" style="display: block;">
                <div class="navigation">
                    <el-text style="margin-left: 16%; color: black;" size="large" tag="b">{{ $t('messages.navigation') }}</el-text>
                </div>
                <div>
                    <a @click="scrollTo('PlatformIntroduction')"><el-button class="navigation"  type="primary"
                            link>{{ $t('messages.platform_introduction') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('FunctionModule')"><el-button class="navigation" type="primary"
                            link>{{ $t('messages.function_module') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('FunctionIntroduction')"><el-button class="navigation" type="primary"
                            link>{{ $t('messages.function_introduction') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('ReportComposition')"><el-button class="navigation" type="primary"
                            link>{{ $t('messages.report_composition') }}</el-button></a>
                </div>
                <div>
                    <a @click="scrollTo('CollectionMethod')"><el-button class="navigation" type="primary"
                            link>{{ $t('messages.collection_method') }}</el-button></a>
                </div>
                <div><el-button link type="primary" class="navigation" @click="toHelpPag">
                        {{ $t('messages.return') }}</el-button>
                </div>
            </el-affix>
        </el-aside>
        <div style="width:83%;">
            <h1 class="tutorial" title="PlatformIntroduction">{{ $t('messages.whatismedseeker_detail_title') }}</h1>
            <div class="content-wrapper">
                <el-text class="indented">{{ $t('messages.whatismedseeker_content8') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content9') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content42') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help1-5.jpg" alt="">
                </div>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content10') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content11') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content12') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content13') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content14') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/1lunbo.png" alt="">
                </div>
                <el-text class="indented" title="FunctionModule">{{ $t('messages.whatismedseeker_content15')
                    }}</el-text>
                <el-text class="indented" tag="b">{{ $t('messages.whatismedseeker_content16') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content17') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content18') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content19') }}</el-text>
                <el-text class="indented" tag="b">{{ $t('messages.whatismedseeker_content20') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content21') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content22') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content23') }}</el-text>
                <el-text class="indented" title="FunctionIntroduction" tag="b">{{ $t('messages.whatismedseeker_content24')
                    }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content25') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content26') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content27') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content28') }}</el-text>
                <el-text class="indented" tag="b">{{ $t('messages.whatismedseeker_content41') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/2lunbo.png" alt="">
                </div>
                <el-text class="indented" title="ReportComposition">{{ $t('messages.whatismedseeker_content29')
                    }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content30') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content31') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content32') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content33') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content34') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content35') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content36') }}</el-text>
                <div class="image-container">
                    <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help1-4.png" alt="">
                </div>
                <el-text class="indented" title="CollectionMethod" tag="b">{{ $t('messages.whatismedseeker_content37')
                    }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content38') }}</el-text>
                <el-text class="indented_cir">{{ $t('messages.whatismedseeker_content39') }}</el-text>
                <el-text class="indented">{{ $t('messages.whatismedseeker_content40') }}</el-text>
                
            </div>
        </div>
    </el-container>
    <el-backtop :right="100" :bottom="100" class="gotop"></el-backtop>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const url = [
    'http://medseeker.genemed.tech/ask/report_css/helpimg/1lunbo.png',
    'http://medseeker.genemed.tech/ask/report_css/helpimg/2lunbo.png'
];

const router = useRouter();
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
/* 缩进 */
.indented_cir {
    font-size: 25px;
    text-indent: 2em;
    padding-left: 2em;
    display: block;
    line-height: 1.8;
    color: black;
}
.content-wrapper {
    text-align: left;
    margin-top: 10px;
    line-height: 1.8;
    text-indent: 2em;
    font-family:'Times New Roman'
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