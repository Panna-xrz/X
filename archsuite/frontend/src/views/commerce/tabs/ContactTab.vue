<script setup lang="ts">
import { h, ref, reactive, computed, watch, onMounted } from 'vue'
import {
  NCard,
  NDataTable,
  NSpace,
  NButton,
  NModal,
  NForm,
  NFormItem,
  NInput,
  NPopconfirm,
  NEmpty,
  useMessage
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { getContacts, createContact, updateContact, deleteContact } from '@/api/contact'
import type { ContactPerson, ContactType } from '@/types'

// 联系单 Tab：委方联系单 + 小组联系单
const props = defineProps<{ projectId: number }>()

const message = useMessage()

// 委方数据
const clientLoading = ref(false)
const clientList = ref<ContactPerson[]>([])
// 小组数据
const teamLoading = ref(false)
const teamList = ref<ContactPerson[]>([])

// 新增/编辑弹窗
const showModal = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const editingType = ref<ContactType>('client')
const formModel = reactive({
  name: '',
  role: '',
  phone: '',
  remarks: ''
})

function makeColumns(type: ContactType): DataTableColumns<ContactPerson> {
  return [
    type === 'client'
      ? { title: '职务', key: 'role', render: (row) => row.role || '-' }
      : { title: '专业', key: 'role', render: (row) => row.role || '-' },
    { title: '姓名', key: 'name' },
    { title: '电话', key: 'phone', width: 160, render: (row) => row.phone || '-' },
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
                default: () => '确认删除该联系人？'
              }
            )
          ]
        })
    }
  ]
}

const clientColumns = computed(() => makeColumns('client'))
const teamColumns = computed(() => makeColumns('team'))

async function loadClient() {
  if (!props.projectId) return
  clientLoading.value = true
  try {
    const res = await getContacts({ projectId: props.projectId, contactType: 'client', page: 1, pageSize: 200 })
    clientList.value = res.list || []
  } catch (e) {
    clientList.value = []
    message.error(e instanceof Error ? e.message : '加载委方联系单失败')
  } finally {
    clientLoading.value = false
  }
}

async function loadTeam() {
  if (!props.projectId) return
  teamLoading.value = true
  try {
    const res = await getContacts({ projectId: props.projectId, contactType: 'team', page: 1, pageSize: 200 })
    teamList.value = res.list || []
  } catch (e) {
    teamList.value = []
    message.error(e instanceof Error ? e.message : '加载小组联系单失败')
  } finally {
    teamLoading.value = false
  }
}

async function loadAll() {
  await Promise.all([loadClient(), loadTeam()])
}

function openCreate(type: ContactType) {
  editingType.value = type
  editingId.value = null
  Object.assign(formModel, { name: '', role: '', phone: '', remarks: '' })
  showModal.value = true
}

function openEdit(row: ContactPerson) {
  editingType.value = row.contactType
  editingId.value = row.id
  Object.assign(formModel, {
    name: row.name,
    role: row.role || '',
    phone: row.phone || '',
    remarks: row.remarks || ''
  })
  showModal.value = true
}

async function submit() {
  if (!formModel.name) {
    message.warning('请填写姓名')
    return
  }
  submitting.value = true
  try {
    const payload = {
      name: formModel.name,
      role: formModel.role || null,
      phone: formModel.phone || null,
      remarks: formModel.remarks || null,
      contactType: editingType.value
    }
    if (editingId.value) {
      await updateContact(editingId.value, payload)
      message.success('更新成功')
    } else {
      await createContact({ ...payload, projectId: props.projectId })
      message.success('新增成功')
    }
    showModal.value = false
    await loadAll()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '提交失败')
  } finally {
    submitting.value = false
  }
}

async function remove(id: number) {
  try {
    await deleteContact(id)
    message.success('删除成功')
    await loadAll()
  } catch (e) {
    message.error(e instanceof Error ? e.message : '删除失败')
  }
}

watch(() => props.projectId, () => loadAll(), { immediate: false })
onMounted(() => loadAll())
</script>

<template>
  <div class="contact-tab">
    <NCard title="委方联系单" :bordered="false" size="small">
      <template #header-extra>
        <NButton size="small" type="primary" @click="openCreate('client')">+ 新增委方联系人</NButton>
      </template>
      <NDataTable :columns="clientColumns" :data="clientList" :loading="clientLoading" :bordered="false" :single-line="false">
        <template #empty>
          <NEmpty description="暂无委方联系人" size="small" />
        </template>
      </NDataTable>
    </NCard>

    <NCard title="小组联系单" :bordered="false" size="small" style="margin-top: 16px">
      <template #header-extra>
        <NButton size="small" type="primary" @click="openCreate('team')">+ 新增小组成员</NButton>
      </template>
      <NDataTable :columns="teamColumns" :data="teamList" :loading="teamLoading" :bordered="false" :single-line="false">
        <template #empty>
          <NEmpty description="暂无小组成员" size="small" />
        </template>
      </NDataTable>
    </NCard>

    <NModal
      v-model:show="showModal"
      preset="card"
      :title="editingId ? '编辑联系人' : '新增联系人'"
      style="width: 440px"
      :bordered="false"
    >
      <NForm label-placement="left" label-width="60">
        <NFormItem label="姓名" required>
          <NInput v-model:value="formModel.name" placeholder="请输入姓名" />
        </NFormItem>
        <NFormItem :label="editingType === 'client' ? '职务' : '专业'">
          <NInput v-model:value="formModel.role" :placeholder="editingType === 'client' ? '如：项目经理' : '如：建筑/结构/机电'" />
        </NFormItem>
        <NFormItem label="电话">
          <NInput v-model:value="formModel.phone" placeholder="联系电话" />
        </NFormItem>
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
  </div>
</template>
