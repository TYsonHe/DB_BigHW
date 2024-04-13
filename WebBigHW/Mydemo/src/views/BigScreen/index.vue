
<template>
  <div class="parent">
    <div class="div1">
      <div id="container">
        <EchartMapShow />
      </div>
    </div>
    <div class="div2"> </div>
    <div class="div3"> </div>
    <div class="div4"> </div>
  </div>
</template>

<script>
import EchartMapShow from './mapPage/echartMapShow'
export default {
  name: 'BigScreen',
  components: {
    EchartMapShow
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
}

.div1 { grid-area: 1 / 1 / 5 / 3; }
.div2 { grid-area: 5 / 1 / 7 / 3; }
.div3 { grid-area: 1 / 3 / 4 / 6; }
.div4 { grid-area: 4 / 3 / 7 / 6; }
#container{
  padding:0px;
  margin: 0px;
  width: 100%;
  height: 100%;
}
</style>
