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
      // const response = await context.$axios.get('https:// ...')
      const response = {data: 'Message via nextServerInit'}
      store.commit('reset_msg', response.data)
    }
    catch(err) {
      context.error({
        message: err.message
      })
    }
  }
}