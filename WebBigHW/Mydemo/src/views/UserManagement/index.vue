<!--用户管理页面 admin专属-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <el-input v-model="formInline.name" placeholder="请输入用户名" clearable />
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="onRefresh">刷新</el-button>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-button type="primary" icon="el-icon-plus" @click="addDialogVisible=true">新增</el-button>
          <el-button type="warning" icon="el-icon-edit" @click="updateBtn">编辑</el-button>
          <el-button type="danger" icon="el-icon-delete" @click="deleteBatch">删除</el-button>
        </el-row>
        <!--展示表格-->
        <el-table
          ref="userTable"
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
            prop="user_id"
            label="用户id"
            align="center"
          />
          <el-table-column
            prop="user_name"
            label="用户名"
            align="center"
          />
          <el-table-column
            prop="password"
            label="密码"
            align="center"
          />
          <el-table-column
            prop="roles"
            label="身份"
            align="center"
          />
          <el-table-column
            prop="station_id"
            label="观测站id"
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
              :total="userList.length"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-footer>
      </el-card>
    </el-col>
    <!--新增弹窗-->
    <el-dialog
      center
      title="新增"
      :visible.sync="addDialogVisible"
      width="30%"
      @close="addFormClose"
    >
      <el-form ref="addRuleForm" :model="addUserForm" label-width="90px">
        <el-form-item label="用户名">
          <el-input v-model="addUserForm.user_name" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="addUserForm.password" />
        </el-form-item>
        <el-form-item label="权限">
          <el-input v-model="addUserForm.roles" />
        </el-form-item>
        <el-form-item label="观测站id">
          <el-input v-model="addUserForm.station_id" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <!--修改弹窗-->
    <el-dialog
      center
      title="修改"
      :visible.sync="updateDialogVisible"
      width="30%"
      @close="updateFormClose"
    >
      <el-form ref="updateRuleForm" :model="updateUserForm" label-width="90px">
        <el-form-item label="用户id" prop="user_id">
          <el-input v-model="updateUserForm.user_id" disabled />
        </el-form-item>
        <el-form-item label="用户名" prop="user_name">
          <el-input v-model="updateUserForm.user_name" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="updateUserForm.password" />
        </el-form-item>
        <el-form-item label="权限" prop="roles">
          <el-input v-model="updateUserForm.roles" />
        </el-form-item>
        <el-form-item label="观测站id" prop="station_id">
          <el-input v-model="updateUserForm.station_id" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="updateDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateSubmit">确 定</el-button>
      </span>
    </el-dialog>
  </el-row>
</template>

<script>
import { getAllUsers, addUser, updateUser, deleteUser } from '@/api/user_management/user_management'

export default {
  name: 'SysUser',
  data() {
    return {
      currentPage: 1,
      pageSize: 6,
      formInline: {
        name: ''
      },
      addDialogVisible: false,
      addUserForm: {
        user_name: '',
        password: '',
        roles: '',
        station_id: ''
      },
      updateDialogVisible: false,
      updateUserForm: {
        user_id: '',
        user_name: '',
        password: '',
        roles: '',
        station_id: ''
      },
      userList: []
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.userList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.station_name.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.userList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getUserList()
  },
  methods: {
    async getUserList() {
      await getAllUsers().then(response => {
        console.log(response)
        this.userList = response.data
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
    },
    addSubmit() {
      addUser(this.addUserForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.addDialogVisible = false
        this.getUserList()
      })
    },
    updateBtn() {
    // 判断是否勾选了 ，无勾选不予弹窗，并给予提示
    // userTable 为table 的ref
      const _selectData = this.$refs.userTable.selection
      if (_selectData.length === 0) {
        this.$message({
          message: '请选择一行数据',
          type: 'warning'
        })
        return false
      } else if (_selectData.length > 1) {
        this.$message({
          message: '只能选中一行数据哦',
          type: 'warning'
        })
        return false
      }
      // 显示弹窗
      this.updateDialogVisible = true
      // 将选中的数据进行赋值
      this.updateUserForm = _selectData[0]
    },
    updateSubmit() {
      updateUser(this.updateUserForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.updateDialogVisible = false
        this.getUserList()
      })
    },
    deleteBatch() {
      const user_ids = []
      const _selectData = this.$refs.userTable.selection
      if (_selectData.length === 0) {
        this.$message({
          message: '请至少选择一行数据',
          type: 'warning'
        })
        return false
      }
      for (const i in _selectData) {
        if (_selectData[i].user_id === 1) {
          this.$message({
            message: '超级管理员不能删除',
            type: 'warning'
          })
          return false
        }
        user_ids.push(_selectData[i].user_id)
      }
      this.$confirm('是否删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const temp = {
          user_ids: user_ids
        }
        deleteUser(temp).then(response => {
          this.$message({
            message: response.message,
            type: 'alert'
          })
          this.getUserList()
        })
      }).catch(() => {
        return false
      })
    },
    addFormClose() {
      this.$refs.addRuleForm.resetFields()
      this.addUserForm = {
        user_name: '',
        password: '',
        roles: '',
        station_id: ''
      }
    },
    // 修改弹窗关闭回调事件
    updateFormClose() {
      this.$refs.updateRuleForm.resetFields()
      this.updateUserForm = {
        user_id: '',
        user_name: '',
        password: '',
        roles: '',
        station_id: ''
      }
    }
  }// end of methods
}
</script>
<style scoped>
</style>
