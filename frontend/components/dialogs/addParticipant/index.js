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
    },
    championshipId: { type: [String, Number], default: null }
  },
  created() {
    this.participant = this.participantProp;
    if (this.participantProp) {
        const index = this.teams.map(x => x.name).indexOf(this.participant.team_name)
        this.selectedTeam = this.teams[index]
    }
  },
  methods: {
    async add_participant () {
      this.updatingParticipant = true;
      this.participant.team = this.selectedTeam.name;
      const prefix = this.championshipId ? `championship/${this.championshipId}/` : '';
      if (!this.participant.id) {
        await this.$axios
          .post(`${prefix}participant/create`, this.participant)
          .then((response) => {
            this.$emit('update', response.data)
          })
          .catch((err) => { });
      } else {
        await this.$axios
          .patch(
            `${prefix}participant/update/${this.participant.id}`,
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