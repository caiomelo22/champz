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
  background: #F0EBE3;
}
.main {
  margin-bottom: 12px;
}
</style>