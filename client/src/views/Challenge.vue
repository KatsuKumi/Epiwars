<template>
    <div v-if="Kata != null">
        <v-row>
            <v-col cols="5" class="pl-5">
                <v-tabs rounded="rounded" class="my-5"
                        v-model="tab" background-color="#222327"
                        fixed-tabs centered>
                    <v-tab dark>Instructions</v-tab>
                    <v-tab dark>Output</v-tab>
                </v-tabs>
                <v-tabs-items v-model="tab">
                    <v-tab-item key="0" :transition="false">
                        <Description :name="Kata.kata" :description="Kata.description"></Description>
                    </v-tab-item>
                    <v-tab-item key="1" class="rounded" :transition="false">
                        <Output :output="output"></Output>
                    </v-tab-item>
                </v-tabs-items>
            </v-col>
            <v-col cols="7" class="pr-5">
                <CodeEditor title="Solution" :status="save_text.code" :code="Code" :submit-event="dataSubmit" height="400px" v-on:editCode="editCode"></CodeEditor>
                <CodeEditor title="Sample Tests" :status="save_text.test" :code="Example" :submit-event="dataSubmit" height="230px" v-on:editCode="editExample"></CodeEditor>
                <v-col class="text-right">
                    <v-btn class="ma-2" outlined color="indigo" @click="codeTest">
                        Test
                    </v-btn>
                    <v-btn class="ma-2" color="indigo" @click="codeSubmit">
                        Attempt
                    </v-btn>
                    <v-fab-transition>
                        <v-btn class="ma-2" color="green darken-4" @click="goNext" v-show="showNext">
                            {{ Kata.is_last ? 'Finish' : 'Next' }}
                        </v-btn>
                    </v-fab-transition>
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
import CodeEditor from "@/components/CodeEditor";
import Description from "@/components/Description";
import Output from "@/components/Output";


String.prototype.isEmpty = function () {
    // This doesn't work the same way as the isEmpty function used
    // in the first example, it will return true for strings containing only whitespace
    return (this.length === 0 || !this.trim());
};

export default {
    name: 'Home',
    data() {
        return {
            tab: 0,
            save_text: {
                code: 'Saved',
                test: 'Saved'
            },
            output: {
                loading: false,
                status: 'Your results will be shown here.',
                showStatus: true,
                error: false,
                stderr: "",
                stdout: '',
                count: 0,
                passed: 0,
                failed: 0,
                tests: null,
                time: 0,
                type: 'test'
            },
        }
    },
    computed: {
        showNext() {
            return this.output.count !== 0 && this.output.passed === this.output.count && this.output.type === 'submit';
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
            }
        },
        Code: {
            get() {
                if (this.$store.state.challenge.currentKata === null)
                    return null;
                return this.$store.state.challenge.currentKata.saved_code
            }
        },
    },
    methods: {
        goNext() {
            axios.get("/api/kata/next/").then(response => {
                if ("is_end" in response.data) {
                    this.$store.commit('updateCurrentKata', null);
                    this.$router.push('/ranking');
                } else {
                    this.resetOutput();
                    this.tab = 1;
                    this.$store.commit('updateCurrentKata', response.data);
                    this.$router.push('/challenge');
                }
            }).catch(error => {
                console.log(error);
            });
        },
        editCode (value) {
            this.save_text.code = "Not Saved"
            this.$store.commit("updateCode", value);
        },
        editExample (value) {
            this.save_text.test = "Not Saved"
            this.$store.commit("updateExample", value);
        },
        saveTimer() {
            this.save_text.code = "Saving..."
            this.save_text.test = "Saving..."
            setTimeout(() => {
                this.save_text.code = "Saved"
                this.save_text.test = "Saved"
            }, 2000);
        },
        dataSubmit() {
            this.$store.dispatch("saveCode");
            this.saveTimer();
        },
        resetOutput() {
            this.$store.dispatch("refreshUser");
            this.output = {
                loading: false,
                status: 'Your results will be shown here.',
                showStatus: true,
                error: false,
                stderr: "",
                stdout: '',
                count: 0,
                passed: 0,
                failed: 0,
                tests: null,
                time: 0,
            };
        },
        gotoOutput() {
            this.tab = 1;
        },
        codeSubmit() {
            this.resetOutput();
            this.output.status = "<b>Status:</b> Submitting code...";
            this.output.showStatus = true;
            this.output.loading = true;
            this.output.type = 'submit';
            this.saveTimer();
            this.gotoOutput()
            let start = new Date().getTime();
            axios.post("/api/test/submit/", {
                code: this.Code,
            }).then(res => {
                this.$store.dispatch("refreshUser");
                let end = new Date().getTime();
                this.processOutput(res.data, start, end);
            }).catch(err => {
                console.log(err);
                this.output.status = "<b>Status:</b> " + err.message;
            });
        },
        processOutput(data, start, end) {
            this.output.loading = false;
            this.output.showStatus = false;
            this.output.time = (end - start) / 1000;
            if (data.error) {
                this.output.error = true;
                this.output.stderr = data.stderr;
                this.output.stdout = data.stdout;
            } else {
                this.output.tests = data.tests;
                this.output.count = data.test_count;
                this.output.passed = data.passed;
                this.output.failed = data.failed;
                this.output.stderr = data.stderr;
            }
        },
        codeTest() {
            this.resetOutput();
            this.output.status = "<b>Status:</b> Sending request...";
            this.output.showStatus = true;
            this.output.loading = true;
            this.output.type = 'test';
            this.saveTimer();
            this.gotoOutput()
            let start = new Date().getTime();
            axios.post("/api/test/", {
                code: this.Code,
                test: this.Example,
            }).then(res => {
                let end = new Date().getTime();
                this.processOutput(res.data, start, end);
            }).catch(err => {
                console.log(err);
                this.output.status = "<b>Status:</b> " + err.message;
            });
        },
    },
    mounted() {
        this.$store.commit("hideFooter");
        this.$store.dispatch("getCurrentKata").then(() => {
            if (this.Kata === null) {
                this.$router.push('/');
            }
            if (this.Kata["is_ended"]) {
                this.$router.push('/ranking');
            }
        }).catch(err => {
            this.$router.push('/home');
        });
    },
    components: {
        Output,
        Description,
        CodeEditor,
        HelloWorld,
        AceEditor
    },
}
</script>

<style>
.row + .row {
    margin: 0;
}

.test-error {
    color: #c05C48;
}

.test-success {
    color: #6cec6c;
}

.bg-success {
    border-color: #6cec6c !important;
}

.bg-error {
    border-color: #c05C48 !important;
}

.bg-error pre {
    border-color: #b63b3b !important;
    background-color: #544747 !important;
    border-width: 2px !important;
    border-style: solid;
}

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
    overflow-x: auto;
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
