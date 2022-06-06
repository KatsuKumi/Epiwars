<template>
    <v-sheet
        class="mx-auto my-5 rounded-t-xl"
        color="#222327"
    >
        <div class="d-flex justify-space-between text-subtitle-1 py-3 px-5">
            <span style="min-width: 70px"></span>
            <span>{{ title }}</span>
            <span style="min-width: 70px"
                  class="text-caption text-decoration-underline font-italic text-right">{{ status }}</span>
        </div>
        <AceEditor
            v-model="innerCode"
            @init="editorInit"
            lang="c_cpp"
            theme="tomorrow_night"
            width="100%"
            :height="height"
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
                    exec: submitEvent,
                    readOnly: true,
                },
            ]"
        />
    </v-sheet>
</template>

<script>
import AceEditor from 'vuejs-ace-editor';

export default {
    name: 'CodeEditor',
    props: {
        title: {
            type: String,
            required: true,
        },
        status: {
            type: String,
            required: true,
        },
        submitEvent: {
            type: Function,
            required: true,
        },
        code: {
            type: String,
            required: true
        },
        height: {
            type: String,
            required: true,
        },
    },
    computed: {
        innerCode: {
            get() {
                return this.code;
            },
            set(value) {
                this.$emit('editCode', value);
            },
        },
    },
    methods: {
        editorInit: function () {
            require('brace/ext/language_tools')
            require('brace/mode/html')
            require('brace/mode/c_cpp')
            require('brace/mode/javascript')
            require('brace/mode/less')
            require('brace/theme/tomorrow_night')
            require('brace/snippets/javascript')
            require('brace/snippets/c_cpp')
        }
    },
    components: {
        AceEditor,
    },
};

</script>