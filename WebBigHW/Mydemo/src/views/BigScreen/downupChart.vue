<template>
  <div ref="chart" style="width: 100%; height: 100%;" />
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'DynamicLineChart',
  data() {
    return {
      chart: null,
      xAxisData: [], // 横轴时间数据
      monitorSeriesData: [],
      predictSeriesData: []
    }
  },
  created() {
    // 先用随机数据
    this.initialData()
  },
  mounted() {
    this.initChart()
    // 每隔5秒更新一次数据
    this.timer = setInterval(() => {
      this.updateData()
    }, 5000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    initialData() {
      // 先随机生成300个数据给monitorData
      // 要求，整数，范围在10000-20000之间
      for (let i = 0; i < 30; i++) {
        // 定义变量
        let randomNum = 425.5 + Math.floor(Math.random() * 10) / 10
        randomNum -= Math.floor(Math.random() * 10) / 10
        if (i < 26) {
          this.monitorSeriesData.push(randomNum * 10000)
        }
        randomNum -= Math.floor(Math.random() * 10) / 10
        randomNum += Math.floor(Math.random() * 10) / 10
        this.predictSeriesData.push(randomNum * 10000)
      }
      // 横轴时间数据
      // 先取当前时间
      let currentTime = new Date()
      for (let i = 0; i < 30; i++) {
        this.xAxisData.push(
          currentTime.getHours() +
            ':' +
            currentTime.getMinutes() +
            ':' +
            currentTime.getSeconds()
        )
        currentTime = new Date(currentTime - 30000)
      }
      // reverse一下
      this.xAxisData.reverse()
    },
    initChart() {
      this.chart = echarts.init(this.$refs.chart)

      this.chart.setOption({
        // 不显示网格
        title: {
          text: '全国流量监控与预测',
          textStyle: {
            fontSize: 15,
            color: 'rgba(120, 178, 218, 1)'
          },
          left: 'center'
        },
        legend: {
          data: ['监控流量', '预测流量'],
          textStyle: {
            color: '#b1cee2'
          },
          // 图例位置
          right: '30px'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.xAxisData,
          axisLine: {
            lineStyle: {
              color: '#b1cee2'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '流量（请求量）',
          min: 4200000,  // 设置最小值
          max: 4300000,  // 设置最大值
          axisLine: {
            lineStyle: {
              color: '#b1cee2'
            }
          }
        },
        grid: {
          top: '50px',
          left: '70px',
          right: '10px',
          bottom: '50px'
        },
        series: [
          {
            name: '监控流量',
            type: 'line',
            data: this.monitorSeriesData,
            smooth: true,
            lable: {
              color: '#b1cee2'
            }
          },
          {
            name: '预测流量',
            type: 'line',
            data: this.predictSeriesData,
            smooth: true,
            lable: {
              color: '#b1cee2'
            }
          }
        ]
      })
    },
    updateData() {
      // 模拟获取最新的监控数据和预测数据
      const newMonitorData = 425.5 + Math.floor(Math.random() * 10) / 10 - Math.floor(Math.random() * 10) / 10
      const newPredictData = newMonitorData - Math.floor(Math.random() * 10) / 10 + Math.floor(Math.random() * 10) / 10

      // 更新横轴时间数据
      const currentTime = new Date()
      this.xAxisData.push(
        currentTime.getHours() +
          ':' +
          currentTime.getMinutes() +
          ':' +
          currentTime.getSeconds()
      )

      // 更新监控流量数据
      // 先把数组末尾的null去掉
      if (this.monitorSeriesData[this.monitorSeriesData.length - 1] === null) {
        this.monitorSeriesData.pop()
      }
      this.monitorSeriesData.push(newMonitorData * 10000)

      // 更新预测流量数据
      this.predictSeriesData.push(newPredictData * 10000)

      // 在monitorSeriesData末尾补齐null, 使得数据长度一致
      if (this.monitorSeriesData.length < 30) {
        this.monitorSeriesData.push(null)
      }

      // 只保留最近15分钟的数据，超过15分钟则删除最旧的数据
      if (this.xAxisData.length > 30) {
        this.xAxisData.shift()
        this.monitorSeriesData.shift()
        this.predictSeriesData.shift()
      }

      // 更新图表
      this.chart.setOption({
        xAxis: {
          data: this.xAxisData
        },
        series: [
          {
            name: '监控流量',
            data: this.monitorSeriesData
          },
          {
            name: '预测流量',
            data: this.predictSeriesData
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
/* 可选的组件样式 */

</style>
