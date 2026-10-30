<template>
  <v-card class="pool-dialog" dark>
    <v-card-title>Draft players</v-card-title>
    <v-card-text class="dialog-content">
      <div v-if="loading" class="loading-players" role="status">
        <v-progress-circular indeterminate size="24" color="#60a5fa" />
        <span>Loading players...</span>
      </div>
      <v-alert v-else-if="loadError" type="error" dense>
        {{ loadError }}
        <v-btn small text @click="load">Retry</v-btn>
      </v-alert>
      <DraftPoolSelection v-else v-model="selectedPlayerIds" :players="players" :positions="positions" />
      <v-alert v-if="error" type="error" dense class="mt-4">{{ error }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text :disabled="saving" @click="$emit('close')">Cancel</v-btn>
      <v-btn color="primary" :loading="saving" :disabled="loading || Boolean(loadError)" @click="save">
        Save
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import DraftPoolSelection from '@/components/draftPool/DraftPoolSelection.vue'

export default {
  name: 'DraftPoolDialog',
  components: { DraftPoolSelection },
  props: {
    championshipId: { type: [String, Number], required: true },
    positions: { type: Array, default: () => [] },
  },
  data: () => ({
    players: [],
    selectedPlayerIds: [],
    loading: false,
    loadError: null,
    saving: false,
    error: null,
  }),
  created() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      this.loadError = null
      try {
        const response = await this.$axios.get(`championship/${this.championshipId}/player/pool`)
        this.players = response.data
        this.selectedPlayerIds = response.data.filter(player => player.selected).map(player => player.id)
      } catch {
        this.loadError = 'Players could not be loaded.'
      } finally {
        this.loading = false
      }
    },
    async save() {
      if (this.saving) { return }
      this.saving = true
      this.error = null
      try {
        await this.$axios.put(`championship/${this.championshipId}/player/pool`, { player_ids: this.selectedPlayerIds })
        this.$emit('saved')
      } catch (error) {
        const detail = error.response && error.response.data && error.response.data.detail
        this.error = typeof detail === 'string' ? detail : 'Draft players could not be saved.'
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style scoped>
.pool-dialog {
  background: #1e293b !important;
  color: rgba(226, 232, 240, 0.95);
  border: 1px solid rgba(100, 116, 139, 0.35);
  border-radius: 8px !important;
}

.dialog-content { padding-top: 12px !important; }
.loading-players { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 32px 0; color: #cbd5e1; }
</style>
