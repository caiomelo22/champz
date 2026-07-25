<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">Champz</h1>
        <p class="login-subtitle">{{ isRegistering ? 'Create your account' : 'Sign in to continue' }}</p>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          outlined
          dark
          dense
          prepend-inner-icon="mdi-email-outline"
          :rules="[v => !!v || 'Email is required']"
          class="login-input"
        />

        <v-text-field
          v-model="password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          outlined
          dark
          dense
          prepend-inner-icon="mdi-lock-outline"
          :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append="showPassword = !showPassword"
          :rules="[v => !!v || 'Password is required']"
          class="login-input"
        />

        <v-text-field
          v-if="isRegistering"
          v-model="confirmPassword"
          label="Confirm Password"
          :type="showPassword ? 'text' : 'password'"
          outlined
          dark
          dense
          prepend-inner-icon="mdi-lock-check-outline"
          :rules="[v => !!v || 'Please confirm your password']"
          class="login-input"
        />

        <v-alert v-if="error" type="error" dense class="mb-4">
          {{ error }}
        </v-alert>

        <v-btn
          type="submit"
          block
          large
          :loading="loading"
          class="login-btn"
          color="primary"
        >
          {{ isRegistering ? 'Create Account' : 'Sign In' }}
        </v-btn>
      </form>

      <div class="divider">
        <span>or</span>
      </div>

      <v-btn
        block
        large
        outlined
        dark
        class="google-btn"
        @click="loginWithGoogle"
      >
        <v-icon left>mdi-google</v-icon>
        Continue with Google
      </v-btn>

      <div class="toggle-mode">
        <span v-if="!isRegistering">
          Don't have an account?
          <a href="#" @click.prevent="isRegistering = true">Sign up</a>
        </span>
        <span v-else>
          Already have an account?
          <a href="#" @click.prevent="isRegistering = false">Sign in</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  layout: 'blank',
  data() {
    return {
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      isRegistering: false,
      loading: false,
      error: null,
    }
  },
  mounted() {
    if (this.$store.getters['auth/isAuthenticated']) {
      this.$router.push('/dashboard')
    }
  },
  methods: {
    async handleSubmit() {
      this.error = null
      this.loading = true

      try {
        if (this.isRegistering) {
          if (this.password !== this.confirmPassword) {
            this.error = 'Passwords do not match.'
            this.loading = false
            return
          }
          await this.$store.dispatch('auth/register', {
            email: this.email,
            password: this.password,
          })
          // Auto-login after registration
          await this.$store.dispatch('auth/login', {
            email: this.email,
            password: this.password,
          })
        } else {
          await this.$store.dispatch('auth/login', {
            email: this.email,
            password: this.password,
          })
        }
        this.$router.push('/dashboard')
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          const detail = err.response.data.detail
          if (typeof detail === 'string') {
            this.error = detail
          } else {
            this.error = 'Invalid credentials. Please try again.'
          }
        } else {
          this.error = 'An error occurred. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
    loginWithGoogle() {
      const baseUrl = process.env.VUE_APP_BASE_URL || 'http://localhost:8000'
      window.location.href = `${baseUrl}/auth/google/authorize`
    },
  },
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: rgba(30, 41, 59, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(100, 116, 139, 0.3);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 8px;
}

.login-subtitle {
  color: rgba(203, 213, 225, 0.8);
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
}

.login-form {
  margin-bottom: 16px;
}

.login-input {
  margin-bottom: 4px;
}

.login-btn {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
  color: white !important;
  font-weight: 600;
  text-transform: none;
  font-size: 16px;
  border-radius: 12px;
  height: 48px !important;
}

.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(100, 116, 139, 0.3);
}

.divider span {
  padding: 0 16px;
  color: rgba(203, 213, 225, 0.6);
  font-size: 13px;
  font-family: 'DM Sans', sans-serif;
}

.google-btn {
  border: 1px solid rgba(100, 116, 139, 0.4) !important;
  color: rgba(226, 232, 240, 0.9) !important;
  text-transform: none;
  font-size: 15px;
  border-radius: 12px;
  height: 48px !important;
  font-weight: 500;
}

.toggle-mode {
  text-align: center;
  margin-top: 24px;
  color: rgba(203, 213, 225, 0.7);
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
}

.toggle-mode a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
}

.toggle-mode a:hover {
  text-decoration: underline;
}
</style>
