<template>
    <v-card :loading="loading">
        <v-card-title>
            <span class="text-h5 py-5">{{ text }}</span>
        </v-card-title>
        <v-card-text>
            <v-form lazy-validation ref="form" v-model="valid"
                    lazy-validation>
                <v-text-field :rules="requiredRule" label="Name" required outlined
                              v-model="newChallenge.name"
                ></v-text-field>
                <v-textarea :rules="requiredRule" required outlined
                            v-model="newChallenge.description">
                    <template v-slot:label>
                        <div>
                            Description
                        </div>
                    </template>
                </v-textarea>
                <v-menu
                    ref="menu"
                    v-model="menu"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            :rules="requiredRule"
                            v-model="newChallenge.startDate"
                            label="Start date"
                            prepend-icon="mdi-calendar"
                            readonly
                            outlined
                            v-bind="attrs"
                            v-on="on"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        :rules="requiredRule"
                        v-model="newChallenge.startDate"
                        year-icon="mdi-calendar-blank"
                        prev-icon="mdi-skip-previous"
                        next-icon="mdi-skip-next"
                        :active-picker.sync="activePicker"
                        min="1950-01-01"
                    ></v-date-picker>
                </v-menu>

                <v-menu
                    ref="menu"
                    v-model="timeMenu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    :return-value.sync="newChallenge.startTime"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="290px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            :rules="requiredRule"
                            v-model="newChallenge.startTime"
                            label="Start time"
                            prepend-icon="mdi-clock-time-four-outline"
                            readonly
                            outlined
                            v-bind="attrs"
                            v-on="on"
                        ></v-text-field>
                    </template>
                    <v-time-picker
                        v-if="timeMenu"
                        v-model="newChallenge.startTime"
                        format="24hr"
                        scrollable
                        full-width
                        @click:minute="$refs.menu.save(newChallenge.startTime)"
                    ></v-time-picker>
                </v-menu>
            </v-form>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="blue darken-1"
                text
                @click="$emit('close');"
            >
                Close
            </v-btn>
            <v-btn
                color="blue darken-1"
                text
                @click="createChallenge"
            >
                Save
            </v-btn>
        </v-card-actions>
    </v-card>
</template>
<script>
export default {
    props: {
        text: {
            type: String,
            default: 'New challenge'
        },
        loading: {
            type: Boolean,
            default: false
        },
        opened: {
            type: Boolean,
            default: false
        },
        challenge: {
            type: Object,
            default: () => ({
                id: null,
                name: '',
                description: '',
                startDate: null,
                startTime: null,
            }),
        }
    },
    data() {
        return {
            newChallenge: {
                id: null,
                name: "",
                description: "",
                startDate: "",
                startTime: "",
            },
            valid: false,
            requiredRule: [
                v => !!v || "This field is required"
            ],
            menu: false,
            timeMenu: false,
            activePicker: null
        }
    },
    mounted() {
        this.newChallenge = Object.assign({}, this.challenge);
    },
    methods: {
        createChallenge() {
            this.valid = this.$refs.form.validate();
            if (this.valid) {
                this.$emit('save', this.newChallenge);
            }
        }
    }
}
</script>