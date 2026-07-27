export const state = () => ({
  user: null,
  token: null,
})

export const getters = {
  isAuthenticated(state) {
    return !!state.token
  },
  getUser(state) {
    return state.user
  },
  getToken(state) {
    return state.token
  },
}

export const mutations = {
  SET_USER(state, user) {
    state.user = user
  },
  SET_TOKEN(state, token) {
    state.token = token
  },
  LOGOUT(state) {
    state.user = null
    state.token = null
  },
}

export const actions = {
  async login({ commit, dispatch }, { email, password }) {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)

    const response = await this.$axios.post('auth/jwt/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const token = response.data.access_token
    commit('SET_TOKEN', token)
    this.$cookies.set('auth_token', token, {
      path: '/',
      maxAge: 60 * 60 * 24,
    })

    await dispatch('fetchUser')
  },

  async register(_, { email, password }) {
    await this.$axios.post('auth/register', { email, password })
  },

  async fetchUser({ commit, state }) {
    try {
      const response = await this.$axios.get('users/me', {
        headers: { Authorization: `Bearer ${state.token}` },
      })
      commit('SET_USER', response.data)
    } catch {
      commit('LOGOUT')
    }
  },

  async initAuth({ commit, dispatch }) {
    const token = this.$cookies.get('auth_token')
    if (token) {
      commit('SET_TOKEN', token)
      await dispatch('fetchUser')
    }
  },

  logout({ commit }) {
    commit('LOGOUT')
    this.$cookies.remove('auth_token')
  },
}
