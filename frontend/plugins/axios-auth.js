export default function ({ $axios, store, redirect }) {
  $axios.onRequest((config) => {
    const token = store.getters['auth/getToken']
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  })

  $axios.onError((error) => {
    if (error.response && error.response.status === 401) {
      store.dispatch('auth/logout')
      redirect('/login')
    }
  })
}
