<template>
    <v-data-table
        :headers="headers"
        :items="challenges"
        :items-per-page="5"
        class="elevation-0"
        style="background-color: #222327"
    >
        <template v-slot:item.description="{ item }">
            {{ truncate(item.description) }}
        </template>
        <template v-slot:item.startDate="{ item }">
            <v-icon dark>
                mdi-calendar-today
            </v-icon>
            {{ formatDate(item.startDate) }}
        </template>
        <template v-slot:item.actions="{ item }">
            <v-dialog v-model="kataDialog[item.id]" max-width="900px" content-class="elevation-0">
                <template v-slot:activator="{ on: menu, attrs }">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                            <v-icon
                                small
                                class="mr-2"
                                v-bind="attrs"
                                v-on="{ ...tooltip, ...menu }"
                            >
                                mdi-script
                            </v-icon>
                        </template>
                        <span>Manage challenge's katas</span>
                    </v-tooltip>
                </template>
                <KataList :challenge="item"></KataList>
            </v-dialog>

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
                        <span>Edit challenge</span>
                    </v-tooltip>
                </template>
                <ChallengeForm text="Edit challenge" :opened="editDialog[item.id]" v-on:close="closeEdit(item)" v-on:save="editChallenge"
                               :challenge="serializeChallenge(item)" :loading="editLoading"></ChallengeForm>
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
                        <span>Delete challenge</span>
                    </v-tooltip>
                </template>

                    <v-sheet
                        width="300px"
                        class="px-7 pt-7 pb-4 mx-auto text-center"
                        dark
                    >
                        <div class="grey--text text--lighten-1 text-body-2 mb-4">
                            Are you sure you want to delete this challenge ?
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
                            @click="deleteChallenge(item)">
                            Delete
                        </v-btn>
                    </v-sheet>
            </v-dialog>
        </template>
    </v-data-table>
</template>

<script>
import {DateTime} from "luxon";
import axios from "axios";
import ChallengeForm from "@/components/Panel/Challenge/ChallengeForm";
import KataList from "@/components/Panel/Challenge/KataList";

export default {
    name: 'TableChallenge',
    components: {ChallengeForm, KataList},
    props: {
        challenges: {
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
                {text: 'Start Date', value: 'startDate'},
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
        deleteChallenge(item) {
            this.loading = true;
            axios.delete('/api/challenges/' + item.id + "/")
                .then(response => {
                    this.$emit("update", () => {
                        this.loading = false;
                        this.$emit("snackbar", "Challenge deleted");
                    });
                })
                .catch(error => {
                    this.loading = false;
                    console.log(error);
                });
        },
        editChallenge(item) {
            if (item.name === '' || item.description === '' || item.startDate === null || item.startTime === null) {
                return;
            }
            this.editLoading = true;
            let hour = item.startTime.split(":")[0];
            let minute = item.startTime.split(":")[1];
            let dateTime = DateTime.fromISO(item.startDate).set({hour, minute}).toISO();
            axios.put('/api/challenges/' + item.id + '/', {
                name: item.name,
                description: item.description,
                startDate: dateTime,
            }).then(response => {
                this.$emit("update", () => {
                    this.editDialog[item.id] = false;
                    this.editLoading = false;
                    this.$emit("snackbar", "Challenge updated");
                });
            }).catch(error => {
                console.log(error);
            });

        },
        serializeChallenge(challenge) {
            let date = DateTime.fromISO(challenge.startDate);
            let hours = date.hour.toString().padStart(2, '0');
            let minutes = date.minute.toString().padStart(2, '0');
            let time = hours + ":" + minutes;
            let startDate = date.toFormat("yyyy-MM-dd");
            return {
                id: challenge.id,
                name: challenge.name,
                description: challenge.description,
                startDate: startDate,
                startTime: time
            };
        },
    }
}
</script>