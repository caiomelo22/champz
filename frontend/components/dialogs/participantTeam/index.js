import DialogHeader from "@/components/dialogs/DialogHeader.vue";
import GeneralServices from "@/services/GeneralServices.js";

export default {
  name: 'ParticipantTeamDialog',
  components: { DialogHeader },
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