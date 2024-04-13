<template>
  <div ref="chart" class="mapCls" />
</template>

<script>
import { MapDrillDown } from './js/echartMapOptions.js'
export default {
  name: 'EchartMapShow',
  mounted() {
    new MapDrillDown(this.$refs.chart, this).init()
  }
}
</script>

<style scoped>
  .mapCls{
    width: 550px;
    height: 550px;
    //background-image: url(./bg.png);
    //background-size: 100% 100%;
    //background-repeat: no-repeat;
  }
</style>
