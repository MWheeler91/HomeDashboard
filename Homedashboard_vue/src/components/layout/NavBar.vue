<template>
  <nav class="navbar navbar-expand-xl navbar-dark bg-dark" role="navigation" aria-label="">
    <div class="container-fluid ">
      <router-link to="/">
        <a class="nav-btn" href="#">Home</a>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">

        <ul class="navbar-nav mr-auto  flex-wrap ms-md-auto">

          <li class="nav-item">
            <a class='nav-link' href="http://localhost:8000/admin/" v-if="isAuthenticated">Admin</a>
          </li>

          <li class="nav-item dropdown" v-if="isAuthenticated">
            <a class="nav-link dropdown-toggle" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
              aria-expanded="false">Welcome: {{ userStore.user.first_name }}</a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <!-- <li><a class="dropdown-item" href="#">My Account</a></li> -->
              <li><a class="dropdown-item" href="#">Another action</a></li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li><a class="dropdown-item" href="/" @click="logout">Log Out</a></li>
            </ul>
          </li>
          <li class="nav-item" v-else>
            <button class="nav-btn" @click="() => TogglePopup('buttonTrigger')" v-if="!isAuthenticated">Login</button>
            <popup v-if="popupTriggers.buttonTrigger">
              <LoginPage :togglePopup="() => TogglePopup('buttonTrigger')" :getData="() => getData()" />
            </popup>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>


<script>
import Popup from '../UI/Popup.vue';
// import LoginPage from '@/components/login/LoginPage.vue';
import { ref } from "vue";
import LoginPage from '../login/LoginPage.vue';
import { useUserStore } from '@/store/user'

export default {
  name: "NavBar",
  components: { Popup, LoginPage },
  data() {
    return {
      first_name: localStorage.getItem('first_name'),
      last_name: localStorage.getItem('last_name'),
      isAuthenticated: this.userStore.user.isAuthenticated,
      buttonTrigger: false,
    };
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
    userStore.initStore()
    return {
      popupTriggers,
      TogglePopup,
      userStore
    }
  },
  methods: {
    logout() {
      this.userStore.removeToken();
    }
  },
  computed: {},
  components: { Popup, LoginPage }
}

</script>


<style scoped>
.nav-btn {
  background-color: transparent;
  border: none;
  color: rgba(255, 255, 255, .55);
  padding-right: 0.5rem;
  padding-left: 0.5rem;
  text-decoration: none;

}
a:hover, a:visited, a:link, a:active{
  text-decoration: none;

}

</style>



<!-- <template>
  <nav class="navbar navbar-expand-xl navbar-dark bg-dark" role="navigation" aria-label="">
    <div class="container-fluid">
        <router-link to="/">
          <a class="navbar-brand" href="#"><img src="~@/assets/images/brand.png" alt="Brand Image"></a>
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent" >
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                    <router-link to="/properties" class="nav-link">Properties</router-link>
                </li>
                <li class="nav-item">
                    <router-link to="/contact" class="nav-link">Contact Us</router-link>
                </li>
            </ul>
            <ul class="navbar-nav mr-auto  flex-wrap ms-md-auto">
               <li class="nav-item" v-if="isAuthenticated">
                   <a class='nav-link' href="#">View Applications</a>
               </li>
               <li class="nav-item">
                   <a class='nav-link' href="http://192.68.50.66:8000/admin/" v-if="isAuthenticated">Admin</a>
               </li>

                <li class="nav-item dropdown" v-if="isAuthenticated">
                    <a class="nav-link dropdown-toggle" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">Welcome: {{ first_name }} {{last_name}}</a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="#">My Account</a></li>
                        <li><a class="dropdown-item" href="#">Another action</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" href="/" @click="logout">Log Out</a></li>
                    </ul>
                </li>
                <li class="nav-item" v-else>
                    <router-link to="/login" class="nav-link" v-if="!isAuthenticated">Login</router-link>
                </li>
            </ul>
        </div>
    </div>
</nav>
</template> -->