import Vue from "vue";
import Router from "vue-router";
import AppHeader from "./layout/AppHeader";
import AppFooter from "./layout/AppFooter";
import Home from "./views/Home.vue";
import Disclaimer from "./views/Disclaimer.vue";
import Simulator from "./views/Simulator.vue";


Vue.use(Router);

export default new Router({
  linkExactActiveClass: "active",
  routes: [
    {
      path: "/",
      name: "Home",
      components: {
        header: AppHeader,
        default: Home,
        footer: AppFooter
      }
    },

    {
      path: "/simulator",
      name: "Simulator",
      components: {
        header: AppHeader,
        default: Simulator,
        footer: AppFooter
      }
    },
    {
      path: "/disclaimer",
      name: "Disclaimer",
      components: {
        header: AppHeader,
        default: Disclaimer,
        footer: AppFooter
      }
    }
  ],
  scrollBehavior: to => {
    if (to.hash) {
      return { selector: to.hash };
    } else {
      return { x: 0, y: 0 };
    }
  }
});
