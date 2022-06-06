<template>
    <v-card class="elevation-0 rounded-xl" height="750" color="#222327">
        <v-card-text>
            <v-card-text class="text-body-1">
                <p>
                    <strong>{{ name }}</strong>
                </p>
                <div v-html="descriptionToHtml">

                </div>
            </v-card-text>
        </v-card-text>
    </v-card>
</template>

<script>
    import {marked} from "marked";

    export default {
        name: 'Description',
        props: {
            name: {
                type: String,
                required: true,
            },
            description: {
                type: String,
                required: true,
            },
        },
        computed: {
            descriptionToHtml() {
                return marked(this.description);
            },
        }
    };
</script>