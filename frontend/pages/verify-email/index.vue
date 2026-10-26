<template>
  <div class="verify-container">
    <div class="verify-panel">
      <v-progress-circular v-if="status === 'loading'" indeterminate color="#3b82f6" size="48" />
      <v-icon v-else-if="status === 'success'" color="#10b981" size="56">mdi-check-circle-outline</v-icon>
      <v-icon v-else color="#ef4444" size="56">mdi-alert-circle-outline</v-icon>

      <h1>{{ title }}</h1>
      <p>{{ message }}</p>
      <v-btn v-if="status !== 'loading'" color="primary" to="/login">Continue to sign in</v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VerifyEmail',
  layout: 'blank',
  data() {
    return {
      status: 'loading',
      message: 'Confirming your email address...',
    }
  },
  computed: {
    title() {
      if (this.status === 'success') return 'Email verified'
      if (this.status === 'error') return 'Verification failed'
      return 'Verifying email'
    },
  },
  async mounted() {
    const token = this.$route.query.token
    if (!token) {
      this.status = 'error'
      this.message = 'The verification link is incomplete.'
      return
    }

    try {
      await this.$store.dispatch('auth/verifyEmail', token)
      this.status = 'success'
      this.message = 'Your account is ready. Any pending championships are now linked.'
    } catch (error) {
      this.status = 'error'
      const detail = error.response && error.response.data && error.response.data.detail
      this.message = detail === 'VERIFY_USER_ALREADY_VERIFIED'
        ? 'This email address has already been verified.'
        : 'This verification link is invalid or has expired. Request a new link from the sign-in page.'
    }
  },
}
</script>

<style scoped>
.verify-container {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

.verify-panel {
  width: min(440px, 100%);
  padding: 40px;
  border: 1px solid rgba(100, 116, 139, 0.3);
  border-radius: 8px;
  background: rgba(30, 41, 59, 0.92);
  color: rgba(226, 232, 240, 0.95);
  text-align: center;
}

.verify-panel h1 {
  margin: 20px 0 8px;
  font-size: 28px;
}

.verify-panel p {
  margin-bottom: 24px;
  color: rgba(203, 213, 225, 0.8);
}
</style>