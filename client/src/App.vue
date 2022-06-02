<template>
    <v-app id="main" class="scrollbar-hidden"
           :style="{ background: $vuetify.theme.themes['dark'].background }"
    >
        <Navbar></Navbar>
        <v-main>
            <router-view/>
        </v-main>
        <Footer></Footer>
    </v-app>
</template>

<script>
import Navbar from "./components/Navbar";
import Footer from './components/Footer'
import {loadScript} from "vue-plugin-load-script";

loadScript("https://unpkg.com/splitting/dist/splitting.min.js")
    .then(() => {
        Splitting();
    })
    .catch(() => {
        // Failed to fetch script
    });

export default {
    name: 'App',

    created() {
    // watch the params of the route to fetch the data again
    this.$watch(
      () => this.$route.params,
      () => {
        this.$store.dispatch("refreshUser");
      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
    )
    },
    components: {
        Navbar,
        Footer,
    },
}

</script>


<style>
body {
    background-color: rgb(22, 23, 27);
}

html::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge add Firefox */
html {
    -ms-overflow-style: none;
    scrollbar-width: none; /* Firefox */
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

#nav {
    padding: 30px;
}

#nav a {
    font-weight: bold;
    color: #2c3e50;
}

#nav a.router-link-exact-active {
    color: #42b983;
}
</style>
