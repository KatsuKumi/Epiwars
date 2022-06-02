<template>
    <v-app-bar
        app
        dark
        elevation="0"
        v-if="isAuthenticated"
    >
        <v-toolbar-title>Homepage</v-toolbar-title>
        <v-spacer></v-spacer>
        <span>Logged as : <b>{{ $store.state.auth.user.email }}</b></span>

        <v-spacer></v-spacer>

        <v-btn
            href="/logout"
            text>
            <span class="mr-2">Logout</span>
            <v-icon>mdi-open-in-new</v-icon>
        </v-btn>
    </v-app-bar>
</template>

<script>
import axios from 'axios';

export default {
    data: () => ({
    }),

    mounted() {
    },

    computed: {
        isAuthenticated() {
            return this.$store.getters["isAuthenticated"];
        }
    }
}

</script>