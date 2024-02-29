<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'App'
}
$(document).ready(function() {
  console.log('ready!')
})
</script>
