<template>
  <v-app class="app">
    <Main class="main">
      <NavBar />
      <Nuxt />
    </Main>
    <Footer />
  </v-app>
</template>
<script>
import Footer from "@/components/core/Footer";
import Main from "@/components/core/Main";
import NavBar from "@/components/core/NavBar";
export default {
  components: {
    Footer,
    Main,
    NavBar
  }
};
</script>
<style scoped>
.app {
  background: transparent;
  min-height: 100vh;
}
.main {
  margin-bottom: 12px;
  padding: 20px;
  background: transparent;
}
</style>