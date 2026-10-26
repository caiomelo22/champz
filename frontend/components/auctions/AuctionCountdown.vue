<template>
  <span :class="['auction-countdown', { expired }]">
    <v-icon small>{{ expired ? 'mdi-timer-off-outline' : 'mdi-timer-outline' }}</v-icon>
    {{ label }}
  </span>
</template>

<script>
export default {
  name: 'AuctionCountdown',
  props: {
    deadline: { type: String, required: true },
  },
  data() {
    return { now: Date.now(), timer: null }
  },
  computed: {
    remaining() {
      return Math.max(0, new Date(this.deadline).getTime() - this.now)
    },
    expired() {
      return this.remaining === 0
    },
    label() {
      if (this.expired) return 'Closing'
      const totalSeconds = Math.floor(this.remaining / 1000)
      const days = Math.floor(totalSeconds / 86400)
      const hours = Math.floor((totalSeconds % 86400) / 3600)
      const minutes = Math.floor((totalSeconds % 3600) / 60)
      const seconds = totalSeconds % 60
      if (days) return `${days}d ${hours}h ${minutes}m`
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
    },
  },
  mounted() {
    this.timer = window.setInterval(() => { this.now = Date.now() }, 1000)
  },
  beforeDestroy() {
    window.clearInterval(this.timer)
  },
}
</script>

<style scoped>
.auction-countdown {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #fbbf24;
  font-variant-numeric: tabular-nums;
  font-weight: 700;
}

.auction-countdown.expired {
  color: #94a3b8;
}
</style>