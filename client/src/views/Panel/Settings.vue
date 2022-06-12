<template>
    <div>
        <PanelNavigation></PanelNavigation>

        <v-container fluid>
            <v-row>
                <v-col cols="12">
                    <h1 class="display-1 text-center">Settings</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="6" offset="3">
                    <v-card class="pa-2 rounded-lg mx-auto my-4" elevation="2"
                            color="#222327">
                        <v-card-text class="px-6">
                            <v-select
                                v-model="selectedChallenge"
                                :items="challenges"
                                label="Current Challenge"
                                v-on:change="changeChallenge"
                                return-object
                                outlined
                                item-text="name">
                            </v-select>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        <v-snackbar
          v-model="snackbar.visible"
          :timeout="snackbar.timeout"
        >
          {{ snackbar.text }}

          <template v-slot:action="{ attrs }">
            <v-btn
              color="blue"
              text
              v-bind="attrs"
              @click="snackbar.visible = false"
            >
              Close
            </v-btn>
          </template>
        </v-snackbar>
    </div>
</template>

<script>
import PanelNavigation from "@/components/PanelNavigation";
import axios from "axios";

export default {
    name: 'Panel',
    components: {PanelNavigation},
    data() {
        return {
            selectedChallenge: null,
            challenges: [],
            snackbar: {
                text: '',
                timeout: 1000,
                visible: false,
            },
        };
    },
    mounted() {
        this.$store.commit("hideFooter");
        axios.get("/api/challenges/")
            .then(response => {
                this.challenges = response.data;
                this.selectedChallenge = this.challenges.find(challenge => challenge.active);
            })
            .catch(error => {
                console.log(error);
            });
    },
    methods: {
        changeChallenge() {
            axios.post("/api/challenges/active", {
                challenge: this.selectedChallenge.id
            }).then(response => {
                this.snackbar.text = "Challenge changed";
                this.snackbar.visible = true;
            }).catch(error => {
                this.snackbar.text = "Error while changing challenge : " + error.response.data.error;
                this.snackbar.visible = true;
                this.selectedChallenge = this.challenges.find(challenge => challenge.active);
            });
        }
    },
}
</script>