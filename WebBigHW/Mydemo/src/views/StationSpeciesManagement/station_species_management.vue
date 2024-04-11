<!-- 站点物种信息展示 user用-->
<template>
  <div class="parent">
    <div class="div1">
      <el-row :gutter="20" style="margin-top: 15px">
        <el-col :span="6">
          <el-statistic
            :value="curStationId"
            :title="title"
          />
        </el-col>
        <el-col :span="6">
          <el-input v-model="formInline.name" placeholder="请输入物种名字" clearable />
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="onRefresh">刷新</el-button>
        </el-col>
      </el-row>
    </div>
    <el-card class="div2">
      <div class="databoard">
        <span>物种总量</span>
        <dv-digital-flop :config="config1" style="width:200px;height:50px;" />
      </div>
    </el-card>
    <el-card class="div3">
      <middle_chart :cur-station-id="curStationId" />
    </el-card>
    <el-card class="div4">
      <dv-scroll-board :config="config2" style="width:420px;height:130px;color: #303031" />
    </el-card>
    <div class="div5">
      <el-col :span="24">
        <el-card class="box-card">
          <!--展示表格-->
          <el-table
            ref="station_species_table"
            :data="currentPageData"
            border
            stripe
            style="width: 100%"
          >
            <el-table-column
              type="selection"
              width="55"
            />
            <el-table-column
              prop="record_id"
              label="记录id"
              align="center"
            />
            <el-table-column
              prop="species_id"
              label="物种id"
              align="center"
            />
            <el-table-column
              prop="species_name"
              label="物种名"
              align="center"
            />
            <el-table-column
              prop="quantity"
              label="物种数量"
              align="center"
            />
            <el-table-column
              prop="station_id"
              label="观测站id"
              align="center"
              sortable
            />
            <el-table-column
              prop="timestamp"
              label="记录时间"
              align="center"
            />
          </el-table>
          <el-footer>
            <div class="block" style="text-align: right;margin-right: 50px;">
              <el-pagination
                :current-page="currentPage"
                :page-sizes="[5,10, 20, 30, 40]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="stationSpeciesList.length"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-footer>
        </el-card>
      </el-col>
    </div>
  </div>
</template>

<script>
import {
  getStationSpeciesList,
  getStationSpeciesQuantityRank,
  getStationSpeciesQuantityTotal
} from '@/api/station_species_management/station_species_management'

import middle_chart from '@/views/StationSpeciesManagement/middle_chart.vue'

export default {
  name: 'SysUser',
  components: {
    middle_chart
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      formInline: {
        name: ''
      },
      stationSpeciesList: [],
      curStationId: 0,
      title: '站点编号',
      config1: {
        number: [],
        content: '{nt}亿个'
      },
      config2: {
        title: '物种数量',
        data: [
        ],
        header: ['物种ID', '数量'],
        align: ['center', 'center'],
        headerBGC: '#409EFF',
        oddRowBGC: '#f5f5f5',
        evenRowBGC: '#e5e5e5'
      }
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.stationSpeciesList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.species_name.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.stationSpeciesList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getUserList()
    this.getRank()
    this.getTotal()
  },
  mounted() {
    // 设置两个轮询
    this.timer1 = setInterval(() => {
      this.getRank()
    }, 3000)
    this.timer2 = setInterval(() => {
      this.getTotal()
    }, 3000)
  },
  beforeDestroy() {
    clearInterval(this.timer1)
    clearInterval(this.timer2)
  },
  methods: {
    async getUserList() {
      await getStationSpeciesList().then(response => {
        this.stationSpeciesList = response.data.species_list
        this.curStationId = response.data.station_id
      })
    },
    async getRank() {
      const post_data = {
        station_id: this.curStationId
      }
      await getStationSpeciesQuantityTotal(post_data).then(response => {
        this.config1.number = [response.data.total]
        // datav 刷新
        this.config1 = { ...this.config1 }
      })
    },
    async getTotal() {
      const post_data = {
        station_id: this.curStationId
      }
      await getStationSpeciesQuantityRank(post_data).then(response => {
        this.config2.data = response.data.species_list
        // datav 刷新
        this.config2 = { ...this.config2 }
      })
    },
    onRefresh() {
      this.getUserList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1 // 每次改变每页显示条数时，回到第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }// end of methods
}
</script>
<style scoped>
.parent {
  margin-left: 10px;
  margin-right: 10px;
display: grid;
grid-template-columns: repeat(6, 1fr);
grid-template-rows: 0.4fr 1.3fr repeat(2, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
}

.div1 { grid-area: 1 / 1 / 2 / 7; }
.div2 { grid-area: 2 / 1 / 3 / 3;
margin-top: 10px;
  margin-left: 10px;
}
.div3 { grid-area: 2 / 3 / 3 / 5;
  margin-left: 10px;
margin-top: 10px;
}
.div4 { grid-area: 2 / 5 / 3 / 7;
  margin-left: 10px;
margin-top: 10px;}
.div5 { grid-area: 3 / 1 / 5 / 7;
margin-top: 10px;}

.databoard {
  margin-top: 20px;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
  height: 100%;
  width: 100%;
}
</style>
