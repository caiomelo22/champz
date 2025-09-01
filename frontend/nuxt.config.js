export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Champz',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', type: 'text/css', href: 'https://use.fontawesome.com/releases/v5.8.1/css/all.css' },
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/style.css',
    '@/assets/transition.css'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/bootstrap.js',
    '@/plugins/iview.js',
    '@/plugins/animate.js',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    '@nuxtjs/google-fonts',
    '@nuxtjs/eslint-module',
    '@nuxtjs/moment',
    '@nuxtjs/fontawesome',
    '@nuxtjs/dotenv',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    'cookie-universal-nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/vuetify',
    "vue-toastification/nuxt"
  ],

  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: process.env.VUE_APP_BASE_URL
  },

  vuetify: {
    theme: {
      themes: {
        light: {
          primary: 'rgba(203, 213, 225, 0.95)',
        }
      }
    }
  },

  googleFonts: {
    families: {
        Inter: [100, 200, 300, 400, 500, 600, 700, 800, 900],
        'DM Sans': [100, 200, 300, 400, 500, 600, 700, 800, 900],
        Poppins: [100, 200, 300, 400, 500, 600, 700]
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },

  router: {
    extendRoutes(routes, resolve) {
      // Add redirect from root to draft
      routes.push({
        path: '/',
        redirect: '/draft'
      })
    }
  }
}
