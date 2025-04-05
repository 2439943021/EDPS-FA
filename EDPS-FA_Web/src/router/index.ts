import { createRouter, createWebHistory } from 'vue-router'
import Result from '..//views/LookReport/Result.vue'
import Connect from '../views/Connect/Connect.vue'
import Report from '../views/TemplateExport/Report.vue'

// 提交检测路由
import SubmitForTest from '../views/SubmitForTest/SubmitForTest.vue'
import SubmitByPmid from '../views/SubmitForTest/SubmitByPmid.vue'
import SubmitByExcel from '../views/SubmitForTest/SubmitByExcel.vue'
import SubmitByPdf from '../views/SubmitForTest/SubmitByPdf.vue'

// 自定义模板路由
import Example from '../views/Example/Example.vue'
import CreateTemp from '../views/Example/CreateTemp.vue'
import Edit from '../views/Example/Edit.vue'
import ExampleList from '../views/Example/List.vue'

// 下拉菜单
import Person from '../views/DropDown/Person.vue'
import Member from '../views/DropDown/Member.vue'

// 微信登录
import WxLogin from '../views/Login/Login.vue'
// 收藏夹
import Favorites from '../views/Favorites/Favorites.vue'

// 帮助
import MedseekerWhat from '../views/Connect/MedseekerWhat.vue'
import Help from '../views/Connect/Help.vue'
import UploadHelp from '../views/Connect/UploadHelp.vue'
import ReportListHelp from '../views/Connect/ReportListHelp.vue'
import TemplateHelp from '../views/Connect/TemplateHelp.vue'
import FavoritesHelp from '../views/Connect/FavoritesHelp.vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/submitfortest/submitbypmid',
            name: 'redirect'
        },
        {
            path: '/submitfortest',
            name: 'submitfortest',
            component: SubmitForTest,
            children: [
                { path: 'submitbypmid', component: SubmitByPmid },
                { path: 'submitbyexcel', component: SubmitByExcel },
                { path: 'submitbypdf', component: SubmitByPdf }
            ]
        },
        {
            path: '/result',
            name: 'result',
            component: Result
        },
        {
            path: '/connect',
            name: 'connect',
            component: Connect,
            redirect: '/connect/help',
            children: [
                { path: 'medseekerwhat', name: 'medseekerwhat', component: MedseekerWhat },
                { path: 'help', name: 'help', component: Help },
                { path: 'uploadhelp', name: 'uploadhelp', component: UploadHelp },
                { path: 'reportlisthelp', name: 'reportlisthelp', component: ReportListHelp },
                { path: 'templatehelp', name: 'templatehelp', component: TemplateHelp },
                { path: 'favoriteshelp', name: 'favoriteshelp', component: FavoritesHelp }
            ]
        },
        {
            path: '/report',
            component: Report
        },
        {
            path: '/example',
            component: Example,
            name: 'example',
            redirect: '/example/list',
            children: [
                {
                    path: 'list',
                    name: 'ExampleList',
                    component: ExampleList
                },
                {
                    path: 'createtemp',
                    name: 'createtemp',
                    component: CreateTemp
                },
                {
                    path: 'edit',
                    name: 'edit',
                    component: Edit
                },
                {
                    path: 'bigmodeledit',
                    name: 'bigmodeledit',
                    component: () => import('../views/Example/BigModelTempEdit.vue')
                }
            ]
        },
        {
            path: '/login',
            name: 'wxlogin',
            component: WxLogin
        },
        {
            path: '/person',
            name: 'person',
            component: Person
        },
        {
            path: '/member',
            name: 'member',
            component: Member
        },
        {
            path: '/favorites',
            name: 'favorites',
            component: Favorites
        },
        {
            path: '/details',
            name: 'details',
            component: () => import('../views/LookReport/Details.vue')
        }
    ]
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem("isAuthenticated");
    if (to.name !== 'wxlogin' && !isAuthenticated) {
        next({ name: 'wxlogin' });
    } else {
        next();
    }
});
export default router