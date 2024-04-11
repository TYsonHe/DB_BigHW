<!-- 监控任务情况+站点人员图表 -->
<template>
  <div id="chartContainer1" />
</template>
<script>
import * as echarts from 'echarts'
import { getMiddleChartData } from '@/api/monitor_mission_management/accept_monitor_task'

export default {
  props: {
    curStationId: {
      // type 是 int
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      dataList: []
    }
  },
  created() {
    this.fetchRates()
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  mounted() {
    this.rightchart = echarts.init(document.getElementById('chartContainer1'))
    // 轮询刷新
    this.timer = setInterval(() => {
      this.fetchRates()
    }, 1000)
  },
  methods: {
    fetchRates() {
      console.log(this.curStationId)
      const post_data = {
        station_id: this.curStationId
      }
      getMiddleChartData(post_data)
        .then(response => {
          this.dataList = response.data.dataList
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
        xAxis: {
          type: 'category',
          data: ['站点的人员总数', '今日已完成', '未完成的任务'],
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        series: [
          {
            data: this.dataList,
            type: 'bar',
            itemStyle: {
              color: function(params) {
                // 在这里为每个数据项设置颜色
                const colorList = ['#c23531', '#2f4554', '#61a0a8']
                return colorList[params.dataIndex]
              }
            }
          }
        ]
      }
      this.rightchart.setOption(this.option)
    }
  }
}

</script>
<style scoped>
#chartContainer1 {
  width: 100%;
  height: 200px;
}
</style>
