<template>
  <v-card class="pa-2 rounded-lg mx-auto my-10" max-width="320" elevation="1"
    color="#222327">
    <v-img class="mx-auto my-5" src="../assets/testlogo.png" max-height="100" max-width="100"
    lazy-src="" transition="scale-transition"></v-img>
    <p class="text-center text-h5 mb-5 text--secondary custom-font">Epiwars</p>
    <v-divider></v-divider>
      <v-alert
          v-if="error !== ''"
          class="mt-2"
        dense
        outlined
        type="error"
  >
        {{ error }}
  </v-alert>
    <v-row align="center">
      <v-btn
          :loading="loading"
          :disabled="loading"
          class="white--text my-7 mx-auto no-uppercase"
          elevation="0"
          @click="loading = true">
        <v-icon left dark>
          mdi-github
        </v-icon>
        Sign in with GitHub
      </v-btn>
    </v-row>
    <v-divider></v-divider>
    <p class="text-center text-body-2 my-5 text--secondary">Only Epitech students can sign in on Epiwars</p>
    <p class="text-center text-body-2 my-5 text--secondary">The project is open source, don't hesitate to take a look on our <a href="https://github.com/KatsuKumi/Epiwars">Github</a></p>

  </v-card>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      error: ""
    }
  },
  created() {
    if ("error" in this.$route.query) {
      if (this.$route.query.error === "notek") {
          this.error = "Your github account is not valid, please use a Github account with a linked Epitech email";
      } else {
          this.error = "An error occurred during sign in, please try again.";
      }
    }
  },
  watch: {
    loading() {
      setTimeout(() => {
            window.location.href = '/login';
        }, 1500)
    },
  },
}
</script>

<style>

.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}

@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
.no-uppercase {
     text-transform: unset !important;
}
</style>