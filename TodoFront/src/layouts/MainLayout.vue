<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()

const router = useRouter()

sessionStore.fetchCurrentSession().catch(() => {
  router.push('/start')
})
</script>
