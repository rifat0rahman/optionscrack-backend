
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Argon from "./plugins/argon-kit";
import './registerServiceWorker';
import { BootstrapVue } from 'bootstrap-vue';
import '@/plugins/apexcharts'
import VueCompositionAPI from '@vue/composition-api';

import '@vueform/slider/themes/default.css';

export const base = 'https://optionscrack.pythonanywhere.com'

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(VueCompositionAPI);
Vue.use(Argon);
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
