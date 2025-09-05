<template>
  <v-card class="participant-team-dialog">
    <v-card-title class="dialog-header">
      <div class="header-content">
        <div class="icon-wrapper">
          <v-icon color="white" size="24">mdi-account-group</v-icon>
        </div>
        <h3 class="dialog-title">{{ currentParticipant.name }}'s Team</h3>
      </div>
    </v-card-title>
    
    <v-card-text class="pa-6">
      <div v-if="!selectedTeam || selectedTeam.length === 0" class="empty-state">
        <v-icon size="64" color="rgba(148, 163, 184, 0.5)">mdi-account-question</v-icon>
        <h4 class="empty-title">No Players Found</h4>
        <p class="empty-text">This team hasn't purchased any players yet.</p>
      </div>
      
      <div v-else class="players-list">
        <div 
          v-for="(player, i) in selectedTeam" 
          :key="i"
          class="player-card"
        >
          <div class="player-avatar">
            <img 
              :src="gs.get_image_path(player.image_path)" 
              class="player-image"
              :alt="player.name"
            />
          </div>
          
          <div class="player-details">
            <div class="player-info">
              <div class="player-header">
                <h4 class="player-name">{{ player.name }}</h4>
                <div class="player-badges">
                  <div class="overall-badge">{{ player.overall }}</div>
                  <img 
                    :src="gs.get_image_path(player.nation_image_path)" 
                    class="nation-flag"
                    :alt="player.nation"
                  />
                </div>
              </div>
              <p class="player-position">{{ player.specific_position }}</p>
              <div class="team-info">
                <img 
                  :src="gs.get_image_path(player.team_origin_image_path)" 
                  class="club-logo"
                  :alt="player.team_origin"
                />
                <span class="team-name">{{ player.team_origin }}</span>
              </div>
            </div>
            
            <div class="player-actions">
              <div class="price-display">
                <span class="price-label">Price:</span>
                <span class="price-value">${{ player.value }}</span>
              </div>
              <v-btn 
                color="#ef4444" 
                small 
                @click="$emit('remove', player)"
                class="remove-btn"
              >
                <v-icon left size="16">mdi-trash-can</v-icon>
                Remove
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.participant-team-dialog {
  background: rgba(30, 41, 59, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 24px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  max-width: 800px;
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
  background: linear-gradient(135deg, #3b82f6, #2563eb);
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 24px;
  gap: 16px;
}

.empty-title {
  color: rgba(226, 232, 240, 0.95);
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1.2rem;
  margin: 0;
}

.empty-text {
  color: rgba(148, 163, 184, 0.8);
  font-family: 'DM Sans', sans-serif;
  margin: 0;
}

.players-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.player-card {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.player-card:hover {
  background: rgba(15, 23, 42, 0.8);
  border-color: rgba(59, 130, 246, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.player-avatar {
  flex-shrink: 0;
}

.player-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid rgba(100, 116, 139, 0.3);
}

.player-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.player-badges {
  display: flex;
  align-items: center;
  gap: 8px;
}

.overall-badge {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 6px;
  min-width: 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.nation-flag {
  width: 24px;
  height: 16px;
  border-radius: 3px;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.player-details {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.player-info {
  flex: 1;
}

.player-name {
  color: rgba(226, 232, 240, 0.95);
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1.1rem;
  margin: 0 0 4px 0;
}

.player-position {
  color: rgba(148, 163, 184, 0.8);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  margin: 0 0 12px 0;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.club-logo {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  object-fit: cover;
}

.team-name {
  color: rgba(148, 163, 184, 0.8);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
}

.player-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.price-display {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.price-label {
  color: rgba(148, 163, 184, 0.8);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.price-value {
  color: rgba(34, 197, 94, 0.95);
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
}

.remove-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626) !important;
  color: white !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  border-radius: 8px;
  text-transform: none;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.remove-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .participant-team-dialog {
    margin: 16px;
    max-width: calc(100vw - 32px);
  }
  
  .player-card {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .player-details {
    flex-direction: column;
    width: 100%;
    gap: 16px;
  }
  
  .player-actions {
    align-items: center;
  }
}
</style>

<script src="./index"></script>