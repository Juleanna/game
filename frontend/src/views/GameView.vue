<template>
  <div class="game-view">
    <header class="game-header">
      <h1>TimeZero</h1>
      <div class="user-info">
        <span>{{ authStore.user?.username || 'Игрок' }}</span>
        <button @click="handleLogout" class="logout-btn">Выйти</button>
      </div>
    </header>

    <div class="game-container">
      <!-- Боковая панель персонажа -->
      <aside class="character-panel">
        <h2>Персонажи</h2>
        <div v-if="characterStore.characters.length === 0" class="no-character">
          <p>У вас нет персонажей</p>
          <button @click="showCreateCharacter = true">Создать персонажа</button>
        </div>
        <div v-else>
          <div class="character-list">
            <div
              v-for="char in characterStore.characters"
              :key="char.id"
              :class="['character-item', { active: character && character.id === char.id }]"
              @click="selectCharacter(char)"
            >
              <div class="char-name">{{ char.name }}</div>
              <div class="char-level">Ур. {{ char.level }}</div>
            </div>
          </div>
          <button v-if="characterStore.characters.length < 3" @click="showCreateCharacter = true" class="create-btn">
            + Создать персонажа
          </button>

          <div v-if="character" class="character-info">
            <h3>{{ character.name }}</h3>
            <p>Пол: {{ getGenderLabel(character.gender) }}</p>
            <p>Профессия: {{ getProfessionLabel(character.profession) }}</p>
            <p>Уровень: {{ character.level }}</p>
            <div class="stats">
            <div class="stat">
              <span>HP:</span>
              <div class="bar">
                <div class="bar-fill" :style="{ width: (character.health / character.max_health * 100) + '%' }"></div>
              </div>
              <span>{{ character.health }}/{{ character.max_health }}</span>
            </div>
            <div class="stat-grid">
              <div>Сила: {{ character.strength }}</div>
              <div>Ловкость: {{ character.dexterity }}</div>
              <div>Интеллект: {{ character.intelligence }}</div>
              <div>Выносливость: {{ character.endurance }}</div>
            </div>
            </div>
            <div class="resources">
              <p>Опыт: {{ character.experience }}</p>
              <p>Золото: {{ character.gold }}</p>
            </div>
          </div>
        </div>
      </aside>

      <!-- Основная игровая область -->
      <main class="game-main">
        <div class="game-canvas">
          <canvas ref="gameCanvas" width="800" height="600" @click="handleCanvasClick"></canvas>
          <div class="location-info">
            <p v-if="currentLocation">📍 {{ currentLocation.name }}</p>
            <p v-if="currentLocation && currentLocation.radiation_level > 0" class="radiation-warning">
              ☢️ Радиация: {{ currentLocation.radiation_level }}
            </p>
            <p v-if="character" class="coordinates">Координаты: ({{ playerX }}, {{ playerY }})</p>
          </div>
        </div>

        <!-- Боевая панель -->
        <div v-if="selectedMonster" class="combat-panel">
          <h3>Бой: {{ selectedMonster.name }}</h3>
          <div class="monster-stats">
            <div class="stat-bar">
              <span>HP: {{ selectedMonster.health }}/{{ selectedMonster.max_health }}</span>
              <div class="bar">
                <div class="bar-fill monster-hp" :style="{ width: (selectedMonster.health / selectedMonster.max_health * 100) + '%' }"></div>
              </div>
            </div>
            <p>Уровень: {{ selectedMonster.level }}</p>
          </div>
          <div class="combat-actions">
            <button @click="attackMonster" class="attack-btn">⚔️ Атаковать</button>
            <button @click="selectedMonster = null" class="flee-btn">🏃 Отступить</button>
          </div>
          <div class="combat-log">
            <div v-for="(log, index) in combatLog" :key="index" class="log-entry" :class="log.type">
              {{ log.message }}
            </div>
          </div>
        </div>

        <!-- Чат -->
        <div class="chat-panel" :class="{ 'compact': selectedMonster }">
          <div class="chat-messages" ref="chatMessages">
            <div v-for="(msg, index) in messages" :key="index" class="chat-message">
              <span class="chat-user">{{ msg.user }}:</span>
              <span class="chat-text">{{ msg.text }}</span>
            </div>
          </div>
          <div class="chat-input">
            <input
              v-model="chatMessage"
              @keyup.enter="sendMessage"
              placeholder="Введите сообщение..."
            />
            <button @click="sendMessage">Отправить</button>
          </div>
        </div>
      </main>
    </div>

    <!-- Модальное окно создания персонажа -->
    <div v-if="showCreateCharacter" class="modal">
      <div class="modal-content">
        <h2>Создание персонажа</h2>
        <form @submit.prevent="createCharacter">
          <div class="form-group">
            <label>Имя персонажа</label>
            <input v-model="newCharacter.name" required />
          </div>
          <div class="form-group">
            <label>Пол</label>
            <select v-model="newCharacter.gender" required>
              <option value="male">Мужчина</option>
              <option value="female">Женщина</option>
              <option value="other">Другое</option>
            </select>
          </div>
          <div class="form-group">
            <label>Профессия</label>
            <select v-model="newCharacter.profession" required>
              <option value="corsair">Корсар</option>
              <option value="mercenary">Наёмник</option>
              <option value="stalker">Сталкер</option>
              <option value="journalist">Журналист</option>
              <option value="trader">Торговец</option>
              <option value="psionic">Псионик</option>
              <option value="engineer">Инженер</option>
              <option value="medic">Медик</option>
              <option value="scout">Разведчик</option>
              <option value="scientist">Учёный</option>
              <option value="hunter">Охотник</option>
              <option value="guard">Страж</option>
              <option value="mechanic">Механик</option>
              <option value="smuggler">Контрабандист</option>
            </select>
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <div class="modal-buttons">
            <button type="submit">Создать</button>
            <button type="button" @click="showCreateCharacter = false">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCharacterStore } from '../stores/character'
import websocketService from '../services/websocket'

const router = useRouter()
const authStore = useAuthStore()
const characterStore = useCharacterStore()

const showCreateCharacter = ref(false)
const newCharacter = ref({
  name: '',
  gender: 'male',
  profession: 'stalker'
})
const error = ref('')

const character = computed(() => characterStore.currentCharacter)

const chatMessage = ref('')
const messages = ref([
  { user: 'Система', text: 'Добро пожаловать в TimeZero!' }
])

const gameCanvas = ref(null)
const playerX = ref(400)
const playerY = ref(300)
const otherPlayers = ref([])
const monsters = ref([])
const selectedMonster = ref(null)
const combatLog = ref([])
const locations = ref([])
const currentLocation = ref(null)

const handleLogout = () => {
  websocketService.disconnect()
  authStore.logout()
  router.push('/')
}

const selectCharacter = async (char) => {
  characterStore.setCurrentCharacter(char)
  playerX.value = char.location_id ? 400 : 400
  playerY.value = char.location_id ? 300 : 300
  await loadMonsters()
  drawCanvas()
}

const getGenderLabel = (gender) => {
  const labels = {
    'male': 'Мужчина',
    'female': 'Женщина',
    'other': 'Другое'
  }
  return labels[gender] || gender
}

const getProfessionLabel = (profession) => {
  const labels = {
    'corsair': 'Корсар',
    'mercenary': 'Наёмник',
    'stalker': 'Сталкер',
    'journalist': 'Журналист',
    'trader': 'Торговец',
    'psionic': 'Псионик',
    'engineer': 'Инженер',
    'medic': 'Медик',
    'scout': 'Разведчик',
    'scientist': 'Учёный',
    'hunter': 'Охотник',
    'guard': 'Страж',
    'mechanic': 'Механик',
    'smuggler': 'Контрабандист'
  }
  return labels[profession] || profession
}

const createCharacter = async () => {
  error.value = ''

  const result = await characterStore.createCharacter(
    newCharacter.value.name,
    newCharacter.value.profession,
    newCharacter.value.gender
  )

  if (result.success) {
    showCreateCharacter.value = false
    newCharacter.value = { name: '', gender: 'male', profession: 'stalker' }
    messages.value.push({
      user: 'Система',
      text: `Персонаж ${result.character.name} успешно создан!`
    })
    // Автоматически выбираем созданного персонажа
    await selectCharacter(result.character)
  } else {
    error.value = result.error
  }
}

const sendMessage = () => {
  if (chatMessage.value.trim()) {
    // Отправка через WebSocket
    websocketService.sendChat(chatMessage.value)

    // Очищаем поле ввода
    chatMessage.value = ''
  }
}

const loadLocations = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/locations/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      locations.value = data

      // Определяем текущую локацию по позиции персонажа
      if (character.value) {
        currentLocation.value = locations.value.find(loc =>
          Math.abs(loc.x - playerX.value) < 100 && Math.abs(loc.y - playerY.value) < 100
        ) || locations.value[0]
      }

      drawCanvas()
    }
  } catch (error) {
    console.error('Ошибка загрузки локаций:', error)
  }
}

const loadMonsters = async () => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/combat/monsters/nearby/${character.value.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      monsters.value = data.monsters
      drawCanvas()
    }
  } catch (error) {
    console.error('Ошибка загрузки монстров:', error)
  }
}

const teleportToLocation = async (location) => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/movement/move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        character_id: character.value.id,
        x: location.x,
        y: location.y
      })
    })

    if (response.ok) {
      playerX.value = location.x
      playerY.value = location.y
      currentLocation.value = location

      messages.value.push({
        user: 'Система',
        text: `Вы переместились в: ${location.name}`
      })

      // Обновляем монстров для новой локации
      await loadMonsters()
      drawCanvas()

      // Отправляем информацию о перемещении через WebSocket
      websocketService.sendMove(character.value.id, location.x, location.y)
    }
  } catch (error) {
    console.error('Ошибка телепортации:', error)
  }
}

const attackMonster = async () => {
  if (!selectedMonster.value || !character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/combat/characters/${character.value.id}/attack`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        target_monster_id: selectedMonster.value.id
      })
    })

    if (response.ok) {
      const result = await response.json()

      // Добавляем лог атаки игрока
      combatLog.value.push({
        type: 'player-attack',
        message: `Вы нанесли ${result.player_attack.damage} урона!`
      })

      // Обновляем HP монстра
      selectedMonster.value.health = result.player_attack.monster_health

      // Если монстр жив - он атакует в ответ
      if (result.monster_counter_attack) {
        combatLog.value.push({
          type: 'monster-attack',
          message: `${selectedMonster.value.name} нанёс вам ${result.monster_counter_attack.damage} урона!`
        })

        // Обновляем HP персонажа
        character.value.health = result.monster_counter_attack.defender_health

        // Проверка смерти персонажа
        if (!result.monster_counter_attack.defender_alive) {
          combatLog.value.push({
            type: 'death',
            message: 'Вы погибли! Возрождение через 5 секунд...'
          })
          selectedMonster.value = null
          setTimeout(() => {
            character.value.health = character.value.max_health
            messages.value.push({
              user: 'Система',
              text: 'Вы возродились в безопасной зоне'
            })
          }, 5000)
        }
      }

      // Если монстр убит
      if (!result.player_attack.monster_alive) {
        combatLog.value.push({
          type: 'victory',
          message: `${selectedMonster.value.name} повержен!`
        })

        if (result.rewards) {
          combatLog.value.push({
            type: 'reward',
            message: `Получено: ${result.rewards.experience} опыта, ${result.rewards.gold} золота`
          })

          // Обновляем характеристики персонажа
          character.value.experience = (character.value.experience || 0) + result.rewards.experience
          character.value.gold += result.rewards.gold
        }

        if (result.level_up) {
          combatLog.value.push({
            type: 'level-up',
            message: `Уровень повышен! Теперь уровень ${result.level_up.new_level}!`
          })
          character.value.level = result.level_up.new_level
        }

        // Удаляем монстра из списка
        monsters.value = monsters.value.filter(m => m.id !== selectedMonster.value.id)
        selectedMonster.value = null

        // Перерисовываем карту
        drawCanvas()
      }

      // Ограничиваем лог до 10 записей
      if (combatLog.value.length > 10) {
        combatLog.value = combatLog.value.slice(-10)
      }

    }
  } catch (error) {
    console.error('Ошибка атаки:', error)
    combatLog.value.push({
      type: 'error',
      message: 'Ошибка атаки!'
    })
  }
}

const drawCanvas = () => {
  const canvas = gameCanvas.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')

  // Очистка canvas
  ctx.fillStyle = '#2a2a2a'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  // Сетка
  ctx.strokeStyle = '#333'
  ctx.lineWidth = 1
  for (let x = 0; x < canvas.width; x += 50) {
    ctx.beginPath()
    ctx.moveTo(x, 0)
    ctx.lineTo(x, canvas.height)
    ctx.stroke()
  }
  for (let y = 0; y < canvas.height; y += 50) {
    ctx.beginPath()
    ctx.moveTo(0, y)
    ctx.lineTo(canvas.width, y)
    ctx.stroke()
  }

  // Отрисовка локаций (порталы)
  locations.value.forEach(location => {
    const isCurrentLocation = currentLocation.value && currentLocation.value.id === location.id

    // Круг локации
    ctx.beginPath()
    ctx.arc(location.x, location.y, 40, 0, Math.PI * 2)

    // Цвет в зависимости от типа локации
    if (location.is_safe_zone) {
      ctx.fillStyle = isCurrentLocation ? '#4a9a4a' : '#3a7a3a'
    } else {
      ctx.fillStyle = isCurrentLocation ? '#aa6644' : '#884422'
    }
    ctx.fill()

    // Рамка для текущей локации
    if (isCurrentLocation) {
      ctx.strokeStyle = '#ffff00'
      ctx.lineWidth = 3
      ctx.stroke()
    }

    // Название локации
    ctx.fillStyle = '#fff'
    ctx.font = 'bold 12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(location.name, location.x, location.y - 50)

    // Уровень радиации
    if (location.radiation_level > 0) {
      ctx.fillStyle = '#ff6666'
      ctx.font = '10px Arial'
      ctx.fillText(`☢️ ${location.radiation_level}`, location.x, location.y + 55)
    }
  })

  // Отрисовка монстров
  monsters.value.forEach(monster => {
    ctx.fillStyle = '#aa4444'
    ctx.fillRect(monster.x - 25, monster.y - 25, 50, 50)

    // Рамка для выбранного монстра
    if (selectedMonster.value && selectedMonster.value.id === monster.id) {
      ctx.strokeStyle = '#ff0000'
      ctx.lineWidth = 3
      ctx.strokeRect(monster.x - 27, monster.y - 27, 54, 54)
    }

    ctx.fillStyle = '#fff'
    ctx.font = '10px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(monster.name, monster.x, monster.y - 30)
    ctx.fillText(`Lv.${monster.level}`, monster.x, monster.y - 18)
  })

  // Отрисовка других игроков
  otherPlayers.value.forEach(player => {
    ctx.fillStyle = '#9a4a4a'
    ctx.fillRect(player.x - 25, player.y - 25, 50, 50)
    ctx.fillStyle = '#fff'
    ctx.font = '12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(player.name || 'Игрок', player.x, player.y - 30)
  })

  // Отрисовка текущего игрока
  ctx.fillStyle = '#4a9a4a'
  ctx.fillRect(playerX.value - 25, playerY.value - 25, 50, 50)

  if (character.value) {
    ctx.fillStyle = '#fff'
    ctx.font = '12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(character.value.name, playerX.value, playerY.value - 30)
  }
}

const handleCanvasClick = async (event) => {
  if (!character.value) return

  const canvas = gameCanvas.value
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  // Проверяем клик по локации (приоритет)
  for (const location of locations.value) {
    const dx = x - location.x
    const dy = y - location.y
    const distance = Math.sqrt(dx * dx + dy * dy)

    if (distance < 40) { // Радиус клика по локации
      await teleportToLocation(location)
      return
    }
  }

  // Проверяем клик по монстру
  let clickedMonster = null
  for (const monster of monsters.value) {
    const dx = x - monster.x
    const dy = y - monster.y
    const distance = Math.sqrt(dx * dx + dy * dy)

    if (distance < 30) { // Радиус клика по монстру
      clickedMonster = monster
      break
    }
  }

  if (clickedMonster) {
    // Выбираем монстра для боя
    selectedMonster.value = clickedMonster
    combatLog.value = [] // Очищаем лог боя
    drawCanvas()
    return
  }

  // Обновление позиции локально
  playerX.value = x
  playerY.value = y

  // Отправка на сервер
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/movement/characters/${character.value.id}/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ x: Math.floor(x), y: Math.floor(y) })
    })

    if (response.ok) {
      // Отправить движение через WebSocket другим игрокам
      websocketService.sendMove(character.value.id, Math.floor(x), Math.floor(y))
    }
  } catch (error) {
    console.error('Ошибка перемещения:', error)
  }

  drawCanvas()
}

onMounted(async () => {
  // Загрузка персонажей пользователя
  await characterStore.fetchCharacters()

  // Подключение к WebSocket
  const token = localStorage.getItem('token')
  if (token) {
    websocketService.connect(token)

    // Обработка входящих чат сообщений
    websocketService.on('chat', (data) => {
      messages.value.push({
        user: data.user,
        text: data.text
      })
    })

    // Обработка подключения пользователей
    websocketService.on('user_connected', (data) => {
      messages.value.push({
        user: 'Система',
        text: `${data.username} подключился к игре`
      })
    })

    // Обработка отключения пользователей
    websocketService.on('user_disconnected', (data) => {
      messages.value.push({
        user: 'Система',
        text: `${data.username} покинул игру`
      })
      // Удалить игрока из списка других игроков
      otherPlayers.value = otherPlayers.value.filter(p => p.user_id !== data.user_id)
      drawCanvas()
    })

    // Обработка движения других игроков
    websocketService.on('player_moved', (data) => {
      // Обновить или добавить игрока
      const playerIndex = otherPlayers.value.findIndex(p => p.character_id === data.character_id)
      if (playerIndex !== -1) {
        otherPlayers.value[playerIndex].x = data.x
        otherPlayers.value[playerIndex].y = data.y
      } else {
        otherPlayers.value.push({
          character_id: data.character_id,
          user_id: data.user_id,
          x: data.x,
          y: data.y,
          name: `Игрок ${data.user_id}`
        })
      }
      drawCanvas()
    })
  }

  // Инициализация Canvas
  drawCanvas()

  // Загрузка локаций
  await loadLocations()

  // Загрузка монстров для боевой системы
  if (character.value) {
    await loadMonsters()
  }
})

onUnmounted(() => {
  websocketService.disconnect()
})
</script>

<style scoped>
.game-view {
  min-height: 100vh;
  background-color: #1a1a1a;
  display: flex;
  flex-direction: column;
}

.game-header {
  background-color: #252525;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
}

.game-header h1 {
  color: #4a9a4a;
  font-size: 24px;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logout-btn {
  background-color: #555;
  padding: 8px 16px;
}

.logout-btn:hover {
  background-color: #666;
}

.game-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.character-panel {
  width: 300px;
  background-color: #252525;
  border-right: 1px solid #333;
  padding: 20px;
  overflow-y: auto;
}

.character-panel h2 {
  color: #4a9a4a;
  margin-bottom: 20px;
}

.no-character {
  text-align: center;
}

.character-list {
  margin-bottom: 15px;
}

.character-item {
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.character-item:hover {
  border-color: #4a9a4a;
  transform: translateX(5px);
}

.character-item.active {
  border-color: #4a9a4a;
  background-color: #2a3a2a;
}

.char-name {
  color: #fff;
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 4px;
}

.char-level {
  color: #888;
  font-size: 14px;
}

.create-btn {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  background-color: #3a7a3a;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.create-btn:hover {
  background-color: #4a9a4a;
}

.character-info {
  border-top: 1px solid #333;
  padding-top: 15px;
}

.character-info h3 {
  color: #4a9a4a;
  margin-bottom: 10px;
}

.stats {
  margin: 20px 0;
}

.stat {
  margin-bottom: 10px;
}

.bar {
  background-color: #333;
  height: 20px;
  border-radius: 4px;
  overflow: hidden;
  margin: 5px 0;
}

.bar-fill {
  background-color: #4a9a4a;
  height: 100%;
  transition: width 0.3s;
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 15px;
  font-size: 14px;
}

.resources {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #333;
}

.game-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.game-canvas {
  position: relative;
  margin-bottom: 20px;
}

canvas {
  border: 2px solid #333;
  border-radius: 4px;
  display: block;
}

.location-info {
  margin-top: 10px;
  font-size: 14px;
  color: #888;
}

.location-info p {
  margin: 5px 0;
}

.radiation-warning {
  color: #ff6666 !important;
  font-weight: bold;
}

.coordinates {
  color: #aaa;
  font-size: 12px;
}

.chat-panel {
  background-color: #252525;
  border: 1px solid #333;
  border-radius: 4px;
  height: 200px;
  display: flex;
  flex-direction: column;
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
  padding: 10px;
  border-top: 1px solid #333;
}

.chat-input input {
  flex: 1;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #252525;
  padding: 30px;
  border-radius: 8px;
  border: 1px solid #333;
  width: 100%;
  max-width: 400px;
}

.modal-content h2 {
  color: #4a9a4a;
  margin-bottom: 20px;
}

.error-message {
  color: #ff6666;
  padding: 10px;
  background-color: #2a1a1a;
  border-radius: 4px;
  margin-bottom: 10px;
  font-size: 14px;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.modal-buttons button {
  flex: 1;
}

/* Combat panel styles */
.combat-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #2a2a2a;
  border: 2px solid #aa4444;
  border-radius: 12px;
  padding: 25px;
  min-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
  z-index: 1000;
}

.combat-panel h3 {
  color: #ff6666;
  margin-bottom: 15px;
  text-align: center;
  font-size: 1.5em;
}

.monster-stats {
  margin-bottom: 20px;
}

.stat-bar {
  background-color: #1a1a1a;
  border-radius: 6px;
  padding: 10px 15px;
  margin-bottom: 8px;
}

.stat-bar span {
  color: #cccccc;
  font-size: 1.1em;
}

.monster-info {
  color: #aaaaaa;
  margin-bottom: 5px;
}

.combat-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.combat-actions button {
  flex: 1;
  padding: 12px 20px;
  font-size: 1.1em;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: bold;
}

.combat-actions button:first-child {
  background-color: #aa4444;
  color: white;
}

.combat-actions button:first-child:hover {
  background-color: #cc5555;
  transform: scale(1.05);
}

.combat-actions button:last-child {
  background-color: #555555;
  color: white;
}

.combat-actions button:last-child:hover {
  background-color: #666666;
}

.combat-log {
  max-height: 200px;
  overflow-y: auto;
  background-color: #1a1a1a;
  border-radius: 6px;
  padding: 12px;
}

.combat-log div {
  padding: 6px 0;
  border-bottom: 1px solid #333;
  font-size: 0.95em;
}

.combat-log div:last-child {
  border-bottom: none;
}

.combat-log .damage {
  color: #ff6666;
}

.combat-log .success {
  color: #66ff66;
}

.combat-log .info {
  color: #6666ff;
}

.combat-log .warning {
  color: #ffaa44;
}

.combat-log .death {
  color: #ff4444;
  font-weight: bold;
}
</style>
