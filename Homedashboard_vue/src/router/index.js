import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue'
import InsuranceHome from '@/components/insurance/InsuranceHome.vue'
// import store from '../store'
import { useUserStore } from '@/store/user'


const index = createRouter({
  scrollBehavior(to, from, savedPosition) {
    console.log(to, from, savedPosition)
    return { top: 0 }
  },
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/insurance-db',
      name: 'InsuranceHome',
      component: InsuranceHome,
      meta: {
        requireLogin: true
      }
    },
    // {
    //   path: '/properties/:slug/',
    //   name: 'propertyDetails',
    //   component: propertyDetails,
    //   props: true
    // },
    // {
    //   path: '/application/id=:id?/address=:address?',
    //   name: 'Application',
    //   component: applicationPage,
    //   meta: {
    //     requireLogin: true
    //   }
    // },
    // {
    //   path: '/contact',
    //   name: 'Contact',
    //   component: contactPage,
    // },
    // {
    //   path: '/login',
    //   name: 'Login',
    //   component: loginPage
    // },
    // {
    //   path: '/registration',
    //   name: 'Registration',
    //   component: registrationPage
    // },
    // {
    //   path: '/password_reset',
    //   name: 'PasswordReset',
    //   component: PasswordReset
    // },
  ],
  linkActiveClass: 'active',


})

index.beforeEach((to, from, next) => {
  const store = useUserStore()
  if (to.matched.some(record => record.meta.requireLogin) && !store.user.isAuthenticated) {
    console.log('you must log in first')
  } else {
    next()
  }
})

export function resetRouter() {
  const newRouter = createRouter()
  index.matcher = newRouter.matcher // reset index
}

export default index