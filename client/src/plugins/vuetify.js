import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            dark: {
                background: '#16171b',
                primary: '#3f51b5',
                secondary: '#d4d4d8',
                accent: '#8c9eff',
                error: '#b71c1c',
            },
        },
    },
});
