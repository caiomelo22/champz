<template>
  <v-card>
    <v-card-title>
      <h3>
        {{text}}
      </h3>
    </v-card-title>
    <v-card-text>
      <v-card-actions class="text-center" style="justify-content: end">
        <v-btn class="mr-2" color="red" dark @click="$emit('close')">Cancel</v-btn>
        <v-btn color="primary" dark @click="$emit('confirm')">Confirm</v-btn>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
<script src="./index"></script>