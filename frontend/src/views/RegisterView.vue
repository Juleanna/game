<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Регистрация</h1>
      <form @submit.prevent="handleRegister">
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
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Введите email"
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

        <div class="form-group">
          <label>Подтверждение пароля</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Повторите пароль"
            required
          />
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="login-link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
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
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Пароль должен содержать минимум 6 символов'
    return
  }

  loading.value = true

  const result = await authStore.register(
    username.value,
    email.value,
    password.value
  )

  loading.value = false

  if (result.success) {
    router.push('/game')
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.register-container {
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

input {
  width: 100%;
}

button {
  width: 100%;
  margin-top: 10px;
  background-color: #4a9a4a;
}

button:hover:not(:disabled) {
  background-color: #5aaa5a;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #888;
  font-size: 14px;
}

.login-link a {
  color: #4a9a4a;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
