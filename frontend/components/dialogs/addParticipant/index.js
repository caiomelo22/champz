export default {
  name: 'AddParticipantDialog',
  data: () => ({
    updatingParticipant: false,
    selectedTeam: null,
    participant: null,
  }),
  props: {
    participantProp: Object,
    teams: {
      type: Array,
      default: []
    }
  },
  created() {
    this.participant = this.participantProp;
    if (this.participantProp) {
        const index = this.teams.map(x => x.id).indexOf(this.participant.team_id)
        this.selectedTeam = this.teams[index]
    }
  },
  methods: {
    async add_participant () {
      this.updatingParticipant = true;
      this.participant.team = this.selectedTeam.id;
      if (!this.participant.id) {
        await this.$axios
          .post("participant/create", this.participant)
          .then((response) => {
            this.$emit('update', response.data)
          })
          .catch((err) => { });
      } else {
        await this.$axios
          .patch(
            `participant/update/${this.participant.id}`,
            this.participant
          )
          .then((response) => {
            this.$emit('update', response.data)
          })
          .catch((err) => { });
      }
      this.updatingParticipant = false;
    },
  }
}