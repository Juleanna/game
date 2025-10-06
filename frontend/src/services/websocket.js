class WebSocketService {
  constructor() {
    this.ws = null
    this.listeners = {}
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 3000
  }

  connect(token) {
    const wsUrl = `ws://localhost:8000/ws/${token}`

    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket подключен')
      this.reconnectAttempts = 0
      this.emit('connected')
    }

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.emit(data.type, data)
      } catch (error) {
        console.error('Ошибка парсинга WebSocket сообщения:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket ошибка:', error)
      this.emit('error', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket отключен')
      this.emit('disconnected')
      this.attemptReconnect(token)
    }
  }

  attemptReconnect(token) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Попытка переподключения ${this.reconnectAttempts}/${this.maxReconnectAttempts}`)
      setTimeout(() => {
        this.connect(token)
      }, this.reconnectDelay)
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  send(type, data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, ...data }))
    } else {
      console.warn('WebSocket не подключен')
    }
  }

  sendChat(text) {
    this.send('chat', { text })
  }

  sendMove(characterId, x, y) {
    this.send('move', { character_id: characterId, x, y })
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = []
    }
    this.listeners[event].push(callback)
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback)
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data))
    }
  }
}

export default new WebSocketService()
