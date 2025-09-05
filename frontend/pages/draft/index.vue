<template>
  <div class="draft-container">
    <div class="page-header">
      <h1 class="page-title">Champz</h1>
    </div>
    
    <v-row>
      <v-col cols="12" md="5" class="pl-0 pr-3 pt-0">
        <!-- Budget Card -->
        <v-card class="budget-card mb-6" elevation="0">
          <v-card-text class="pa-6">
            <div class="card-header mb-4">
              <div class="icon-wrapper">
                <v-icon color="white" size="20">mdi-wallet</v-icon>
              </div>
              <h3 class="card-title">Set Budget</h3>
            </div>
            <v-text-field 
              v-model="genericBudget" 
              type="number"
              prefix="$"
              placeholder="Enter budget amount"
              solo
              flat
              hide-details
              class="budget-input"
            ></v-text-field>
          </v-card-text>
        </v-card>

        <!-- Participants Card -->
        <v-card class="participants-card" elevation="0">
          <v-card-text class="pa-6">
            <div class="card-header mb-4">
              <div class="flex-header">
                <div class="title-section">
                  <div class="icon-wrapper">
                    <v-icon color="white" size="20">mdi-account-group</v-icon>
                  </div>
                  <h3 class="card-title">Participants</h3>
                </div>
                <v-btn
                  fab
                  small
                  color="#3b82f6"
                  @click="open_participant_dialog(null)"
                  elevation="2"
                  class="add-btn"
                >
                  <v-icon color="white" size="20">mdi-plus</v-icon>
                </v-btn>
              </div>
            </div>

            <div v-if="participantsLoading" class="loading-state">
              <v-progress-circular indeterminate size="32" color="#3b82f6"></v-progress-circular>
              <p class="loading-text">Loading participants...</p>
            </div>

            <div v-else-if="participants.length === 0" class="empty-state">
              <v-icon size="48" color="#94a3b8">mdi-account-plus</v-icon>
              <p class="empty-text">No participants yet</p>
              <p class="empty-subtext">Add participants to start the draft</p>
            </div>

            <div v-else class="participants-list">
              <div v-for="(participant, i) in participants" :key="i" class="participant-item">
                <div class="participant-info">
                  <img 
                    :src="gs.get_image_path(participant.team_image_path)" 
                    class="team-logo"
                    :alt="participant.team_name"
                  />
                  <div class="participant-details">
                    <h4 class="participant-name">{{ participant.name }}</h4>
                    <p class="participant-team">{{ participant.team_name }}</p>
                  </div>
                </div>
                <div class="participant-budget">
                  <span class="budget-amount">${{ participant.budget }}</span>
                </div>
                <div class="participant-actions">
                  <v-btn icon small @click="open_participant_dialog(participant)" class="action-btn">
                    <v-icon size="18" color="#3b82f6">mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon small @click="delete_participant(participant.id)" class="action-btn">
                    <v-icon size="18" color="#ef4444">mdi-trash-can</v-icon>
                  </v-btn>
                  <v-btn 
                    icon 
                    small 
                    :loading="participant.team_loading_att" 
                    @click="get_players_by_team(participant, participant.team_name)"
                    class="action-btn"
                  >
                    <v-icon size="18" color="#3b82f6">mdi-eye</v-icon>
                  </v-btn>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="7" class="pr-0 pl-3 pt-0">
        <!-- Players Card -->
        <v-card class="players-card" elevation="0">
          <v-card-text class="pa-6">
            <div class="card-header mb-4">
              <div class="icon-wrapper">
                <v-icon color="white" size="20">mdi-soccer</v-icon>
              </div>
              <h3 class="card-title">Players</h3>
            </div>

            <v-tabs 
              v-model="tab" 
              color="#3b82f6" 
              class="position-tabs mb-6"
              show-arrows
            >
              <v-tab 
                v-for="(p, i) in positions" 
                :key="i" 
                class="position-tab"
              >
                {{ p.name }}
              </v-tab>
            </v-tabs>

            <div v-if="playersLoading" class="loading-state">
              <v-progress-circular indeterminate size="32" color="#3b82f6"></v-progress-circular>
              <p class="loading-text">Loading players...</p>
            </div>

            <div v-else-if="tab != -1 && selectedPosition.length === 0" class="empty-state">
              <v-icon size="48" color="#94a3b8">mdi-soccer</v-icon>
              <p class="empty-text">No players available</p>
              <p class="empty-subtext">Select a different position</p>
            </div>

            <div v-else-if="tab != -1" class="players-grid">
              <div 
                v-for="player in selectedPosition" 
                :key="`${player.id}-${player.team_participant}-${player.value}`"
                class="player-card"
              >
                <div class="player-image-section">
                  <img 
                    :src="gs.get_image_path(player.image_path)" 
                    class="player-image"
                    :alt="player.name"
                  />
                  <div class="player-badges">
                    <div class="overall-badge">{{ player.overall }}</div>
                    <img 
                      :src="gs.get_image_path(player.nation_image_path)" 
                      class="nation-flag"
                      :alt="player.nation"
                    />
                  </div>
                </div>
                
                <div class="player-info-section">
                  <h4 class="player-name">{{ player.name }}</h4>
                  <p class="player-position">{{ player.specific_position }}</p>
                  
                  <div class="player-meta">
                    <div class="team-info">
                      <img 
                        :src="gs.get_image_path(player.team_origin_image_path)" 
                        class="club-logo"
                        :alt="player.team"
                      />
                    </div>
                    <div class="owner-info">
                      <span class="owner-label">Owner:</span>
                      <span class="owner-name">
                        {{ player.team_participant ? get_participant_name(player.participant_id) : "Available" }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="player-footer">
                    <div class="price-section">
                      <span class="price">${{ player.value }}</span>
                    </div>
                    <div class="action-buttons">
                      <v-btn 
                        icon 
                        small 
                        color="#10b981" 
                        @click="get_player(player)"
                        class="action-btn"
                      >
                        <v-icon size="18">mdi-cash-plus</v-icon>
                      </v-btn>
                      <v-btn 
                        icon 
                        small 
                        color="#ef4444" 
                        @click="remove_buy(player)"
                        class="action-btn"
                      >
                        <v-icon size="18">mdi-cash-minus</v-icon>
                      </v-btn>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modals -->
    <v-dialog v-if="addParticipantDialog" v-model="addParticipantDialog" width="500px" max-width="90%">
      <AddParticipant 
        :participant-prop="newParticipant" 
        :teams="teams" 
        @close="reset_participant_dialog"
        @update="participant_added" 
      />
    </v-dialog>

    <v-dialog v-if="buyPlayerDialog" v-model="buyPlayerDialog" width="500px" max-width="90%" persistent>
      <BuyPlayer 
        :participants="participants" 
        :current-player="currentPlayer" 
        @close="reset_player_modal" 
        @update="player_updated" 
      />
    </v-dialog>

    <v-dialog v-if="participantTeamDialog" v-model="participantTeamDialog" width="700px" max-width="90%">
      <ParticipantTeam 
        :selected-team="selectedTeam" 
        :current-participant="currentParticipant" 
        @remove="remove_buy" 
      />
    </v-dialog>
  </div>
</template>

<style lang="scss" scoped>
.draft-container {
  padding: 0 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(226, 232, 240, 0.9));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  font-family: 'DM Sans', sans-serif;
}

.page-subtitle {
  color: rgba(203, 213, 225, 0.95);
  font-size: 1.2rem;
  margin: 0;
  font-weight: 500;
  font-family: 'DM Sans', sans-serif;
}

/* Card Styles */
.budget-card,
.participants-card,
.players-card {
  background: rgba(30, 41, 59, 0.15) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 24px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.budget-card:hover,
.participants-card:hover,
.players-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25);
  border-color: rgba(59, 130, 246, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.flex-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-wrapper {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 12px;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.card-title {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.25rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

/* Budget Input */
.budget-input ::v-deep .v-input__control {
  background: rgba(15, 23, 42, 0.6) !important;
  border-radius: 16px;
  border: 1px solid rgba(100, 116, 139, 0.4);
}

.budget-input ::v-deep .v-input__slot {
  background: transparent !important;
}

.budget-input ::v-deep .v-text-field__details {
  display: none;
}

.budget-input ::v-deep input {
  color: rgba(226, 232, 240, 0.95) !important;
  font-weight: 600;
  font-size: 1.1rem;
  font-family: 'DM Sans', sans-serif;
}

.budget-input ::v-deep input::placeholder {
  color: rgba(148, 163, 184, 0.7) !important;
}

.budget-input ::v-deep .v-input__prepend-inner {
  color: rgba(148, 163, 184, 0.8) !important;
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.loading-text,
.empty-text {
  color: rgba(226, 232, 240, 0.9);
  font-weight: 600;
  font-size: 1.1rem;
  margin: 1rem 0 0.5rem 0;
  font-family: 'DM Sans', sans-serif;
}

.empty-subtext {
  color: rgba(148, 163, 184, 0.8);
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

/* Participants List */
.participants-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.participant-item {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
}

.participant-item:hover {
  background: rgba(30, 41, 59, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border-color: rgba(59, 130, 246, 0.4);
}

.participant-info {
  display: flex;
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

.participant-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.participant-name {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.1rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.participant-team {
  color: rgba(148, 163, 184, 0.8);
  font-size: 0.9rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.participant-budget {
  margin: 0 20px;
}

.budget-amount {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.participant-actions {
  display: flex;
  gap: 8px;
}

/* Tabs */
.position-tabs ::v-deep .v-tabs-bar {
  background: transparent !important;
  border-radius: 16px;
}

.position-tabs ::v-deep .v-tab {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(100, 116, 139, 0.4) !important;
  border-radius: 12px;
  margin: 0 4px;
  color: rgba(148, 163, 184, 0.9) !important;
  text-transform: none;
  font-weight: 600;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.position-tabs ::v-deep .v-tab--active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
  color: white !important;
  border-color: rgba(59, 130, 246, 0.6) !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.position-tabs ::v-deep .v-tab:hover:not(.v-tab--active) {
  background: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(100, 116, 139, 0.6) !important;
}

.position-tabs ::v-deep .v-tabs-slider {
  display: none;
}

/* Players Grid */
.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.player-card {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 20px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.player-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.player-card:hover {
  background: rgba(30, 41, 59, 0.7);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
  border-color: rgba(59, 130, 246, 0.4);
}

.player-image-section {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  margin-bottom: 16px;
}

.player-image {
  width: 96px;
  height: 96px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid rgba(100, 116, 139, 0.4);
}

.player-badges {
  position: absolute;
  top: -12px;
  right: -12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
}

.overall-badge {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 6px 12px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
  font-family: 'DM Sans', sans-serif;
}

.nation-flag {
  width: 32px;
  height: 20px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid rgba(100, 116, 139, 0.4);
}

.player-info-section {
  text-align: center;
}

.player-name {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.1rem;
  margin: 0 0 4px 0;
  font-family: 'DM Sans', sans-serif;
}

.player-position {
  color: rgba(148, 163, 184, 0.8);
  font-size: 0.9rem;
  margin: 0 0 16px 0;
  font-family: 'DM Sans', sans-serif;
}

.player-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(100, 116, 139, 0.2);
}

.team-info {
  display: flex;
  align-items: center;
}

.club-logo {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid rgba(100, 116, 139, 0.4);
}

.owner-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
}

.owner-label {
  color: rgba(148, 163, 184, 0.7);
  font-size: 0.75rem;
  margin-bottom: 2px;
  font-family: 'DM Sans', sans-serif;
}

.owner-name {
  color: rgba(226, 232, 240, 0.9);
  font-weight: 600;
  font-size: 0.85rem;
  font-family: 'DM Sans', sans-serif;
}

.player-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-section {
  flex: 1;
}

.price {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(100, 116, 139, 0.4) !important;
  transition: all 0.3s ease !important;
}

.action-btn:hover {
  background: rgba(59, 130, 246, 0.2) !important;
  border-color: rgba(59, 130, 246, 0.5) !important;
  transform: scale(1.1) !important;
}

.add-btn {
  transition: all 0.3s ease !important;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
}

.add-btn:hover {
  transform: rotate(90deg) scale(1.1) !important;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .draft-container {
    padding: 0 16px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .players-grid {
    grid-template-columns: 1fr;
  }
  
  .participant-item {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .participant-actions {
    justify-content: center;
  }
}
</style>
<script src="./index"></script>