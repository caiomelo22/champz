import GeneralServices from "@/services/GeneralServices";
import AddParticipant from "@/components/dialogs/addParticipant/index.vue";
import BuyPlayer from "@/components/dialogs/buyPlayer/index.vue";
import ParticipantTeam from "@/components/dialogs/participantTeam/index.vue";
export default {
    name: "Draft",
    components: { AddParticipant, BuyPlayer, ParticipantTeam },
    data: () => ({
        gs: new GeneralServices(),
        tab: 0,
        addParticipantDialog: false,
        buyPlayerDialog: false,
        participantTeamDialog: false,
        participants: [],
        genericBudget: 250,
        positions: [],
        selectedPosition: [],
        teams: [],
        playersLoading: false,
        participantsLoading: false,
        currentPlayer: null,
        currentParticipant: {},
        selectedTeam: null,
        newParticipant: { name: null, budget: null, team: null },
    }),
    watch: {
        participantTeamDialog() {
            if (!this.participantTeamDialog) {
                this.selectedTeam = [];
            }
        },
        tab() {
            this.get_players_by_position_algorithm(this.positions[this.tab].id);
        },
    },
    async created() {
        await this.get_participants();
        await this.get_most_popular_teams();
        await this.get_positions();
    },
    methods: {
        reset_player_modal() {
            this.currentPlayer = null;
            this.buyPlayerDialog = false;
        },
        reset_participant_dialog() {
            this.newParticipant = null;
            this.addParticipantDialog = false;
        },
        participant_added(participant) {
            if (!this.newParticipant.id) {
                this.participants.push(participant);
                this.reset_participant_dialog();
                this.get_players_by_position_algorithm(this.positions[this.tab].id);
            } else {
                let index = this.participants
                    .map((x) => x.id)
                    .indexOf(this.newParticipant.id);
                this.participants = this.participants
                    .slice(0, index)
                    .concat([participant])
                    .concat(
                        this.participants.slice(index + 1, this.participants.length)
                    );
                this.addParticipantDialog = false;
                this.get_players_by_position_algorithm(this.positions[this.tab].id);
            }
            const plTeamIndex = this.teams.map(x => x.name).indexOf(participant.team_name)
            this.teams[plTeamIndex].participant_id = participant.id
        },
        get_participant_name(id) {
            if (!id) {
                return null;
            }
            let participants_filtered = this.participants.filter(x => x.id == id);
            if (!participants_filtered.length) {
                return null
            }
            return participants_filtered[0].name;
        },
        open_participant_dialog(participant) {
            if (!participant) {
                this.newParticipant = { name: null, budget: this.genericBudget, team: null };
            } else {
                this.newParticipant = { ...participant };
            }
            this.addParticipantDialog = true;
        },
        async get_participants() {
            this.participantsLoading = true;
            await this.$axios
                .get("participant/list")
                .then((response) => {
                    this.participants = response.data;
                });
            this.participantsLoading = false;
        },
        async get_positions() {
            this.playersLoading = true;
            await this.$axios
                .get("position/list")
                .then((response) => {
                    this.positions = response.data;
                    this.get_players_by_position_algorithm(this.positions[0].id);
                });
        },
        async get_players_by_position_algorithm(idPosition) {
            this.playersLoading = true;
            await this.$axios
                .get(`player/list?position=${idPosition}`)
                .then((response) => {
                    this.selectedPosition = response.data;
                });
            this.playersLoading = false;
        },
        async get_players_by_team(participant, teamName) {
            this.currentParticipant = participant;
            let index = this.participants.map((x) => x.id).indexOf(participant.id);
            this.participants[index].team_loading_att = true;
            await this.$axios
                .get(`player/list?team_participant=${teamName}`)
                .then((response) => {
                    this.selectedTeam = response.data;
                });
            this.participants[index].team_loading_att = false;
            this.participantTeamDialog = true;
        },
        async get_most_popular_teams() {
            await this.$axios
                .get(`team/most-popular`)
                .then((response) => {
                    this.teams = response.data;
                });
        },
        get_player(player) {
            this.currentPlayer = player;
            this.buyPlayerDialog = true;
        },
        async delete_participant(id) {
            let url = `participant/delete/${id}`;
            let index = this.participants.map((x) => x.id).indexOf(id);
            this.participants.splice(index, 1);
            await this.$axios
                .delete(url)
                .then((response) => {
                    this.get_players_by_position_algorithm(this.positions[this.tab].id);
                });
        },
        async remove_buy(player) {
            this.update_participant_budget(player, true);
            await this.$axios
                .post(`player/buy/${player.id}`, { team_participant: null })
                .then((response) => {
                    this.update_player(response.data);
                    if (this.selectedTeam && this.selectedTeam.length > 0) {
                        let index = this.selectedTeam.map((x) => x.id).indexOf(player.id);
                        if (index != -1) {
                            this.selectedTeam.splice(index, 1);
                        }
                    }
                });
        },
        update_participant_budget(player, add) {
            let index = this.participants
                .map((x) => x.team_name)
                .indexOf(player.team_participant);
            if (index != -1) {
                if (add) {
                    this.participants[index].budget += player.value;
                } else {
                    this.participants[index].budget -= player.value;
                }
            }
        },
        update_player(player) {
            console.log(player)
            if (this.positions[this.tab].id == player.position_id) {
                let index = this.selectedPosition.map((x) => x.id).indexOf(player.id);
                this.selectedPosition = this.selectedPosition
                    .slice(0, index)
                    .concat([player])
                    .concat(
                        this.selectedPosition.slice(
                            index + 1,
                            this.selectedPosition.length
                        )
                    );
            }
        },
        player_updated(player) {
            this.update_player(player);
            this.update_participant_budget(player, false);
            this.reset_player_modal()
        },
        async generate_transfers_file() {
            let url = "transfers";
            await this.$axios.post(url);
        },
        async generate_teams_file() {
            let url = "participants_teams";
            await this.$axios.post(url);
        },
        async generate_players_file() {
            let url = "champz_players";
            await this.$axios.post(url);
        },
    },
};