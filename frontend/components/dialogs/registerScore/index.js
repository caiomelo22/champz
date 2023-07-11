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
    this.match = JSON.parse(JSON.stringify(this.currentMatch))
  },
  methods: {
    async register_score() {
      this.registerScoreLoading = true;
      let url = `match/${this.match.id}`;
      await this.$axios.patch(url, this.match)
      this.$emit('update', this.match)
      this.registerScoreLoading = false;
    },
  }
}