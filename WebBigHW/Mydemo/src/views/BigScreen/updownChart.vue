<!-- 物种总数数量排行TOP10（柱状）横向 -->
<template>
  <div id="updownChart" />
</template>
<script>
import * as echarts from 'echarts'
import { getUpDownChartData } from '@/api/bigscreen/bigscreen'

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
    this.rightchart = echarts.init(document.getElementById('updownChart'))
    // 轮询刷新
    this.timer = setInterval(() => {
      this.fetchRates()
    }, 1000)
  },
  methods: {
    fetchRates() {
      getUpDownChartData()
        .then(response => {
          this.dataList = response.data
          console.log(this.dataList)
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
          text: '物种总数数量排行TOP10',
          left: 'center',
          textStyle: {
            color: '#b1cee2'
          },
          top: 20
        },
        xAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#b1cee2'
            }
          }
        },
        yAxis: {
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
      this.option.yAxis.data = this.dataList.map(item => item.species_id)
      this.option.series[0].data = this.dataList.map(item => item.total_quantity)
      this.rightchart.setOption(this.option)
    }
  }
}

</script>
<style scoped>
#updownChart {
  width: 100%;
  height: 200px;
}
</style>
