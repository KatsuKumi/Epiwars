<template>
    <v-card class="pa-2 rounded-lg mx-auto my-10" max-width="320" elevation="1"
    color="#222327">
        <v-img class="mx-auto my-5" src="../assets/testlogo.png" max-height="100" max-width="100"
               lazy-src="" transition="scale-transition"></v-img>
        <div class="text-center text-h5 mb-5 text--secondary custom-font rainbow-text animated">{{ challengeName }}
        </div>
        <div class="text-center text-subtitle-1 mb-5 text--secondary custom-font">{{ challengeDescription }}
        </div>
        <v-divider class="my-2"></v-divider>
        <div v-if="$store.state.challenge.info">
            <p class="text-center text-body-2 my-5 text--secondary">The challenge will start in</p>
            <CountDown v-if="$store.state.challenge.info" :end-date="$store.state.challenge.info.startDate"></CountDown>
            <v-divider class="my-2"></v-divider>
            <v-btn href="/challenge" block color="primary" :disabled="!started">
                Start challenge
            </v-btn>
        </div>
        <div v-else>
            <p class="text-center text-body-2 my-5 text--secondary">No challenge is currently active</p>
        </div>
    </v-card>
</template>

<script>
import CountDown from "@/components/CountDown";
import {DateTime} from "luxon";

export default {
    components: {CountDown},
    data() {
        return {
            timer: null,
            started: false
        }
    },
    computed: {
        startDate() {
            if (this.$store.state.challenge.info === null)
                return null;
            return this.$store.state.challenge.info.startDate
        },
        challengeName() {
            if (this.$store.state.challenge.info === null)
                return null;
            return this.$store.state.challenge.info.name
        },
        challengeDescription() {
            if (this.$store.state.challenge.info === null)
                return null;
            return this.$store.state.challenge.info.description
        }
    },
    created() {
        this.$store.dispatch("refreshCallenge");
    },
    watch: {
        startDate() {
            if (this.startDate != null) {

                const endDateTimeObj = DateTime.fromISO(this.startDate);
                this.timer = setInterval(() => {
                  if (endDateTimeObj < DateTime.now()) {
                      clearInterval(this.timer);
                      this.started = true;
                  }
                }, 1000)
                console.log(this.startDate);
            }
        }
    },
}
</script>

<style>

.theme--dark.v-application .text--secondary.custom-font {
    font-family: EpiFont !important;
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