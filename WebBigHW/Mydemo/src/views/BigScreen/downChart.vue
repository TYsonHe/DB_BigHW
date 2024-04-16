<!-- 上方图表 -->
<template>
  <div class="parent-downChart">
    <div class="div5">监控+预警任务统计信息</div>
    <div class="div1">
      <span class="text">监控任务总数</span>
      <dv-digital-flop :config="config" />
    </div>
    <div class="div2">
      <span class="text">预警任务总数</span>
      <dv-digital-flop :config="config2" />
    </div>
    <div class="div3">
      <downupChart />
    </div>
    <div class="div4">
      <downdownChart />
    </div>
  </div>
</template>
<script>
import downupChart from '@/views/BigScreen/downupChart.vue'
import downdownChart from '@/views/BigScreen/downdownChart.vue'
import { getAllmonitoringTaskCount, getAllalertTaskCount } from '@/api/bigscreen/bigscreen'

export default {
  name: 'BigScreen',
  components: {
    downupChart,
    downdownChart
  },
  data() {
    return {
      config: {
        number: [100],
        content: '{nt}个',
        fontSize: 30,
        color: '#fff',
        bgColor: 'rgba(0,0,0,0)',
        formatter: this.formatter
      },
      config2: {
        number: [100],
        content: '{nt}个',
        fontSize: 30,
        color: '#fff',
        bgColor: 'rgba(0,0,0,0)',
        formatter: this.formatter
      }
    }
  },
  created() {
    this.getAllmonitoringTaskCount()
    this.getAllalertTaskCount()
  },
  mounted() {
    this.timer = setInterval(() => {
      this.getAllmonitoringTaskCount()
      this.getAllalertTaskCount()
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    async getAllmonitoringTaskCount() {
      const res = await getAllmonitoringTaskCount()
      if (res.code === 200) {
        this.config.number = [res.data]
        // 刷新datav
        this.config = { ...this.config }
      }
    },
    async getAllalertTaskCount() {
      const res = await getAllalertTaskCount()
      if (res.code === 200) {
        this.config2.number = [res.data]
        // 刷新datav
        this.config2 = { ...this.config2 }
      }
    },
    formatter(number) {
      const numbers = number.toString().split('').reverse()
      const segs = []

      while (numbers.length) segs.push(numbers.splice(0, 3).join(''))

      return segs.join(',').split('').reverse().join('')
    }
  }
}

</script>
<style scoped>
.parent-downChart {
display: grid;
grid-template-columns: repeat(3, 1fr);
grid-template-rows: 0.1fr repeat(2, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
}

.text {
  color: #409EFF;
  font-size: 20px;
}

.div1 { grid-area: 2 / 1 / 3 / 2;
    margin-top: 20px;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
  height: 100%;
  width: 100%;
}
.div2 { grid-area: 3 / 1 / 4 / 2;
      margin-top: 20px;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
  height: 100%;
  width: 100%;
}
.div3 { grid-area: 2 / 2 / 3 / 4; }
.div4 { grid-area: 3 / 2 / 4 / 4; }
.div5 { grid-area: 1 / 1 / 2 / 4;
  margin-top:7px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    color: #409EFF;
  font-weight: bold;
}
</style>
