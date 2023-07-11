<template>
  <v-toolbar color="primary" dark>
    <v-btn :disabled="!currentGroupIndex" icon @click="$emit('previous_stage_click')">
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>
    <v-toolbar-title class="mx-auto">{{
        groupName
    }}</v-toolbar-title>
    <v-btn icon @click="$emit('next_stage_click')" class="mr-2">
      <v-icon>mdi-chevron-right</v-icon>
    </v-btn>
  </v-toolbar>
</template>
<script src="./index"></script>