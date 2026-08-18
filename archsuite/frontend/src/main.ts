import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/global.scss'

// 应用入口：装配 Pinia 与路由并挂载
const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
