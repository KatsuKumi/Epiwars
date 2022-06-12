<template>
    <div class="fill-height">
        <PanelNavigation :selected-item="1"></PanelNavigation>
        <v-container fluid>
            <v-row>
                <v-col cols="12">
                    <h1 class="display-1 text-center">Katas</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                    <v-card class="pa-2 rounded-lg mx-auto my-4" min-height="700" elevation="2"
                            color="#222327">
                        <v-card-title>
                            <span class="headline">Katas</span>
                        </v-card-title>
                        <v-container>
                            <v-row align="center" justify="center" class="px-3">
                                <v-col cols="6">
                                    <v-text-field
                                        v-model="search"
                                        class="pt-0"
                                        append-icon="mdi-magnify"
                                        label="Search"
                                        single-line
                                        hide-details
                                    ></v-text-field>
                                </v-col>
                                <v-col cols="6" class="text-right">
                                    <v-dialog
                                        v-model="createDialog"
                                        persistent
                                        max-width="900px"
                                    >
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-btn
                                                class="mx-2"
                                                dark
                                                outlined
                                                color="indigo"
                                                v-bind="attrs"
                                                v-on="on"
                                            >
                                                <v-icon dark>
                                                    mdi-plus
                                                </v-icon>
                                                Create
                                            </v-btn>
                                        </template>

                                        <KataForm :opened="createDialog" v-on:close="createDialog = false" v-on:save="createKata" :loading="createLoading"></KataForm>
                                    </v-dialog>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <TableKatas :kataDialog="kataDialog"
                                                    :katas="katas"
                                                    :search="search"
                                                    v-on:snackbar="showSnackbar"
                                                    v-on:update="updateKatas"
                                                    v-on:close="kataDialog = false">
                                    </TableKatas>
                                </v-col>
                            </v-row>
                        </v-container>
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
import {DateTime} from "luxon";
import TableKatas from "@/components/Panel/Katas/TableKatas";
import axios from "axios";
import KataForm from "@/components/Panel/Katas/KataForm";

export default {
    name: 'Panel',
    components: {KataForm, PanelNavigation, TableKatas},
    data() {
        return {
            createDialog: false,
            createLoading: false,
            kataDialog: false,
            search: '',
            snackbar: {
                text: '',
                timeout: 3000,
                visible: false,
            },
            katas: [],
        }
    },
    methods: {
        save(date) {
            this.$refs.menu.save(date)
        },
        showSnackbar(text) {
            this.snackbar.text = text;
            this.snackbar.visible = true;
        },
        createKata(item) {
            if (item.name === '' || item.description === '' || item.starter_code === '' || item.test_example === '' || item.test_script === '') {
                return;
            }
            this.createLoading = true;
            axios.post('/api/katas/', item).then(response => {
                this.updateKatas(() => {
                    this.showSnackbar('Kata created');
                    this.createDialog = false;
                    this.createLoading = false;
                });
            }).catch(error => {
                console.log(error);
                this.createLoading = false;
            });
        },
        updateKatas(callback=null) {
            axios.get('/api/katas/').then(response => {
                this.katas = response.data;
                if (callback !== null) {
                    callback();
                }
            }).catch(error => {
                console.log(error);
            });
        }
    },
    mounted() {
        this.$store.commit("hideFooter");
        this.updateKatas();
    },
    watch: {
        menu(val) {
            val && setTimeout(() => (this.activePicker = 'YEAR'))
        },
    },
}
</script>