<script setup lang="ts">
import { h, ref, reactive, computed, onMounted, watch } from 'vue'
import {
  NCard,
  NDataTable,
  NSpace,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NPopconfirm,
  NEmpty,
  NTag,
  useMessage
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import {
  getProjectBuildings,
  createProjectBuilding,
  updateProjectBuilding,
  deleteProjectBuilding
} from '@/api/project'
import type { ProjectBuilding } from '@/types'

// 建筑单体 Tab：表格列表 + 新增/编辑弹窗 + 删除
const props = defineProps<{ projectId: number }>()

const message = useMessage()
const loading = ref(false)
const dataList = ref<ProjectBuilding[]>([])

// 表格列
const columns = computed<DataTableColumns<ProjectBuilding>>(() => [
  { title: '编号', key: 'code', width: 120, render: (row) => row.code || '-' },
  { title: '名称', key: 'name' },
  { title: '性质', key: 'buildingNature', width: 120, render: (row) => row.buildingNature || '-' },
  { title: '功能', key: 'buildingFunction', width: 120, render: (row) => row.buildingFunction || '-' },
  { title: '地上层数', key: 'floorsAbove', width: 100, render: (row) => row.floorsAbove ?? '-' },
  { title: '地下层数', key: 'floorsUnder', width: 100, render: (row) => row.floorsUnder ?? '-' },
  { title: '高度（m）', key: 'height', width: 100, render: (row) => row.height ?? '-' },
  { title: '面积（㎡）', key: 'floorArea', width: 120, render: (row) => row.floorArea ?? '-' },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    render: (row) =>
      h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            { size: 'small', text: true, type: 'primary', onClick: () => openEdit(row) },
            { default: () => '编辑' }
          ),
          h(
            NPopconfirm,
            { onPositiveClick: () => remove(row.id) },
            {
              trigger: () =>
                h(
                  NButton,
                  { size: 'small', text: true, type: 'error' },
                  { default: () => '删除' }
                ),
              default: () => '确认删除该建筑单体？'
            }
          )
        ]
      })
  }
])

// 新增/编辑弹窗
const showModal = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const formModel = reactive({
  code: '',
  name: '',
  buildingNature: '',
  buildingFunction: '',
  floorsAbove: null as number | null,
  floorsUnder: null as number | null,
  height: null as number | null,
  floorArea: null as number | null,
  remarks: ''
})

async function loadList() {
  if (!props.projectId) return
  loading.value = true
  try {
    const data = await getProjectBuildings(props.projectId)
    dataList.value = data || []
  } catch (e) {
    dataList.value = []
    message.error(e instanceof Error ? e.message : '加载建筑单体失败')
  } finally {
    loading.value = false
  }
}

function resetForm() {
  Object.assign(formModel, {
    code: '',
    name: '',
    buildingNature: '',
    buildingFunction: '',
    floorsAbove: null,
    floorsUnder: null,
    height: null,
    floorArea: null,
    remarks: ''
  })
}

function openCreate() {
  editingId.value = null
  resetForm()
  showModal.value = true
}

function openEdit(row: ProjectBuilding) {
  editingId.value = row.id
  Object.assign(formModel, {
    code: row.code || '',
    name: row.name,
    buildingNature: row.buildingNature || '',
    buildingFunction: row.buildingFunction || '',
    floorsAbove: row.floorsAbove,
    floorsUnder: row.floorsUnder,
    height: row.height,
    floorArea: row.floorArea,
    remarks: row.remarks || ''
  })
  showModal.value = true
}

async function submit() {
  if (!formModel.name) {
    message.warning('请填写建筑名称')
    return
  }
  submitting.value = true
  try {
    const payload = {
      code: formModel.code || undefined,
      name: formModel.name,
      buildingNature: formModel.buildingNature || null,
      buildingFunction: formModel.buildingFunction || null,
      floorsAbove: formModel.floorsAbove,
      floorsUnder: formModel.floorsUnder,
      height: formModel.height,
      floorArea: formModel.floorArea,
      remarks: formModel.remarks || null
    }
    if (editingId.value) {
      await updateProjectBuilding(props.projectId, editingId.value, payload)
      message.success('更新成功')
    } else {
      await createProjectBuilding(props.projectId, payload)
      message.success('新增成功')
    }
    showModal.value = false
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '提交失败')
  } finally {
    submitting.value = false
  }
}

async function remove(id: number) {
  try {
    await deleteProjectBuilding(props.projectId, id)
    message.success('删除成功')
    await loadList()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

watch(() => props.projectId, () => loadList(), { immediate: false })
onMounted(() => loadList())
</script>

<template>
  <NCard :bordered="false" size="small">
    <template #header-extra>
      <NSpace>
        <NButton size="small" @click="loadList">刷新</NButton>
        <NButton size="small" type="primary" @click="openCreate">+ 新增建筑</NButton>
      </NSpace>
    </template>

    <NDataTable :columns="columns" :data="dataList" :loading="loading" :bordered="false" :single-line="false">
      <template #empty>
        <NEmpty description="暂无建筑单体，请新增" />
      </template>
    </NDataTable>

    <NModal
      v-model:show="showModal"
      preset="card"
      :title="editingId ? '编辑建筑单体' : '新增建筑单体'"
      style="width: 520px"
      :bordered="false"
    >
      <NForm label-placement="left" label-width="88">
        <div class="form-grid">
          <NFormItem label="编号">
            <NInput v-model:value="formModel.code" placeholder="如：B-01" />
          </NFormItem>
          <NFormItem label="名称" required>
            <NInput v-model:value="formModel.name" placeholder="如：1# 楼" />
          </NFormItem>
          <NFormItem label="性质">
            <NInput v-model:value="formModel.buildingNature" placeholder="如：办公楼/住宅" />
          </NFormItem>
          <NFormItem label="功能">
            <NInput v-model:value="formModel.buildingFunction" placeholder="如：办公/商业" />
          </NFormItem>
          <NFormItem label="地上层数">
            <NInputNumber v-model:value="formModel.floorsAbove" :min="0" :precision="0" style="width: 100%" />
          </NFormItem>
          <NFormItem label="地下层数">
            <NInputNumber v-model:value="formModel.floorsUnder" :min="0" :precision="0" style="width: 100%" />
          </NFormItem>
          <NFormItem label="高度（m）">
            <NInputNumber v-model:value="formModel.height" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
          <NFormItem label="面积（㎡）">
            <NInputNumber v-model:value="formModel.floorArea" :min="0" :precision="2" style="width: 100%" />
          </NFormItem>
        </div>
        <NFormItem label="备注">
          <NInput v-model:value="formModel.remarks" type="textarea" :rows="2" />
        </NFormItem>
      </NForm>
      <template #footer>
        <NSpace justify="end">
          <NButton size="small" @click="showModal = false">取消</NButton>
          <NButton size="small" type="primary" :loading="submitting" @click="submit">确定</NButton>
        </NSpace>
      </template>
    </NModal>
  </NCard>
</template>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 16px;
}
</style>
