export const state = () => ({
  msg: 'Message in store'
})

export const getters = {
  get_message(state) {
    return state.msg;
  }
}

export const mutations = {
  reset_msg(state, arg) {
    state.msg = arg;
  }
}

export const actions = {
  async nuxtServerInit(store, context) {
    try {
      await store.dispatch('auth/initAuth')
    }
    catch(err) {
      // Auth init failed silently
    }
  }
}