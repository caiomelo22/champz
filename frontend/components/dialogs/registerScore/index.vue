<template>
  <v-card>
    <v-card-title>
      <h5>Register Score</h5>
    </v-card-title>
    <v-card-text>
      <form @submit.prevent="register_score()">
        <v-row>
          <v-col cols="12" md="3">
            <span class="champz-font mr-2 mt-1" style="float: right">{{
                match.participant_1.name
            }}</span>
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field outlined dense type="number" v-model="match.goals_participant_1" min="0" required="required">
            </v-text-field>
          </v-col>
          <v-col cols="12" md="2">
            <span class="champz-font ml-7 mt-1">X</span>
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field outlined dense type="number" v-model="match.goals_participant_2" min="0" required="required">
            </v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <span class="champz-font ml-3 mt-1" style="float: left">{{
                match.participant_2.name
            }}</span>
          </v-col>
        </v-row>
        <v-card-actions style="justify-content: end">
          <v-btn type="button" color="red" dark @click="$emit('close')">Close</v-btn>
          <v-btn type="submit" color="green" :dark="!(!match.goals_participant_2 ||
          !match.goals_participant_1)" :disabled="
    !match.goals_participant_2 ||
    !match.goals_participant_1
  " :loading="registerScoreLoading">Save changes</v-btn>
        </v-card-actions>
      </form>
    </v-card-text>
  </v-card>
</template>
<script src="./index"></script>