import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from "./routes"
import { Quasar, Notify, Dialog } from 'quasar'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'
const app = createApp(App)


app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: { Notify, Dialog }, // import Quasar plugins and add here
})


app.mount('#app')
