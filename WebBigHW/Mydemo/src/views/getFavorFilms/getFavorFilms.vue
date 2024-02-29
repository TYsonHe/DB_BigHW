<template>
  <el-col span="24">
    <el-col span="24">
      <h2 class="head">获取你最喜欢的电影的评论信息</h2>
      <el-row gutter="20">
        <el-col span="11">
          <div class="head">
            <span>评论词频</span>
          </div>
          <div v-show="Freq" class="img">
            <img :src="picurl1" alt="评论词频图" width="650px" height="550px">
          </div>
        </el-col>
        <el-col span="11">
          <div class="head">
            <span>评论词云</span>
          </div>
          <div v-show="Cloud" class="img">
            <img :src="picurl2" alt="评论词云图" width="650px" height="550px">
          </div>
        </el-col>
      </el-row>
      <el-col span="24">
        <el-form>
          <div class="getFilmName">
            <span>你需要爬取的电影名字</span>
            <el-input
              v-model="inputFilmName"
              placeholder="请输入电影名字"
              clearable
            />
          </div>
          <div class="getFilmUrl">
            <span>你需要爬取的电影的地址</span>
            <el-input
              v-model="inputFilmUrl"
              placeholder="请输入电影地址"
              clearable
            />
          </div>
          <div class="button">
            <el-button type="primary" @click="func1">提交并生成</el-button>
          </div>
        </el-form>
      </el-col>
    </el-col>
  </el-col></template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      nowFilmName: '《肖申克的救赎》',
      picurl1: '',
      picurl2: '',
      Freq: true,
      Cloud: true,
      inputFilmName: '',
      inputFilmUrl: ''
    }
  },
  created() {
    this.getPic()
  },
  methods: {
    getPic() {
      const that = this
      const path = 'http://localhost:5000/getPic'
      const path1 = path + '1'
      const path2 = path + '2'
      axios.request({
        url: path1,
        responseType: 'blob',
        method: 'post',
        data: {
          filmName: that.nowFilmName
        }
      }).then(res => {
        const blob = new Blob([res.data], { type: 'image/png' })
        that.picurl1 = URL.createObjectURL(blob)
      }).catch(err => {
        console.log(err)
      })
      axios.request({
        url: path2,
        responseType: 'blob',
        method: 'post',
        data: {
          filmName: that.nowFilmName
        }
      }).then(res => {
        const blob = new Blob([res.data], { type: 'image/png' })
        that.picurl2 = URL.createObjectURL(blob)
      }).catch(err => {
        console.log(err)
      })
    },
    func1() {
      const that = this
      that.Freq = false
      that.Cloud = false
      // 前端处理书名号问题
      that.inputFilmName = '《' + that.inputFilmName + '》'
      const path = 'http://localhost:5000/favoriteFilm'
      const data = {
        filmName: that.inputFilmName,
        filmUrl: that.inputFilmUrl
      }
      axios.post(path, data)
        .then(res => {
          console.log(res.data)
          if (res.data.status === 200) {
            that.$message({
              message: '提交成功',
              type: 'success'
            })
            that.nowFilmName = that.inputFilmName
            that.getPic()
            that.Freq = true
            that.Cloud = true
          } else {
            that.$message({
              message: '提交失败',
              type: 'error'
            })
          }
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
.getFilmName {
  margin-left: 40px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}
.getFilmUrl {
  margin-left: 40px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}
.button{
  marg-top: 10px;
  margin-right: 80px;
  text-align: center;
}
</style>
