<template>
  <v-card>
    <v-card-title>
      <h5>Buy Player</h5>
    </v-card-title>
    <v-card-text>
      <div class="text-center" style="display: flex; justify-content: center; position: relative">
        <div class="card-info">
          <div class="card-left-info">
            <span style="
                    margin-bottom: 10px;
                    font-size: 40px;
                    font-weight: bold;
                    z-index: 2;
                  ">{{ player.overall }}</span>
            <span style="font-size: 25px; z-index: 2">{{
                player.specific_position
            }}</span>
            <img style="width: 60px; z-index: 2; margin: auto"
              :src="gs.get_image_path(player.nation_image_path)" />
            <img style="width: 60px; z-index: 2; margin: auto" :src="
              gs.get_image_path(player.team_origin_image_path)
            " />
          </div>
          <img :src="gs.get_image_path(player.image_path)" style="
                  max-height: 160px;
                  z-index: 2;
                  position: absolute;
                  top: 100px;
                  left: -28px;
                " />
          <div class="card-name">
            <span style="font-weight: 700; font-size: 17px">{{
                player.name
            }}</span>
          </div>
          <div class="card-stats">
            <div class="vertical-divisor"></div>
            <div class="card-stats-left">
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.pace
                }}</span><span class="mr-1 card-stat-name">PAC</span>
              </v-row>
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.shooting
                }}</span><span class="mr-1 card-stat-name">SHO</span>
              </v-row>
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.passing
                }}</span><span class="mr-1 card-stat-name">PAS</span>
              </v-row>
            </div>
            <div class="card-stats-right text-end">
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.dribbling
                }}</span><span class="mr-1 card-stat-name">DRI</span>
              </v-row>
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.defending
                }}</span><span class="mr-1 card-stat-name">DEF</span>
              </v-row>
              <v-row no-gutters>
                <span class="mr-1 card-stat-value">{{
                    player.physical
                }}</span><span class="mr-1 card-stat-name">PHY</span>
              </v-row>
            </div>
          </div>
        </div>
        <img src="~/assets/gold.png" style="height: 500px; z-index: 1" />
      </div>
      <form v-on:submit.prevent="buy_player()">
        <v-text-field type="number" v-model="player.value" label="Value" prefix="$"></v-text-field>
        <v-combobox v-model="participantSelected" :items="participants" item-text="name" @change="
          player.team_participant_id = participantSelected.team_id
        " label="Participant" outlined dense></v-combobox>
        <v-card-actions style="display: flex; justify-content: flex-end">
          <v-btn color="red" dark @click="$emit('close')">Cancel</v-btn>
          <v-btn type="submit" dark color="green" :loading="updatingPlayer">Save changes</v-btn>
        </v-card-actions>
      </form>
    </v-card-text>
  </v-card>
</template>
<script src="./index"></script>