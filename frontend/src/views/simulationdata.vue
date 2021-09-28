<template>
  <div class="data">
    <!-- endpositions -->
    <showgraph-vue :graphdata="graphdata" :SpotPrice = simulationdata[0].SpotPrice />
    <div class="list-group" style="width: 400px; margin: auto">
      <b>Future Price</b>
      <li class="list-group-item mt-2">
        <div class="row">
          <span class="col" v-if="simulationdata">{{
            simulationdata[0].FuturePrice
          }}</span>
          <span class="col"
            ><button
              class="btn btn-sm btn-success"
              @click="make_oplist('f', 'b', simulationdata[0].id)"
            >
              Buy
            </button>
          </span>
          <span class="col"
            ><button
              class="btn btn-sm btn-warning"
              @click="make_oplist('f', 's', simulationdata[0].id)"
            >
              Sell
            </button>
          </span>
          <span class="col"
            ><input
              v-model="contracts['f']"
              value="1"
              min="1"
              type="number"
              class="btn btn-sm border lots"
              placeholder="1"
          /></span>

        </div>
      </li>
    </div>

    <ul class="list-group optionchain">
      <!-- header -->
      <li class="list-group-item">
        <div class="row">
          <span class="col"><b>Call LTP</b></span>
          <span class="col extra-col"><b>Strike</b></span>
          <span class="col"><b>Put LTP</b></span>
        </div>
      </li>
      <!-- data -->
      <li
        class="list-group-item"
        v-for="simulation in simulationdata"
        :key="simulation.id"
      >
        <div class="row">
          <span class="col">{{ simulation.CallLTP }}</span>
          <span class="col extra-col">
            <span class="col"
              ><input
                v-model="contracts[`${simulation.id}c`]"
                value="1"
                min="1"
                type="number"
                class="btn btn-sm border lots"
                placeholder="1"
            /></span>
            <button
              class="btn btn-sm btn-success bt"
              @click="make_oplist('c', 'b', simulation.id)"
            >
              B
            </button>
            <button
              class="btn btn-sm btn-warning bt"
              @click="make_oplist('c', 's', simulation.id)"
            >
              S
            </button>
            {{ simulation.Strikes }}
            <button
              class="btn btn-sm btn-success bt"
              @click="make_oplist('p', 'b', simulation.id)"
            >
              B
            </button>
            <button
              class="btn btn-sm btn-warning bt"
              @click="make_oplist('p', 's', simulation.id)"
            >
              S
            </button>
            <span class="col"
              ><input
                v-model="contracts[`${simulation.id}p`]"
                value="1"
                min="1"
                type="number"
                class="btn btn-sm border lots"
                placeholder="1"
            /></span>
          </span>

          <span class="col">{{ simulation.PutLTP }}</span>
        </div>
      </li>
    </ul>

    <div class="poision">
      <b>Positions</b>
    </div>
    <!-- dates -->

    <!-- dates -->

    <ul class="list-group">
      <!-- header -->
      <li class="list-group-item">
        <div class="row pos" style="font-weight: 700">
          <span class="col extra-col">Entry Date</span>
          <span class="col">Strike</span>
          <span class="col">CE/PE</span>
          <span class="col">Buy/Sell</span>
          <span class="col">Lots</span>
          <span class="col">Price</span>
          <span class="col">LTP</span>
          <span class="col">Booked Price</span>
          <span class="col extra-col">Booked Date</span>
          <span class="col">P&L</span>
          <span class="col extra-col">Book/Cancel</span>
        </div>
      </li>
      <!-- data -->
      <li
        class="list-group-item"
        v-for="(position, index) in positions"
        :key="index"
      >
        <div class="row pos">
          <span class="col extra-col">{{ position.date }}</span>
          <span class="col">{{ position.strikes }}</span>
          <span class="col">{{ position.corp }}</span>
          <span class="col">{{ position.bors }}</span>
          <span class="col">{{ position.lots }}</span>
          <span class="col extra-sp">{{ position.price }}</span>
          <span class="col extra-sl">{{ position.LTP }}</span>
          <span class="col">{{ position.booked_price }}</span>
          <span class="col extra-col">{{ position.booked_date }}</span>
          <span class="col">{{ position.pandl.toFixed(2) }}</span>
          <span class="col extra-col">
            <button
              class="btn btn-sm btn-success"
              v-if="position.is_booked == false"
              @click="
                booked(
                  index,
                  position.LTP,
                  position.price,
                  position.lots,
                  position.lotsize,
                  position.date,
                  position.bors,
                  position.op
                )
              "
            >
              <i class="ni ni-check-bold"></i>
            </button>
            <button
              class="btn btn-sm btn-danger"
              @click="delete_position(index)"
            >
              <i class="ni ni-fat-remove"></i>
            </button>
          </span>
        </div>
      </li>
    </ul>

    <!-- greeks -->

    <div class="list-group mt-5 mb-5">
      <div>
        <button @click="refresh_greeks" class="btn btn-success btn-sm">Refresh</button>
      </div>
      <b class="fw-bolder mb-2">Greeks</b>
      <div class="list-group-item">
        <div class="row" style="font-weight: 700">
          <span class="col">CE/PE</span>
          <span class="col">B/S</span>
          <span class="col">Strike</span>
          <span class="col">Delta</span>
          <span class="col">Theta</span>
          <span class="col">Vega</span>
          <span class="col">Gamma</span>
          <span class="col">IV</span>
        </div>
      </div>
      <div class="list-group-item" v-for="greek in greeks" :key="greek">
        <div class="row">
          <span class="col">{{ greek.type }}</span>
          <span class="col">{{ greek.ttype }}</span>
          <span class="col">{{ greek.K.toFixed(2) }}</span>
          <span class="col">{{ greek.delta.toFixed(2) }}</span>
          <span class="col">{{ greek.theta.toFixed(2) }}</span>
          <span class="col">{{ greek.vega.toFixed(2) }}</span>
          <span class="col">{{ greek.gamma.toFixed(2) }}</span>
          <span class="col">{{ greek.iv.toFixed(2) }}</span>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import showgraphVue from "./showgraph.vue";
import {base} from '../main'
export default {
  components: {
    showgraphVue,
  },
  props: {
    simulationdata: Array,
    date: String,
  },

  data() {
    return {
      greeks: [],
      contracts: [],
      positions: [],
      op_list: [],
      graphdata: [],
      op: {
        op_type: "",
        strike: "",
        tr_type: "",
        op_pr: "",
        contract: "",
        lotsize: "",
        fp:"",
      },
      dates: [],
    };
  },

  watch: {
    simulationdata: {
      immediate: true,
      deep: true,

      handler(val, oldVal) {
        val, oldVal;
        this.updatedate();
      },
    },
    date: {
      immediate: true,
      deep: true,

      handler(val, oldVal) {
        val, oldVal;
        this.updatedate();
      },
    },
  },

  methods: {
    // making the op_list here
    make_oplist(ltp, borc, simulationid) {
      const simulation = this.simulationdata.filter((data) => {
        return data.id == simulationid;
      });

      let op_pr = null;
      let contract = null;


      if (ltp == "c") {
        op_pr = simulation[0].CallLTP;
        this.contracts[`${simulationid}c`]
          ? (contract = this.contracts[`${simulationid}c`])
          : (contract = 1);
      }

      if (ltp == "p") {
        op_pr = simulation[0].PutLTP;
        this.contracts[`${simulationid}p`]
          ? (contract = this.contracts[`${simulationid}p`])
          : (contract = 1);
      }

      if (ltp == "f") {
        op_pr = simulation[0].FuturePrice;
        this.contracts[`f`]
          ? (contract = this.contracts['f'])
          : (contract = 1);
      }

      this.op = {
        op_type: ltp,
        strike: parseFloat(simulation[0].Strikes),
        tr_type: borc,
        op_pr: parseFloat(op_pr),
        contract: contract,
        lotsize: parseFloat(simulation[0].Lotsize),
        fp:this.simulationdata[0].FuturePrice
      };

      this.op_list.push(this.op);

      this.get_positions(simulation[0], this.op);
      this.get_prediction(this.op_list);
    },

    // getting x,y from the backend here
    get_prediction(op_list) {
      if (op_list.length) {
        
        op_list = JSON.stringify(op_list);
        const context = {
          op_list: op_list,
          optionchain: this.simulationdata,
        };

        axios
          .post(`${base}/api/payoff/`, context)
          .then((data) => {
            this.graphdata = data.data;
            this.greeks = data.data.greeks;
          });
      } else {
        this.graphdata = [];
      }
    },

    // making the position here
    get_positions(simulation, op_list) {
      let op_pr = null;
      let tr_type = null;
      let pandl = null;

      op_list.op_type == "c"
        ? (op_pr = "CE")
        : op_list.op_type == "p"
        ? (op_pr = "PE")
        : op_list.op_type == "f"
        ? (op_pr = "FU")
        : null;

      op_list.tr_type == "b" ? (tr_type = "B") : (tr_type = "S");

      op_list.tr_type == "b"
        ? (pandl =
            (parseFloat(op_list.op_pr) - parseFloat(op_list.op_pr)) *
            parseInt(op_list.contract) *
            parseInt(simulation.Lotsize))
        : (pandl =
            (parseFloat(op_list.op_pr) - parseFloat(op_list.op_pr)) *
            parseInt(op_list.contract) *
            parseInt(simulation.Lotsize) *
            -1);

      let strikes = null;
      let temp_strikes = simulation.Strikes;

      op_list.op_type == "f" ? (strikes = 0) : (strikes = simulation.Strikes);

      const p = {
        date: simulation.Date,
        strikes: strikes,
        corp: op_pr,
        bors: tr_type,
        lots: op_list.contract,
        price: op_list.op_pr,
        LTP: op_list.op_pr,
        booked_price: "unreserved",
        booked_date: "unreserved",
        is_booked: false,
        pandl: pandl,
        lotsize: simulation.Lotsize,
        op: op_list,
        temp_strikes: temp_strikes,
      };

      this.positions.push(p);
    },

    // BOOKED COND HERE
    booked(index, pre_price, price, contract, lotsize, date, bors, op) {
      const i = this.op_list.indexOf(op);

      const gainorloss = pre_price - price;
      let pandl = null;
      bors == "b"
        ? (pandl = (pre_price - price) * contract * lotsize)
        : (pandl = (pre_price - price) * contract * lotsize * -1);

      if (this.positions[index].is_booked == false) {
        this.positions[index].is_booked = true;
        this.positions[index].pandl = pandl;
        this.positions[index].booked_price = pre_price;

        this.date == ""
          ? (this.positions[index].booked_date = date)
          : (this.positions[index].booked_date = this.date);

        this.op_list[i].op_pr = gainorloss;
        this.op_list[i].contract = 0;
        this.get_prediction(
          this.op_list,
          this.simulationdata[0].Symbol,
          this.simulationdata[0].Expiry
        );
      } else {
        this.positions[index].is_booked = false;

        this.positions[index].booked_price = "unreserved";
        this.positions[index].booked_date = "unreserved";

        this.op_list[i].op_pr = price;
        this.op_list[i].contract = contract;
        this.get_prediction(
          this.op_list,
          this.simulationdata[0].Symbol,
          this.simulationdata[0].Expiry
        );
      }
    },

    // CHNGING LTP BASED ON TEHE UPDATE DATE
    updatedate() {
      for (let p in this.positions) {
        const update_data = this.simulationdata.filter((data) => {
          return (
            data.Strikes == this.positions[p].temp_strikes &&
            data.Date == this.date
          );
        });

        console.log(this.positions[p].corp == "FU" && update_data[0]);

        if (this.positions[p].is_booked == false) {
          if (this.positions[p].corp == "CE" && update_data[0]) {
            this.positions[p].LTP = update_data[0].CallLTP;
            this.positions[p].pandl = this.update_pandl(
              this.positions[p].price,
              this.positions[p].LTP,
              this.positions[p].op,
              this.positions[p].lotsize
            );
          } else if (this.positions[p].corp == "PE" && update_data[0]) {
            this.positions[p].LTP = update_data[0].PutLTP;
            this.positions[p].pandl = this.update_pandl(
              this.positions[p].price,
              this.positions[p].LTP,
              this.positions[p].op,
              this.positions[p].lotsize
            );
          } else if (this.positions[p].corp == "FU" && update_data[0]) {
            console.log(update_data[0].FuturePrice);
            this.positions[p].LTP = update_data[0].FuturePrice;
            this.positions[p].pandl = this.update_pandl(
              this.positions[p].price,
              this.positions[p].LTP,
              this.positions[p].op,
              this.positions[p].lotsize
            );
          } else {
            this.positions[p].LTP = 0.0;
          }
        }
      }
    },

    // update the pandl (updated)
    update_pandl(price, pre_price, op, lotsize) {
      const bors = op.tr_type;

      console.log(bors);
      let pandl = null;
      bors == "b"
        ? (pandl = (pre_price - price) * op.contract * lotsize)
        : (pandl = (pre_price - price) * op.contract * lotsize * -1);

      return pandl;
    },

    // delete positons
    delete_position(index) {
      const opindex = this.op_list.indexOf(this.positions[index].op);

      this.op_list.splice(opindex, 1);
      this.positions.splice(index, 1);
      this.greeks.splice(index, 1);

     
      this.get_prediction(
        this.op_list,
        this.simulationdata[0].Symbol,
        this.simulationdata[0].Expiry
      );
    },

    refresh_greeks(){
      this.get_prediction(this.op_list)
    }
  },
};
</script>

<style scoped>
.extra-sl {
  left: 17px;
}
.extra-sp {
  padding-right: 0px;
}
.pos {
  font-size: 12px;
}
.extra-col {
  flex: 2;
}
.bt {
  margin-left: 2px;
}
.lots {
  width: 50px;
}
.form-select {
  width: 200px;
  margin: auto;
  margin-bottom: 20px;
}
.optionchain {
  max-height: 500px;
  overflow-x: hidden;
  overflow-y: scroll;
  margin-top: 20px;
}
.poision {
  margin-top: 50px;
  margin-bottom: 10px;
}

.data {
  margin-top: 50px !important;
  margin: auto;
}
</style>