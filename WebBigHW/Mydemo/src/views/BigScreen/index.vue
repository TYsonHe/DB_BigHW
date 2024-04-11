
<template>
  <div>
    <div id="container">
      <EchartMapShow />
    </div>
  </div>
</template>

<script>
import EchartMapShow from './mapPage/echartMapShow'
export default {
  name: 'BigScreen',
  components: {
    EchartMapShow
  },

}
</script>

<style scoped>
    #container{
        padding:0px;
        margin: 0px;
        width: 100%;
        height: 100%;
    }
</style>
