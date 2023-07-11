<template>
  <v-card>
    <v-card-title>
      <h5>Add Participant</h5>
    </v-card-title>
    <v-card-text>
      <form @submit.prevent="add_participant()">
        <v-text-field label="Name" v-model="participant.name"></v-text-field>
        <v-combobox v-model="participant.team" :items="
          plTeams.filter(
            (x) => !x.participant
          )
        " item-text="name" label="Team" outlined dense></v-combobox>
        <v-card-actions style="justify-content: end">
          <v-btn color="red" @click="$emit('close')" dark>Cancel</v-btn>
          <v-btn type="submit" color="green" :loading="updatingParticipant" dark>Save changes</v-btn>
        </v-card-actions>
      </form>
    </v-card-text>
  </v-card>
</template>
<script src="./index"></script>