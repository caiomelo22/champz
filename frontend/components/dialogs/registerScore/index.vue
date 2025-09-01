<template>
  <v-card class="register-score-dialog">
    <v-card-title class="dialog-header">
      <div class="header-content">
        <div class="icon-wrapper">
          <v-icon color="white" size="24">mdi-scoreboard</v-icon>
        </div>
        <h3 class="dialog-title">Register Score</h3>
      </div>
    </v-card-title>
    
    <v-card-text class="pa-6">
      <form @submit.prevent="registerScore()" class="score-form">
        <div class="match-header">
          <div class="team-section">
            <div class="team-info">
              <img 
                :src="gs.get_image_path(match.participant_1_team_image_path)" 
                class="team-logo"
                :alt="match.participant_1_name"
              />
              <h4 class="team-name">{{ match.participant_1_name }}</h4>
            </div>
            
            <div class="vs-section">
              <span class="vs-text">VS</span>
            </div>
            
            <div class="team-info">
              <h4 class="team-name">{{ match.participant_2_name }}</h4>
              <img 
                :src="gs.get_image_path(match.participant_2_team_image_path)" 
                class="team-logo"
                :alt="match.participant_2_name"
              />
            </div>
          </div>
        </div>

        <div class="score-inputs">
          <div class="score-input-group">
            <label class="input-label">{{ match.participant_1_name }} Goals</label>
            <v-text-field 
              v-model="match.goals_1"
              type="number" 
              min="0" 
              required
              solo
              flat
              hide-details
              class="professional-input score-field"
            ></v-text-field>
          </div>

          <div class="score-separator">
            <div class="separator-line"></div>
          </div>

          <div class="score-input-group">
            <label class="input-label">{{ match.participant_2_name }} Goals</label>
            <v-text-field 
              v-model="match.goals_2"
              type="number" 
              min="0" 
              required
              solo
              flat
              hide-details
              class="professional-input score-field"
            ></v-text-field>
          </div>
        </div>
        
        <v-card-actions class="dialog-actions">
          <v-btn 
            color="transparent" 
            text
            @click="$emit('close')"
            class="cancel-btn"
          >
            <v-icon left size="20">mdi-close</v-icon>
            Cancel
          </v-btn>
          <v-btn 
            type="submit" 
            :disabled="!goalFieldsFilled()"
            :loading="registerScoreLoading"
            class="save-btn"
          >
            <v-icon left size="20">mdi-check</v-icon>
            Save Score
          </v-btn>
        </v-card-actions>
      </form>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.register-score-dialog {
  background: rgba(30, 41, 59, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 24px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  max-width: 600px;
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

.score-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.match-header {
  background: rgba(15, 23, 42, 0.4);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(100, 116, 139, 0.2);
}

.team-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.team-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.team-logo {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid rgba(100, 116, 139, 0.4);
}

.team-name {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.1rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.vs-section {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  border: 2px solid rgba(59, 130, 246, 0.4);
}

.vs-text {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 0.9rem;
  font-family: 'DM Sans', sans-serif;
}

.score-inputs {
  display: flex;
  align-items: end;
  gap: 24px;
}

.score-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.input-label {
  color: rgba(226, 232, 240, 0.9);
  font-weight: 600;
  font-size: 0.9rem;
  font-family: 'DM Sans', sans-serif;
  text-align: center;
}

.score-separator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  margin-bottom: 24px;
}

.separator-line {
  width: 40px;
  height: 2px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 2px;
}

.professional-input.score-field ::v-deep .v-input__control {
  background: rgba(15, 23, 42, 0.6) !important;
  border-radius: 12px;
  border: 2px solid rgba(100, 116, 139, 0.4);
}

.professional-input.score-field ::v-deep .v-input__slot {
  background: transparent !important;
  padding: 0 16px;
}

.professional-input.score-field ::v-deep input {
  color: rgba(226, 232, 240, 0.95) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  text-align: center;
  padding: 16px 0;
}

.professional-input.score-field:focus-within ::v-deep .v-input__control {
  border-color: rgba(59, 130, 246, 0.6);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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
  border-radius: 12px;
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

.save-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.save-btn:disabled {
  background: rgba(100, 116, 139, 0.3) !important;
  color: rgba(148, 163, 184, 0.5) !important;
  box-shadow: none;
}

/* Responsive */
@media (max-width: 600px) {
  .team-section {
    flex-direction: column;
    gap: 16px;
  }
  
  .team-info {
    justify-content: center !important;
    flex-direction: row !important;
  }
  
  .score-inputs {
    flex-direction: column;
    gap: 16px;
  }
  
  .score-separator {
    transform: rotate(90deg);
    margin: 0;
  }
}
</style>
<script src="./index"></script>