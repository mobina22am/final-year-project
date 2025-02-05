<template>
  <RouterView/>
</template>

<script>

export default {
  name: 'App',
  components: {
  },

  mounted() {
    const token = localStorage.getItem('token');

    if (token) {
      this.$router.push('/mainpage');
    } 
    
    else {
      this.$router.push('/');
    }
  }
}
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
