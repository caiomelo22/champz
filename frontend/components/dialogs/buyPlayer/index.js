import GeneralServices from "@/services/GeneralServices";
export default {
  name: 'BuyPlayerDialog',
  props: {
    participants: Array,
    currentPlayer: Object
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
      this.player.team_participant = this.player.team_participant;
      let url = `player/buy/${this.currentPlayer.id}`;
      await this.$axios
        .post(url, this.player)
        .then((response) => {
          this.$emit('update', response.data)
        })
        .catch((err) => { });
      this.updatingPlayer = false;
    },
  }
}