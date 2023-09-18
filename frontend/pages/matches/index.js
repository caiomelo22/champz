import GeneralServices from "@/services/GeneralServices";
import Confirmation from "@/components/dialogs/confirmation/index.vue";
import RegisterScore from "@/components/dialogs/registerScore/index.vue";
import GroupToolbar from "@/components/matches/groupToolbar/index.vue";
export default {
    name: "Matches",
    components: { Confirmation, RegisterScore, GroupToolbar },
    data: () => ({
        gs: new GeneralServices(),
        registerScoreDialog: false,
        resetConfirmationDialog: false,
        group: {},
        table: [],
        matches: {},
        currentMatch: {},
        currentRound: 0,
        previousRounds: {},
        groupStageRound: 0,
        loading: true,
        groupLoading: false,
        registerScoreLoading: false,
    }),
    async created() {
        await this.get_group_stage();
        this.loading = false;
    },
    methods: {
        async score_changed(match) {
            let matchIndex = this.matches[match.round]
                .map((x) => x.id)
                .indexOf(match.id);
            this.matches[match.round][matchIndex] = {
                ...this.matches[match.round][matchIndex],
                goals_1: match.goals_1,
                goals_2: match.goals_2,
            };
            if (this.currentRound == this.groupStageRound) {
                await this.get_table(this.group.id);
            }
            this.registerScoreDialog = false;
        },
        get_round_name() {
            if (this.currentRound == this.groupStageRound) {
                return "Group Stage";
            } else if (this.currentRound == 4) {
                return "Quarter finals";
            } else if (this.currentRound == 2) {
                return "Semi finals";
            } else {
                return "Final";
            }
        },
        async next_stage_click() {
            this.groupLoading = true;
            this.generate_knockouts();
            this.groupLoading = false;
        },
        async previous_stage_click() {
            this.groupLoading = true;
            this.currentRound = this.previousRounds[this.currentRound];
            this.groupLoading = false;
        },
        get_match(match) {
            this.currentMatch = {...match};
            this.registerScoreDialog = true;
        },
        async delete_group(group_id) {
            await this.$axios.delete(`group/delete/${group_id}`);
        },
        async reset_matches_click() {
            this.resetConfirmationDialog = false;
            this.loading = true;
            await this.delete_group(this.group.id);
            await this.create_group_stage();
            await this.get_group_stage();
            this.loading = false;
        },
        async create_group_stage() {
            await this.$axios
            .post(`group/create`)
            .then((create_response) => {
                const group_id = create_response.data;
                this.group = { id: group_id };
            });
        },
        async get_group_stage() {
            await this.$axios
                .get(`group/get`)
                .then((response) => {
                    this.group = response.data;
                })
                .catch(async () => {
                    await this.create_group_stage();
                });
            await this.get_table(this.group.id);
            const num_participants = this.table.length;
            this.groupStageRound = (num_participants * (num_participants - 1)) / 2;
            this.currentRound = this.groupStageRound;
            this.previousRounds[this.currentRound] = null;
            await this.get_matches(this.group.id, this.groupStageRound);
        },
        async get_matches(group_id, round) {
            await this.$axios
                .get(`group/matches/${group_id}?round=${round}`)
                .then((response) => {
                    this.matches[round] = response.data;
                });
        },
        async get_table(id) {
            await this.$axios
                .get(`group/table/${id}`)
                .then((response) => {
                    this.table = response.data;
                });
        },
        async generate_knockouts() {
            const body = {
                group_id: this.group.id,
                previous_round: this.currentRound
            }
            await this.$axios
                .post("group/generate-knockout", body)
                .then(async (response) => {
                    const round_generation = response.data;
                    this.previousRounds[round_generation['round']] = this.currentRound;
                    if (round_generation['generated'] || !(round_generation['round'] in this.matches)) {
                        await this.get_matches(this.group.id, round_generation['round']);
                    }
                    this.currentRound = round_generation['round'];
                });
        },
    },
};