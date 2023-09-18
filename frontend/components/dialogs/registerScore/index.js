export default {
  name: 'RegisterScoreDialog',
  props: {
    currentMatch: Object
  },
  data: () => ({
    registerScoreLoading: false,
    match: null
  }),
  created() {
    this.match = {...this.currentMatch}
  },
  methods: {
    async register_score() {
      this.registerScoreLoading = true;
      this.match.goals_1 = parseInt(this.match.goals_1);
      this.match.goals_2 = parseInt(this.match.goals_2);
      let url = `match/update/${this.match.id}`;
      await this.$axios.patch(url, this.match)
      this.$emit('update', this.match)
      this.registerScoreLoading = false;
    },
  }
}