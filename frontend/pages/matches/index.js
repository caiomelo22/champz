import GeneralServices from "@/services/GeneralServices";
import Confirmation from "@/components/dialogs/confirmation/index.vue";
import RegisterScore from "@/components/dialogs/registerScore/index.vue";
import GroupToolbar from "@/components/matches/groupToolbar/index.vue";
export default {
  name: "Matches",
  components: { Confirmation, RegisterScore, GroupToolbar },
  data: () => ({
    gs: new GeneralServices(),
    final: false,
    registerScoreDialog: false,
    resetConfirmationDialog: false,
    selectedGroup: {},
    table: [],
    currentMatch: {},
    currentGroupIndex: 0,
    loading: true,
    groupLoading: false,
    registerScoreLoading: false,
    champzFileLoading: false,
    replace: [false, false, false, false],
  }),
  async created() {
    await this.get_group_stage(false);
    this.loading = false;
  },
  methods: {
    async score_changed(match) {
      let matchIndex = this.selectedGroup.matches
        .map((x) => x.id)
        .indexOf(match.id);
      this.selectedGroup.matches = this.selectedGroup.matches
        .slice(0, matchIndex)
        .concat([match])
        .concat(
          this.selectedGroup.matches.slice(
            matchIndex + 1,
            this.selectedGroup.length
          )
        );
      // Setting the replace flag to true to update de matchups for the next stage
      if (this.currentGroupIndex != 3) {
        this.replace[this.currentGroupIndex + 1] = true;
      }
      if (this.currentGroupIndex == 0) {
        await this.get_table(this.selectedGroup.id);
      }
      this.registerScoreDialog = false;
    },
    async next_stage_click() {
      this.groupLoading = true;
      this.currentGroupIndex += 1;
      switch (this.currentGroupIndex) {
        case 1:
          await this.get_wildcard(this.replace[this.currentGroupIndex]);
          break;
        case 2:
          await this.get_semis(this.replace[this.currentGroupIndex]);
          break;
        case 3:
          await this.get_final(this.replace[this.currentGroupIndex]);
          break;
      }
      this.replace[this.currentGroupIndex] = false;
      this.groupLoading = false;
    },
    async previous_stage_click() {
      this.groupLoading = true;
      this.currentGroupIndex -= 1;
      switch (this.currentGroupIndex) {
        case 0:
          await this.get_group_stage(false);
          break;
        case 1:
          await this.get_wildcard(false);
          break;
        case 2:
          await this.get_semis(false);
          break;
      }
      this.groupLoading = false;
    },
    get_match(match) {
      this.currentMatch = JSON.parse(JSON.stringify(match));
      this.registerScoreDialog = true;
    },
    async reset_matches_click() {
      await this.get_group_stage(true);
      this.replace = [false, false, false, false];
      this.currentGroupIndex = 0;
      this.resetConfirmationDialog = false;
    },
    async get_group_stage() {
      await this.$axios
        .post(`group-stage`, { replace })
        .then((response) => {
          this.selectedGroup = response.data;
        });
      if ((this.table.length == 0 || replace) && this.selectedGroup.id) {
        await this.get_table(this.selectedGroup.id);
      }
    },
    async get_table(id) {
      await this.$axios
        .get(`table/${id}`)
        .then((response) => {
          this.table = response.data;
        });
    },
    async get_wildcard(replace) {
      await this.$axios
        .post("wildcards", { replace })
        .then((response) => {
          this.selectedGroup = response.data;
        });
    },
    async get_semis(replace) {
      await this.$axios
        .post("semis", { replace })
        .then((response) => {
          this.selectedGroup = response.data;
          this.final = false;
        });
    },
    async get_final(replace) {
      await this.$axios
        .post("final", { replace })
        .then((response) => {
          this.selectedGroup = response.data;
          this.final = true;
        });
    },
    async generate_champz_file() {
      this.champzFileLoading = true;
      await this.$axios.post("end-champz");
      this.champzFileLoading = false;
    },
  },
};