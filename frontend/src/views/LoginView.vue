<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Вход в игру</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            placeholder="Введите имя пользователя"
            required
          />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="Введите пароль"
            required
          />
        </div>

        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input
              v-model="rememberMe"
              type="checkbox"
            />
            <span>Запомнить меня</span>
          </label>
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <p class="register-link">
        Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const error = ref('')
const loading = ref(false)

// Загрузка сохраненных данных при монтировании
const savedUsername = localStorage.getItem('rememberedUsername')
const savedPassword = localStorage.getItem('rememberedPassword')
if (savedUsername && savedPassword) {
  username.value = savedUsername
  password.value = savedPassword
  rememberMe.value = true
}

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  const result = await authStore.login(username.value, password.value)

  loading.value = false

  if (result.success) {
    // Сохранение или удаление учетных данных
    if (rememberMe.value) {
      localStorage.setItem('rememberedUsername', username.value)
      localStorage.setItem('rememberedPassword', password.value)
    } else {
      localStorage.removeItem('rememberedUsername')
      localStorage.removeItem('rememberedPassword')
    }

    router.push('/game')
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.login-container {
  background-color: #252525;
  padding: 40px;
  border-radius: 8px;
  border: 1px solid #333;
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #4a9a4a;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #ccc;
  font-size: 14px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
}

.checkbox-group {
  margin-bottom: 15px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #ccc;
  font-size: 14px;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: #4a9a4a;
}

.checkbox-label span {
  user-select: none;
}

button {
  width: 100%;
  margin-top: 10px;
  background-color: #4a9a4a;
}

button:hover:not(:disabled) {
  background-color: #5aaa5a;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #888;
  font-size: 14px;
}

.register-link a {
  color: #4a9a4a;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
