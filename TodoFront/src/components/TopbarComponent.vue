<template>
    <q-toolbar class="text-white bg-primary" >
      <q-toolbar-title class="text-center">
      Hi {{ name }}!
      </q-toolbar-title>
      <q-btn flat round dense icon="logout" @click="$emit('closeSession')" />
    </q-toolbar>
</template>

<script setup lang="ts">

defineProps(['name'])
const $emit = defineEmits(['closeSession'])


</script>
