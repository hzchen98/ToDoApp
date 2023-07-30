<template>
  <q-list bordered class="rounded-borders" padding>
    <q-expansion-item expand-separator icon="add" label="New task">
      <q-card class="q-mt-md">
        <q-card-section>
          <q-input v-model="newTask.title" label="Title" />
          <q-input v-model="newTask.description" label="Description" />
        </q-card-section>

        <q-card-actions>
          <q-btn
            label="Add Task"
            @click="addTask"
            icon="add"
            class="q-mx-auto"
            color="primary"
          />
        </q-card-actions> </q-card
    ></q-expansion-item>
    <q-item v-for="(task, index) in tasks" :key="index">
      <q-item-section side>
        <q-checkbox v-model="task.done" color="positive" @update:model-value="updateTask(task)" />
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ task.title }}</q-item-label>
        <q-item-label caption>{{ task.description }}</q-item-label>
      </q-item-section>
      <q-item-section side>
        <q-btn icon="delete" color="red" @click="deleteTask(task)"></q-btn>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import type Task from '@/models/Task'
import { ref } from 'vue'

const props = defineProps({
  tasks: { type: Array<Task>, required: true }
})

const $emit = defineEmits(['deleteTask', 'addTask', 'updateTask'])

const deleteTask = (task: Task) => {
  $emit('deleteTask', task)
}

const newTask = ref({} as Task)

const addTask = () => {
  $emit('addTask', newTask.value)
  newTask.value = {} as Task
}

const updateTask = (task: Task) => {
  $emit('updateTask', task)
}
</script>
