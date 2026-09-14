export default function ({ store, redirect, route }) {
  const publicPaths = ['/login', '/verify-email']
  if (publicPaths.includes(route.path)) {
    return
  }
  if (!store.getters['auth/isAuthenticated']) {
    return redirect('/login')
  }
}
