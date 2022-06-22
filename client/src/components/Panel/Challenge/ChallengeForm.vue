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
                <datetimepicker label="Select starting date" v-model="newChallenge.startDate"> </datetimepicker>
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
import datetimepicker from '../../DateTimePicker.vue'

export default {
    components: {
        datetimepicker
    },
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
                startDate: Date.now(),
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
        if (this.challenge.id) {
            this.newChallenge = Object.assign({}, this.challenge);
        }
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