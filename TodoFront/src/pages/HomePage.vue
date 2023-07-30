<template>
  <topbar-component :name="name" @close-session="closeSession"></topbar-component>

  <q-page-container>
    <q-page class="q-py-xl bg">
      <div class="q-pa-md q-gutter-md">
        <h1 class="text-h6">To-Do List</h1>
        <q-input rounded outlined v-model="searchText" @update:model-value="searchTasks">
          <template v-slot:append> <q-icon name="search" /> </template
        ></q-input>
        <task-list-component
          :tasks="tasks"
          @delete-task="deleteTask"
          @add-task="addTask"
          @update-task="updateTask"
        ></task-list-component>
      </div>
    </q-page>
  </q-page-container>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia'
import { useSessionStore } from '@/stores/session'
import { useTaskStore } from '@/stores/taskStore'
import TopbarComponent from '@/components/TopbarComponent.vue'
import TaskListComponent from '@/components/TaskListComponent.vue'
import { ref } from 'vue'
import type Task from '@/models/Task'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const router = useRouter()
const sessionStore = useSessionStore()
const taskStore = useTaskStore()

const { name } = storeToRefs(sessionStore)
const { tasks } = storeToRefs(taskStore)

const searchText = ref('')

const $q = useQuasar()

taskStore.getTasks('')

const searchTasks = () => {
  taskStore.getTasks(searchText.value)
}

const addTask = (newTask: Task) => {
  taskStore.addTask(newTask).then(() => {
    $q.notify('New task created!')
  })
}

const deleteTask = (task: Task) => {
  taskStore.deleteTask(task.uuid).then(() => {
    $q.notify(`Task "${task.title}" is deleted`)
  })
}

const updateTask = (task: Task) => {
  taskStore.updateTask(task).then(() => {
    $q.notify(`Task "${task.title}" is updated`)
  })
}

const closeSession = () => {
  sessionStore.exit()
  $q.notify(`Bye ${name.value}!`)
  router.push('/start')
}
</script>

<style scoped></style>
