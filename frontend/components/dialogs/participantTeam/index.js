import GeneralServices from "@/services/GeneralServices.js";

export default {
  name: 'ParticipantTeamDialog',
  props: {
    currentParticipant: Object,
    selectedTeam: Array
  },
  data() {
    return {
      gs: new GeneralServices(),
    };
  },
}