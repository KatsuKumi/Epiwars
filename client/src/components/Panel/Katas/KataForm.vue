<template>
    <v-card :loading="loading">
        <v-card-title>
            <span class="text-h5 py-5">{{ text }}</span>
        </v-card-title>
        <v-card-text>
            <v-form lazy-validation ref="form" v-model="valid"
                    lazy-validation>
                <v-text-field :rules="requiredRule" label="Name" required outlined
                              v-model="newKata.name"
                ></v-text-field>
                <v-textarea :rules="requiredRule" required outlined
                            v-model="newKata.description">
                    <template v-slot:label>
                        <div>
                            Description (Markdown supported)
                        </div>
                    </template>
                </v-textarea>
                <CodeEditor title="Base code" status="" :code="newKata.starter_code" :submit-event="dataSubmit" height="230px" v-on:editCode="editStarter"></CodeEditor>
                <CodeEditor title="Example test code" status="" :code="newKata.test_example" :submit-event="dataSubmit" height="230px" v-on:editCode="editExample"></CodeEditor>
                <CodeEditor title="Server side validation tests" status="" :code="newKata.test_script" :submit-event="dataSubmit" height="230px" v-on:editCode="editScript"></CodeEditor>
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
                @click="createKata"
            >
                Save
            </v-btn>
        </v-card-actions>
    </v-card>
</template>
<script>
import CodeEditor from "@/components/CodeEditor";
export default {
    components: {CodeEditor},
    props: {
        text: {
            type: String,
            default: 'New kata'
        },
        loading: {
            type: Boolean,
            default: false
        },
        opened: {
            type: Boolean,
            default: false
        },
        kata: {
            type: Object,
            default: () => ({
                id: null,
                name: '',
                description: '',
                starter_code: '',
                test_example: '',
                test_script: ''
            }),
        }
    },
    data() {
        return {
            newKata: {
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
        this.newKata = Object.assign({}, this.kata);
    },
    methods: {
        editStarter(code) {
            this.newKata.starter_code = code;
        },
        editExample(code) {
            this.newKata.test_example = code;
        },
        editScript(code) {
            this.newKata.test_script = code;
        },
        createKata() {
            this.valid = this.$refs.form.validate();
            if (this.valid) {
                this.$emit('save', this.newKata);
            }
        },
        dataSubmit() {
        },
    }
}
</script>