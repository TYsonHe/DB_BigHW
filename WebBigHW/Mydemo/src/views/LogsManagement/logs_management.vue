<!--日志管理页面 admin专属-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <el-input v-model="formInline.name" placeholder="请输入记录动作" clearable />
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="onRefresh">刷新</el-button>
          </el-col>
        </el-row>
        <!--展示表格-->
        <el-table
          ref="logsTable"
          :data="currentPageData"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column
            type="selection"
            width="55"
          />
          <el-table-column
            prop="log_id"
            label="日志id"
            align="center"
          />
          <el-table-column
            prop="user_id"
            label="用户id"
            align="center"
          />
          <el-table-column
            prop="action"
            label="动作"
            align="center"
          />
          <el-table-column
            prop="timestamp"
            label="执行时间"
            align="center"
          />
        </el-table>
        <el-footer>
          <div class="block" style="text-align: right;margin-right: 50px;">
            <el-pagination
              :current-page="currentPage"
              :page-sizes="[5,10, 20, 30, 40]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="logsList.length"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-footer>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { getAllLogs } from '@/api/logs_management/logs_management'

export default {
  name: 'SysUser',
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      formInline: {
        name: ''
      },
      logsList: []
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.logsList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.action.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.logsList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getUserList()
  },
  methods: {
    async getUserList() {
      await getAllLogs().then(response => {
        console.log(response)
        this.logsList = response.data
      })
    },
    onRefresh() {
      this.getUserList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1 // 每次改变每页显示条数时，回到第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }// end of methods
}
</script>
<style scoped>
</style>
