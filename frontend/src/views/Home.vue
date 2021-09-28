<template>
    <div>

        <div class="position-relative">
            <!-- shape Hero -->
            <section class="section-shaped my-0">
                <div class="shape shape-style-3 shape-default shape-skew">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="container shape-container d-flex">
                    <div class="col px-0">
                        <div class="row">
                            <div class="col-lg-6">
                                <h1 class="display-3  text-white">Trade Options Smarter
                                    <span>Find your edge in options trading with our free tools</span>
                                </h1>
                                <p class="lead  text-white">The platform comes with information tools to help
                                    you get started in Options trading. You can review your strategies and basics before going live.</p>
                                <div class="btn-wrapper">
                                    <base-button tag="a"
                                                 href="https://demos.creative-tim.com/argon-design-system/docs/components/alerts.html"
                                                 class="mb-3 mb-sm-0"
                                                 type="info"
                                                 icon="fa fa-play" aria-hidden="true"
                                                 >
                                        Get started
                                    </base-button>
                                    <base-button tag="a"
                                                 href="https://www.creative-tim.com/product/argon-design-system"
                                                 class="mb-3 mb-sm-0"
                                                 type="white"
                                                 icon="fa fa-youtube"
            
                                                 >
                                        Learn more </base-button>
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <!-- 1st Hero Variation -->
        </div>
        <section class="section section-lg pt-lg-0 mt--200">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-12">
                        <div class="row row-grid">
                            <div class="col-lg-4">
                                <card class="border-0" hover shadow body-classes="py-5">
                                    <icon name="ni ni-check-bold" type="primary" rounded class="mb-4">
                                    </icon>
                                    <h6 class="text-primary text-uppercase">Options as a hedging tool</h6>
                                    <p class="description mt-3">Watch this short story to understand how options contract work.</p>
                                    <div>
                                        <b-embed
                                            type="iframe"
                                            aspect="16by9"
                                            src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0"
                                            allowfullscreen
                                        ></b-embed>
                                    </div>
                                    <div>
                                        <badge type="primary" rounded>Options contract</badge>
                                        <badge type="primary" rounded>Call options</badge>
                                        <badge type="primary" rounded>Put options</badge>
                                    </div>
                                    <base-button tag="a" href="#" type="primary" class="mt-4">
                                        Learn more
                                    </base-button>
                                </card>
                            </div>
                            <div class="col-lg-4">
                                <card class="border-0" hover shadow body-classes="py-5">
                                    <icon name="ni ni-istanbul" type="success" rounded class="mb-4">
                                    </icon>
                                    <h6 class="text-success text-uppercase">Why you should look at the greeks</h6>
                                    <p class="description mt-3">Argon is a great free UI package based on Bootstrap
                                        4 that includes the most important components and features.</p>
                                    <div>
                                        <badge type="success" rounded>business</badge>
                                        <badge type="success" rounded>vision</badge>
                                        <badge type="success" rounded>success</badge>
                                    </div>
                                    <base-button tag="a" href="#" type="success" class="mt-4">
                                        Learn more
                                    </base-button>
                                </card>
                            </div>
                            <div class="col-lg-4">
                                <card class="border-0" hover shadow body-classes="py-5">
                                    <icon name="ni ni-planet" type="warning" rounded class="mb-4">
                                    </icon>
                                    <h6 class="text-warning text-uppercase">Why risk management is crutial</h6>
                                    <p class="description mt-3">Argon is a great free UI package based on Bootstrap
                                        4 that includes the most important components and features.</p>
                                    <div>
                                        <badge type="warning" rounded>marketing</badge>
                                        <badge type="warning" rounded>product</badge>
                                        <badge type="warning" rounded>launch</badge>
                                    </div>
                                    <base-button tag="a" href="#" type="warning" class="mt-4">
                                        Learn more
                                    </base-button>
                                </card>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
       

    </div>
</template>

<script>
export default {
  name: "Home",
  components: {}
};
</script>
