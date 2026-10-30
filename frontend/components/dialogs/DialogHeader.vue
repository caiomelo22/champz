<template>
  <v-card-title class="dialog-header">
    <div v-if="icon" class="icon-wrapper" :class="`icon-wrapper--${color}`">
      <v-icon color="white" size="18">{{ icon }}</v-icon>
    </div>
    <h3 class="dialog-title">{{ title }}</h3>
    <slot />
    <v-btn icon small aria-label="Close" class="close-button" @click="$emit('close')">
      <v-icon size="20">mdi-close</v-icon>
    </v-btn>
  </v-card-title>
</template>

<script>
export default {
  name: 'DialogHeader',
  props: {
    title: { type: String, required: true },
    icon: { type: String, default: null },
    color: { type: String, default: 'primary', validator: value => ['primary', 'warning', 'danger'].includes(value) },
  },
}
</script>

<style scoped>
.dialog-header {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  gap: 12px;
  padding: 14px 12px 14px 20px !important;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
  border-bottom: 1px solid rgba(100, 116, 139, 0.3);
  border-top-left-radius: inherit;
  border-top-right-radius: inherit;
}

.icon-wrapper {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  padding: 7px;
  border-radius: 10px;
}

.icon-wrapper--primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.35);
}

.icon-wrapper--warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 3px 10px rgba(245, 158, 11, 0.35);
}

.icon-wrapper--danger {
  background: linear-gradient(135deg, #ef4444, #b91c1c);
  box-shadow: 0 3px 10px rgba(239, 68, 68, 0.35);
}

.dialog-title {
  flex: 1;
  min-width: 0;
  margin: 0;
  overflow: hidden;
  color: rgba(226, 232, 240, 0.95);
  font-family: 'DM Sans', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1.3;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.close-button {
  flex-shrink: 0;
  margin-left: auto;
  color: #94a3b8 !important;
}

.close-button:hover {
  color: #f1f5f9 !important;
}
</style>
