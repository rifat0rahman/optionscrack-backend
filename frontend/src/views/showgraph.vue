<template>
  <div>
    <div>
      <!-- grph view -->
      <div>
        <apexchart type="area" :options="options" :series="series"> </apexchart>
      </div>
      <!-- graph view -->
    </div>
  </div>
</template>

<script>
export default {
  props: {
    graphdata: Object,
    SpotPrice:String,
  },
  // graph
  data: () => ({
    options: {
      chart: {
        id: "payoff",
      },

      stroke: {
        curve: "straight",
      },

      dataLabels: {
        enabled: false,
      },
      xaxis: {
        categories: [],
      },
    },

    series: [
      {
        name: "P&L",
        data: [],
      },
    ],
  }),

// graph
// optionscrack
// H9+IL:@kN

  watch: {
    graphdata: {
      immediate: true,
      deep: true,

      handler(val, oldVal) {
        console.log(val, oldVal, "valss");
        this.showgraph();
      },
    },
    SpotPrice: {
      immediate: true,
      deep: true,
      handler(val, oldVal) {
        console.log(val, oldVal, "valss");
        this.showgraph();
      },
    },
  },

  mounted() {
    console.log(this.graphdata);
  },

  methods: {
    showgraph() {

      console.log(this.graphdata,'graphfsd')
      console.log(parseInt(this.SpotPrice.replace(/\s/g, '')))

      this.series = [
        {
          name:"P&L",
          data: this.graphdata.y
        }
      ];

      this.options = {
        chart: {
        id: "payoff",
      },

      stroke: {
        curve: "straight",
      },

      dataLabels: {
        enabled: false,
      },
        xaxis :{
          type:"numeric",
          categories:this.graphdata.x
      },
      annotations: {
        xaxis: [
          {
            x:parseInt(this.SpotPrice.replace(/\s/g, '')),
            borderColor: '#775DD0',
            label: {
              borderColor: '#775DD0',
              style: {
                    color: '#fff',
                    background: '#775DD0',
              },
              text: `Spot-Price ${this.SpotPrice}`
            }
          }
        ]
    }
    }

  },
  }
};
</script>

<style scoped>
#myChart {
  margin-top: 50px;
  height: 500px !important;
}
</style>
