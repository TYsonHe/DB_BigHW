<template>
  <el-col span="24" class="total">
    <el-col span="24" class="head">
      <h2>豆瓣书本Top250评分图表</h2>
    </el-col>
    <el-row :gutter="10">
      <el-col span="12">
        <div id="ScoreCharts" style="width: 100%;height: 600px;margin-left: 15px" />
      </el-col>
      <el-col span="12">
        <div id="CommentsNumCharts" style="width: 100%;height: 600px; padding-top:7px" />
      </el-col>
    </el-row>
  </el-col>

</template>

<script>
import axios from 'axios'
import * as echarts from 'echarts'
export default {
  data() {
    return {
      myScoreChart: null,
      myCommentsNumChart: null,
      BookScores: [],
      BookNums: [],
      commNum: [],
      bookTitle: []
    }
  },
  mounted() {
    this.initScoresChart()
    this.initCommentsNumChart()
    this.updateBookScoreCharts()
    this.updateCommentsNumCharts()
  },
  methods: {
    initScoresChart() {
      this.myScoreChart = echarts.init(document.getElementById('ScoreCharts'))
      this.myScoreChart.setOption({
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
          name: '评分',
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
    initCommentsNumChart() {
      this.myCommentsNumChart = echarts.init(document.getElementById('CommentsNumCharts'))
      this.myCommentsNumChart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '9%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          name: '评论人数',
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          name: '书名',
          type: 'category',
          data: []
        },
        series: [{
          data: [],
          name: '评论人数',
          type: 'bar'
        }]
      })
    },
    updateBookScoreCharts() {
      const path = 'http://localhost:5000/getBookScoreInfo'
      axios.get(path)
        .then(res => {
          console.log('访问后端数据成功')
          this.BookScores = res.data.scores
          this.BookNums = res.data.nums
          console.log(this.BookScores)
          console.log(this.BookNums)
          this.myScoreChart.setOption({
            xAxis: {
              data: this.BookScores
            },
            series: [{
              data: this.BookNums
            }]
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateCommentsNumCharts() {
      const path = 'http://localhost:5000/getBookPeopleTop10'
      axios.get(path)
        .then(res => {
          console.log('访问后端数据成功')
          this.commNum = res.data.commNum
          this.bookTitle = res.data.bookTitle
          console.log(this.commNum)
          console.log(this.bookTitle)
          this.myCommentsNumChart.setOption({
            yAxis: {
              data: this.bookTitle
            },
            series: [{
              data: this.commNum
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
.head{
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}
</style>
