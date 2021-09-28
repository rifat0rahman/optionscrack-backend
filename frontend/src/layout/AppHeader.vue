<template>
    <header class="header-global">
        <base-nav class="navbar-main" transparent type="" effect="light" expand>
            <router-link slot="brand" class="navbar-brand mr-lg-5" to="/">
                <a class="navbar-brand"  href="/" >Optionscrack</a>
            </router-link>

            <div class="row" slot="content-header" slot-scope="{closeMenu}">
                <div class="col-6 collapse-brand">
                    <a href="https://demos.creative-tim.com/vue-argon-design-system/documentation/">
                        <img src="img/brand/blue.png">
                    </a>
                </div>
                <div class="col-6 collapse-close">
                    <close-button @click="closeMenu"></close-button>
                </div>
            </div>

            <ul class="navbar-nav navbar-nav-hover align-items-lg-right">
                <base-dropdown class="nav-item" menu-classes="dropdown-menu-xl">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <i class="ni ni-ui-04 d-lg-none"></i>
                        <span class="nav-link-inner--text">Options Tools</span>
                    </a>
                    <div class="dropdown-menu-inner">
                        <router-link slot="brand" class="media d-flex align-items-center" to="/simulator">
                        <a href="#"
                           class="media d-flex align-items-center">
                            <div class="icon icon-shape bg-gradient-warning rounded-circle text-white">
                                <i class="ni ni-spaceship"></i>
                            </div>
                            <div class="media-body ml-3">
                                <h6 class="heading text-warning mb-md-1">Options Simulator</h6>
                                <p class="description d-none d-md-inline-block mb-0">Validate your discretionary strategy on historical data.</p>
                            </div>
                            
                        </a>
                        </router-link>

                        <a href="https://demos.creative-tim.com/vue-argon-design-system/documentation/"
                           class="media d-flex align-items-center">
                            <div class="icon icon-shape bg-gradient-warning rounded-circle text-white">
                                <i class="fa fa-money"></i>
                            </div>
                            <div class="media-body ml-3">
                                <h6 class="heading text-warning mb-md-1">Position Analyzer</h6>
                                <p class="description d-none d-md-inline-block mb-0">Analyze your positions payoff.</p>
                            </div>
                        </a>
                        <a href="https://demos.creative-tim.com/vue-argon-design-system/documentation/"
                           class="media d-flex align-items-center">
                            <div class="icon icon-shape bg-gradient-warning rounded-circle text-white">
                                <i class="fa fa-lightbulb-o" aria-hidden="true"></i>
                            </div>
                            <div class="media-body ml-3">
                                <h5 class="heading text-warning mb-md-1">Strategy Explorer</h5>
                                <p class="description d-none d-md-inline-block mb-0">Explore and understand strategies with the help of payoff chart</p>
                            </div>
                        </a>
                    </div>
                </base-dropdown>
                <base-dropdown tag="li" class="nav-item">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <i class="ni ni-collection d-lg-none"></i>
                        <span class="nav-link-inner--text">Knowledge Hub</span>
                    </a>
                    <router-link to="/landing" class="dropdown-item">Options basics</router-link>
                    <router-link to="/profile" class="dropdown-item">Options greeks</router-link>
                    <router-link to="/login" class="dropdown-item">Risk management</router-link>
                </base-dropdown>
            </ul>

            <ul class="navbar-nav navbar-nav-hover align-items-lg-right ml-lg-auto">
                <li class="nav-item">
                    <base-dropdown tag="li" class="nav-item">
                    <a slot="title" href="#" class="nav-link" data-toggle="dropdown" role="button">
                        <i class="fa fa-google" aria-hidden="true"></i>
                        <span class="nav-link-inner--text">Login</span>
                    </a>
                    <router-link to="/login" class="dropdown-item">Login</router-link>
                    <router-link to="/profile" class="dropdown-item">Disclaimer</router-link>
                    </base-dropdown>
                </li>
            </ul>
              
        </base-nav>
    </header>
</template>
<script>
import BaseNav from "@/components/BaseNav";
import BaseDropdown from "@/components/BaseDropdown";
import CloseButton from "@/components/CloseButton";

export default {
  components: {
    BaseNav,
    CloseButton,
    BaseDropdown
  }
};
</script>
<style>
</style>
