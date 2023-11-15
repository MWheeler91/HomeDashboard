<template>
  <div>
    <NavBar />
  </div>

  <div class="content">
    <router-view />
  </div>


  <div class="footer">
        <hr>
        <p role="contentinfo" class="container"> Copyright &copy; {% now "Y" %} MWheeler Development. </p>
    </div>
</template>

<script>

// import { defineComponent } from "vue";
import HomePage from "@/components/HomePage.vue"
import NavBar from "@/components/layout/NavBar.vue";

// import { useUserStore } from '@/store/user'

export default {
  name: 'App',
  components: {
    HomePage,
    NavBar
  },

}
</script>

<style>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
}
body {
  background-color: #0f0f0f;
}
.content {
  min-height: calc(100vh - 70px);
}
.footer {
  height: 50px;
  color: white;
}
</style>
