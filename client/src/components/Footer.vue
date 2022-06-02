<template>
  <v-footer
    dark
    padless
  >
    <v-card
      flat
      tile
      width="100%"
      class="py-1 lighten-1 white--text text-center"
    >
      <v-card-text class="py-2">
        <v-btn
          v-for="icon in icons"
          :key="icon.icon"
          class="mx-4 white--text"
          icon
          :href="icon.link"
        >
          <v-icon size="24px">
            {{ icon.icon }}
          </v-icon>
        </v-btn>
      </v-card-text>


      <v-divider></v-divider>

      <v-card-text class="white--text py-2">
        {{ new Date().getFullYear() }} — <strong>Epiwars </strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>


<script>
  export default {
    data: () => ({
      icons: [
        { icon: 'mdi-linkedin', link: "https://www.linkedin.com/in/frobot/" },
        { icon: 'mdi-github', link: "https://github.com/KatsuKumi/Epiwars" },
      ],
    }),
  }

</script>