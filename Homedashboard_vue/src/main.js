import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
// import plugin from "vue-axios";



axios.defaults.baseURL = 'http://127.0.0.1:8000'
const app = createApp(App)

//createApp(App).mount('#app')

// app.use(store)
app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.mount('#app')