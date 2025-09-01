import GeneralServices from "@/services/GeneralServices.js";

export default {
  name: 'RegisterScoreDialog',
  props: {
    currentMatch: Object
  },
  data: () => ({
    registerScoreLoading: false,
    match: null,
    gs: new GeneralServices()
  }),
  created() {
    this.match = {...this.currentMatch}
  },
  methods: {
    isNullOrEmpty(value) {
        return value === null || value === undefined || value === '';
    },
    goalFieldsFilled() {
        return (!this.isNullOrEmpty(this.match.goals_2) &&
            !this.isNullOrEmpty(this.match.goals_1))
    },
    async registerScore() {
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