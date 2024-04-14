
<template>
  <div class="parent">
    <div class="div1">
      <div id="container">
        <EchartMapShow />
      </div>
    </div>
    <div class="div2">
      <dv-scroll-board :config="scroll1" style="height: 95%;margin-left:5px;"/>
    </div>
    <div class="div3" />
    <div class="div4" />
  </div>
</template>

<script>
import EchartMapShow from './mapPage/echartMapShow'
import { getBigScreenDownScrollData } from '@/api/bigscreen/bigscreen'
export default {
  name: 'BigScreen',
  components: {
    EchartMapShow
  },

  data() {
    return {
      scroll1: {
        title: '实时数据',
        data: [],
        columnWidth: [150, 150, 150, 150],
        header: ['任务id', '任务类型', '任务站点', '任务状态'],
        align: ['center', 'center', 'center', 'center'],
        rowNum: 4,
        headerHeight: 40,
        headerBGC: 'rgb(12, 46, 86)',
        oddRowBGC: 'rgba(12, 47, 86, 0.6)',
        evenRowBGC: 'rgba(12, 47, 86, 0.3)'
      }
    }
  },
  mounted() {
    this.getBigScreenDownScrollData() // 取一次就好
  },
  methods: {
    async getBigScreenDownScrollData() {
      const res = await getBigScreenDownScrollData()
      if (res.code === 200) {
        this.scroll1.data = res.data
        // datav 刷新
        this.scroll1 = { ...this.scroll1 }
      }
    }
  }

}
</script>

<style scoped>
.parent {
display: grid;
grid-template-columns: repeat(5, 1fr);
grid-template-rows: repeat(6, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
  background-image: url('./mapPage/bg.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.div1 { grid-area: 1 / 1 / 5 / 3; }
.div2 { grid-area: 5 / 1 / 7 / 3;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
  height: 100%;
  width: 100%;}
.div3 { grid-area: 1 / 3 / 4 / 6; }
.div4 { grid-area: 4 / 3 / 7 / 6; }
#container{
  padding:0px;
  margin: 0px;
  width: 100%;
  height: 100%;
}
</style>
