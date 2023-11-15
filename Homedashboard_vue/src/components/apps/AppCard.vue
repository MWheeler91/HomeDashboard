<template>
    <div class="">
        <div class="row">
            <div class="">
                <img class="icon" :src="app.icon"  alt="Service Icon">
            </div>
        </div>
        <div class="row text-center">
            <p class="text-center">{{ app.app_name }}</p>
        </div>
    </div>

</template>

<script>
export default {
    name: "AppCard",
    props: ['app'],
    data() {
        return {}
    },
    methods: {
        getContentImageLink(link) {
            return "http://127.0.0.1:8000/" + link
        }
    }
}
</script>

<style scoped>

.icon {
    display: block;
    object-fit: contain;
    margin: 0 auto;
    background-color: white;
    height: 50px;
    width: 50px;
}

.text-center {
    text-align: center;
}
</style>