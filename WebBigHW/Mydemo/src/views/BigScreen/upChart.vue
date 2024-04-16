<!-- 上方图表 -->
<template>
  <div class="parent-upChart">
    <div class="div5">物种数量统计信息</div>
    <div class="div1">
      <span class="text">物种种类数据量</span>
      <dv-digital-flop :config="config" />
    </div>
    <div class="div2">
      <span class="text">物种总数数据量</span>
      <dv-digital-flop :config="config2" />
    </div>
    <div class="div3">
      <upupChart />
    </div>
    <div class="div4">
      <updownChart />
    </div>
  </div>
</template>
<script>
import upupChart from '@/views/BigScreen/upupChart.vue'
import updownChart from '@/views/BigScreen/updownChart.vue'
import { getSpeciesNumber, getAllSpeciesCount } from '@/api/bigscreen/bigscreen'
export default {
  name: 'BigScreen',
  components: {
    upupChart,
    updownChart
  },
  data() {
    return {
      config: {
        number: [],
        content: '{nt}个',
        fontSize: 24,
        color: '#fff',
        bgColor: 'rgba(0,0,0,0)',
        formatter: this.formatter
      },
      config2: {
        number: [445124],
        content: '{nt}万个',
        fontSize: 24,
        color: '#fff',
        bgColor: 'rgba(0,0,0,0)',
        formatter: this.formatter
      }
    }
  },
  created() {
    this.getSpeciesNumber()
    this.getAllSpeciesCount()
  },
  mounted() {
    this.timer = setInterval(() => {
      this.getSpeciesNumber()
      this.getAllSpeciesCount()
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    async getSpeciesNumber() {
      const res = await getSpeciesNumber()
      if (res.code === 200) {
        this.config.number = [res.data]
        // 刷新datav
        this.config = { ...this.config }
      }
    },
    async getAllSpeciesCount() {
      const res = await getAllSpeciesCount()
      if (res.code === 200) {
        console.log(res.data)
        this.config2.number = [parseInt(res.data)]
        // 刷新datav
        this.config2 = { ...this.config2 }
        console.log(this.config2.number)
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
.parent-upChart {
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
  margin-top:10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    color: #409EFF;
  font-weight: bold;
}
</style>
