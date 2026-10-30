<template>
  <section class="pool-selection" aria-label="Draft players">
    <div class="selection-summary" aria-live="polite">
      <h3>Draft players</h3>
      <span>{{ value.length }} selected</span>
    </div>
    <p class="selection-hint">Only selected players take part in the draft. Players assigned to a participant or with an open auction cannot be removed.</p>

    <v-tabs v-model="tab" color="#3b82f6" background-color="transparent" show-arrows dark>
      <v-tab v-for="group in groups" :key="group.id" class="position-tab">
        {{ group.name }}
        <span class="tab-count">{{ selectedCount(group) }}/{{ group.players.length }}</span>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" class="pool-tabs-items">
      <v-tab-item v-for="group in groups" :key="group.id">
        <div class="position-toolbar">
          <v-text-field
            v-model="search"
            placeholder="Search player"
            prepend-inner-icon="mdi-magnify"
            dense
            outlined
            dark
            hide-details
            clearable
            class="search-field"
          />
          <v-btn
            small
            text
            color="#93c5fd"
            :disabled="!group.players.length"
            :aria-label="`${allSelected(group) ? 'Deselect' : 'Select'} all ${group.name} players`"
            @click="togglePosition(group)"
          >
            {{ allSelected(group) ? 'Deselect all' : 'Select all' }}
          </v-btn>
        </div>

        <div v-if="!filteredPlayers(group).length" class="empty-position">No players found.</div>
        <div v-else class="position-players">
          <div
            v-for="player in filteredPlayers(group)"
            :key="player.id"
            class="player-option"
            :class="{ 'is-selected': selectedIds.has(player.id), 'is-locked': player.locked }"
          >
            <v-checkbox
              :input-value="selectedIds.has(player.id)"
              :disabled="player.locked"
              :aria-label="`${player.name}, overall ${player.overall}${player.locked ? ', ' + lockedReason(player) : ''}`"
              color="#60a5fa"
              dark
              hide-details
              class="player-checkbox"
              @change="togglePlayer(player, $event)"
            >
              <template #label>
                <img :src="gs.get_image_path(player.team_origin_image_path)" :alt="player.team_origin_name" class="club-logo" />
                <span class="option-info">
                  <span class="option-name">{{ player.name }}</span>
                  <span class="option-meta">{{ player.locked ? lockedReason(player) : player.specific_position }}</span>
                </span>
                <span class="option-overall">{{ player.overall }}</span>
              </template>
            </v-checkbox>
          </div>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </section>
</template>

<script>
import GeneralServices from '@/services/GeneralServices'

export default {
  name: 'DraftPoolSelection',
  props: {
    value: { type: Array, default: () => [] },
    players: { type: Array, default: () => [] },
    positions: { type: Array, default: () => [] },
  },
  data: () => ({
    gs: new GeneralServices(),
    tab: 0,
    search: '',
  }),
  computed: {
    selectedIds() {
      return new Set(this.value)
    },
    groups() {
      return this.positions.map(position => ({
        ...position,
        players: this.players.filter(player => player.position_id === position.id),
      }))
    },
  },
  methods: {
    lockedReason(player) {
      return player.participant_id ? `Assigned to ${player.team_participant}` : 'Open auction'
    },
    filteredPlayers(group) {
      const term = (this.search || '').trim().toLowerCase()
      return term ? group.players.filter(player => player.name.toLowerCase().includes(term)) : group.players
    },
    selectedCount(group) {
      return group.players.filter(player => this.selectedIds.has(player.id)).length
    },
    allSelected(group) {
      return group.players.length > 0 && group.players.every(player => this.selectedIds.has(player.id))
    },
    togglePlayer(player, selected) {
      if (player.locked) { return }
      const next = this.value.filter(id => id !== player.id)
      if (selected) { next.push(player.id) }
      this.$emit('input', next)
    },
    togglePosition(group) {
      if (this.allSelected(group)) {
        const removable = new Set(group.players.filter(player => !player.locked).map(player => player.id))
        this.$emit('input', this.value.filter(id => !removable.has(id)))
      } else {
        this.$emit('input', [...new Set([...this.value, ...group.players.map(player => player.id)])])
      }
    },
  },
}
</script>

<style scoped>
.selection-summary, .position-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.selection-summary h3 { margin: 0; color: #e2e8f0; }
.selection-summary span { color: #93c5fd; white-space: nowrap; }
.selection-hint, .empty-position { color: #94a3b8; font-size: 13px; margin: 8px 0 12px; }
.position-tab { text-transform: none; }
.tab-count { margin-left: 6px; color: #94a3b8; font-size: 12px; }
.pool-tabs-items { background: transparent !important; padding-top: 12px; }
.position-toolbar { margin-bottom: 12px; }
.search-field { max-width: 280px; }
.position-players { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.player-option { background: #162033; border: 1px solid #334155; border-radius: 10px; padding: 8px 12px; min-width: 0; }
.player-option.is-selected { border-color: #60a5fa; background: #1e3352; }
.player-option.is-locked { border-style: dashed; }
.player-checkbox { margin: 0; padding: 0; }
.player-checkbox ::v-deep .v-input--selection-controls__input { margin-right: 10px; }
.player-checkbox ::v-deep .v-label { flex: 1; min-width: 0; gap: 10px; }
.club-logo { width: 24px; height: 24px; object-fit: contain; flex-shrink: 0; }
.option-info { display: flex; flex-direction: column; min-width: 0; }
.option-name { color: #e2e8f0; font-size: 13px; overflow-wrap: anywhere; }
.option-meta { color: #94a3b8; font-size: 11px; }
.option-overall { margin-left: auto; color: #93c5fd; font-weight: 700; font-size: 13px; }
@media (max-width: 600px) {
  .position-players { grid-template-columns: minmax(0, 1fr); }
  .search-field { max-width: none; }
}
</style>
