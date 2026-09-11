<template>
  <v-card class="bid-dialog">
    <v-card-title>Bid for {{ auction.player_name }}</v-card-title>
    <v-card-text>
      <div class="bid-summary">
        <span>Current bid</span>
        <strong>${{ auction.leading_bid || auction.minimum_bid }}</strong>
      </div>
      <div class="bid-summary">
        <span>Available budget</span>
        <strong>${{ availableBudget }}</strong>
      </div>
      <v-text-field
        v-model.number="amount"
        label="Your bid"
        type="number"
        :min="minimumAmount"
        prefix="$"
        outlined
        dark
        autofocus
        @keyup.enter="submit"
      />
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('close')">Cancel</v-btn>
      <v-btn color="primary" :loading="saving" @click="submit">Place bid</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'PlaceBidDialog',
  props: {
    championshipId: { type: [String, Number], required: true },
    auction: { type: Object, required: true },
    availableBudget: { type: Number, required: true },
  },
  data() {
    return {
      amount: this.auction.leading_bid
        ? this.auction.leading_bid + 1
        : this.auction.minimum_bid,
      saving: false,
      error: null,
    }
  },
  computed: {
    minimumAmount() {
      return this.auction.leading_bid ? this.auction.leading_bid + 1 : this.auction.minimum_bid
    },
  },
  methods: {
    async submit() {
      this.error = null
      this.saving = true
      try {
        const response = await this.$axios.post(
          `championship/${this.championshipId}/auction/${this.auction.id}/bid`,
          { amount: Number(this.amount) }
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
.bid-dialog {
  background: #1e293b !important;
  color: rgba(226, 232, 240, 0.95);
  border: 1px solid rgba(100, 116, 139, 0.35);
  border-radius: 8px !important;
}

.bid-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: rgba(203, 213, 225, 0.85);
}
</style>