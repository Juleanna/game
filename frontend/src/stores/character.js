import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [],
    currentCharacter: null,
    loading: false
  }),

  actions: {
    async fetchCharacters() {
      const authStore = useAuthStore()

      try {
        this.loading = true
        const response = await axios.get('http://localhost:8000/characters/', {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })
        this.characters = response.data

        // Установить текущего персонажа, если есть
        if (this.characters.length > 0 && !this.currentCharacter) {
          this.currentCharacter = this.characters[0]
        }

        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка загрузки персонажей'
        }
      } finally {
        this.loading = false
      }
    },

    async createCharacter(name, profession, gender) {
      const authStore = useAuthStore()

      try {
        this.loading = true
        const response = await axios.post(
          'http://localhost:8000/characters/',
          { name, profession, gender },
          {
            headers: {
              Authorization: `Bearer ${authStore.token}`
            }
          }
        )

        this.characters.push(response.data)
        this.currentCharacter = response.data

        return { success: true, character: response.data }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка создания персонажа'
        }
      } finally {
        this.loading = false
      }
    },

    async deleteCharacter(characterId) {
      const authStore = useAuthStore()

      try {
        await axios.delete(`http://localhost:8000/characters/${characterId}`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`
          }
        })

        this.characters = this.characters.filter(c => c.id !== characterId)

        if (this.currentCharacter?.id === characterId) {
          this.currentCharacter = this.characters[0] || null
        }

        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data?.detail || 'Ошибка удаления персонажа'
        }
      }
    },

    setCurrentCharacter(character) {
      this.currentCharacter = character
    }
  }
})
