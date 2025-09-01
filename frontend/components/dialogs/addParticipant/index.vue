<template>
  <v-card class="add-participant-dialog">
    <v-card-title class="dialog-header">
      <div class="header-content">
        <div class="icon-wrapper">
          <v-icon color="white" size="24">mdi-account-plus</v-icon>
        </div>
        <h3 class="dialog-title">Add Participant</h3>
      </div>
    </v-card-title>
    
    <v-card-text class="pa-6">
      <form @submit.prevent="add_participant()" class="form-section">
        <div class="input-group">
          <label class="input-label">Name</label>
          <v-text-field 
            v-model="participant.name"
            solo
            flat
            hide-details
            class="professional-input"
            placeholder="Enter participant name"
          ></v-text-field>
        </div>
        
        <div class="input-group">
          <label class="input-label">Team</label>
          <v-combobox 
            v-model="selectedTeam" 
            :items="teams.filter((x) => !x.participant_id)" 
            item-text="name"
            solo
            flat
            hide-details
            class="professional-input"
            placeholder="Select a team"
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
            :loading="updatingParticipant"
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
.add-participant-dialog {
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

.professional-input ::v-deep input::placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
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