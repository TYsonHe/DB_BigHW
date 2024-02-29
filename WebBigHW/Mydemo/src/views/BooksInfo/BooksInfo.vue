<template>
  <el-col span="24" class="total">
    <el-col span="24" class="head">
      <h2>豆瓣Top250书本清单</h2>
    </el-col>
    <el-col span="23" class="table_container">
      <!--  表格：表头固定，行、列可滑动，一些信息可排序，可搜索   -->
      <el-table
        :data="tableData.filter(data => !search || data.title.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%"
        max-height="600"
        height="600"
      >
        <el-table-column
          fixed
          label="书名"
          prop="title"
        />
        <el-table-column
          label="链接"
          prop="link"
        />
        <el-table-column
          label="国家"
          prop="country"
        />
        <el-table-column
          label="作者"
          prop="author"
        />
        <el-table-column
          label="译者"
          prop="translator"
        />
        <el-table-column
          label="出版社"
          prop="publisher"
        />
        <el-table-column
          label="出版日期"
          prop="press_time"
          sortable
          sort-orders="['ascending', 'descending']"
        />
        <el-table-column
          label="价格"
          prop="price"
          sortable
          sort-orders="['ascending', 'descending']"
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
              placeholder="书名搜索"
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
      tableData: [],
      search: ''
    }
  },
  created() {
    this.getBooksInfo()
  },
  methods: {
    getBooksInfo() {
      const path = 'http://localhost:5000/getBookInfo'
      axios.get(path)
        .then(res => {
          this.tableData = res.data.BookData
        })
        .catch(err => {
          console.log(err)
        })
    },
    sortByTime(a, b) {
      return new Date(a.press_time) - new Date(b.press_time)
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
