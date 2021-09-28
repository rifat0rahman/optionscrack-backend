<template>
  <div class="simulator">
    <div class="contains">
      <div class="files">
        <div class="">
          <form @submit.prevent="get_files" enctype="multipart/form-data">
            <input
              class="btn btn-success btn-sm"
              type="file"
              @change="ce_file"
              accept=".csv"
              required
            />
            <input
              class="btn btn-success btn-sm"
              type="file"
              @change="pe_file"
              accept=".csv"
              required

            />
            <input
              class="btn btn-success btn-sm"
              type="file"
              @change="fudi_file"
              accept=".csv"
              required

            /><br />
            <div class="btn btn-success btn-sm mt-2">
              <label for="">Lots</label>
              <input
                v-model="lots"
                value="75"
                min="1"
                type="number"
                class="btn btn-sm border lots"
                placeholder="1"
              />
            </div>
            <br />
            <input type="submit" class="btn btn-success mt-4" />
          </form>
        </div>
      </div>

<!-- spinner -->

      <div class="text-center" v-show="slick">
        <p>Processing...</p>
      </div>


      <div class="options">
        <!-- Symbol -->
        <select
          v-model="symbol"
          class="form-select btn btn-dark btn-sm"
          aria-label="Default select example"
        >
          <option selected value="">Symbol</option>
          <option value="NIFTY">NIFTY</option>
        </select>
        <!-- expiry date -->
        <select
          v-model="expirydate"
          class="form-select btn btn-dark btn-sm"
          aria-label="Default select example"
        >
          <option selected value="">Expiry Date</option>
          <option>
            {{ expirydate }}
          </option>
        </select>

        <!-- date -->
        <select
          @change="show_all"
          v-model="date"
          class="form-select btn btn-dark btn-sm"
          aria-label="Default select example"
        >
          <option selected value="">Date</option>
          <option v-for="date in datelist" :key="date.id" :value="date">
            {{ date }}
          </option>
        </select>
        <!-- end -->
      </div>

      <!-- simulator data -->
      <simulationdata-vue :simulationdata="all_data" :date="date" />
      <!-- simulator ends -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import simulationdataVue from "./simulationdata.vue";
import {base} from '../main'
export default {
  components: {
    simulationdataVue,
  },
  data() {
    return {
      uploads: {
        ce: null,
        pe: null,
        fudi: null,
      },
      all_data: [],
      temp_data: [],
      expirylist: [],
      datelist: [],
      expirydate: "",
      symbol: "",
      date: "",
      lots: 75,
      slick: false,
    };
  },

  methods: {
    show_all() {
      if (this.date) {
        this.all_data = this.temp_data.filter((data) => {
          return data.Date == this.date;
        });
        this.all_data.sort((a, b) =>
          a.Strikes > b.Strikes ? 1 : b.Strikes > a.Strikes ? -1 : 0
        );
      }
    },

    ce_file(e) {
      var files = e.target.files || e.dataTransfer.files;
      this.uploads.ce = files[0];
    },

    pe_file(e) {
      var files = e.target.files || e.dataTransfer.files;
      this.uploads.pe = files[0];
    },

    fudi_file(e) {
      var files = e.target.files || e.dataTransfer.files;
      this.uploads.fudi = files[0];
    },

    get_files() {
      this.slick = true;
      console.log(this.uploads);
      const headers = {
        "content-type": "multipart/form-data",
      };

      let formData = new FormData();
      formData.append("ce", this.uploads.ce);
      formData.append("pe", this.uploads.pe);
      formData.append("fudi", this.uploads.fudi);
      formData.append("lots", this.lots);
      console.log(base)
      axios.post(`${base}`, formData, headers).then((data) => {
        this.slick = false;
        this.temp_data = data.data.option_chain;
        this.expirydate = data.data.basics.expiry;
        this.symbol = data.data.basics.symbol;
        console.log(data.data);
        for (let i in data.data.option_chain) {
          this.datelist.push(data.data.option_chain[i].Date);
        }
        this.datelist = this.datelist.filter(
          (item, i, ar) => ar.indexOf(item) === i
        );
      });
    },
  },
};
</script>

<style scoped>
.files {
  margin-bottom: 50px;
}
.form-select {
  display: inline;
  margin-left: 10px;
  width: 15% !important;
}
.contains {
  text-align: center;
  margin-top: 50px;
}
.lots {
  width: 80px;
  margin: 2px;
}
</style>