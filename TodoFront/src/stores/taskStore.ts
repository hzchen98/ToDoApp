import { defineStore } from 'pinia'
import api from '@/boot/axios'
import type Task from '@/models/Task'

export const useTaskStore = defineStore('tasks', {
  state: () => ({ _tasks: [] as Array<Task> }),
  getters: {
    tasks: (state) => state._tasks,
  },
  actions: {
    getTasks(search: string) {
      api
        .get('/items', { params: { search: search, limit: 1000 } })
        .then((response) => {
          this._tasks = response.data.items
        })
    },
    async addTask(newTask: Task) {
      return new Promise((resolve, reject) => {
        api
          .post('/items', newTask)
          .then((response) => {
            this._tasks.push(response.data)
            resolve(response.data)
          }).catch(err => {
            reject(err)
          })
      }
      )
    },
    async deleteTask(uuid: string) {
      return new Promise((resolve, reject) => {
        api
          .delete(`/items/${uuid}`)
          .then((response) => {
            this.getTasks('')
            resolve(null)
          }).catch(err => {
            reject(err)
          })
      }
      )
    }, async updateTask(task: Task) {
      return new Promise((resolve, reject) => {
        api
          .put(`/items/${task.uuid}`, task)
          .then((response) => {
            this.getTasks('')
            resolve(null)
          }).catch(err => {
            reject(err)
          })
      }
      )
    }
  }
})
