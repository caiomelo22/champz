<template>
  <v-card class="buy-player-dialog">
    <DialogHeader title="Buy Player" icon="mdi-cash-plus" @close="$emit('close')" />
    
    <v-card-text class="pa-5">
      <div class="player-card-section">
        <PlayerCard :player="player" :width="200" />
      </div>

      <form v-on:submit.prevent="buy_player()" class="form-section">
        <div class="input-group">
          <label class="input-label">Value</label>
          <v-text-field 
            type="number" 
            v-model="player.value" 
            prefix="$"
            solo
            dense
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
            dense
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

.player-card-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
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