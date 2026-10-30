<template>
  <v-card class="bid-dialog">
    <DialogHeader :title="`Bid for ${auction.player_name}`" icon="mdi-gavel" @close="$emit('close')" />
    <v-card-text>
      <div v-if="player" class="bid-card">
        <PlayerCard :player="player" :width="200" />
      </div>
      <div class="bid-summary">
        <span>Current bid</span>
        <strong>${{ auction.leading_bid || auction.minimum_bid }}</strong>
      </div>
      <v-select
        v-if="isOwner"
        v-model="selectedParticipantId"
        :items="participants"
        item-text="name"
        item-value="id"
        label="Bid for participant"
        outlined
        dense
        dark
      />
      <div class="bid-summary">
        <span>Available budget</span>
        <strong>${{ displayedBudget }}</strong>
      </div>
      <v-text-field
        v-model.number="amount"
        label="Your bid"
        type="number"
        :min="minimumAmount"
        prefix="$"
        outlined
        dense
        dark
        autofocus
        @keyup.enter="submit"
      />
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text class="cancel-button" @click="$emit('close')">Cancel</v-btn>
      <v-btn
        color="primary"
        :loading="saving"
        :disabled="isOwner && !selectedParticipantId"
        @click="submit"
      >
        Place bid
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import DialogHeader from '@/components/dialogs/DialogHeader.vue'
import PlayerCard from '@/components/players/PlayerCard.vue'

export default {
  name: 'PlaceBidDialog',
  components: { DialogHeader, PlayerCard },
  props: {
    championshipId: { type: [String, Number], required: true },
    auction: { type: Object, required: true },
    player: { type: Object, default: null },
    availableBudget: { type: Number, required: true },
    participants: { type: Array, default: () => [] },
    isOwner: { type: Boolean, default: false },
    currentParticipantId: { type: [Number, String], default: null },
  },
  data() {
    const linkedParticipant = this.participants.find(
      participant => String(participant.id) === String(this.currentParticipantId)
    )
    let selectedParticipantId = null
    if (linkedParticipant) {
      selectedParticipantId = linkedParticipant.id
    } else if (this.isOwner && this.participants.length) {
      selectedParticipantId = this.participants[0].id
    }
    return {
      amount: this.auction.leading_bid
        ? this.auction.leading_bid + 1
        : this.auction.minimum_bid,
      selectedParticipantId,
      saving: false,
      error: null,
    }
  },
  computed: {
    minimumAmount() {
      return this.auction.leading_bid ? this.auction.leading_bid + 1 : this.auction.minimum_bid
    },
    selectedParticipant() {
      return this.participants.find(participant => participant.id === this.selectedParticipantId) || null
    },
    displayedBudget() {
      if (this.isOwner) {
        return this.selectedParticipant ? this.selectedParticipant.budget : 0
      }
      return this.availableBudget
    },
  },
  methods: {
    async submit() {
      this.error = null
      if (this.isOwner && !this.selectedParticipantId) {
        this.error = 'Select a participant to place the bid.'
        return
      }
      this.saving = true
      const payload = { amount: Number(this.amount) }
      if (this.isOwner) {
        payload.participant_id = this.selectedParticipantId
      }
      try {
        const response = await this.$axios.post(
          `championship/${this.championshipId}/auction/${this.auction.id}/bid`,
          payload
        )
        this.$emit('saved', response.data)
      } catch (error) {
        this.error = error.response && error.response.data && error.response.data.detail
          ? error.response.data.detail
          : 'Bid could not be placed.'
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style scoped>
.bid-card {
  display: flex;
  justify-content: center;
  margin: 4px 0 16px;
}

.bid-dialog {
  background: #1e293b !important;
  color: rgba(226, 232, 240, 0.95);
  border: 1px solid rgba(100, 116, 139, 0.35);
  border-radius: 8px !important;
}

.bid-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.875rem;
  color: rgba(203, 213, 225, 0.85);
}

.cancel-button {
  color: #cbd5e1 !important;
  text-transform: none;
}

.cancel-button:hover,
.cancel-button:focus-visible {
  color: #f1f5f9 !important;
  background: rgba(148, 163, 184, 0.12);
}
</style>