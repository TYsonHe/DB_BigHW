<!-- 站点物种种数量数量排行Top10（柱状）竖向 -->
<template>
  <div id="upupChart" />
</template>
<script>
import * as echarts from 'echarts'
import { getMiddleChartData } from '@/api/alert_task_management/check_alert_task'

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
    this.rightchart = echarts.init(document.getElementById('upupChart'))
    // 轮询刷新
    this.timer = setInterval(() => {
      this.fetchRates()
    }, 1000)
  },
  methods: {
    fetchRates() {
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
          },
          axisLine: {
            lineStyle: {
              color: '#b1cee2'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#b1cee2'
            }
          }
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
#upupChart {
  width: 100%;
  height: 200px;
}
</style>
