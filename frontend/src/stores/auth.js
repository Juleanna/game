import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async register(username, email, password) {
      try {
        const response = await axios.post('http://localhost:8000/auth/register', {
          username,
          email,
          password
        })
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка регистрации'
        }
      }
    },

    async login(username, password) {
      try {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const response = await axios.post('http://localhost:8000/auth/login', formData)
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка входа'
        }
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
