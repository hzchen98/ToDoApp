import { defineStore } from 'pinia'
import api from '@/boot/axios'

export type SessionState = {
  name: string | null;
};

export const useSessionStore = defineStore('session', {
  state: () => ({ _name: '' as string, }),
  getters: {
    name: (state) => state._name,
  },
  actions: {
    async fetchCurrentSession() {
      return new Promise((resolve, reject) => {
        api
          .get('/me')
          .then((response) => {
            this._name = response.data.name
            resolve(response.data)
          })
          .catch(err => {
            reject(err)
          })
      })

    },

    exit(){
      api.delete("/me").then((response) => {
        this._name = response.data.name
      })
    }
  }
})
