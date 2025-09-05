<template>
  <v-card class="buy-player-dialog">
    <v-card-title class="dialog-header">
      <div class="header-content">
        <div class="icon-wrapper">
          <v-icon color="white" size="24">mdi-cash-plus</v-icon>
        </div>
        <h3 class="dialog-title">Buy Player</h3>
      </div>
    </v-card-title>
    
    <v-card-text class="pa-6">
      <div class="player-card-section">
        <div class="text-center" style="display: flex; justify-content: center; position: relative">
          <div class="card-info">
            <div class="card-left-info">
              <span class="overall-rating">{{ player.overall }}</span>
              <span class="position-text">{{ player.specific_position.split(',')[0] }}</span>
              <img class="nation-flag-large" :src="gs.get_image_path(player.nation_image_path)" />
              <img class="team-logo-large" :src="gs.get_image_path(player.team_origin_image_path)" />
            </div>
            <img :src="gs.get_image_path(player.image_path)" class="player-image-large" />
            <div class="card-name">
              <span class="player-name-large">{{ player.name }}</span>
            </div>
            <div class="card-stats">
              <div class="vertical-divisor"></div>
              <div class="card-stats-left">
                <v-row no-gutters style="justify-content: center;">
                  <span class="mr-1 card-stat-value">{{ player.pace }}</span>
                  <span class="mr-1 card-stat-name">PAC</span>
                </v-row>
                <v-row no-gutters style="justify-content: center; margin-top: 8px;">
                  <span class="mr-1 card-stat-value">{{ player.shooting }}</span>
                  <span class="mr-1 card-stat-name">SHO</span>
                </v-row>
                <v-row no-gutters style="justify-content: center; margin-top: 8px;">
                  <span class="mr-1 card-stat-value">{{ player.passing }}</span>
                  <span class="mr-1 card-stat-name">PAS</span>
                </v-row>
              </div>
              <div class="card-stats-right text-end">
                <v-row no-gutters style="justify-content: center;">
                  <span class="mr-1 card-stat-value">{{ player.dribbling }}</span>
                  <span class="mr-1 card-stat-name">DRI</span>
                </v-row>
                <v-row no-gutters style="justify-content: center; margin-top: 8px;">
                  <span class="mr-1 card-stat-value">{{ player.defending }}</span>
                  <span class="mr-1 card-stat-name">DEF</span>
                </v-row>
                <v-row no-gutters style="justify-content: center; margin-top: 8px;">
                  <span class="mr-1 card-stat-value">{{ player.physical }}</span>
                  <span class="mr-1 card-stat-name">PHY</span>
                </v-row>
              </div>
            </div>
          </div>
          <img src="~/assets/gold.png" style="height: 500px; z-index: 1" />
        </div>
      </div>
      
      <form v-on:submit.prevent="buy_player()" class="form-section">
        <div class="input-group">
          <label class="input-label">Value</label>
          <v-text-field 
            type="number" 
            v-model="player.value" 
            prefix="$"
            solo
            flat
            hide-details
            class="professional-input"
          ></v-text-field>
        </div>
        
        <div class="input-group">
          <label class="input-label">Participant</label>
          <v-combobox 
            v-model="participantSelected" 
            :items="participants" 
            item-text="name" 
            @change="player.team_participant = participantSelected.team_name"
            solo
            flat
            hide-details
            class="professional-input"
          ></v-combobox>
        </div>
        
        <v-card-actions class="dialog-actions">
          <v-btn 
            color="transparent" 
            text
            @click="$emit('close')"
            class="cancel-btn"
          >
            Cancel
          </v-btn>
          <v-btn 
            type="submit" 
            :loading="updatingPlayer"
            class="save-btn"
          >
            <v-icon left size="20">mdi-check</v-icon>
            Save Changes
          </v-btn>
        </v-card-actions>
      </form>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.buy-player-dialog {
  background: rgba(30, 41, 59, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 24px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.dialog-header {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
  border-bottom: 1px solid rgba(100, 116, 139, 0.3);
  padding: 24px !important;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.icon-wrapper {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 12px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.dialog-title {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.5rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.player-card-section {
  margin-bottom: 32px;
}

.overall-rating {
  margin-bottom: 10px;
  font-size: 40px;
  font-weight: bold;
  z-index: 2;
  color: #1e293b;
  font-family: 'DM Sans', sans-serif;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.position-text {
  font-size: 25px;
  z-index: 2;
  color: #1e293b;
  font-family: 'DM Sans', sans-serif;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.nation-flag-large {
  width: 60px;
  z-index: 2;
  margin: auto;
  border-radius: 4px;
}

.team-logo-large {
  width: 60px;
  z-index: 2;
  margin: auto;
  border-radius: 50%;
}

.player-image-large {
  max-height: 160px;
  z-index: 2;
  position: absolute;
  top: 100px;
  left: -28px;
}

.player-name-large {
  font-weight: 700;
  font-size: 20px;
  color: #1e293b;
  font-family: 'DM Sans', sans-serif;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.card-stat-value {
  color: #1e293b;
  font-weight: 700;
  font-family: 'DM Sans', sans-serif;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.card-stat-name {
  color: #334155;
  font-family: 'DM Sans', sans-serif;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  color: rgba(226, 232, 240, 0.9);
  font-weight: 600;
  font-size: 0.9rem;
  font-family: 'DM Sans', sans-serif;
  margin-bottom: 4px;
}

.professional-input ::v-deep .v-input__control {
  background: rgba(15, 23, 42, 0.6) !important;
  border-radius: 12px;
  border: 1px solid rgba(100, 116, 139, 0.4);
}

.professional-input ::v-deep .v-input__slot {
  background: transparent !important;
}

.professional-input ::v-deep input {
  color: rgba(226, 232, 240, 0.95) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
}

.professional-input ::v-deep .v-input__prepend-inner {
  color: rgba(148, 163, 184, 0.8) !important;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 !important;
  margin-top: 8px;
}

.cancel-btn {
  color: rgba(148, 163, 184, 0.8) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
}

.cancel-btn:hover {
  background: rgba(239, 68, 68, 0.1) !important;
  color: rgba(239, 68, 68, 0.9) !important;
}

.save-btn {
  background: linear-gradient(135deg, #10b981, #059669) !important;
  color: white !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  border-radius: 12px;
  padding: 0 24px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.save-btn:hover {
  background: linear-gradient(135deg, #059669, #047857) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}
</style>
<script src="./index"></script>