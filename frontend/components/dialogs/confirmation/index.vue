<template>
  <v-card class="confirmation-dialog">
    <DialogHeader title="Confirm Action" icon="mdi-alert-circle" color="warning" @close="$emit('close')" />
    
    <v-card-text class="pa-5">
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

.confirmation-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.warning-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;
  padding: 16px;
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