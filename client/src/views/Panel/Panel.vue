<template>
    <div class="fill-height">
        <PanelNavigation :selected-item="0"></PanelNavigation>
        <v-container fluid>
            <v-row>
                <v-col cols="12">
                    <h1 class="display-1 text-center">Dashboard</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="4">
                    <v-card class="pa-2 rounded-lg mx-auto my-4" min-height="700" elevation="2"
                            color="#222327">
                        <v-card-title>
                            <span class="headline">Ranking</span>
                        </v-card-title>
                        <v-divider></v-divider>
                        <v-card-text class="px-2">
                              <v-text-field
                                v-model="search"
                                append-icon="mdi-magnify"
                                label="Search"
                                single-line
                                hide-details
                              ></v-text-field>
                            <v-data-table
                                :headers="headers"
                                :items="ranking"
                                :items-per-page="10"
                                class="elevation-1"
                                :search="search"
                                style="background-color: #222327"
                            >
                                <template v-slot:item.avatar="{ item }">
                                    <div class="p-2">
                                        <v-img
                                            :src="item.avatar"
                                            lazy-src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAQAAAC0NkA6AAAALElEQVR42u3NMQEAAAwCoNm/9DL4eEEBcgORSCQSiUQikUgkEolEIpFIJJ0HCt8AM0IRFnUAAAAASUVORK5CYII="
                                            class="mx-4 rounded-circle"
                                            elevation="1"
                                            max-height="50" contain
                                            max-width="50"
                                        ></v-img>
                                    </div>
                                </template>
                            </v-data-table>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="8">
                    <v-card class="pa-2 rounded-lg mx-auto my-4" min-height="700" elevation="2"
                            color="#222327">
                        <v-card-title>
                            <span class="headline">Challenges</span>
                        </v-card-title>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import PanelNavigation from "@/components/PanelNavigation";
export default {
    name: 'Panel',
    components: {PanelNavigation},
    data() {
        return {

            search: '',
            headers: [
                {
                    text: 'Avatar',
                    align: 'start',
                    sortable: false,
                    filterable: false,
                    value: 'avatar',
                },
                {text: 'Position', value: 'position'},
                {text: 'Username', value: 'username'},
                {text: "Score", value: 'score', filterable: false}
            ],
            ranking: [
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 1,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 2,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 3,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 4,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 5,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 6,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 7,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 8,
                    username: 'John Doe',
                    score: 0
                },
                {
                    avatar: 'https://avatars.githubusercontent.com/u/1857648?v=4',
                    position: 9,
                    username: 'John Doe',
                    score: 0
                }
            ]
        }
    },
    mounted() {
        this.$store.commit("hideFooter");
    }
}
</script>