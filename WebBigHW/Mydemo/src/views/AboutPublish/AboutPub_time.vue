<template>
  <el-col span="24">
    <el-col span="24">
      <h2>豆瓣TOP250图书出版时间统计</h2>
    </el-col>
    <el-col span="24">
      <div id="pub_time" style="width: 100%;height: 600px;" />
    </el-col>
  </el-col>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      PressYear: [],
      PressNum: [],
      pub_timeChart: null
    }
  },
  mounted() {
    this.initPub_timeChart()
    this.updatePub_timeChart()
  },
  methods: {
    initPub_timeChart() {
      this.pub_timeChart = echarts.init(document.getElementById('pub_time'))
      this.pub_timeChart.setOption({
        color: ['#3398DB'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          name: '时间',
          type: 'category',
          data: []
        },
        yAxis: {
          name: '数量',
          type: 'value'
        },
        series: [{
          data: [],
          barWidth: '60%',
          type: 'bar'
        }]
      })
    },
    updatePub_timeChart() {
      const path = 'http://localhost:5000/getBookPressTime'
      axios.get(path)
        .then(res => {
          console.log('已经获取到出版时间信息')
          this.PressYear = res.data.pressYear
          this.PressNum = res.data.pressNum
          this.pub_timeChart.setOption({
            xAxis: {
              data: this.PressYear
            },
            series: [{
              data: this.PressNum
            }]
          })
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>
h2 {
  text-align: center;
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #409EFF;
}
</style>
