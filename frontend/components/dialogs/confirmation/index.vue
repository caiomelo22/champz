<template>
  <v-card class="confirmation-dialog">
    <v-card-title class="dialog-header">
      <div class="header-content">
        <div class="icon-wrapper">
          <v-icon color="white" size="24">mdi-alert-circle</v-icon>
        </div>
        <h3 class="dialog-title">Confirm Action</h3>
      </div>
    </v-card-title>
    
    <v-card-text class="pa-6">
      <div class="confirmation-content">
        <div class="warning-section">
          <v-icon size="48" color="#f59e0b" class="warning-icon">mdi-alert-triangle</v-icon>
          <p class="confirmation-text">{{ text }}</p>
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
            @click="$emit('confirm')"
            class="confirm-btn"
          >
            <v-icon left size="20">mdi-check</v-icon>
            Confirm
          </v-btn>
        </v-card-actions>
      </div>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.confirmation-dialog {
  background: rgba(30, 41, 59, 0.95) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 24px !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  max-width: 500px;
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
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 12px;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.dialog-title {
  color: rgba(226, 232, 240, 0.95);
  font-weight: 700;
  font-size: 1.5rem;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.confirmation-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.warning-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;
  padding: 24px;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 16px;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.warning-icon {
  filter: drop-shadow(0 4px 8px rgba(245, 158, 11, 0.3));
}

.confirmation-text {
  color: rgba(226, 232, 240, 0.95);
  font-size: 1.1rem;
  font-weight: 500;
  line-height: 1.6;
  margin: 0;
  font-family: 'DM Sans', sans-serif;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 !important;
}

.cancel-btn {
  color: rgba(148, 163, 184, 0.8) !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  border-radius: 12px;
  padding: 0 24px;
}

.cancel-btn:hover {
  background: rgba(100, 116, 139, 0.2) !important;
  color: rgba(226, 232, 240, 0.95) !important;
}

.confirm-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626) !important;
  color: white !important;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  border-radius: 12px;
  padding: 0 24px;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

/* Responsive */
@media (max-width: 600px) {
  .confirmation-dialog {
    margin: 16px;
    max-width: calc(100vw - 32px);
  }
  
  .dialog-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .cancel-btn,
  .confirm-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
<script src="./index"></script>