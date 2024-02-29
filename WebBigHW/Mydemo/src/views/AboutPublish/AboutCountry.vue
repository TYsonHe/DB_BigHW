<template>
  <el-col span="24">
    <el-col span="24">
      <h2 class="header">豆瓣TOP250图书出版国家统计</h2>
      <div id="CountryChart" style="width: 100%;height: 650px;"/>
    </el-col>
  </el-col>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'
export default {
  data() {
    return {
      CountryName: [],
      CountryNum: [],
      CountryChart: null
    }
  },
  mounted() {
    this.initCountryChart()
    this.updateCountryChart()
  },
  methods: {
    initCountryChart() {
      this.CountryChart = echarts.init(document.getElementById('CountryChart'))
      this.CountryChart.setOption({
        title: {
          text: '各个国家出版图书数量',
          subtext: '数据来自豆瓣图书top250'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['出版量']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.02]
        },
        yAxis: {
          type: 'category',
          data: []
        },
        series: [{
          name: '出版数量',
          type: 'bar',
          data: []
        }]
      })
    },
    updateCountryChart() {
      const path = 'http://localhost:5000/getBookCountryInfo'
      axios.get(path)
        .then(res => {
          this.CountryName = res.data.CountryName
          this.CountryNum = res.data.CountryNum
          this.CountryChart.setOption({
            yAxis: {
              data: this.CountryName
            },
            series: [{
              data: this.CountryNum
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
