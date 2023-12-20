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
.verticalBtn{
  vertical-align: middle
}

/* Pagination */
.pagination-container {
    display: flex;
    column-gap: 10px;
  }
  .paginate-buttons {
    height: 40px;
    width: 40px;
    border-radius: 20px;
    cursor: pointer;
    background-color: rgb(242, 242, 242);
    border: 1px solid rgb(217, 217, 217);
    color: black;
  }
  .paginate-buttons:hover {
    background-color: #d8d8d8;
  }
  .active-page {
    background-color: #3498db;
    border: 1px solid #3498db;
    color: white;
  }
  .active-page:hover {
    background-color: #2988c8;
  }

</style>
