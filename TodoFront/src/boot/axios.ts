import axios from 'axios'
import { Notify } from 'quasar'
// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: import.meta.env.VITE_API_SERVER_URL, withCredentials: true, })

api.interceptors.response.use(
    Response => Response,
    error => {
        if (error.response.status === 403) {
            Notify.create('Must start a session first!')
        }
    }
)

export default api