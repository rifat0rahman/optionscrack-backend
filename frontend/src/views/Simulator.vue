<template>
  <div>
    <div class="position-relative">
      <section class="section section-shaped section-lg my-0">
        <div class="shape shape-style-2 shape-default">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="container pt-lg-md">
          <div class="row justify-content-right">
            <div class="col-lg-13">
              <card
                type="secondary"
                shadow
                header-classes="bg-white pb-5"
                body-classes="px-lg-5 py-lg-5"
                class="border-1">
              <!-- simulator funtions -->
              <simulatorold />
              <!-- simulator ends -->
              </card>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>


<script>
import showgraphVue from './showgraph.vue';
import  simulatorold from './simulator-old.vue'
export default {
  components:{
    showgraphVue,
    simulatorold,
  },



};
</script>
<style scoped>
</style>
