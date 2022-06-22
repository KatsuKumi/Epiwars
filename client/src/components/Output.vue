<template>

    <v-card v-bind:class="boxClasses" class="elevation-0 rounded-xl overflow-auto" height="750" outlined>
        <v-card-text style="height:100%">
            <div v-if="output.showStatus" class="fill-height overflow-hidden">
                <div v-html="output.status">
                </div>
                <div class="d-flex flex-column align-center justify-center fill-height" v-if="output.loading">
                    <v-progress-circular
                        :size="70"
                        :width="7"
                        color="white"
                        indeterminate
                        class="justify-center"
                    ></v-progress-circular>
                </div>
            </div>
            <div v-else-if="showError">
                <span class="text-overline">
                    <v-icon dark>mdi-alert-circle</v-icon>
                        Stderr
                </span>
                <pre v-html="output.stderr">
                </pre>
            </div>
            <v-fade-transition origin="center center">
                <v-container v-if="output.tests != null">
                    <v-row align="start">
                        <v-col>
                        <span class="text-overline">
                            <span class="mr-5 white--text">Time: {{ this.output.time * 1000 }}ms</span>
                            <span class="mr-5 white--text">Count: {{ output.count }}</span>
                            <span class="mr-5"
                                  v-bind:class="{'test-success': output.passed}">Passed: {{ output.passed }}</span>
                            <span class="mr-5"
                                  v-bind:class="{'test-error': output.failed}">Failed: {{ output.failed }}</span>
                        </span>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-divider class="my-5"></v-divider>
                    </v-row>
                    <v-row v-if="output.stderr">
                        <v-expansion-panels v-model="panelStderr" multiple>
                            <v-expansion-panel>
                                <v-expansion-panel-header>
                                <span class="text-overline">
                                    <v-icon dark>mdi-alert-circle</v-icon>
                                        Stderr
                                </span>
                                </v-expansion-panel-header>
                                <v-expansion-panel-content>
                                <pre v-html="output.stderr">
                                </pre>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-row>

                    <v-row v-if="output.stderr">
                        <v-divider class="my-5"></v-divider>
                    </v-row>
                    <v-row justify="center">

                    <span class="text-overline">
                        <v-icon dark>mdi-success</v-icon>
                            Test Results:
                    </span>
                        <v-expansion-panels multiple accordion v-model="panels">
                            <v-expansion-panel v-for="(item, index) in output.tests" :key="index">
                                <v-expansion-panel-header>
                                    <div class="text-overline" v-bind:class="checkTestStatus(item)">
                                        {{ item.name }}
                                    </div>
                                    <template v-slot:actions>
                                        <v-icon color="teal" v-if="checkTestStatus(item) === 'test-success'">
                                            mdi-check
                                        </v-icon>
                                        <v-icon color="error" v-else>
                                            mdi-alert-circle
                                        </v-icon>
                                    </template>
                                </v-expansion-panel-header>
                                <v-expansion-panel-content>
                                    <v-expansion-panels multiple v-model="subpanels[index]">
                                        <v-expansion-panel v-for="(test, index) in item.it"
                                                           :key="index">
                                            <v-expansion-panel-header>
                                                <div class="text-caption"
                                                     v-bind:class="{ 'test-error': !test.passed, 'test-success': test.passed }">
                                                    {{ test.name }}
                                                </div>
                                                <template v-slot:actions>
                                                    <v-icon color="teal" v-if="test.passed">
                                                        mdi-check
                                                    </v-icon>
                                                    <v-icon color="error" v-else>
                                                        mdi-alert-circle
                                                    </v-icon>
                                                </template>
                                            </v-expansion-panel-header>
                                            <v-expansion-panel-content>

                                                <pre v-if="!test.passed" v-html="test.err"></pre>
                                                <v-alert outlined type="success" text v-else>
                                                    Test Passed in {{ test.time * 1000 }}ms
                                                </v-alert>
                                            </v-expansion-panel-content>
                                        </v-expansion-panel>
                                    </v-expansion-panels>
                                    <v-alert class="mt-5" outlined type="info" elevation="2"
                                             v-if="checkTestStatus(item) === 'test-success'">
                                        Passed in {{ getTotal(item) * 1000 }}ms
                                    </v-alert>
                                    <v-alert class="mt-5" outlined type="error" elevation="2" v-else>
                                        Not passed
                                    </v-alert>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-row>
                    <v-row v-if="output.failed <= 0">
                        <v-alert class="mt-5" outlined type="success" elevation="2" width="100%"
                                 v-if="output.type === 'test'">
                            All test passed, you can try to submit your code !
                        </v-alert>
                        <v-alert class="mt-5" outlined type="success" elevation="2" width="100%" v-else>
                            All test passed, you can now go to next challenge !
                        </v-alert>
                    </v-row>
                </v-container>
            </v-fade-transition>
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    name: 'Output',
    props: {
        output: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            panelStderr: [0],
            panels: [],
            subpanels: [],
        }
    },
    methods: {
        getTotal(item) {
            return item.it.reduce((acc, cur) => acc + cur.time, 0)
        },
        checkTestStatus(test) {
            for (let i = 0; i < test.it.length; i++) {
                if (!test.it[i].passed) {
                    return 'test-error';
                }
            }
            return 'test-success';
        },
    },
    computed: {
        showError() {
            return this.output.error;
        },
        boxClasses() {
            if (this.output.error || this.output.failed > 0) {
                return 'bg-error';
            } else if (this.output.count !== 0) {
                return 'bg-success';
            }
        },
    },
    watch: {
        output: {
            handler(newVal, oldVal) {
                if (newVal.tests != null) {
                    this.panels = [];
                    for (let y = 0; y < this.output.tests.length; y++) {
                        this.subpanels.push([]);
                        for (let i = 0; i < this.output.tests[y].it.length; i++) {
                            if (!this.output.tests[y].it[i].passed) {
                                if (this.panels.indexOf(y) === -1) {
                                    this.panels.push(y);
                                }
                                this.subpanels[y].push(i);
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
}
</script>