import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
// import the package
import VueAwesomePaginate from "vue-awesome-paginate";
// import the necessary css file
import "vue-awesome-paginate/dist/style.css";


// axios.defaults.baseURL = 'http://127.0.0.1:8000';
axios.defaults.baseURL = 'http://192.168.50.67:8000';

const app = createApp(App);

//createApp(App).mount('#app')

// app.use(store)
app.use(createPinia());
app.use(router);
app.use(VueAxios, axios);
app.use(VueAwesomePaginate);
app.mount('#app');