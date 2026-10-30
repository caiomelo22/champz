<template>
  <div class="fut-card" :style="sizeStyle" role="img" :aria-label="`${player.name}, overall ${player.overall}, ${mainPosition}`">
    <div class="fut-card__meta">
      <span class="fut-card__overall">{{ player.overall }}</span>
      <span class="fut-card__position">{{ mainPosition }}</span>
      <span v-if="otherPositions.length" class="fut-card__other-positions">{{ otherPositions.join(' ') }}</span>
    </div>

    <img class="fut-card__photo" :src="gs.get_image_path(player.image_path)" alt="" />

    <div class="fut-card__name" :class="{ 'fut-card__name--long': player.name.length > 16 }">{{ player.name }}</div>

    <div class="fut-card__stats">
      <div v-for="stat in stats" :key="stat.label" class="fut-card__stat">
        <span class="fut-card__stat-label">{{ stat.label }}</span>
        <span class="fut-card__stat-value">{{ stat.value }}</span>
      </div>
    </div>

    <div class="fut-card__origin">
      <img class="fut-card__flag" :src="gs.get_image_path(player.nation_image_path)" :alt="player.nation_name || player.nation" />
      <img class="fut-card__club" :src="gs.get_image_path(player.team_origin_image_path)" :alt="player.team_origin_name || player.team_origin" />
    </div>
  </div>
</template>

<script>
import GeneralServices from '@/services/GeneralServices'

export default {
  name: 'PlayerCard',
  props: {
    player: { type: Object, required: true },
    width: { type: Number, default: 300 },
  },
  data: () => ({
    gs: new GeneralServices(),
  }),
  computed: {
    sizeStyle() {
      // Every inner dimension is in em, so the whole card scales with its width
      return { width: `${this.width}px`, fontSize: `${this.width / 30}px` }
    },
    positions() {
      return (this.player.specific_position || '').split(',').map(position => position.trim()).filter(Boolean)
    },
    mainPosition() {
      return this.positions[0] || ''
    },
    otherPositions() {
      return this.positions.slice(1)
    },
    stats() {
      return [
        { label: 'PAC', value: this.player.pace },
        { label: 'SHO', value: this.player.shooting },
        { label: 'PAS', value: this.player.passing },
        { label: 'DRI', value: this.player.dribbling },
        { label: 'DEF', value: this.player.defending },
        { label: 'PHY', value: this.player.physical },
      ]
    },
  },
}
</script>

<style scoped>
/* Positions are percentages of card-gold.png (252x350); sizes are em (1em = width / 30) */
.fut-card {
  position: relative;
  aspect-ratio: 252 / 350;
  background: url('~/assets/card-gold.png') center / contain no-repeat;
  filter: drop-shadow(0 1.6em 2.8em rgba(0, 0, 0, 0.45));
  font-family: 'DM Sans', sans-serif;
  color: #3b2a07;
}

.fut-card__meta {
  position: absolute;
  top: 22%;
  left: 16%;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4em;
  width: 17%;
}

.fut-card__overall {
  font-size: 4em;
  font-weight: 800;
  line-height: 0.9;
  letter-spacing: -0.1em;
}

.fut-card__position {
  font-size: 1.8em;
  font-weight: 700;
  line-height: 1;
}

.fut-card__other-positions {
  font-size: 1em;
  font-weight: 600;
  line-height: 1.2;
  text-align: center;
  opacity: 0.75;
}

.fut-card__flag {
  width: 3em;
  height: 1.9em;
  object-fit: cover;
  border-radius: 0.2em;
  box-shadow: 0 0.1em 0.3em rgba(0, 0, 0, 0.3);
}

.fut-card__club {
  width: 2.6em;
  height: 2.6em;
  object-fit: contain;
  filter: drop-shadow(0 0.1em 0.2em rgba(0, 0, 0, 0.3));
}

.fut-card__photo {
  position: absolute;
  top: 19%;
  left: 27%;
  z-index: 1;
  width: 62%;
  height: 44%;
  object-fit: contain;
  object-position: center bottom;
}

.fut-card__name {
  position: absolute;
  top: 64.5%;
  left: 14%;
  right: 14%;
  z-index: 2;
  font-size: 2.2em;
  line-height: 1.15;
  font-weight: 800;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fut-card__name--long {
  font-size: 1.7em;
  padding-top: 0.3em;
}

.fut-card__stats {
  position: absolute;
  top: 71.5%;
  left: 14%;
  right: 14%;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  text-align: center;
}

.fut-card__stat {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.fut-card__stat-label {
  font-size: 1em;
  font-weight: 700;
  opacity: 0.75;
}

.fut-card__stat-value {
  font-size: 2em;
  font-weight: 800;
  line-height: 1;
}

.fut-card__origin {
  position: absolute;
  top: 80%;
  left: 0;
  right: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1em;
}
</style>
