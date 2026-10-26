<template>
  <section class="player-selection" aria-label="Players for auction">
    <div class="selection-summary" aria-live="polite">
      <h3>Players by position</h3>
      <span>{{ value.length }} selected</span>
    </div>
    <p class="selection-hint">Select players below to start or restart auctions. Cancelled auctions can be selected again. The minimum bid and deadline apply to every selected player.</p>
    <div v-if="!groups.length" class="empty-position">No positions available.</div>
    <section v-for="group in groups" :key="group.id" class="position-group">
      <div class="position-heading">
        <h4>{{ group.name }} <span>({{ selectedCount(group) }}/{{ eligiblePlayers(group).length }})</span></h4>
        <v-btn
          small
          text
          color="#93c5fd"
          :disabled="!eligiblePlayers(group).length"
          :aria-label="`${allSelected(group) ? 'Deselect' : 'Select'} all ${group.name} players`"
          @click="togglePosition(group)"
        >
          {{ allSelected(group) ? 'Deselect all' : 'Select all' }}
        </v-btn>
      </div>
      <div v-if="!group.players.length" class="empty-position">No players in this position.</div>
      <div v-else class="position-players">
        <v-tooltip v-for="player in group.players" :key="player.id" bottom :disabled="!unavailableReason(player)">
          <template #activator="{ on, attrs }">
            <div
              class="player-option"
              :class="{ 'is-unavailable': unavailableReason(player), 'is-selected': value.includes(player.id) }"
              :tabindex="unavailableReason(player) ? 0 : null"
              v-bind="attrs"
              v-on="on"
            >
              <v-checkbox
                :input-value="value.includes(player.id)"
                :disabled="Boolean(unavailableReason(player))"
                :aria-label="`${player.name}, overall ${player.overall}${unavailableReason(player) ? ', ' + unavailableReason(player) : ''}`"
                color="#60a5fa"
                dark
                hide-details
                class="player-checkbox"
                @change="togglePlayer(player, $event)"
              >
                <template #label>
                  <span class="option-name">{{ player.name }}</span>
                  <span class="option-overall">{{ player.overall }}</span>
                </template>
              </v-checkbox>
            </div>
          </template>
          <span>{{ unavailableReason(player) }}</span>
        </v-tooltip>
      </div>
    </section>
  </section>
</template>

<script>
export default {
  name: 'AuctionPlayerSelection',
  props: {
    value: { type: Array, default: () => [] },
    groups: { type: Array, default: () => [] },
    auctionsByPlayer: { type: Object, default: () => ({}) },
  },
  computed: {
    eligibleIds() {
      return this.groups.flatMap(group => this.eligiblePlayers(group).map(player => player.id))
    },
  },
  watch: {
    eligibleIds() {
      const next = this.value.filter(id => this.eligibleIds.includes(id))
      if (next.length !== this.value.length) { this.$emit('input', next) }
    },
  },
  methods: {
    unavailableReason(player) {
      if (player.participant_id) { return 'This player already has an owner.' }
      const auction = this.auctionsByPlayer[player.id]
      if (!auction || auction.status === 'cancelled') { return '' }
      return auction.status === 'open' ? 'This player already has an active auction.' : 'This player already has a closed auction.'
    },
    eligiblePlayers(group) {
      return group.players.filter(player => !this.unavailableReason(player))
    },
    selectedCount(group) {
      return this.eligiblePlayers(group).filter(player => this.value.includes(player.id)).length
    },
    allSelected(group) {
      const eligible = this.eligiblePlayers(group)
      return eligible.length > 0 && eligible.every(player => this.value.includes(player.id))
    },
    togglePlayer(player, selected) {
      if (this.unavailableReason(player)) { return }
      const next = this.value.filter(id => id !== player.id)
      if (selected) { next.push(player.id) }
      this.$emit('input', next)
    },
    togglePosition(group) {
      const ids = this.eligiblePlayers(group).map(player => player.id)
      const next = this.allSelected(group)
        ? this.value.filter(id => !ids.includes(id))
        : [...new Set([...this.value, ...ids])]
      this.$emit('input', next)
    },
  },
}
</script>

<style scoped>
.selection-summary, .position-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.selection-summary h3, .position-heading h4 { margin: 0; color: #e2e8f0; }
.selection-summary span { color: #93c5fd; white-space: nowrap; }
.selection-hint, .empty-position { color: #94a3b8; font-size: 13px; margin: 8px 0 16px; }
.position-group { margin-top: 16px; }
.position-heading { margin-bottom: 8px; }
.position-heading h4 span { color: #94a3b8; font-size: 12px; font-weight: 400; }
.position-players { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.player-option { background: #162033; border: 1px solid #334155; border-radius: 10px; padding: 8px 12px; min-width: 0; }
.player-option.is-selected { border-color: #60a5fa; background: #1e3352; }
.player-option.is-unavailable { background: #192334; }
.player-option:focus-visible { outline: 2px solid #93c5fd; outline-offset: 2px; }
.player-checkbox { margin: 0; padding: 0; }
.player-checkbox ::v-deep .v-input--selection-controls__input { margin-right: 10px; }
.player-checkbox ::v-deep .v-label { flex: 1; min-width: 0; gap: 10px; }
.is-unavailable ::v-deep .v-input--selection-controls__input { pointer-events: none; }
.option-name { color: #e2e8f0; font-size: 13px; overflow-wrap: anywhere; }
.option-overall { margin-left: auto; color: #93c5fd; font-weight: 700; font-size: 13px; }
.is-unavailable .option-name, .is-unavailable .option-overall { color: #94a3b8; }
@media (max-width: 600px) {
  .position-players { grid-template-columns: minmax(0, 1fr); }
}
</style>