<template>
  <v-card class="auction-dialog">
    <v-card-title>{{ dialogTitle }}</v-card-title>
    <v-card-text>
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
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text class="cancel-button" @click="$emit('close')">Cancel</v-btn>
      <v-btn color="primary" class="save-button" :loading="saving" @click="save">
        <v-icon left small>mdi-gavel</v-icon>
        {{ submitLabel }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ConfigureAuctionDialog',
  props: {
    championshipId: { type: [String, Number], required: true },
    playerIds: { type: Array, default: () => [] },
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
    }
  },
  computed: {
    isRestart() {
      return this.auction && this.auction.status === 'cancelled'
    },
    dialogTitle() {
      if (this.isRestart) {
        return 'Restart auction'
      }
      return this.auction ? 'Edit auction' : `Configure ${this.playerIds.length} auction(s)`
    },
    submitLabel() {
      if (this.isRestart) {
        return 'Restart auction'
      }
      return this.auction ? 'Update auction' : 'Create auction'
    },
  },
  methods: {
    async save() {
      this.error = null
      if (!this.deadline || !this.minimumBid || (!this.auction && !this.playerIds.length)) {
        this.error = 'Deadline, minimum bid and players are required.'
        return
      }
      this.saving = true
      const payload = {
        deadline: new Date(this.deadline).toISOString(),
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
            { ...payload, player_ids: this.playerIds }
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