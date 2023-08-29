export default {
  name: 'AddParticipantDialog',
  data: () => ({
    updatingParticipant: false,
    selectedTeam: null,
    participant: null,
  }),
  props: {
    participantProp: Object,
    plTeams: {
      type: Array,
      default: []
    }
  },
  created() {
    this.participant = this.participantProp;
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