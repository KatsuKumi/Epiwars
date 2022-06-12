<template>
    <v-data-table
        :headers="headers"
        :items="katas"
        :items-per-page="5"
        class="elevation-0"
        style="background-color: #222327"
    >
        <template v-slot:item.description="{ item }">
            {{ truncate(item.description) }}
        </template>
        <template v-slot:item.actions="{ item }">
            <v-dialog v-model="editDialog[item.id]" max-width="900px" :retain-focus="false">
                <template v-slot:activator="{ on: menu, attrs }">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-icon
                                small
                                class="mr-2"
                                v-on="{ ...tooltip, ...menu }"
                            >
                                mdi-pencil
                            </v-icon>
                        </template>
                        <span>Edit kata</span>
                    </v-tooltip>
                </template>
                <KataForm text="Edit kata" :opened="editDialog[item.id]" v-on:close="closeEdit(item)" v-on:save="editKata"
                               :kata="item" :loading="editLoading"></KataForm>
            </v-dialog>


            <v-dialog v-model="deleteDialog[item.id]" width="300px" :retain-focus="false">
                <template v-slot:activator="{ on: menu, attrs }">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-icon
                                small
                                v-on="{ ...tooltip, ...menu }"
                            >
                                mdi-delete
                            </v-icon>
                        </template>
                        <span>Delete kata</span>
                    </v-tooltip>
                </template>

                    <v-sheet
                        width="300px"
                        class="px-7 pt-7 pb-4 mx-auto text-center"
                        dark
                    >
                        <div class="grey--text text--lighten-1 text-body-2 mb-4">
                            Are you sure you want to delete this kata ?
                        </div>

                        <v-btn
                            :disabled="loading"
                            class="ma-1"
                            color="grey"
                            plain
                            @click="closeDelete(item)"
                        >
                            Cancel
                        </v-btn>

                        <v-btn
                            :loading="loading"
                            class="ma-1"
                            color="error"
                            plain
                            @click="deleteKata(item)">
                            Delete
                        </v-btn>
                    </v-sheet>
            </v-dialog>
        </template>
    </v-data-table>
</template>

<script>
import {DateTime} from "luxon";
import axios from "axios"
import KataForm from "@/components/Panel/Katas/KataForm";

export default {
    name: 'TableKatas',
    components: {KataForm},
    props: {
        katas: {
            type: Array,
            required: true,
        },
        search: {
            type: String,
            required: true,
        }
    },
    data() {
        return {
            loading: false,
            deleteDialog: [],
            editDialog: [],
            kataDialog: [],
            editLoading: false,
            headers: [
                {
                    text: 'Id',
                    align: 'start',
                    sortable: false,
                    filterable: false,
                    value: 'id',
                },
                {text: 'Name', value: 'name'},
                {text: "Description", value: 'description', width: '400'},
                {text: 'Actions', value: 'actions', sortable: false}
            ],
        }
    },
    methods: {
        truncate(text) {
            return text.length > 100 ? text.substring(0, 100) + '...' : text;
        },
        closeDelete(item) {
            console.log(item);
            console.log(this.deleteDialog);
            this.$set(this.deleteDialog, item.id, false)
            console.log(this.deleteDialog);
        },
        closeEdit(item) {
            this.$set(this.editDialog, item.id, false)
        },
        formatDate(date) {
            return DateTime.fromISO(date).toFormat("dd LLL yyyy HH:mm:ss");
        },
        deleteKata(item) {
            this.loading = true;
            axios.delete('/api/katas/' + item.id + "/")
                .then(response => {
                    this.$emit("update", () => {
                        this.loading = false;
                        this.$emit("snackbar", "Kata deleted");
                    });
                })
                .catch(error => {
                    this.loading = false;
                    console.log(error);
                });
        },
        editKata(item) {
            if (item.name === ''
                || item.description === ''
                || item.starter_code === ''
                || item.test_example === '' ||
                item.test_script === '') {
                return;
            }
            axios.put('/api/katas/' + item.id + '/', item).then(response => {
                this.$emit("update", () => {
                    this.editDialog[item.id] = false;
                    this.editLoading = false;
                    this.$emit("snackbar", "Kata updated");
                });
            }).catch(error => {
                console.log(error);
            });

        },
    }
}
</script>