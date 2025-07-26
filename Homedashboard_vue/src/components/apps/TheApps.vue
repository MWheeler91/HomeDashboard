<template>
    <div class="container flex-container">
        <div v-for="app in apps" :key="app.id">
            <app-card-wrapper v-if="app.is_vue_app">
                <router-link class="routerLink" :to="{ path: app.web_address }">
                    <app-card :app="app"  />
                </router-link>
            </app-card-wrapper>

            <app-card-wrapper v-else>
                <app-card :app="app" @click="openInNewTab(app.web_address)" />
            </app-card-wrapper>
        </div>


        <div>
            <app-card-wrapper>
                <app-card :app="empty" @click="() => TogglePopup('buttonTrigger')" />
            </app-card-wrapper>
        </div>
    </div>
    <popup v-if="popupTriggers.buttonTrigger">
        <new-app :togglePopup="() => TogglePopup('buttonTrigger')" :getData="() => getData()" />
    </popup>
</template>

<script>
import axios from "axios";
import AppCard from "@/components/apps/AppCard.vue";
import AppCardWrapper from "@/components/apps/AppCardWrapper.vue";
import Popup from "@/components/UI/Popup.vue";
import { ref } from "vue";
import NewApp from "@/components/apps/NewApp.vue";
import { useUserStore } from '@/store/user'


export default {
    name: "TheApps",
    components: { NewApp, Popup, AppCardWrapper, AppCard },
    data() {
        return {
            apps: {},
            empty: {
                id: 999,
                app_name: 'Create New',
                web_address: 'nah',
                icon: './src/assets/plus.png'
            },
        }
    },
    setup() {
        const userStore = useUserStore()
        const popupTriggers = ref({
            buttonTrigger: false,
            timedTrigger: false
        });

        const TogglePopup = (trigger) => {
            popupTriggers.value[trigger] = !popupTriggers.value[trigger]
        }
        return {
            popupTriggers,
            TogglePopup,
            userStore
        }
    },
    mounted() {
        this.getData()
        console.log(this.apps)
    },
    methods: {
        async getData() {
            if (this.userStore.user.isAuthenticated) {
                axios
                    .get('/apps/applist', this.data)
                    .then(response => {
                        this.apps = response.data
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                console.log(this.apps)
            } else {
                axios
                    .get('/apps/applistnoauth', this.data)
                    .then(response => {
                        this.apps = response.data
                        console.log(response.data)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                console.log(this.apps)
            }

        },
        openInNewTab(url) {
            window.open(url, '_blank', 'noreferrer')
        }
    }
}
</script>

<style scoped>
.flex-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    /*margin-right: 50px;*/
    height: auto;
    width: 150px;
}

.routerLink{
    text-decoration: none;
    color: inherit;
    padding: 0px;
    /* margin: px; */
}
</style>