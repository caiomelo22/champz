<template>
  <v-card class="auction-dialog" dark>
    <v-card-title>{{ dialogTitle }}</v-card-title>
    <v-card-text class="dialog-content">
      <div v-if="player" class="single-player">
        <span>{{ player.name }}</span>
        <strong>{{ player.overall }}</strong>
      </div>
      <div class="auction-settings" :class="{ 'batch-settings': isBatch }">
        <v-text-field
          v-model.number="minimumBid"
          label="Minimum bid"
          type="number"
          min="1"
          prefix="$"
          outlined
          dark
        />
        <v-text-field
          v-model="deadline"
          label="Deadline"
          type="datetime-local"
          outlined
          dark
        />
      </div>
      <template v-if="isBatch">
        <div v-if="loadingPlayers" class="loading-players" role="status">
          <v-progress-circular indeterminate size="24" color="#60a5fa" />
          <span>Loading draft players...</span>
        </div>
        <v-alert v-else-if="playersError" type="error" dense>
          {{ playersError }}
          <v-btn small text @click="loadPlayers">Retry</v-btn>
        </v-alert>
        <AuctionPlayerSelection
          v-else
          v-model="selectedPlayerIds"
          :groups="playerGroups"
          :auctions-by-player="auctionsByPlayer"
        />
      </template>
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text class="cancel-button" :disabled="saving" @click="$emit('close')">Cancel</v-btn>
      <v-btn color="primary" class="save-button" :loading="saving" :disabled="loadingPlayers || Boolean(playersError) || (!auction && !creationPlayerIds.length)" @click="save">
        <v-icon left small>mdi-gavel</v-icon>
        {{ submitLabel }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import AuctionPlayerSelection from '@/components/auctions/AuctionPlayerSelection.vue'

export default {
  name: 'ConfigureAuctionDialog',
  components: { AuctionPlayerSelection },
  props: {
    championshipId: { type: [String, Number], required: true },
    player: { type: Object, default: null },
    positions: { type: Array, default: () => [] },
    auctionsByPlayer: { type: Object, default: () => ({}) },
    auction: { type: Object, default: null },
  },
  data() {
    const initialDeadline = this.auction
      ? new Date(this.auction.deadline)
      : new Date(Date.now() + 24 * 60 * 60 * 1000)
    initialDeadline.setSeconds(0, 0)
    const localDeadline = new Date(initialDeadline.getTime() - initialDeadline.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16)
    return {
      minimumBid: this.auction ? this.auction.minimum_bid : 1,
      deadline: localDeadline,
      saving: false,
      error: null,
      selectedPlayerIds: [],
      playerGroups: [],
      loadingPlayers: false,
      playersError: null,
    }
  },
  computed: {
    isBatch() {
      return !this.auction && !this.player
    },
    creationPlayerIds() {
      if (this.player) { return [this.player.id] }
      const eligibleIds = new Set(this.playerGroups.flatMap(group => group.players
        .filter(player => !player.participant_id && (
          !this.auctionsByPlayer[player.id] || this.auctionsByPlayer[player.id].status === 'cancelled'
        ))
        .map(player => player.id)))
      return this.selectedPlayerIds.filter(id => eligibleIds.has(id))
    },
    isRestart() {
      return this.auction && this.auction.status === 'cancelled'
    },
    dialogTitle() {
      if (this.isRestart) {
        return 'Restart auction'
      }
      return this.auction ? 'Edit auction' : this.isBatch ? 'Start auctions' : 'Start auction'
    },
    submitLabel() {
      if (this.isRestart) {
        return 'Restart auction'
      }
      return this.auction ? 'Update auction' : this.isBatch ? `Start auctions (${this.creationPlayerIds.length})` : 'Start auction'
    },
  },
  created() {
    if (this.isBatch) { this.loadPlayers() }
  },
  methods: {
    async loadPlayers() {
      this.loadingPlayers = true
      this.playersError = null
      this.selectedPlayerIds = []
      try {
        this.playerGroups = await Promise.all(this.positions.map(async (position) => {
          const response = await this.$axios.get(
            `championship/${this.championshipId}/player/list?position=${position.id}`
          )
          return { ...position, players: response.data }
        }))
      } catch {
        this.playersError = 'Draft players could not be loaded.'
      } finally {
        this.loadingPlayers = false
      }
    },
    async save() {
      if (this.saving || this.loadingPlayers || this.playersError) { return }
      this.error = null
      if (!this.deadline || !this.minimumBid || (!this.auction && !this.creationPlayerIds.length)) {
        this.error = 'Deadline, minimum bid and players are required.'
        return
      }
      const deadline = new Date(this.deadline)
      if (!Number.isFinite(deadline.getTime()) || deadline.getTime() <= Date.now()) {
        this.error = 'Deadline must be in the future.'
        return
      }
      if (!Number.isFinite(Number(this.minimumBid)) || Number(this.minimumBid) <= 0) {
        this.error = 'Minimum bid must be greater than zero.'
        return
      }
      this.saving = true
      const payload = {
        deadline: deadline.toISOString(),
        minimum_bid: Number(this.minimumBid),
      }
      try {
        const response = this.auction
          ? await this.$axios.patch(
            `championship/${this.championshipId}/auction/${this.auction.id}`,
            payload
          )
          : await this.$axios.post(
            `championship/${this.championshipId}/auction/configure`,
            { ...payload, player_ids: this.creationPlayerIds }
          )
        this.$emit('saved', response.data)
      } catch (error) {
        this.error = error.response && error.response.data && error.response.data.detail
          ? error.response.data.detail
          : 'Auction could not be configured.'
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style scoped>
.auction-dialog {
  background: #1e293b !important;
  color: rgba(226, 232, 240, 0.95);
  border: 1px solid rgba(100, 116, 139, 0.35);
  border-radius: 8px !important;
}

.dialog-content { padding-top: 12px !important; }
.batch-settings { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.single-player {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  margin-bottom: 24px;
  background: #162033;
  border: 1px solid #334155;
  border-radius: 10px;
  color: #e2e8f0;
}
.single-player strong { color: #93c5fd; }
.loading-players { display: flex; align-items: center; justify-content: center; gap: 12px; padding: 32px 0; color: #cbd5e1; }
@media (max-width: 600px) {
  .batch-settings { grid-template-columns: 1fr; gap: 0; }
}

.cancel-button {
  color: #cbd5e1 !important;
  text-transform: none;
}

.save-button {
  background: #2563eb !important;
  color: #ffffff !important;
  min-width: 156px;
  text-transform: none;
  font-weight: 700;
}

.save-button:hover {
  background: #1d4ed8 !important;
}
</style>