import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { compression } from 'vite-plugin-compression2'
import { autoComplete, Plugin as importToCDN } from "vite-plugin-cdn-import"
import { visualizer } from 'rollup-plugin-visualizer';

// https://vitejs.dev/config/
export default defineConfig(({ mode })=>{
  // 加载环境变量
  const env = loadEnv(mode, process.cwd());
  return {
    plugins: [
      vue(),
      // visualizer({
      //   emitFile: false,
      //   filename: 'analysis-chart.html', // 分析图生成的文件名
      //   open:false // 如果存在本地服务端口，将在打包后自动展示
      // }),
      // 就是使用这个插件实现的文件压缩
      compression({
        threshold:2000, // 设置只有超过 2k 的文件才执行压缩
        deleteOriginalAssets:false, // 设置是否删除原文件
        skipIfLargerOrEqual:true, // 如果压缩后的文件大小与原文件大小一致或者更大时，不进行压缩
        // 其他的属性暂不需要配置，使用默认即可
      }),
      importToCDN({
        modules:[
          {
            name: 'vue',
            var: 'Vue',
            // path:'http://medseeker.genemed.tech/ask/report_css/vue.global.js'
            path:'https://medseeker.genemed.tech/ask/report_css/vue.global.prod.js'
          },
          {     
            name: 'vue-demi',
            var: 'VueDemi',
            path:'https://medseeker.genemed.tech/ask/report_css/vue-demi.index.iife.js'
          },
          {
            name:'pinia',
            var:'Pinia',
            path:'https://medseeker.genemed.tech/ask/report_css/pinia.iife.min.js'
          },
          {
            name: 'element-plus',
            var: 'ElementPlus',
            // path: 'https://cdn.bootcdn.net/ajax/libs/element-plus/2.3.12/index.full.js',
            // css:'https://cdn.bootcdn.net/ajax/libs/element-plus/2.3.12/index.css'
            // path:'http://medseeker.genemed.tech/ask/report_css/element-index.full.js',
            // css:'http://medseeker.genemed.tech/ask/report_css/element-cssindex.css'
            path:'https://medseeker.genemed.tech/ask/report_css/ele_index.full.js',
            css:'https://medseeker.genemed.tech/ask/report_css/ele_index.css'
          },
          {
            name: '@element-plus/icons-vue',
            var: 'ElementPlusIconsVue', // 根据main.js中定义的来
            path: 'https://medseeker.genemed.tech/ask/report_css/Iconsglobal.iife.js'
          },
          {
            name:'jszip',
            var:'JSZip',
            path:'https://medseeker.genemed.tech/ask/report_css/jszip.min.js',
          },
          {
            name:'qiniu-js',
            var:'qiniu',
            path:'https://medseeker.genemed.tech/ask/report_css/qiniu.min.js'
          },
          {
            name:'xlsx',
            var:'XLSX',
            path:'https://medseeker.genemed.tech/ask/report_css/xlsx.full.min.js'
          },
        ]
      })
    ],
    build: {
      outDir: env.VITE_OUTPUT_DIR,
      rollupOptions: {
        output: {
          // 使用 Vite 的默认文件名格式
        },
      },
    },
    server: {
      proxy: {
        '/api': {
          target: env.VITE_PROXY_TARGET,
          changeOrigin: true, // 将请求头中的 host 设置为 target
          rewrite: (path) => path.replace(/^\/api/, ''), // 重写请求路径，去掉 '/api' 前缀
          headers: {
            // 可选的请求头配置
            // 'Authorization': 'Bearer token'
          },
          // 可选的其他选项
          // 如果需要，你还可以配置代理的其他选项，如 cookieDomainRewrite、pathRewrite 等
        }
        
      }
    },
  }
})
