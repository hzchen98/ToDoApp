<template>
  <q-page-container>
    <q-page class="q-py-xl bg">
      <div class="absolute-right q-ma-xl q-py-xl box">
        <h1 class="text-center text-primary q-mx-xl">ToDo App</h1>
        <q-input v-model="username" label="Insert a name for start" />
        <p></p>
        <q-btn
          size="xl"
          icon="login"
          label="Start"
          class="block q-mx-auto q-margin-top"
          color="primary"
          @click="login"
        />
      </div>
    </q-page>
  </q-page-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import api from '@/boot/axios'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()

const username = ref(null)
const router = useRouter()

const login = () => {
  api.post('/', { name: username.value }).then((response) => {
    console.log(response.data)
    sessionStore.fetchCurrentSession().then(() => {
      router.push('/')
    })
  })
}
</script>

<style scoped></style>
