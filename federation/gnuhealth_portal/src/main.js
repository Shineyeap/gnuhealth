import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

// Add global objects
Vue.prototype.$thalamus_server = 'http://localhost:5000'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
