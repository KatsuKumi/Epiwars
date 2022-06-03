<template>
    <div v-if="Kata != null">
        <v-row>
            <v-col cols="5" class="pl-5">
                <v-tabs rounded="rounded" class="my-5"
                        v-model="tab" background-color="#222327"
                        fixed-tabs centered>
                    <v-tab>Instructions</v-tab>
                    <v-tab>Output</v-tab>
                </v-tabs>
                <v-tabs-items v-model="tab">
                    <v-tab-item key="0" :transition="false">
                        <v-card class="elevation-0 rounded-xl" height="750" color="#222327">
                            <v-card-text>
                                <v-card-text class="text-body-1">
                                    <p>
                                        <strong>{{ Kata.kata }}</strong>
                                    </p>
                                    <div v-html="descriptionToHtml">

                                    </div>
                                </v-card-text>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item key="1" class="rounded" :transition="false">
                        <v-card class="elevation-0 rounded-xl" height="750" outlined>
                            <v-card-text>
                                <v-card-text class="text-body-1">
                                    <p v-html="statusText">
                                    </p>
                                </v-card-text>
                            </v-card-text>
                        </v-card>
                    </v-tab-item>
                </v-tabs-items>
            </v-col>
            <v-col cols="7" class="pr-5">
                <v-sheet
                    class="mx-auto my-5 rounded-t-xl"
                    color="#222327"
                >
                    <div class="d-flex justify-space-between text-subtitle-1 py-3 px-5">
                        <span style="min-width: 70px"></span>
                        <span>Solution</span>
                        <span style="min-width: 70px" class="text-caption text-decoration-underline font-italic text-right">{{ save_text.code }}</span>
                    </div>
                    <AceEditor
                        v-model="Code"
                        @init="editorInit"
                        lang="c_cpp"
                        theme="tomorrow_night"
                        width="100%"
                        height="400px"
                        :options="{
                        enableBasicAutocompletion: true,
                        enableLiveAutocompletion: true,
                        fontSize: 16,
                        highlightActiveLine: true,
                        enableSnippets: true,
                        showLineNumbers: true,
                        tabSize: 4,
                        showPrintMargin: false,
                        showGutter: true,
                        }"
                        :commands="[
                            {
                                name: 'save',
                                bindKey: { win: 'Ctrl-s', mac: 'Command-s' },
                                exec: dataSumit,
                                readOnly: true,
                            },
                        ]"
                    />
                </v-sheet>
                <v-sheet
                    class="mx-auto mt-5 rounded-t-xl"
                    color="#222327"
                >
                    <div class="d-flex justify-space-between text-subtitle-1 py-3 px-5">
                        <span style="min-width: 70px"></span>
                        <span>Sample Tests</span>
                        <span style="min-width: 70px" class="text-caption text-decoration-underline font-italic text-right">{{ save_text.test }}</span>
                    </div>
                    <AceEditor
                        v-model="Example"
                        @init="editorInit"
                        lang="c_cpp"
                        theme="tomorrow_night"
                        width="100%"
                        height="230px"
                        :options="{
                        enableBasicAutocompletion: true,
                        enableLiveAutocompletion: true,
                        fontSize: 16,
                        highlightActiveLine: true,
                        enableSnippets: true,
                        showLineNumbers: true,
                        tabSize: 2,
                        showPrintMargin: false,
                        showGutter: true,
                        }"
                        :commands="[
                            {
                                name: 'save',
                                bindKey: { win: 'Ctrl-s', mac: 'Command-s' },
                                exec: dataSumit,
                                readOnly: true,
                            },
                        ]"
                    />
                </v-sheet>
                <v-col class="text-right">
                    <v-btn class="ma-2" outlined color="indigo" @click="codeTest">
                        Test
                    </v-btn>
                    <v-btn class="ma-2" color="indigo">
                        Attempt
                    </v-btn>
                </v-col>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import {marked} from 'marked'
import HelloWorld from '../components/HelloWorld'
import AceEditor from 'vuejs-ace-editor';
import axios from "axios";

export default {
    name: 'Home',
    data() {
        return {
            tab: 0,
            content: "coco",
            save_text: {
                code: 'Saved',
                test: 'Saved'
            },
            statusText: 'Your results will be shown here.',
        }
    },
    computed: {
        descriptionToHtml() {
            if (this.$store.state.challenge.currentKata === null)
                return null;
            return marked(this.$store.state.challenge.currentKata.description);
        },
        Kata() {
            if (this.$store.state.challenge.currentKata === null)
                return null;
            console.log(this.$store.state.challenge.currentKata);
            return this.$store.state.challenge.currentKata
        },
        Example: {
            get() {
                if (this.$store.state.challenge.currentKata === null)
                    return null;
                return this.$store.state.challenge.currentKata.saved_test
            },
            set(value) {
                this.save_text.test = "Not Saved"
                this.$store.commit("updateExample", value);
            }
        },
        Code: {
            get() {
                if (this.$store.state.challenge.currentKata === null)
                    return null;
                return this.$store.state.challenge.currentKata.saved_code
            },
            set(value) {
                this.save_text.code = "Not Saved"
                this.$store.commit("updateCode", value);
            }
        },
    },
    methods: {
        dataSumit() {
            this.$store.dispatch("saveCode");
            this.save_text.code = "Saving..."
            this.save_text.test = "Saving..."
            setTimeout(() => {
                this.save_text.code = "Saved"
                this.save_text.test = "Saved"
            }, 2000);
        },
        codeTest() {
            this.$store.dispatch("saveCode");
            this.save_text.code = "Saving..."
            this.save_text.test = "Saving..."
            setTimeout(() => {
                this.save_text.code = "Saved"
                this.save_text.test = "Saved"
            }, 2000);
            this.tab = 1;
            this.statusText = "<b>Status:</b> Sending request...";
            axios.post("/api/test/", {
                code: this.Code,
                test: this.Example,
            }).then(res => {
                this.statusText = "<b>Status:</b> " + res.data.status;
            }).catch(err => {
                console.log(err);
                this.statusText = "<b>Status:</b> " + err.message;
            });
        },
        editorInit: function () {
            require('brace/ext/language_tools') //language extension prerequsite...
            require('brace/mode/html')
            require('brace/mode/c_cpp')
            require('brace/mode/javascript')    //language
            require('brace/mode/less')
            require('brace/theme/tomorrow_night')
            require('brace/snippets/javascript') //snippet
            require('brace/snippets/c_cpp') //snippet
        }
    },
    mounted() {
        this.$store.commit("hideFooter");
        this.$store.dispatch("getCurrentKata");
    },
    components: {
        HelloWorld,
        AceEditor
    },
}
</script>

<style>
.theme--dark.v-sheet--outlined {
    border-width: 3px;
}
.v-application .text-caption {
    line-height: 28px;
}

.v-window.v-item-group.theme--dark.v-tabs-items {
    background-color: transparent;
}

.v-tabs {
    border-radius: 10px;
}

pre {
    background-color: rgba(255, 255, 255, 0.1);
    overflow: scroll;
    overflow-y: hidden;
    border-radius: 10px;
    padding: 10px;
}

pre code {
    background-color: transparent !important;
}

p code {
    border-radius: 6px !important;
}
</style>
