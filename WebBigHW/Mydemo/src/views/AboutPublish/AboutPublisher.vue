<template>
  <el-col span="24">
    <el-col span="24" class="header">
      <h2>豆瓣图书Top250出版社信息</h2>
    </el-col>
    <el-col span="24">
      <div id="publisher" style="width: 100%;height: 600px;margin-left: 15px" />
    </el-col>
  </el-col>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      PublisherName: [],
      PublisherNum: [],
      publisherChart: null,
    }
  },
  mounted() {
    this.initPublisherChart()
    this.updatePublisherChart()
  },
  methods: {
    initPublisherChart() {
      this.publisherChart = echarts.init(document.getElementById('publisher'))
      this.publisherChart.setOption({
        color: ['#3398DB'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '8%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          name: '出版社',
          type: 'category',
          data: []
        },
        yAxis: {
          name: '数量',
          type: 'value'
        },
        series: [{
          data: [],
          barWidth: '100%',
          type: 'bar'
        }]
      })
    },
    updatePublisherChart() {
      const path = 'http://localhost:5000/getBookPublisher'
      axios.get(path)
        .then(res => {
          console.log('已经获取到出版社信息')
          this.PublisherName = res.data.PublisherName
          this.PublisherNum = res.data.PublisherNum
          console.log(this.PublisherName)
          console.log(this.PublisherNum)
          this.publisherChart.setOption({
            xAxis: {
              data: this.PublisherName
            },
            series: [{
              data: this.PublisherNum
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
h2{
  text-align: center;
  color: #409EFF;
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 20px;
}
</style>
