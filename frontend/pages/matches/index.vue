<template>
  <div class="matches-container">
    <!-- Header Section -->
    <div class="page-header">
      <h1 class="page-title">Champz</h1>
    </div>

    <v-row v-if="loading" justify="center" align="center" class="loading-state">
      <v-progress-circular indeterminate size="40" color="#3b82f6"></v-progress-circular>
      <p class="loading-text">Loading matches...</p>
    </v-row>

    <div v-else class="content-wrapper">
      <v-row v-if="groupLoading" justify="center" align="center" class="loading-state">
        <v-progress-circular indeterminate size="32" color="#3b82f6"></v-progress-circular>
        <p class="loading-text">Loading groups...</p>
      </v-row>

      <v-row v-else class="main-content">
        <!-- Group Stage Table -->
        <v-col v-if="currentRound == groupStageRound" cols="12" xl="8" class="matches-col">
          <v-card class="group-table-card" elevation="0">
            <v-card-text class="pa-6">
              <div class="card-header mb-4">
                <div class="icon-wrapper">
                  <v-icon color="white" size="24">mdi-trophy</v-icon>
                </div>
                <h3 class="card-title">{{ get_round_name() }}</h3>
                <div class="navigation-controls">
                  <v-btn 
                    icon 
                    small 
                    @click="previous_stage_click"
                    class="nav-btn"
                  >
                    <v-icon size="20" color="#3b82f6">mdi-chevron-left</v-icon>
                  </v-btn>
                  <v-btn 
                    icon 
                    small 
                    @click="next_stage_click"
                    class="nav-btn"
                  >
                    <v-icon size="20" color="#3b82f6">mdi-chevron-right</v-icon>
                  </v-btn>
                </div>
              </div>

              <div class="table-wrapper">
                <div class="table-header">
                  <div class="table-cell team-header">Team</div>
                  <div class="table-cell stat-header">P</div>
                  <div class="table-cell stat-header">W</div>
                  <div class="table-cell stat-header">D</div>
                  <div class="table-cell stat-header">L</div>
                  <div class="table-cell stat-header">GF</div>
                  <div class="table-cell stat-header">GA</div>
                  <div class="table-cell stat-header">GD</div>
                  <div class="table-cell stat-header">%</div>
                </div>

                <div class="table-body">
                  <div 
                    v-for="(participant, i) in table" 
                    :key="i" 
                    class="table-row"
                    :class="{ 'qualified': i < 2 }"
                  >
                    <div class="table-cell team-cell">
                      <div class="team-info">
                        <img 
                          :src="gs.get_image_path(participant.team_image_path)" 
                          class="team-logo"
                          :alt="participant.name"
                        />
                        <span class="team-name">{{ participant.name.toUpperCase() }}</span>
                      </div>
                    </div>
                    <div class="table-cell stat-cell">{{ participant.P }}</div>
                    <div class="table-cell stat-cell">{{ participant.W }}</div>
                    <div class="table-cell stat-cell">{{ participant.D }}</div>
                    <div class="table-cell stat-cell">{{ participant.L }}</div>
                    <div class="table-cell stat-cell">{{ participant.GF }}</div>
                    <div class="table-cell stat-cell">{{ participant.GA }}</div>
                    <div class="table-cell stat-cell">{{ participant.GD }}</div>
                    <div class="table-cell stat-cell">{{ getParticipantPercentage(participant) }}</div>
                  </div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Matches Section -->
        <v-col cols="12" :xl="currentRound != groupStageRound ? 12 : 4" class="matches-col">
          <v-card class="matches-card" elevation="0">
            <v-card-text class="pa-6">
              <div class="card-header mb-4" v-if="currentRound != groupStageRound">
                <div class="icon-wrapper">
                  <v-icon color="white" size="24">mdi-soccer</v-icon>
                </div>
                <h3 class="card-title">{{ get_round_name() }}</h3>
                <div class="navigation-controls">
                  <v-btn 
                    icon 
                    small 
                    @click="previous_stage_click"
                    class="nav-btn"
                  >
                    <v-icon size="20" color="#3b82f6">mdi-chevron-left</v-icon>
                  </v-btn>
                  <v-btn 
                    icon 
                    small 
                    @click="next_stage_click"
                    class="nav-btn"
                  >
                    <v-icon size="20" color="#3b82f6">mdi-chevron-right</v-icon>
                  </v-btn>
                </div>
              </div>
              
              <div class="card-header mb-4" v-else>
                <div class="icon-wrapper">
                  <v-icon color="white" size="24">mdi-soccer</v-icon>
                </div>
                <h3 class="card-title">Matches</h3>
              </div>

              <div class="matches-list">
                <div 
                  v-for="(match, i) in matches[currentRound]" 
                  :key="i" 
                  class="match-item"
                >
                  <div class="match-content">
                    <div v-if="registerScoreDialog && currentMatch.id == match.id" class="match-loading">
                      <v-progress-circular indeterminate size="20" color="#3b82f6"></v-progress-circular>
                    </div>

                    <div v-else-if="match.goals_1 == null && match.goals_2 == null" class="match-fixture">
                      <div class="team team-1">
                        <span class="team-name">{{ match.participant_1_name.slice(0, 3).toUpperCase() }}</span>
                        <img 
                          :src="gs.get_image_path(match.participant_1_team_image_path)" 
                          class="team-logo"
                          :alt="match.participant_1_name"
                        />
                      </div>
                      <div class="vs-section">
                        <span class="vs-text">VS</span>
                      </div>
                      <div class="team team-2">
                        <img 
                          :src="gs.get_image_path(match.participant_2_team_image_path)" 
                          class="team-logo"
                          :alt="match.participant_2_name"
                        />
                        <span class="team-name">{{ match.participant_2_name.slice(0, 3).toUpperCase() }}</span>
                      </div>
                    </div>

                    <div v-else class="match-result">
                      <div class="team team-1">
                        <span class="team-name">{{ match.participant_1_name.slice(0, 3).toUpperCase() }}</span>
                        <img 
                          :src="gs.get_image_path(match.participant_1_team_image_path)" 
                          class="team-logo"
                          :alt="match.participant_1_name"
                        />
                        <span class="score">{{ match.goals_1 }}</span>
                      </div>
                      <div class="result-separator">-</div>
                      <div class="team team-2">
                        <span class="score">{{ match.goals_2 }}</span>
                        <img 
                          :src="gs.get_image_path(match.participant_2_team_image_path)" 
                          class="team-logo"
                          :alt="match.participant_2_name"
                        />
                        <span class="team-name">{{ match.participant_2_name.slice(0, 3).toUpperCase() }}</span>
                      </div>
                    </div>
                  </div>

                  <v-btn 
                    icon 
                    small 
                    @click="get_match(match)"
                    class="edit-btn"
                  >
                    <v-icon size="18" color="#3b82f6">mdi-pencil</v-icon>
                  </v-btn>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Reset Section -->
      <div class="reset-section">
        <v-btn 
          text 
          color="#ef4444" 
          @click="resetConfirmationDialog = true"
          class="reset-btn"
        >
          <v-icon left size="20">mdi-refresh</v-icon>
          Reset matches
        </v-btn>
      </div>
    </div>

    <!-- Dialogs -->
    <v-dialog v-model="resetConfirmationDialog" max-width="500" persistent>
      <Confirmation 
        text="Are you sure that you want to reset the matches? All of the current groups are going to be erased." 
        @close="resetConfirmationDialog = false"
        @confirm="reset_matches_click" 
      />
    </v-dialog>

    <v-dialog v-if="registerScoreDialog" v-model="registerScoreDialog" max-width="600">
      <RegisterScore 
        :current-match="currentMatch" 
        @close="registerScoreDialog = false" 
        @update="score_changed" 
      />
    </v-dialog>
  </div>
</template>
<style lang="scss" scoped>
.matches-col {
    padding: 0px 16px;
}
.matches-container {
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
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

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
}

.loading-text {
  color: rgba(148, 163, 184, 0.8);
  font-size: 0.9rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.main-content {
  gap: 0px;
}

/* Card Styles */
.group-table-card,
.matches-card {
  background: rgba(30, 41, 59, 0.15) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 24px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.group-table-card:hover,
.matches-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25);
  border-color: rgba(59, 130, 246, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
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

.card-title {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.25rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
  flex: 1;
}

.navigation-controls {
  display: flex;
  gap: 8px;
}

.nav-btn {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 8px;
}

.nav-btn:hover {
  background: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(59, 130, 246, 0.4);
}

/* Table Styles */
.table-wrapper {
  background: rgba(15, 23, 42, 0.4);
  border-radius: 16px;
  border: 1px solid rgba(100, 116, 139, 0.2);
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 3fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr;
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(100, 116, 139, 0.2);
}

.table-cell {
  padding: 16px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Sans', sans-serif;
}

.team-header {
  color: rgba(226, 232, 240, 0.9);
  justify-content: flex-start;
}

.stat-header {
  color: rgba(226, 232, 240, 0.9);
  font-weight: 600;
  font-size: 0.9rem;
}

.table-body {
  background: rgba(30, 41, 59, 0.2);
}

.table-row {
  display: grid;
  grid-template-columns: 3fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr 1fr;
  border-bottom: 1px solid rgba(100, 116, 139, 0.1);
  transition: all 0.2s ease;
}

.table-row:hover {
  background: rgba(59, 130, 246, 0.1);
}

.table-row.qualified {
  background: rgba(16, 185, 129, 0.1);
  border-left: 4px solid #10b981;
}

.team-cell {
  justify-content: flex-start;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-logo {
  width: 32px;
  height: 32px;
  object-fit: cover;
  border-radius: 50%;
  border: 1px solid rgba(100, 116, 139, 0.3);
}

.team-name {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 600;
  font-size: 0.9rem;
}

.stat-cell {
  color: rgba(203, 213, 225, 0.9);
  font-weight: 500;
  font-size: 0.9rem;
}

/* Matches Styles */
.matches-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.match-item {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(100, 116, 139, 0.2);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
}

.match-item:hover {
  background: rgba(30, 41, 59, 0.6);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-2px);
}

.match-content {
  flex: 1;
}

.match-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.match-fixture,
.match-result {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.team {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.team-1 {
  justify-content: flex-end;
}

.team-2 {
  justify-content: flex-start;
}

.team-name {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 600;
  font-size: 0.9rem;
}

.vs-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
}

.vs-text {
  color: rgba(148, 163, 184, 0.7);
  font-weight: 600;
  font-size: 0.8rem;
}

.result-separator {
  color: rgba(148, 163, 184, 0.7);
  font-weight: 600;
  font-size: 1.2rem;
  padding: 0 16px;
}

.score {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.edit-btn {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 8px;
}

.edit-btn:hover {
  background: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(59, 130, 246, 0.4);
}

/* Reset Section */
.reset-section {
  display: flex;
  justify-content: center;
  padding: 40px 0;
  margin-top: 40px;
  border-top: 1px solid rgba(100, 116, 139, 0.2);
}

.reset-btn {
  color: rgba(239, 68, 68, 0.9) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
}

.reset-btn:hover {
  background: rgba(239, 68, 68, 0.1) !important;
  color: rgba(239, 68, 68, 1) !important;
}

/* Responsive */
@media (max-width: 960px) {
  .page-title {
    font-size: 2.5rem;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 2.5fr 0.7fr 0.7fr 0.7fr 0.7fr 0.7fr 0.7fr 0.7fr 0.9fr;
  }
  
  .table-cell {
    padding: 12px 8px;
    font-size: 0.8rem;
  }
  
  .team-logo {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 600px) {
  .matches-container {
    padding: 16px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .match-fixture,
  .match-result {
    flex-direction: column;
    gap: 12px;
  }
  
  .team {
    justify-content: center !important;
  }
}
</style>
<script src="./index.js"></script>