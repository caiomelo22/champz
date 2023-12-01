<template>
  <div class="mx-4">
    <v-row style="margin-top: 32px" class="mt-4">
      <v-col cols="12" md="5" class="pl-0">
        <v-row>
          <v-card style="width: 100%">
            <v-card-text>
              <h5>Set budget</h5>
              <v-text-field class="mt-2" min="0" v-model="genericBudget" hide-details dense outlined flat>
              </v-text-field>
            </v-card-text>
          </v-card>
        </v-row>
        <v-row style="margin-top: 32px">
          <v-card style="width: 100%">
            <v-card-title>
              <h3>List of participants</h3>
              <v-spacer></v-spacer>
              <v-icon large color="green" @click="open_participant_dialog(null)">mdi-plus</v-icon>
            </v-card-title>
            <v-card-text>
              <v-row v-if="participantsLoading" class="loader-row">
                <v-progress-circular indeterminate size="20" color="#3330E4"></v-progress-circular>
              </v-row>
              <div class="champz-table-wrapper" v-else>
                <table class="champz-table">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">
                        <b>Name</b>
                      </th>
                      <th scope="col">
                        <b>Budget</b>
                      </th>
                      <th scope="col">
                        <b>Team</b>
                      </th>
                      <th scope="col" class="text-center">
                        <b>Action</b>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(participant, i) in participants" :key="i">
                      <td class="champzFont">{{ participant.id }}</td>
                      <td class="champzFont">{{ participant.name }}</td>
                      <td class="champzFont">${{ participant.budget }}</td>
                      <td class="champzFont">
                        <img style="width: 30px" :src="gs.get_image_path(participant.team_image_path)" />
                        {{ participant.team_name }}
                      </td>
                      <td class="text-center">
                        <v-icon color="#3330E4" @click="open_participant_dialog(participant)">mdi-pencil</v-icon>
                        <v-icon color="#EB1D36" class="ml-2" @click="delete_participant(participant.id)">mdi-trash-can
                        </v-icon>
                        <v-icon color="#3330E4" class="ml-2" :loading="participant.team_loading_att" @click="
                          get_players_by_team(participant, participant.team_id)
                        ">mdi-eye</v-icon>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </v-card-text>
          </v-card>
        </v-row>
      </v-col>
      <v-col cols="12" md="7" class="pr-0">
        <v-row>
          <v-card style="width: 100%">
            <v-card-title>
              <h3>List of Players</h3>
            </v-card-title>
            <v-card-text>
              <v-tabs v-model="tab" color="#3330E4">
                <v-tab v-for="(p, i) in positions" :key="i">
                  {{ p.name }}
                </v-tab>
              </v-tabs>
              <v-row justify="center" v-if="playersLoading" class="my-6 pa-4">
                <v-progress-circular indeterminate size="15" color="primary"></v-progress-circular>
              </v-row>
              <div class="champz-table-wrapper mt-4" v-else-if="tab != -1">
                <table class="champz-table">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">
                        <b>Player</b>
                      </th>
                      <th></th>
                      <th scope="col">
                        <b>Overall</b>
                      </th>
                      <th scope="col">
                        <b>Position</b>
                      </th>
                      <th scope="col">
                        <b>Owner</b>
                      </th>
                      <th scope="col">
                        <b>Price</b>
                      </th>
                      <th scope="col">
                        <b>Action</b>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="player in selectedPosition"
                      :key="`${player.id}-${player.team_participant}-${player.value}`">
                      <td class="champzFont">{{ player.id }}</td>
                      <td class="champzFont">
                        <img :src="gs.get_image_path(player.image_path)" style="max-height: 65px" />
                        <img style="width: 30px" :src="gs.get_image_path(player.nation_image_path)" />
                        <img style="width: 30px" :src="gs.get_image_path(player.team_origin_image_path)" />
                      </td>
                      <td class="champzFont">
                        <span>{{ player.name }}</span>
                      </td>
                      <td class="champzFont">{{ player.overall }}</td>
                      <td class="champzFont">{{ player.specific_position }}</td>
                      <td class="champzFont">
                        {{
                            player.team_participant_id
                              ? get_participant_name(
                                player.participant_id
                              )
                              : "-"
                        }}
                      </td>
                      <td class="champzFont">${{ player.value }}</td>
                      <td>
                        <v-icon color="#2B7A0B" large @click="get_player(player)">mdi-cash-plus</v-icon>
                        <v-icon color="#EB1D36" class="ml-2" large @click="remove_buy(player)">mdi-cash-minus</v-icon>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </v-card-text>
          </v-card>
        </v-row>
      </v-col>
    </v-row>

    <!-- <h3>List of Players</h3>
      
      <div class="container">
        <button
          class="btn btn-outline-info"
          v-on:click="generate_transfers_file()"
        >Generate Transfers File</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generate_players_file()"
        >Generate Players Excel</button>
        <button
          class="btn btn-outline-info"
          v-on:click="generate_teams_file()"
        >Generate Participants Teams Excel</button>
        <a style="float: right;" class="btn btn-success" :href="'/webapp/matches'">Matches</a>
      </div>
      <br />
      <br />
      <br />
    <br />-->
    <!-- Add Participant Modal -->
    <v-dialog v-if="addParticipantDialog" v-model="addParticipantDialog" width="700px" max-width="100%">
      <AddParticipant :participant-prop="newParticipant" :teams="teams" @close="reset_participant_dialog"
        @update="participant_added" />
    </v-dialog>
    <!-- Buy Player Modal -->
    <v-dialog v-if="buyPlayerDialog" v-model="buyPlayerDialog" width="700px" max-width="100%" persistent>
      <BuyPlayer :participants="participants" :current-player="currentPlayer" @close="reset_player_modal" @update="player_updated" />
    </v-dialog>
    <!-- Show participant team Modal -->
    <v-dialog v-model="participantTeamDialog" width="700px" max-width="100%">
      <ParticipantTeam :selected-team="selectedTeam" :current-participant="currentParticipant" @remove="remove_buy" />
    </v-dialog>
  </div>
</template>

<style lang="scss" scoped>
</style>
<script src="./index"></script>