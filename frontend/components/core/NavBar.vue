<template>
  <div id="nav">
    <nuxt-link :class="{active: $route.path == '/draft'}" to="/draft">Draft</nuxt-link>
    <nuxt-link :class="{active: $route.path == '/matches'}" to="/matches">Matches</nuxt-link>
  </div>
</template>

<script>
export default {
  
}
</script>

<style scoped>
#nav {
  margin: 0px 0px 20px 0px;
  padding: 8px 0px;
  text-align: center;
  background: white;
}

#nav a {
  text-decoration: none;
  display: inline-block;
  padding: 5px 10px 5px 10px;
  font-size: 20px; line-height: 24px;
  color: #3330E4;
}

#nav a:hover {
  background: #3330E4;
  color: white;
  border-radius: 4px;
}
</style>