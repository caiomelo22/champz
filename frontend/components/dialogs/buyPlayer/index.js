import GeneralServices from "@/services/GeneralServices";
export default {
  name: 'BuyPlayerDialog',
  props: {
    participants: Array,
    currentPlayer: Object,
    championshipId: { type: [String, Number], default: null }
  },
  data: () => ({
    gs: new GeneralServices(),
    participantSelected: null,
    updatingPlayer: false,
    player: null
  }),
  created() {
    this.player = {...this.currentPlayer}
  },
  methods: {
    async buy_player() {
      this.updatingPlayer = true;
      let url, body;
      if (this.championshipId) {
        url = `championship/${this.championshipId}/player/buy/${this.currentPlayer.id}`;
        body = {
          participant_id: this.participantSelected ? this.participantSelected.id : null,
          value: this.player.value ? parseInt(this.player.value) : null
        };
      } else {
        url = `player/buy/${this.currentPlayer.id}`;
        body = this.player;
      }
      await this.$axios
        .post(url, body)
        .then((response) => {
          this.$emit('update', response.data)
        })
        .catch((err) => { });
      this.updatingPlayer = false;
    },
  }
}