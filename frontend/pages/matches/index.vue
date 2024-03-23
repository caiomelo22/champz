<template>
    <div class="mx-4">
        <v-row v-if="loading" justify="center" align="center" class="pa-4">
            <v-progress-circular indeterminate size="40" color="primary">
            </v-progress-circular>
        </v-row>
        <div v-else>
            <v-row v-if="groupLoading" justify="center" align="center" class="pa-4">
                <v-progress-circular indeterminate size="20" color="primary">
                </v-progress-circular>
            </v-row>
            <v-row v-else>
                <v-col v-if="currentRound == groupStageRound" cols="12" md="8" class="fit-screen-div">
                    <v-card>
                        <GroupToolbar :group-stage-round="groupStageRound" :current-round="currentRound"
                            :group-name="get_round_name()" @previous_stage_click="previous_stage_click"
                            @next_stage_click="next_stage_click" />
                        <v-row>
                            <v-col cols="12" class="pa-0 pt-4">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th class="champz-font" scope="col">Team</th>
                                            <th class="champz-font" scope="col">P</th>
                                            <th class="champz-font" scope="col">W</th>
                                            <th class="champz-font" scope="col">D</th>
                                            <th class="champz-font" scope="col">L</th>
                                            <th class="champz-font" scope="col">GF</th>
                                            <th class="champz-font" scope="col">GA</th>
                                            <th class="champz-font" scope="col">GD</th>
                                            <th class="champz-font" scope="col">%</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(participant, i) in table" :key="i">
                                            <td class="champz-font">
                                                <img style="width: 30px" :src="gs.get_image_path(
                                                    participant.team_image_path
                                                )
                                                    " />
                                                {{ participant.name.toUpperCase() }}
                                            </td>
                                            <td class="champz-font">{{ participant.P }}</td>
                                            <td class="champz-font">{{ participant.W }}</td>
                                            <td class="champz-font">{{ participant.D }}</td>
                                            <td class="champz-font">{{ participant.L }}</td>
                                            <td class="champz-font">{{ participant.GF }}</td>
                                            <td class="champz-font">{{ participant.GA }}</td>
                                            <td class="champz-font">{{ participant.GD }}</td>
                                            <td class="champz-font">{{ getParticipantPercentage(participant) }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
                <v-col cols="12" :md="currentRound != groupStageRound ? 12 : 4" class="fit-screen-div"
                    :class="currentRound != groupStageRound ? 'champz-knockout' : 'champz-matches'">
                    <v-card>
                        <GroupToolbar v-if="currentRound != groupStageRound" :group-stage-round="groupStageRound"
                            :current-round="currentRound" :group-name="get_round_name()"
                            @previous_stage_click="previous_stage_click" @next_stage_click="next_stage_click" />
                        <v-simple-table :class="currentRound != groupStageRound ? 'mx-8' : 'mr-0'">
                            <template #default>
                                <thead class="thead-dark">
                                    <tr>
                                        <th class="champz-font text-center" scope="col">Match</th>
                                        <th class="champz-font" scope="col">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(match, i) in matches[currentRound]" :key="i">
                                        <td v-if="registerScoreDialog && currentMatch.id == match.id"><v-progress-circular indeterminate size="20" color="primary">
                                            </v-progress-circular></td>
                                        <td class="champz-font text-center" v-else-if="match.goals_1 == null &&
                                            match.goals_2 == null
                                            ">
                                            {{ match.participant_1_name.slice(0, 3).toUpperCase() }}

                                            <img style="width: 30px" :src="gs.get_image_path(
                                                match.participant_1_team_image_path
                                            )
                                                " />
                                            X
                                            <img style="width: 30px" :src="gs.get_image_path(
                                                match.participant_2_team_image_path
                                            )
                                                " />
                                            {{ match.participant_2_name.slice(0, 3).toUpperCase() }}
                                        </td>
                                        <td class="champz-font text-center" v-else>
                                            {{ match.participant_1_name.slice(0, 3).toUpperCase() }}
                                            <img style="width: 30px" :src="gs.get_image_path(
                                                match.participant_1_team_image_path
                                            )
                                                " />
                                            {{ match.goals_1 }} X
                                            {{ match.goals_2 }}
                                            <img style="width: 30px" :src="gs.get_image_path(
                                                match.participant_2_team_image_path
                                            )
                                                " />
                                            {{ match.participant_2_name.slice(0, 3).toUpperCase() }}
                                        </td>
                                        <td>
                                            <v-btn x-small fab color="primary" @click="get_match(match)">
                                                <v-icon small>mdi-pencil</v-icon>
                                            </v-btn>
                                        </td>
                                    </tr>
                                </tbody>
                            </template>
                        </v-simple-table>
                    </v-card>
                    <v-divider></v-divider>
                </v-col>
            </v-row>
            <v-spacer></v-spacer>
            <a @click="resetConfirmationDialog = true">Reset matches</a>
            <v-dialog v-model="resetConfirmationDialog" width="700px" max-width="100%">
                <Confirmation text="Are you sure that you want to reset the matches? All of the
              current groups are going to be erased." @close="resetConfirmationDialog = false"
                    @confirm="reset_matches_click" />
            </v-dialog>
        </div>
        <!-- Register Score Modal -->
        <v-dialog v-if="registerScoreDialog" v-model="registerScoreDialog" width="700px" max-width="100%">
            <RegisterScore :current-match="currentMatch" @close="registerScoreDialog = false" @update="score_changed" />
        </v-dialog>
        <!-- End Register Score modal -->
    </div>
</template>
<style lang="scss" scoped>
.champz-font {
    font-size: 15px;
    font-weight: 500;
    font-family: system-ui;
    vertical-align: inherit !important;
}

td,
th {
    text-align: center !important;
}

.table {
    margin-bottom: 0px;
}

.champz-knockout {
    height: 100%;
}

.champz-matches {
    height: 100%;
    overflow-y: auto;
}

.fit-screen-div {
    max-height: 85vh;
    overflow-y: auto;
}
</style>
<script src="./index.js"></script>