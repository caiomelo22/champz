import DialogHeader from "@/components/dialogs/DialogHeader.vue";
export default {
  name: 'ConfirmationDialog',
  components: { DialogHeader },
  props: {
    text: String
  },
}