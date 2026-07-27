<template>
  <div id="nav-wrapper">
    <div id="nav">
      <template v-if="championshipId">
        <nuxt-link :to="`/championship/${championshipId}/draft`" :class="{active: isDraftPage}">Draft</nuxt-link>
        <nuxt-link :to="`/championship/${championshipId}/matches`" :class="{active: isMatchesPage}">Matches</nuxt-link>
      </template>
      <template v-else-if="isAuthenticated">
        <nuxt-link to="/dashboard" :class="{active: $route.path === '/dashboard'}">Dashboard</nuxt-link>
      </template>
    </div>
    <div v-if="isAuthenticated" class="user-section">
      <span class="user-email">{{ userEmail }}</span>
      <v-btn icon small @click="logout" class="logout-btn">
        <v-icon size="18" color="rgba(203,213,225,0.8)">mdi-logout</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return this.$store.getters['auth/isAuthenticated']
    },
    userEmail() {
      const user = this.$store.getters['auth/getUser']
      return user ? user.email : ''
    },
    championshipId() {
      return this.$route.params.id || null
    },
    isDraftPage() {
      return this.$route.path.includes('/championship/') && this.$route.path.includes('/draft')
    },
    isMatchesPage() {
      return this.$route.path.includes('/championship/') && this.$route.path.includes('/matches')
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
#nav-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
  position: relative;
}

#nav {
  padding: 0;
  text-align: center;
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(100, 116, 139, 0.3);
  display: inline-flex;
}

#nav a {
  text-decoration: none;
  display: inline-block;
  padding: 16px 32px;
  margin: 0;
  font-size: 16px; 
  line-height: 20px;
  color: rgba(226, 232, 240, 0.8);
  border-radius: 50px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  position: relative;
  overflow: hidden;
  min-width: 120px;
  font-family: 'DM Sans', sans-serif;
}

#nav a::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(59, 130, 246, 0.2);
  transition: left 0.3s ease;
  z-index: -1;
  border-radius: 50px;
}

#nav a:hover::before {
  left: 0;
}

#nav a:hover {
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

#nav a.active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.user-section {
  position: absolute;
  right: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-email {
  color: rgba(203, 213, 225, 0.7);
  font-size: 13px;
  font-family: 'DM Sans', sans-serif;
}

.logout-btn {
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(100, 116, 139, 0.3);
}
</style>