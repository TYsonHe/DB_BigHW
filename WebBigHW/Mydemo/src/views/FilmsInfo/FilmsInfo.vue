<template>
  <el-col span="24">
    <el-col span="24" class="head">
      <h2>豆瓣TOP250电影清单</h2>
    </el-col>
    <el-col span="23" class="table_container">
      <el-table
        :data="FilmsData.filter(data => !search || data.Title.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%"
        max-height="600"
        height="600"
      >
        <el-table-column
          fixed
          label="电影名字"
          prop="Title"
        />
        <el-table-column
          label="别名"
          prop="otherTitle"
        />
        <el-table-column
          label="链接"
          prop="link"
        />
        <el-table-column
          label="导演"
          prop="director"
        />
        <el-table-column
          label="主演"
          prop="actor"
        />
        <el-table-column
          label="年份"
          prop="year"
          sortable
          sort-orders="['ascending', 'descending']"
        />
        <el-table-column
          label="国家"
          prop="country"
        />
        <el-table-column
          label="类型"
          prop="type"
        />
        <el-table-column
          label="星级"
          prop="star"
          sortable
          sort-orders="['ascending', 'descending']"
        />
        <el-table-column
          label="评分"
          prop="score"
          sortable
          sort-orders="['ascending', 'descending']"
        />
        <el-table-column
          label="评价人数"
          prop="people"
          sortable
          sort-orders="['ascending', 'descending']"
        />
        <el-table-column
          align="right"
        >
          <template slot="header" slot-scope="scope">
            <el-input
              v-model="search"
              size="mini"
              placeholder="电影搜索"
            />
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-col>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      FilmsData: [],
      search: ''
    }
  },
  created() {
    this.getFilmsData()
  },
  methods: {
    getFilmsData() {
      const path = 'http://localhost:5000/getFilmsInfo'
      axios.get(path)
        .then(res => {
          this.FilmsData = res.data.FilmData
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
.table_container{
  margin-top: 20px;
  margin-left: 40px;
  border: 1px solid #DCDFE6;
  border-radius: 5px;
  padding: 10px;
}
</style>
