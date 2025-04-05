import { createApp } from 'vue'
// import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// import 'element-plus/dist/index.css'

import 'default-passive-events' // 解决Chrome增加新的事件捕获机制而产生的错误
import '../src/utils/browserPatch' //解决Chrome增加新的事件捕获机制而产生的错误

import router from './router'                   
import { createPinia } from 'pinia' // 使用pinia状态管理工具

import i18n from './local' // 引入国际化
const pinia = createPinia()

const app = createApp(App)
// app.provide('router', router)
app.use(ElementPlus)
app.use(router)
app.use(pinia)
app.use(i18n)
app.mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}


