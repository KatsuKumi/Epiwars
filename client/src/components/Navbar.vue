<template>
    <v-app-bar
        app
        dark
        elevation="0"
        v-if="isAuthenticated"
    >
        <v-img
            :src="$store.state.auth.user.avatar"
            lazy-src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAQAAAC0NkA6AAAALElEQVR42u3NMQEAAAwCoNm/9DL4eEEBcgORSCQSiUQikUgkEolEIpFIJJ0HCt8AM0IRFnUAAAAASUVORK5CYII="
            class="mx-4 rounded-circle"
            elevation="1"
            max-height="50" contain
            max-width="50"
        ></v-img>
        <div>
            <span><b>{{ $store.state.auth.user.email }}</b></span>
            <v-spacer></v-spacer>
            <span v-if="$route.name === 'Challenge'">Score : <b>{{ $store.state.auth.user.score }}</b></span>
        </div>
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
    props: {
        showScore: {
            type: Boolean,
            default: false
        }
    },
    data: () => ({
    }),

    mounted() {
    },

    computed: {
        currentRouteName() {
            return this.$route.name;
        },
        isAuthenticated() {
            return this.$store.getters["isAuthenticated"];
        }
    }
}

</script>