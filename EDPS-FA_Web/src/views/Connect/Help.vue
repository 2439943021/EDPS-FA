<template>
    <div style="margin-left: 9%">
        <!-- <a href="http://ask.genemed.tech/report/20241211152945517/33382412/33382412.html" style="" target="_blank">
            <el-button type="primary" size="large" style="font-size: 25px;">{{$t('messages.viewSampleReport1')}}</el-button>
        </a>
        <a href="http://ask.genemed.tech/report/20241211072754392/38469092/38469092.html" target="_blank">
            <el-button type="primary" size="large" style="font-size: 25px; margin-left: 2%">{{$t('messages.viewSampleReport2')}}</el-button>
        </a> -->
        <a href="https://medseeker.genemed.tech/details?url=%22https://ask.genemed.tech/report/20250111105839623/38469092/38469092.html%22&articleId=%221877910273377988610%22" style="" target="_blank">
            <el-button type="primary" size="large" style="font-size: 25px;">{{$t('messages.viewSampleReport1')}}</el-button>
        </a>
        <a href="https://medseeker.genemed.tech/details?url=%22https://ask.genemed.tech/report/20250111110801721/33382412/33382412.html%22&articleId=%221877910395876831233%22" target="_blank">
            <el-button type="primary" size="large" style="font-size: 25px; margin-left: 2%">{{$t('messages.viewSampleReport2')}}</el-button>
        </a>
    </div>
    <div style="float: left;">
        <el-affix :offset="220" style="height: 0px;">
            <div style="margin-bottom: 10px;">
                <el-text size="large" tag="b" class="navigation">{{ $t('messages.navigation') }}</el-text>
            </div>
            <div>
                <a @click="scrollTo('MedSeekerDef')">
                    <el-button link type="primary" class="navigation">{{
                        $t('messages.whatismedseeker_title2') }}</el-button>
                </a>

            </div>
            <div>
                <a @click="scrollTo('Submit')"><el-button link type="primary" class="navigation">{{
                    $t('messages.submit_for_testing') }}</el-button></a>

            </div>
            <div>
                <a @click="scrollTo('Template')"><el-button link type="primary" class="navigation">{{
                    $t('messages.reportlist_title') }}</el-button></a>

            </div>
            <div>
                <a @click="scrollTo('Template')"><el-button link type="primary" class="navigation">{{
                    $t('messages.templatelist_title') }}</el-button></a>

            </div>
            <div>
                <a @click="scrollTo('Favorites')"><el-button link type="primary" class="navigation">{{
                    $t('messages.favorites_title') }}</el-button></a>

            </div>

        </el-affix>
    </div>
    <el-row :gutter="20">
        <!-- MedSeeker是什么 -->
        <el-col :span="12" :push="1" style="margin-bottom: 10px;" >
            <el-card shadow="hover" @click="navigateToPage('medseekerwhat')" title="MedSeekerDef" class="card_boder">
                <div>
                    <!-- 标题 -->
                    <div style="text-align: center;"><el-text class="cardtitle" tag="b">{{
                        $t('messages.whatismedseeker_title') }}</el-text></div>
                    <!-- 正文 -->
                    <el-text size="large" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content1')
                        }}</el-text>
                    <el-text size="large" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content2')
                        }}</el-text>
                    <el-text size="large" tag="b" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content3')
                        }}</el-text>
                    <el-text size="large" tag="b" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content4')
                        }}</el-text>
                    <el-text size="large" tag="b" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content5')
                        }}</el-text>
                    <el-text size="large" tag="b" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content6')
                        }}</el-text>
                    <el-text size="large" tag="b" type="primary" class="indented">{{
                        $t('messages.whatismedseeker_content7')
                        }}</el-text>
                    <div class="image-wrapper">
                        <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/1lunbo.png">
                    </div>
                </div>
            </el-card>
        </el-col>
        <!-- 提交检测 -->
        <el-col :span="12" :pull="1" style="margin-bottom: 10px;">
            <el-card shadow="hover" @click="navigateToPage('uploadhelp')" class="card_boder">
                <div title="Submit">
                    <div style="text-align: center;"><el-text class="cardtitle" tag="b">{{
                        $t('messages.detection_title') }}</el-text></div>
                    <div class="content-wrapper">
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.detection_content1')
                            }}</el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.detection_content2')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content3')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content4')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content5')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.detection_content6')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.detection_content7')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content8')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content9')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content10')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.detection_content11')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content12')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.detection_content13')
                            }}
                        </el-text>
                    </div>
                    <div class="image-wrapper">
                        <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help2-1-1.png">
                    </div>
                </div>
            </el-card>
        </el-col>
        <!-- 报告列表 -->
        <el-col :span="12" :push="1" style="margin-bottom: 10px;">
            <el-card shadow="hover" @click="navigateToPage('reportlisthelp')" class="card_boder">
                <div title="Report">
                    <div style="text-align: center;"><el-text class="cardtitle" tag="b">{{
                        $t('messages.reportlist_title') }}</el-text></div>
                    <div class="content-wrapper">
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.reportlist_content1')
                            }}</el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">{{
                            $t('messages.reportlist_content2')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content3')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content4')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">
                            {{ $t('messages.reportlist_content5')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content6')
                            }}
                        </el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">
                            {{ $t('messages.reportlist_content7')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content8')
                            }}
                        </el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">
                            {{ $t('messages.reportlist_content9')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content10')
                            }}
                        </el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">
                            {{ $t('messages.reportlist_content11')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content12')
                            }}
                        </el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">
                            {{ $t('messages.reportlist_content13')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content14')
                            }}
                        </el-text>
                        <el-text size="large" tag="b" type="primary" class="indented">
                            {{ $t('messages.reportlist_content15')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.reportlist_content16')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <CaretRight style="width: 15px; margin-right: 5px;" />{{
                                $t('messages.reportlist_content17')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <CaretRight style="width: 15px; margin-right: 5px;" />{{
                                $t('messages.reportlist_content18')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <CaretRight style="width: 15px; margin-right: 5px;" />{{
                                $t('messages.reportlist_content19')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <CaretRight style="width: 15px; margin-right: 5px;" />{{
                                $t('messages.reportlist_content20')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <CaretRight style="width: 15px; margin-right: 5px;" />{{
                                $t('messages.reportlist_content21')
                            }}
                        </el-text>
                    </div>
                    <div class="image-wrapper">
                        <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help3-1.png">
                    </div>
                </div>
            </el-card>
        </el-col>
        <!-- 模版列表 -->
        <el-col :span="12" :pull="1" style="margin-bottom: 10px;">
            <el-card shadow="hover" class="card_boder" @click="navigateToPage('templatehelp')">
                <div title="Template">
                    <div style="text-align: center;"><el-text class="cardtitle" tag="b">{{
                        $t('messages.templatelist_title') }}</el-text></div>
                    <div class="content-wrapper">
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.templatelist_content1')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.templatelist_content2')
                            }}</el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.templatelist_content3')
                            }}</el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.templatelist_content4')
                            }}</el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">
                            {{
                                $t('messages.templatelist_content5')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">{{
                            $t('messages.templatelist_content6')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented">
                            {{
                                $t('messages.templatelist_content7')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented">{{
                            $t('messages.templatelist_content8')
                            }}</el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.templatelist_content9')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.templatelist_content10')
                            }}
                        </el-text>
                        <el-text size="large" type="primary" class="indented_cir">
                            <!-- <CaretRight style="width: 15px; margin-right: 5px;" /> -->
                            {{
                                $t('messages.templatelist_content11')
                            }}
                        </el-text>
                    </div>
                    <div class="image-wrapper">
                        <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help4-1.png">
                    </div>
                </div>
            </el-card>
        </el-col>
        <!-- 收藏夹 -->
        <el-col :span="12" :push="1" style="margin-bottom: 10px;">
            <el-card shadow="hover" class="card_boder" @click="navigateToPage('favoriteshelp')">
                <div title="Favorites">
                    <div style="text-align: center;"><el-text class="cardtitle" tag="b">{{
                        $t('messages.favorites_title') }}</el-text></div>
                    <div class="content-wrapper">
                        <el-text size="large" type="primary" class="indented">
                            {{ $t('messages.favorites_content13') }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">
                            {{ $t('messages.favorites_content14') }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">
                            {{ $t('messages.favorites_content15') }}
                        </el-text>
                        <el-text size="large" type="primary" tag="b" class="indented">
                            {{ $t('messages.favorites_content16') }}
                        </el-text>
                    </div>
                    <div class="image-wrapper">
                        <img src="https://medseeker.genemed.tech/ask/report_css/helpimg/help5-1.png">
                    </div>
                </div>
            </el-card>
        </el-col>
    </el-row>
    <el-backtop :right="100" :bottom="100" class="gotop"></el-backtop>
</template>


<script setup lang="ts">
import { useRouter } from 'vue-router';
import { CaretRight } from '@element-plus/icons-vue';
const router = useRouter();

const navigateToPage = (page: string) => {
    console.log(page)
    router.push({ name: page })
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
.card_boder {
    border: 2px solid #000;
    border-radius: 10px;
}

.grid-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.cardtitle {
    font-size: 30px;
    color: black;
}

.content-wrapper {
    text-align: left;
    /* margin-top: 10px; */
    line-height: 1.8;
    text-indent: 2em;
}

.indented {
    text-indent: 2em;
    display: block;
    line-height: 1.8;
    font-size: 20px;
    color: black;
}

.indented_cir {
    text-indent: 2em;
    padding-left: 2em;
    display: block;
    line-height: 1.8;
    font-size: 20px;
    color: black;
}

.image-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    /* border: 2px solid #000; */
    /* border-radius: 10px; */
}

.image-wrapper img {
    width: 100%;
}

.el-card {
    margin: 10px auto;
    width: 80%;
    height: 100%;
}

/* 导航栏 */
.navigation {
    font-size: 20px;
    margin-bottom: 10px;
    color: #000;
}

/* 回到顶部 */
.gotop {
    color: #000;
}
</style>