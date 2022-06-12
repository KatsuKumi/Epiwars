<template>
    <v-navigation-drawer permanent dark color="#222327" app
        expand-on-hover
        :mini-variant.sync="mini">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title class="text-h6 text-center my-1">
                    Admin panel
                </v-list-item-title>
            </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
            dense
            nav
        >
            <v-list-item-group>
                <v-list-item link to="/panel/dashboard" :key="0">
                    <v-list-item-icon>
                        <v-icon>mdi-view-dashboard</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link to="/panel/challenges" :key="1">
                    <v-list-item-icon>
                        <v-icon>mdi-manjaro</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>Challenges</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link to="/panel/katas" :key="2">
                    <v-list-item-icon>
                        <v-icon>mdi-script</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>Katas</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link to="/panel/settings" :key="3">
                    <v-list-item-icon>
                        <v-icon>mdi-cog</v-icon>
                    </v-list-item-icon>

                    <v-list-item-content>
                        <v-list-item-title>Settings</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
export default {
    name: 'PanelNavigation',
    data() {
        return {
            mini: true
        }
    },
    mounted() {
    }
}
</script>