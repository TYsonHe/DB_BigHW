<!-- 预警任务变化情况图表 -->
<template>
  <div id="chartContainer2" />
</template>

<script>
import * as echarts from 'echarts'
import { getRightChartData } from '@/api/alert_task_management/check_alert_task'

export default {
  props: {
    curStationId: {
      // type 是 int
      type: Number
    }
  },
  data() {
    return {
      dataQuantityList: []
    }
  },
  created() {
    this.fetchRates()
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  mounted() {
    this.rightchart = echarts.init(document.getElementById('chartContainer2'))
    // 轮询刷新
    this.timer = setInterval(() => {
      this.fetchRates()
    }, 10000)
  },
  methods: {
    fetchRates() {
      const post_data = {
        station_id: this.curStationId
      }
      getRightChartData(post_data)
        .then(response => {
          this.dataQuantityList = response.data.dataQuantityList
          this.updateChart()
        })
        .catch(error => {
          this.$message({
            message: error,
            type: 'error'
          })
        })
    },
    updateChart() {
      this.option = {
        title: {
          text: '预警任务完成变化趋势',
          textStyle: {
            color: '#000',
            fontSize: 12
          },
          left: 'center'
        },
        tooltips: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '数据量',
            data: this.dataQuantityList,
            type: 'line',
            areaStyle: {}
          }
        ],
        grid: { // 让图表占满容器
          top: '20px',
          left: '40px',
          right: '40px',
          bottom: '10px'
        }
      }
      this.rightchart.setOption(this.option)
    }
  }
}

</script>

<style scoped>
#chartContainer2 {
  width: 100%;
  height: 200px;
}
</style>
