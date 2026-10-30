import GeneralServices from '@/services/GeneralServices'
import AddParticipant from '@/components/dialogs/addParticipant/index.vue'
import BuyPlayer from '@/components/dialogs/buyPlayer/index.vue'
import ParticipantTeam from '@/components/dialogs/participantTeam/index.vue'
import AuctionCountdown from '@/components/auctions/AuctionCountdown.vue'
import ConfigureAuction from '@/components/dialogs/configureAuction/index.vue'
import PlaceBid from '@/components/dialogs/placeBid/index.vue'
import DraftPool from '@/components/dialogs/draftPool/index.vue'

export default {
  name: 'ChampionshipDraft',
  components: {
    AddParticipant,
    BuyPlayer,
    ParticipantTeam,
    AuctionCountdown,
    ConfigureAuction,
    PlaceBid,
    DraftPool,
  },
  data: () => ({
    gs: new GeneralServices(),
    tab: 0,
    addParticipantDialog: false,
    buyPlayerDialog: false,
    participantTeamDialog: false,
    configureAuctionDialog: false,
    placeBidDialog: false,
    draftPoolDialog: false,
    participants: [],
    genericBudget: 250,
    positions: [],
    selectedPosition: [],
    teams: [],
    auctionsByPlayer: {},
    auctionPlayer: null,
    playersLoading: false,
    participantsLoading: false,
    participantBudgetsDirty: false,
    auctionPolling: false,
    pollingTimer: null,
    currentPlayer: null,
    currentParticipant: {},
    currentAuction: null,
    selectedTeam: null,
    newParticipant: { name: null, budget: null, team: null, user_email: null },
    championshipName: '',
    championshipStatus: null,
    accessRole: null,
    myParticipantId: null,
  }),
  computed: {
    championshipId() {
      return this.$route.params.id
    },
    isOwner() {
      return this.accessRole === 'owner'
    },
    myParticipant() {
      return this.participants.find(participant => participant.id === this.myParticipantId) || null
    },
    linkedManagerParticipantId() {
      if (!this.isOwner) {
        return this.myParticipantId
      }
      const participantById = this.participants.find(
        participant => String(participant.id) === String(this.myParticipantId)
      )
      if (participantById) {
        return participantById.id
      }
      const user = this.$store.getters['auth/getUser']
      const email = user && user.email ? user.email.trim().toLowerCase() : null
      const participantByEmail = email
        ? this.participants.find(
          participant => participant.user_email && participant.user_email.trim().toLowerCase() === email
        )
        : null
      return participantByEmail ? participantByEmail.id : null
    },
    availableBudget() {
      return this.myParticipant && this.myParticipant.budget != null ? this.myParticipant.budget : 0
    },
  },
  watch: {
    participantTeamDialog() {
      if (!this.participantTeamDialog) { this.selectedTeam = [] }
    },
    tab() {
      if (this.positions[this.tab]) {
        this.get_players_by_position_algorithm(this.positions[this.tab].id)
      }
    },
  },
  async mounted() {
    await this.get_championship()
    await this.get_participants()
    if (this.isOwner) { await this.get_most_popular_teams() }
    await this.get_positions()
    await this.get_auctions()
    this.pollingTimer = window.setInterval(this.get_auctions, 3000)
  },
  beforeDestroy() {
    window.clearInterval(this.pollingTimer)
  },
  methods: {
    async get_championship() {
      try {
        const response = await this.$axios.get(`championship/${this.championshipId}`)
        this.championshipName = response.data.name
        this.championshipStatus = response.data.status
        this.genericBudget = response.data.budget_default
        this.accessRole = response.data.access_role
        this.myParticipantId = response.data.participant_id
      } catch {
        this.$router.push('/dashboard')
      }
    },
    async get_auctions() {
      if (this.auctionPolling) { return }
      this.auctionPolling = true
      try {
        const previous = this.auctionsByPlayer
        const response = await this.$axios.get(`championship/${this.championshipId}/auction/list`)
        const next = response.data.reduce((map, auction) => {
          map[auction.player_id] = auction
          return map
        }, {})

        let refreshDraft = false
        response.data.forEach((auction) => {
          const oldAuction = previous[auction.player_id]
          if (!oldAuction || oldAuction.status !== auction.status ||
            oldAuction.leading_participant_id !== auction.leading_participant_id ||
            oldAuction.leading_bid !== auction.leading_bid) {
            this.participantBudgetsDirty = true
          }
          if (oldAuction && oldAuction.is_current_user_leader && !auction.is_current_user_leader && auction.status === 'open') {
            this.$toast.info(`You were outbid for ${auction.player_name}.`)
          }
          if (oldAuction && oldAuction.status === 'open' && auction.status === 'closed') { refreshDraft = true }
        })
        if (Object.keys(previous).some(playerId => !next[playerId])) {
          this.participantBudgetsDirty = true
        }
        this.auctionsByPlayer = next
        if (this.participantBudgetsDirty) {
          await this.get_participants(false)
          this.participantBudgetsDirty = false
        }
        if (refreshDraft && this.positions[this.tab]) {
          await this.get_players_by_position_algorithm(this.positions[this.tab].id)
        }
      } catch (error) {
        if (!error.response || error.response.status !== 401) {
          this.$toast.error('Auction status could not be updated.')
        }
      } finally {
        this.auctionPolling = false
      }
    },
    auction_for(playerId) {
      return this.auctionsByPlayer[playerId] || null
    },
    can_assign_manually(playerId) {
      const auction = this.auction_for(playerId)
      return this.isOwner && (!auction || auction.status === 'cancelled')
    },
    can_bid(auction) {
      return Boolean(
        (this.isOwner ? this.participants.length : this.myParticipantId) &&
        auction &&
        auction.status === 'open' &&
        new Date(auction.deadline).getTime() > Date.now()
      )
    },
    reset_player_modal() {
      this.currentPlayer = null
      this.buyPlayerDialog = false
    },
    reset_participant_dialog() {
      this.newParticipant = null
      this.addParticipantDialog = false
    },
    participant_added(participant) {
      const index = this.participants.findIndex(item => item.id === participant.id)
      if (index === -1) { this.participants.push(participant) } else { this.$set(this.participants, index, participant) }
      this.reset_participant_dialog()
      if (this.positions[this.tab]) { this.get_players_by_position_algorithm(this.positions[this.tab].id) }
      const teamIndex = this.teams.findIndex(team => team.name === participant.team_name)
      if (teamIndex !== -1) { this.$set(this.teams[teamIndex], 'participant_id', participant.id) }
    },
    get_participant_name(id) {
      const participant = this.participants.find(item => item.id === id)
      return participant ? participant.name : null
    },
    open_participant_dialog(participant) {
      this.newParticipant = participant
        ? { ...participant }
        : { name: null, budget: this.genericBudget, team: null, user_email: null }
      this.addParticipantDialog = true
    },
    async get_participants(showLoading = true) {
      if (showLoading) { this.participantsLoading = true }
      try {
        const response = await this.$axios.get(`championship/${this.championshipId}/participant/list`)
        this.participants = response.data
      } finally {
        if (showLoading) { this.participantsLoading = false }
      }
    },
    async get_positions() {
      this.playersLoading = true
      try {
        const response = await this.$axios.get('position/list')
        this.positions = response.data
        if (this.positions.length) { await this.get_players_by_position_algorithm(this.positions[0].id) }
      } finally {
        this.playersLoading = false
      }
    },
    async get_players_by_position_algorithm(positionId) {
      this.playersLoading = true
      try {
        const response = await this.$axios.get(
          `championship/${this.championshipId}/player/list?position=${positionId}`
        )
        this.selectedPosition = response.data
      } finally {
        this.playersLoading = false
      }
    },
    async get_players_by_team(participant) {
      this.currentParticipant = participant
      const index = this.participants.findIndex(item => item.id === participant.id)
      this.$set(this.participants[index], 'team_loading_att', true)
      try {
        const response = await this.$axios.get(
          `championship/${this.championshipId}/player/list?participant_id=${participant.id}`
        )
        this.selectedTeam = response.data
        this.participantTeamDialog = true
      } finally {
        this.$set(this.participants[index], 'team_loading_att', false)
      }
    },
    async get_most_popular_teams() {
      const response = await this.$axios.get('team/most-popular')
      this.teams = response.data
    },
    get_player(player) {
      this.currentPlayer = player
      this.buyPlayerDialog = true
    },
    async delete_participant(id) {
      try {
        await this.$axios.delete(`championship/${this.championshipId}/participant/delete/${id}`)
        this.participants = this.participants.filter(participant => participant.id !== id)
        if (this.positions[this.tab]) { await this.get_players_by_position_algorithm(this.positions[this.tab].id) }
      } catch (error) {
        const detail = error.response && error.response.data && error.response.data.detail
        this.$toast.error(detail || 'Participant could not be deleted.')
      }
    },
    async remove_buy(player) {
      try {
        const response = await this.$axios.post(
          `championship/${this.championshipId}/player/buy/${player.id}`,
          { participant_id: null }
        )
        await this.get_participants()
        this.update_player(response.data)
      } catch (error) {
        const detail = error.response && error.response.data && error.response.data.detail
        this.$toast.error(detail || 'Player could not be removed.')
      }
    },
    update_player(player) {
      if (!this.positions[this.tab] || this.positions[this.tab].id !== player.position_id) { return }
      const index = this.selectedPosition.findIndex(item => item.id === player.id)
      if (index !== -1) { this.$set(this.selectedPosition, index, player) }
    },
    async player_updated(player) {
      this.update_player(player)
      await this.get_participants()
      this.reset_player_modal()
    },
    async draft_pool_saved() {
      this.draftPoolDialog = false
      this.$toast.success('Draft players updated.')
      if (this.positions[this.tab]) { await this.get_players_by_position_algorithm(this.positions[this.tab].id) }
    },
    open_batch_auction() {
      this.currentAuction = null
      this.auctionPlayer = null
      this.configureAuctionDialog = true
    },
    open_player_auction(player) {
      this.currentAuction = null
      this.auctionPlayer = player
      this.configureAuctionDialog = true
    },
    edit_auction(auction) {
      this.auctionPlayer = null
      this.currentAuction = auction
      this.configureAuctionDialog = true
    },
    async auction_saved() {
      this.configureAuctionDialog = false
      this.currentAuction = null
      this.auctionPlayer = null
      await this.get_auctions()
    },
    async cancel_auction(auction) {
      try {
        await this.$axios.delete(`championship/${this.championshipId}/auction/${auction.id}`)
        await Promise.all([this.get_auctions(), this.get_participants()])
      } catch (error) {
        const detail = error.response && error.response.data && error.response.data.detail
        this.$toast.error(detail || 'Auction could not be cancelled.')
      }
    },
    open_bid(auction) {
      this.currentAuction = auction
      this.placeBidDialog = true
    },
    async bid_saved(result) {
      this.placeBidDialog = false
      this.participantBudgetsDirty = true
      this.$set(this.auctionsByPlayer, result.auction.player_id, result.auction)
      const participantIndex = this.participants.findIndex(
        item => item.id === result.auction.leading_participant_id
      )
      if (participantIndex !== -1) {
        this.$set(this.participants[participantIndex], 'budget', result.available_budget)
      }
      this.$toast.success('Bid placed.')
      try {
        await this.get_participants(false)
        this.participantBudgetsDirty = false
      } catch {
        this.$toast.error('Bid placed, but balances could not be updated. Retrying automatically.')
      }
    },
  },
}