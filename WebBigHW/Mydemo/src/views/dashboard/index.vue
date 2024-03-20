<template>
  <el-col class="total">
    <el-col span="24">
      <div class="container">
        <div class="logo">
          <h2 class="title">海洋生物多样性检测和保护系统</h2>
          <div class="tech">
            <p class="tech-text">所用技术: Python、Flask、Vue2、Echarts、</p>
            <p class="tech-text">技术让世界更美好</p>
          </div>
        </div>
        <div class="img">
          <img :src="imgsrc" alt="" width="980px" height="500px">
        </div>
      </div>
    </el-col>
    <!-- 底部版权 -->
    <el-col span="24">
      <div class="container">
        <div class="slogan">
          <h3>一个有梦想的程序员</h3>
        </div>
        <div class="copyright">
          &copy; Copyright <strong><span>He ShiKun</span></strong>. All Rights Reserved
        </div>
      </div>
    </el-col>
  </el-col>

</template>

<script>

export default {
  data() {
    return {
      imgsrc: require('@/assets/images/主页.png')
    }
  }
}
</script>

<style scoped>
.title{
  text-align: center;
  color: #409EFF;
  font-size: 30px;
  font-weight: bold;
}
.tech{
  background: #fff; /*设置元素背景颜色*/
  margin: 0 auto; /*设置元素外边距*/
}
.tech-text{
  font-family: "Microsoft YaHei";
  font-size: 20px;
  text-align: center;
  background: -webkit-linear-gradient(left, #0f0, #00f) 0 0 no-repeat;/*设置线性渐变*/
  -webkit-background-size: 160px;                        /*设置背景大小*/
  -webkit-background-clip: text;                            /*背景被裁剪到文字*/
  -webkit-text-fill-color: rgba(0, 0, 0, 0.3);        /*设置文字的填充颜色*/
  -webkit-animation: shine 3s infinite;                    /*设置动画*/
}
@-webkit-keyframes shine{   /*创建动画*/
    0%{
        background-position: 0 0;
    }
    100%{
        background-position: 100% 100%;
    }
}
.img{
  text-align: center;
}
.slogan{
  text-align: center;
  color: #888;
  font-size: 13px;
  font-weight: 500;
}
.copyright{
  text-align: center;
  color: #888;
  font-size: 13px;
  font-weight: 500;
}
</style>
