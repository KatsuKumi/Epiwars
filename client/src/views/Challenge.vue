<template>
    <hello-world/>
</template>

<script>
import HelloWorld from '../components/HelloWorld'

export default {
    name: 'Home',
    mounted() {
        this.$store.commit("hideFooter");
    },
    components: {
        HelloWorld,
    },
}
</script>
