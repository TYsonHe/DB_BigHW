<!-- 站点物种种数量数量排行Top10（柱状）竖向 -->
<template>
  <div id="upupChart" />
</template>
<script>
import * as echarts from 'echarts'
import { getUpUpChartData } from '@/api/bigscreen/bigscreen'

export default {
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
    }, 10000)
  },
  methods: {
    fetchRates() {
      getUpUpChartData()
        .then(response => {
          this.dataList = response.data
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
          text: '站点物种种数量数量排行Top10',
          left: 'center',
          textStyle: {
            color: '#b1cee2'
          },
          top: 20
        },
        xAxis: {
          type: 'category',
          data: [],
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
        grid:
        {
          left: '1%',
          right: '10%',
          bottom: '10%',
          containLabel: true
        },
        series: [
          {
            data: [],
            type: 'bar',
            itemStyle: {
              color: function(params) {
                // 在这里为每个数据项设置颜色,设置10个颜色
                const colorList = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570']
                return colorList[params.dataIndex]
              }
            }
          }
        ]
      }
      this.option.xAxis.data = this.dataList.map(item => item.station_id)
      this.option.series[0].data = this.dataList.map(item => item.species_id_count)
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
