<template>
    <div>
        <v-card class="ma-9 elevation-9">
            <v-card-title>
                <span class="headline">Add new kata to challenge</span>
            </v-card-title>
            <v-card-text>
                <div class="d-flex">
                    <v-select
                        class="pt-5 mr-5"
                        :items="filterDuplicates"
                        v-model="selectedKata"
                        label="New kata"
                        item-text="name"
                        outlined
                        return-object
                    ></v-select>
                    <v-btn class="mt-7 mr-5" dark large width="150px" @click="addKata('start')">Add to top</v-btn>
                    <v-btn class="mt-7" dark large width="150px" @click="addKata('end')">Add to end</v-btn>
                </div>
                <small>You have to create katas before adding them to challenges</small>
            </v-card-text>
        </v-card>
        <v-card :loading="loading" class="elevation-9 ma-9">
            <v-card-title>
                <span class="text-h5 py-5">Katas management</span>
            </v-card-title>
            <v-card-text>
                <v-data-table
                    :headers="headers"
                    :items="itemsWithIndex"
                    :items-per-page="5"
                    class="elevation-0"
                >
                    <template v-slot:item.actions="{ item }">
                        <v-icon
                            small
                            class="mr-2"
                            v-on="{ ...tooltip }"
                            :disabled="loading"
                            @click="moveUp(item)"
                        >
                            mdi-arrow-up
                        </v-icon>
                        <v-icon
                            small
                            class="mr-2"
                            v-on="tooltip"
                            :disabled="loading"
                            @click="moveDown(item)"
                        >
                            mdi-arrow-down
                        </v-icon>

                        <v-tooltip bottom>
                            <template v-slot:activator="{ on: tooltip }">
                                <v-icon
                                    small
                                    class="mr-2"
                                    v-on="tooltip"
                                    :disabled="loading"
                                    @click="removeKata(item)"
                                >
                                    mdi-delete
                                </v-icon>
                            </template>
                            <span>Delete this katas from this challenge</span>
                        </v-tooltip>
                    </template>
                </v-data-table>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'KataList',
    components: {},
    props: {
        challenge: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            selectedKata: null,
            loading: false,
            search: '',
            allKatas: [],
            katas: [],

            headers: [
                {
                    text: '#',
                    align: 'start',
                    sortable: true,
                    filterable: false,
                    value: 'index',
                },
                {text: 'Name', value: 'name'},
                {text: 'Actions', value: 'actions', sortable: false}
            ],
        }
    },
    methods: {
        addKata(position) {
            if (!this.selectedKata) {
                return;
            }
            this.loading = true;
            console.log(this.selectedKata);
            axios.put(`/api/challenges/${this.challenge.id}/katas/${this.selectedKata.id}/`, {
                position: position,
            }).then(response => {
                this.loading = false;
                this.katas = response.data;
                this.selectedKata = null;
                this.refreshAll();
            }).catch(error => {
                this.loading = false;
                console.log(error);
            });
        },
        move(item, direction) {
            this.loading = true;
            axios.post(`/api/challenges/${this.challenge.id}/katas/${item.id}/`,
                {
                    direction: direction,
                })
                .then(response => {
                    this.katas = response.data;
                    this.loading = false;
                })
                .catch(error => {
                    this.loading = false;
                    console.log(error);
                });
        },
        removeKata(item) {
            this.loading = true;
            axios.delete(`/api/challenges/${this.challenge.id}/katas/${item.id}/`)
                .then(response => {
                    this.katas = response.data;
                    this.loading = false;
                })
                .catch(error => {
                    this.loading = false;
                    console.log(error);
                });
        },
        moveUp(item) {
            this.move(item, 'up');
        },
        moveDown(item) {
            this.move(item, 'down');
        },
        refreshAll() {
            axios.get('/api/katas/')
                .then(response => {
                    this.allKatas = response.data;
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    computed: {
        filterDuplicates() {
            return this.allKatas.filter(item => {
                return !this.katas.find(kata => kata.id === item.id);
            });
        },
        itemsWithIndex: {
          get() {
              return this.katas.map((item, index) => {
                  return {
                      ...item,
                      index: index + 1,
                  }
              })
          },
      }
    },
    mounted() {
        axios.get('/api/challenges/' + this.challenge.id + '/katas/')
            .then(response => {
                this.katas = response.data;
            })
            .catch(error => {
                console.log(error);
            });
        this.refreshAll();
    }
}
</script>