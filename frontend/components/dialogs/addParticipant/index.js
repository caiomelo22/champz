export default {
  name: 'AddParticipantDialog',
  data: () => ({
    updatingParticipant: false,
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
      this.participant.team = this.participant.team.id;
      if (!this.participant.id) {
        await this.$axios
          .post("participant", this.participant)
          .then((response) => {
            this.$emit('update', response.data)
          })
          .catch((err) => { });
      } else {
        await this.$axios
          .patch(
            `participant/${this.participant.id}`,
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