<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="dashboard-title">My Championships</h1>
      <v-btn class="create-btn" @click="createDialog = true">
        <v-icon left>mdi-plus</v-icon>
        New Champz
      </v-btn>
    </div>

    <div v-if="loading" class="text-center py-12">
      <v-progress-circular indeterminate color="blue" size="48" />
    </div>

    <div v-else-if="championships.length === 0" class="empty-state">
      <v-icon size="80" color="rgba(100,116,139,0.4)">mdi-trophy-outline</v-icon>
      <p class="empty-text">You don't have any championships yet.</p>
      <v-btn class="create-btn" @click="createDialog = true">
        Create your first Champz
      </v-btn>
    </div>

    <div v-else class="championship-grid">
      <div
        v-for="champ in championships"
        :key="champ.id"
        class="championship-card"
        @click="openChampionship(champ)"
      >
        <div class="card-header">
          <h2 class="card-title">{{ champ.name }}</h2>
          <v-chip
            small
            :color="statusColor(champ.status)"
            dark
            class="status-chip"
          >
            {{ statusLabel(champ.status) }}
          </v-chip>
        </div>

        <div class="card-stats">
          <div class="stat">
            <v-icon small color="rgba(203,213,225,0.7)">mdi-account-group</v-icon>
            <span>{{ champ.num_participants }} participants</span>
          </div>
          <div class="stat">
            <v-icon small color="rgba(203,213,225,0.7)">mdi-calendar</v-icon>
            <span>{{ formatDate(champ.created_at) }}</span>
          </div>
          <div class="stat">
            <v-icon small color="rgba(203,213,225,0.7)">mdi-cash</v-icon>
            <span>Budget: ${{ champ.budget_default }}</span>
          </div>
        </div>

        <div class="card-actions" @click.stop>
          <v-btn icon small @click="confirmDelete(champ)">
            <v-icon small color="rgba(239,68,68,0.8)">mdi-delete-outline</v-icon>
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Create Dialog -->
    <v-dialog v-model="createDialog" max-width="450" dark>
      <v-card class="dialog-card">
        <v-card-title class="dialog-title">Create New Championship</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newChampionship.name"
            label="Championship Name"
            outlined
            dense
            dark
            autofocus
          />
          <v-text-field
            v-model.number="newChampionship.budget_default"
            label="Default Budget per Participant"
            outlined
            dense
            dark
            type="number"
            prefix="$"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="createDialog = false">Cancel</v-btn>
          <v-btn color="primary" :loading="creating" @click="createChampionship" class="create-action-btn">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400" dark>
      <v-card class="dialog-card">
        <v-card-title class="dialog-title">Delete Championship</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ championshipToDelete ? championshipToDelete.name : '' }}</strong>?
          This will permanently delete all participants, draft picks, and matches.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteChampionship">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      championships: [],
      loading: true,
      createDialog: false,
      deleteDialog: false,
      creating: false,
      deleting: false,
      newChampionship: { name: '', budget_default: 250 },
      championshipToDelete: null,
    }
  },
  async mounted() {
    await this.fetchChampionships()
  },
  methods: {
    async fetchChampionships() {
      this.loading = true
      try {
        const response = await this.$axios.get('championship/list')
        this.championships = response.data
      } catch (err) {
        this.$toast.error('Failed to load championships')
      }
      this.loading = false
    },
    async createChampionship() {
      if (!this.newChampionship.name) return
      this.creating = true
      try {
        await this.$axios.post('championship/create', this.newChampionship)
        this.createDialog = false
        this.newChampionship = { name: '', budget_default: 250 }
        await this.fetchChampionships()
        this.$toast.success('Championship created!')
      } catch (err) {
        this.$toast.error('Failed to create championship')
      }
      this.creating = false
    },
    confirmDelete(champ) {
      this.championshipToDelete = champ
      this.deleteDialog = true
    },
    async deleteChampionship() {
      this.deleting = true
      try {
        await this.$axios.delete(`championship/${this.championshipToDelete.id}`)
        this.deleteDialog = false
        this.championshipToDelete = null
        await this.fetchChampionships()
        this.$toast.success('Championship deleted')
      } catch (err) {
        this.$toast.error('Failed to delete championship')
      }
      this.deleting = false
    },
    openChampionship(champ) {
      this.$router.push(`/championship/${champ.id}/draft`)
    },
    statusColor(status) {
      const map = { draft: '#3b82f6', games: '#f59e0b', complete: '#10b981' }
      return map[status] || '#64748b'
    },
    statusLabel(status) {
      const map = { draft: 'Draft', games: 'In Progress', complete: 'Complete' }
      return map[status] || status
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      return this.$moment(dateStr).format('MMM D, YYYY')
    },
  },
}
</script>

<style scoped>
.dashboard {
  max-width: 960px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.dashboard-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: rgba(226, 232, 240, 0.95);
}

.create-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
  color: white !important;
  text-transform: none;
  font-weight: 600;
  border-radius: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-text {
  color: rgba(203, 213, 225, 0.7);
  font-size: 16px;
  margin: 16px 0 24px;
  font-family: 'DM Sans', sans-serif;
}

.championship-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.championship-card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(100, 116, 139, 0.3);
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.championship-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  border-color: rgba(59, 130, 246, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.card-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: rgba(226, 232, 240, 0.95);
  margin: 0;
}

.status-chip {
  font-size: 11px !important;
  font-weight: 600;
}

.card-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(203, 213, 225, 0.7);
  font-size: 13px;
  font-family: 'DM Sans', sans-serif;
}

.card-actions {
  position: absolute;
  bottom: 16px;
  right: 16px;
}

.dialog-card {
  background: #1e293b !important;
  border-radius: 16px !important;
}

.dialog-title {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  color: rgba(226, 232, 240, 0.95);
}

.create-action-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
  color: white !important;
  text-transform: none;
}
</style>
