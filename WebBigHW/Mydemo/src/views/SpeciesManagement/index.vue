<!--物种管理页面-->
<template>
  <el-row>
    <el-col :span="24">
      <el-card class="box-card">
        <el-row :gutter="20" style="margin-bottom: 15px">
          <el-col :span="6">
            <el-input v-model="formInline.name" placeholder="请输入物种名" clearable />
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
          ref="speciesTable"
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
            prop="species_id"
            label="物种id"
            align="center"
          />
          <el-table-column
            prop="species_name"
            label="物种名"
            align="center"
          />
          <el-table-column
            prop="description"
            label="物种描述"
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
              :total="speciesList.length"
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
      <el-form ref="addRuleForm" :model="addSpeciesForm" label-width="90px">
        <el-form-item label="物种名">
          <el-input v-model="addSpeciesForm.species_name" />
        </el-form-item>
        <el-form-item label="物种描述">
          <el-input
            v-model="addSpeciesForm.description"
            type="textarea"
            :rows="2"
            placeholder="请输入物种描述"
          />
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
      <el-form ref="updateRuleForm" :model="updateSpeciesForm" label-width="90px">
        <el-form-item label="物种id" prop="species_id">
          <el-input v-model="updateSpeciesForm.species_id" disabled />
        </el-form-item>
        <el-form-item label="物种名" prop="species_name">
          <el-input v-model="updateSpeciesForm.species_name" />
        </el-form-item>
        <el-form-item label="物种描述" prop="description">
          <el-input v-model="updateSpeciesForm.description" />
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
import { getAllSpecies, addSpecies, updateSpecies, deleteSpecies } from '@/api/species_management/species_management'
export default {
  name: 'SysSpecies',
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      formInline: {
        name: ''
      },
      addDialogVisible: false,
      addSpeciesForm: {
        species_name: '',
        description: ''
      },
      updateDialogVisible: false,
      updateSpeciesForm: {
        species_id: '',
        species_name: '',
        description: ''
      },
      speciesList: []
    }
  },
  computed: {
    currentPageData() {
      const startIndex = (this.currentPage - 1) * this.pageSize
      const endIndex = startIndex + this.pageSize
      if (this.formInline.name.trim()) {
        return this.speciesList.filter(item => {
          const nameMatch = !this.formInline.name.trim() || item.species_name.toLowerCase().includes(this.formInline.name.trim().toLowerCase())
          return nameMatch
        })
      }
      return this.speciesList.slice(startIndex, endIndex)
    }
  },
  created() {
    this.getSpeciesList()
  },
  methods: {
    async getSpeciesList() {
      await getAllSpecies().then(response => {
        console.log(response)
        this.speciesList = response.data
      })
    },
    onRefresh() {
      this.getSpeciesList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1 // 每次改变每页显示条数时，回到第一页
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    addSubmit() {
      addSpecies(this.addSpeciesForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.addDialogVisible = false
        this.getSpeciesList()
      })
    },
    updateBtn() {
    // 判断是否勾选了 ，无勾选不予弹窗，并给予提示
    // speciesTable 为table 的ref
      const _selectData = this.$refs.speciesTable.selection
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
      this.updateSpeciesForm = _selectData[0]
    },
    updateSubmit() {
      updateSpecies(this.updateSpeciesForm).then(response => {
        this.$message({
          message: response.message,
          type: 'alert'
        })
        this.updateDialogVisible = false
        this.getSpeciesList()
      })
    },
    deleteBatch() {
      const species_ids = []
      const _selectData = this.$refs.speciesTable.selection
      if (_selectData.length === 0) {
        this.$message({
          message: '请至少选择一行数据',
          type: 'warning'
        })
        return false
      }
      for (const i in _selectData) {
        species_ids.push(_selectData[i].species_id)
      }
      this.$confirm('是否删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const temp = {
          species_ids: species_ids
        }
        deleteSpecies(temp).then(response => {
          this.$message({
            message: response.message,
            type: 'alert'
          })
          this.getSpeciesList()
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
