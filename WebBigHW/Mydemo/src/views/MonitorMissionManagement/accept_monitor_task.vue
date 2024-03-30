<!--接受监控任务页面 user使用-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <div>
              你的身份是：{{ curRole }}
              来自观测站：{{ curStation }} 号
            </div>
          </el-col>
          <el-col :span="6">
            <el-input v-model="formInline.name" placeholder="请输入任务名" clearable />
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="onRefresh">刷新</el-button>
          </el-col>
          <el-col :span="6">
            <el-button type="success" icon="el-icon-plus" @click="acceptBtn">接受</el-button>
          </el-col>
        </el-row>
        <!--展示表格-->
        <el-table
          ref="monitoring_taskTable"
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
            prop="monitoring_task_id"
            label="任务id"
            align="center"
          />
          <el-table-column
            prop="monitoring_task_name"
            label="任务名"
            align="center"
          />
          <el-table-column
            prop="station_id"
            label="观测站id"
            align="center"
          />
          <el-table-column
            prop="start_time"
            label="开始时间"
            align="center"
          />
          <el-table-column
            prop="end_time"
            label="结束时间"
            align="center"
          />
          <el-table-column
            prop="status"
            label="状态"
            align="center"
            :filters="[{ text: 'Undone', value: 'Undone' }, { text: 'Done', value: 'Done'}
            ]"
            :filter-method="filterTag"
            filter-placement="bottom-end"
          >
            <template slot-scope="scope">
              <!--根据tag值来选择颜色-->
              <el-tag
                :type="ChooseType(scope.row.status)"
                disable-transitions
              >{{ scope.row.status }}
              </el-tag>
            </template>
            />
          </el-table-column>
        </el-table>
        <el-footer style="height: 25px;">
          <div class="block" style="text-align: right;margin-right: 50px;">
            <el-pagination
              :current-page="currentPage"
              :page-sizes="[5,10, 20, 30, 40]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="monitoring_taskList.length"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-footer>
      </el-card>
    </el-col>
    <!--接受弹窗-->
    <el-dialog
      center
      title="执行任务"
      :visible.sync="updateDialogVisible"
      width="30%"
      @close="updateFormClose"
    >
      <el-form ref="updateRuleForm" :model="updateMonitoringTaskForm" label-width="100px">
        <el-form-item label="任务id" prop="monitoring_task_id">
          <el-input v-model="updateMonitoringTaskForm.monitoring_task_id" disabled />
        </el-form-item>
        <el-form-item label="任务名" prop="monitoring_task_name">
          <el-input v-model="updateMonitoringTaskForm.monitoring_task_name" disabled/>
        </el-form-item>
        <el-form-item label="所属站点id" prop="station_id">
          <el-input v-model="updateMonitoringTaskForm.station_id" disabled />
        </el-form-item>
        <el-form-item label="监测物种">
          <el-select v-model="updateMonitoringTaskForm.species_id">
            <el-option
              v-for="item in speciesList"
              :key="item.species_id"
              :label="item.species_id+ ' ' + item.species_name"
              :value="item.species_id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="该物种数量">
          <el-input v-model="updateMonitoringTaskForm.quantity" />
        </el-form-item>
        <el-form-item label="是否完成" prop="is_done">
          <el-radio-group v-model="updateMonitoringTaskForm.is_done">
            <el-radio label="Undone">未完成</el-radio>
            <el-radio label="Done">已完成</el-radio>
          </el-radio-group>
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
import { getMonitorTaskListByRole, acceptMonitorTask } from '@/api/monitor_mission_management/accept_monitor_task'
import { getAllSpecies } from '@/api/species_management/species_management'

export default {
  name: 'SysAcceptMonitoringTask',
  data() {
    return {
      currentPage: 1,
      pageSize: 6,
      curRole: '', // 当前用户的角色
      curStation: '', // 当前用户所在的观测站
      formInline: {
        name: ''
      },
      updateDialogVisible: false,
      updateMonitoringTaskForm: {
        monitoring_task_id: '',
        monitoring_task_name: '',
        station_id: '',
        start_time: '',
        species_id: '',
        quantity: '',
        is_done: ''
      },
      monitoring_taskList: [],
      speciesList: []
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.monitoring_taskList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.station_name.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.monitoring_taskList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getMonitoringTaskList()
    this.getSpeciesList()
  },
  methods: {
    async getMonitoringTaskList() {
      await getMonitorTaskListByRole().then(response => {
        console.log(response)
        this.monitoring_taskList = response.data.task_list
        this.curRole = response.data.user_role
        this.curStation = response.data.station_id
      })
    },
    async getSpeciesList() {
      await getAllSpecies().then(response => {
        console.log(response)
        this.speciesList = response.data
      })
    },
    onRefresh() {
      this.getMonitoringTaskList()
      this.getSpeciesList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1 // 每次改变每页显示条数时，回到第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    acceptBtn() {
    // 判断是否勾选了 ，无勾选不予弹窗，并给予提示
    // monitoring_taskTable 为table 的ref
      const _selectData = this.$refs.monitoring_taskTable.selection
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
      } else if (_selectData[0].status === 'Done') {
        this.$message({
          message: '该任务已完成，无法接受',
          type: 'warning'
        })
        return false
      }
      // 显示弹窗
      this.updateDialogVisible = true
      // 将选中的数据进行赋值
      this.updateMonitoringTaskForm = _selectData[0]
    },
    updateSubmit() {
      acceptMonitorTask(this.updateMonitoringTaskForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.updateDialogVisible = false
        this.getMonitoringTaskList()
      })
    },
    // 修改弹窗关闭回调事件
    updateFormClose() {
      this.$refs.updateRuleForm.resetFields()
      this.updateMonitoringTaskForm = {
        monitoring_task_id: '',
        monitoring_task_name: '',
        station_id: '',
        start_time: '',
        species_id: '',
        quantity: '',
        is_done: ''
      }
    },
    filterTag(value, row) {
      return row.status === value
    },
    ChooseType(tag) {
      if (tag === 'Undone') {
        return 'danger'
      } else if (tag === 'Done') {
        return 'success'
      }
    }
  }// end of methods
}
</script>
<style scoped>
</style>

