<template>
  <div class="chat-panel-bottom">
    <div class="chat-messages" ref="chatMessages">
      <div v-for="(msg, index) in messages" :key="index" class="chat-message">
        <span class="chat-user">{{ msg.user }}:</span>
        <span class="chat-text">{{ msg.text }}</span>
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="messageText"
        @keyup.enter="sendMessage"
        placeholder="Введите сообщение..."
      />
      <button @click="sendMessage">Отправить</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  messages: Array
})

const emit = defineEmits(['send-message'])

const messageText = ref('')

const sendMessage = () => {
  if (messageText.value.trim()) {
    emit('send-message', messageText.value)
    messageText.value = ''
  }
}
</script>

<style scoped>
.chat-panel-bottom {
  background-color: #252525;
  border-top: 1px solid #333;
  height: 240px;
  display: flex;
  flex-direction: column;
  padding: 15px 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.chat-message {
  margin-bottom: 8px;
  font-size: 14px;
}

.chat-user {
  color: #4a9a4a;
  font-weight: bold;
  margin-right: 5px;
}

.chat-text {
  color: #ccc;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #333;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: 4px;
  color: #fff;
  font-size: 14px;
}

.chat-input input:focus {
  outline: none;
  border-color: #4a9a4a;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #4a9a4a;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #5aaa5a;
}
</style>
