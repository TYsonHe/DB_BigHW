<!--观测站管理页面 admin专属-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <el-input v-model="formInline.name" placeholder="请输入观测站名" clearable />
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
        <el-footer>
          <div class="block" style="text-align: right;margin-right: 50px;">
            <el-pagination
              :current-page="currentPage"
              :page-sizes="[5,10, 20, 30, 40]"
              :page-size="pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              :total="stationList.length"
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
      <el-form ref="addRuleForm" :model="addStationForm" label-width="90px">
        <el-form-item label="观测站名">
          <el-input v-model="addStationForm.station_name" />
        </el-form-item>
        <el-form-item label="观测站位置">
          <el-input v-model="addStationForm.location_name" />
        </el-form-item>
        <el-form-item label="装置信息">
          <el-input v-model="addStationForm.equipment" />
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
      <el-form ref="updateRuleForm" :model="updateStationForm" label-width="90px">
        <el-form-item label="站点id" prop="station_id">
          <el-input v-model="updateStationForm.station_id" disabled />
        </el-form-item>
        <el-form-item label="观测站名" prop="station_name">
          <el-input v-model="updateStationForm.station_name" />
        </el-form-item>
        <el-form-item label="位置" prop="location_name">
          <el-input v-model="updateStationForm.location_name" />
        </el-form-item>
        <el-form-item label="装置信息" prop="equipment">
          <el-input v-model="updateStationForm.equipment" />
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
      currentPage: 1,
      pageSize: 6,
      formInline: {
        name: ''
      },
      addDialogVisible: false,
      addStationForm: {
        station_name: '',
        location_name: '',
        equipment: ''
      },
      updateDialogVisible: false,
      updateStationForm: {
        station_id: '',
        station_name: '',
        location_name: '',
        equipment: ''
      },
      stationList: []
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.stationList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.station_name.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.stationList.slice(startIndex, endIndex)
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
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1 // 每次改变每页显示条数时，回到第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val
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
      console.log(this.updateStationForm)
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
    },
    addFormClose() {
      this.$refs.addRuleForm.resetFields()
      this.addSpeciesForm = {
        species_name: '',
        description: ''
      }
    },
    // 修改弹窗关闭回调事件
    updateFormClose() {
      this.$refs.updateRuleForm.resetFields()
      this.updateSpeciesForm = {
        species_id: '',
        species_name: '',
        description: ''
      }
    }
  }// end of methods
}
</script>
<style scoped>
</style>
