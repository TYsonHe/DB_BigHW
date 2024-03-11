<!--观测站管理页面 admin专属-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <el-input v-model="query.name" placeholder="请输入观测站名" clearable>
              <el-button slot="append" icon="el-icon-search" @click="queryBtn" />
            </el-input>
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
          ref="stationTable"
          :data="stationList"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column
            type="selection"
            width="55"
          />
          <el-table-column
            prop="station_id"
            label="观测站id"
            align="center"
          />
          <el-table-column
            prop="station_name"
            label="观测站名字"
            align="center"
          />
          <el-table-column
            prop="location_name"
            label="位置"
            align="center"
          />
          <el-table-column
            prop="equipment"
            label="装置信息"
            align="center"
          />
        </el-table>
      </el-card>
    </el-col>
    <!--新增弹窗-->
    <el-dialog
      center
      title="新增"
      :visible.sync="addDialogVisible"
      width="30%"
    >
      <el-form ref="addRuleForm" :model="addStationForm" label-width="90px">
        <el-form-item label="用户名">
          <el-input v-model="addStationForm.station_name" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="addStationForm.password" />
        </el-form-item>
        <el-form-item label="权限">
          <el-input v-model="addStationForm.roles" />
        </el-form-item>
        <el-form-item label="观测站id">
          <el-input v-model="addStationForm.station_id" />
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
    >
      <el-form ref="updateRuleForm" :model="updateStationForm" label-width="90px">
        <el-form-item label="用户id" prop="station_id">
          <el-input v-model="updateStationForm.station_id" disabled />
        </el-form-item>
        <el-form-item label="用户名" prop="station_name">
          <el-input v-model="updateStationForm.station_name" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="updateStationForm.password" />
        </el-form-item>
        <el-form-item label="权限" prop="roles">
          <el-input v-model="updateStationForm.roles" />
        </el-form-item>
        <el-form-item label="观测站id" prop="station_id">
          <el-input v-model="updateStationForm.station_id" />
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
import { getAllStations, addStation, updateStation, deleteStation } from '@/api/station_management/station_management'

export default {
  name: 'SysStation',
  data() {
    return {
      query: {
        current: 1,
        size: 10,
        name: ''
      },
      addDialogVisible: false,
      addStationForm: {
        station_name: '',
        password: '',
        roles: '',
        station_id: ''
      },
      updateDialogVisible: false,
      updateStationForm: {
        station_id: '',
        station_name: '',
        password: '',
        roles: ''
      },
      stationList: []
    }
  },
  created() {
    this.getStationList()
  },
  methods: {
    async getStationList() {
      await getAllStations().then(response => {
        console.log(response)
        this.stationList = response.data
      })
    },
    onRefresh() {
      this.getStationList()
    },
    addSubmit() {
      addStation(this.addStationForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.addDialogVisible = false
        this.getStationList()
      })
    },
    updateBtn() {
    // 判断是否勾选了 ，无勾选不予弹窗，并给予提示
    // stationTable 为table 的ref
      const _selectData = this.$refs.stationTable.selection
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
      this.updateStationForm = _selectData[0]
    },
    updateSubmit() {
      updateStation(this.updateStationForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.updateDialogVisible = false
        this.getStationList()
      })
    },
    deleteBatch() {
      const station_ids = []
      const _selectData = this.$refs.stationTable.selection
      if (_selectData.length === 0) {
        this.$message({
          message: '请至少选择一行数据',
          type: 'warning'
        })
        return false
      }
      for (const i in _selectData) {
        station_ids.push(_selectData[i].station_id)
      }
      this.$confirm('是否删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const temp = {
          station_ids: station_ids
        }
        deleteStation(temp).then(response => {
          this.$message({
            message: response.message,
            type: 'alert'
          })
          this.getStationList()
        })
      }).catch(() => {
        return false
      })
    }
  }// end of methods
}
</script>
<style scoped>
</style>
