<!--报警任务页面 user使用-->
<template>
  <div class="parent">
    <div class="div1">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <div>
              你的身份是：{{ curRole }}
              来自观测站：{{ curStation }} 号
            </div>
          </el-col>
          <el-col :span="4">
            <el-input v-model="formInline.name" placeholder="请输入报警类型" clearable />
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="onRefresh">刷新</el-button>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="onGenerate">自动预警</el-button>
          </el-col>
          <el-col :span="4">
            <el-button type="success" icon="el-icon-plus" @click="acceptBtn">接受</el-button>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-card class="div2">
      <div class="databoard">
        <span style="font-weight: bold; font-size: 24px;">任务总量</span>
        <dv-digital-flop :config="config1" />
      </div>
    </el-card>
    <el-card class="div3">
      <middle_chart v-if="waitforReady" :cur-station-id="curStation" />
    </el-card>
    <el-card class="div4">
      <right_chart :cur-station-id="curStation" />
    </el-card>
    <el-card class="div5">
      <!--展示表格-->
      <el-table
        ref="alert_taskTable"
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
          prop="alert_task_id"
          label="任务id"
          align="center"
        />
        <el-table-column
          prop="station_id"
          label="观测站id"
          align="center"
        />
        <el-table-column
          prop="alert_type"
          label="报警类型"
          align="center"
        />
        <el-table-column
          prop="species_id"
          label="异常物种ID"
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
            :total="alert_taskList.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-footer>
    </el-card>
    <!--接受弹窗-->
    <el-dialog
      center
      title="执行任务"
      :visible.sync="updateDialogVisible"
      width="30%"
      @close="updateFormClose"
    >
      <el-form ref="updateRuleForm" :model="updateAlertTaskForm" label-width="100px">
        <el-form-item label="任务id" prop="alert_task_id">
          <el-input v-model="updateAlertTaskForm.alert_task_id" disabled />
        </el-form-item>
        <el-form-item label="报警类型" prop="alert_type">
          <el-input v-model="updateAlertTaskForm.alert_type" disabled />
        </el-form-item>
        <el-form-item label="所属站点id" prop="station_id">
          <el-input v-model="updateAlertTaskForm.station_id" disabled />
        </el-form-item>
        <el-form-item label="报警物种">
          <el-select v-model="updateAlertTaskForm.species_id">
            <el-option
              v-for="item in speciesList"
              :key="item.species_id"
              :label="item.species_id+ ' ' + item.species_name"
              :value="item.species_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="该物种数量">
          <el-input v-model="updateAlertTaskForm.quantity" />
        </el-form-item>
        <el-form-item label="是否完成" prop="is_done">
          <el-radio-group v-model="updateAlertTaskForm.is_done">
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
  </div>
</template>

<script>
import { getAlertTaskListByRole, getAllAlertTaskCount, acceptAlertTask, generateAlertTask } from '@/api/alert_task_management/check_alert_task'
import { getAllSpecies } from '@/api/species_management/species_management'

import right_chart from '@/views/AlertTaskManagement/right_chart.vue'
import middle_chart from '@/views/AlertTaskManagement/middle_chart.vue'

export default {
  name: 'SysAcceptAlertTask',
  components: {
    right_chart,
    middle_chart
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 6,
      curRole: '', // 当前用户的角色
      curStation: 0, // 当前用户所在的观测站
      formInline: {
        name: ''
      },
      updateDialogVisible: false,
      updateAlertTaskForm: {
        alert_task_id: '',
        alert_type: '',
        station_id: '',
        start_time: '',
        species_id: '',
        quantity: '',
        is_done: ''
      },
      alert_taskList: [],
      speciesList: [],
      config1: {
        number: [],
        content: '{nt}个'
      },
      waitforReady: false
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.alert_taskList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.alert_type.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.alert_taskList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getAlertTaskList()
    this.getSpeciesList()
    this.getAlertTaskCount()
  },
  mounted() {
    this.waitforReady = true
    // 轮询
    this.timer = setInterval(() => {
      this.getAlertTaskCount()
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    async getAlertTaskList() {
      await getAlertTaskListByRole().then(response => {
        this.alert_taskList = response.data.task_list
        this.curRole = response.data.user_role
        this.curStation = response.data.station_id
      })
    },
    async getSpeciesList() {
      await getAllSpecies().then(response => {
        this.speciesList = response.data
      })
    },
    async getAlertTaskCount() {
      await getAllAlertTaskCount().then(response => {
        this.config1.number = [response.data.task_count]
        this.config1 = { ...this.config1 }
      })
    },
    onRefresh() {
      this.getAlertTaskList()
      this.getSpeciesList()
    },
    onGenerate() {
      generateAlertTask().then(response => {
        this.$message({
          message: response.message,
          type: 'info'
        })
        this.getAlertTaskList()
      })
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
    // alert_taskTable 为table 的ref
      const _selectData = this.$refs.alert_taskTable.selection
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
      this.updateAlertTaskForm = _selectData[0]
    },
    updateSubmit() {
      acceptAlertTask(this.updateAlertTaskForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.updateDialogVisible = false
        this.getAlertTaskList()
      })
    },
    // 修改弹窗关闭回调事件
    updateFormClose() {
      this.$refs.updateRuleForm.resetFields()
      this.updateAlertTaskForm = {
        alert_task_id: '',
        alert_type: '',
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
.parent {
  margin-left: 10px;
  margin-right: 10px;
display: grid;
grid-template-columns: repeat(6, 1fr);
grid-template-rows: 0.4fr 1fr repeat(2, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
}

.div1 { grid-area: 1 / 1 / 2 / 7; }
.div2 { grid-area: 2 / 1 / 3 / 3;
margin-top: 10px;
  margin-left: 10px;
}
.div3 { grid-area: 2 / 3 / 3 / 5;
  margin-left: 10px;
margin-top: 10px;
}
.div4 { grid-area: 2 / 5 / 3 / 7;
  margin-left: 10px;
margin-top: 10px;
}
.div5 { grid-area: 3 / 1 / 5 / 7;
margin-top: 10px;}

.databoard {
  margin-top: 20px;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
  height: 100%;
  width: 100%;
}
</style>

