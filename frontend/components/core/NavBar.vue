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
  margin: 0px 0px 24px 0px;
  padding: 0;
  text-align: center;
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(100, 116, 139, 0.3);
  display: inline-flex;
  width: auto;
  margin-left: 50%;
  transform: translateX(-50%);
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
</style>