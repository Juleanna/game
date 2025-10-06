<template>
  <div class="game-view">
    <header class="game-header">
      <h1>TimeZero</h1>
      <div class="user-info">
        <button @click="showSettings = true" class="settings-btn" title="Настройки">⚙️</button>
        <span>{{ authStore.user?.username || 'Игрок' }}</span>
        <button @click="handleLogout" class="logout-btn">Выйти</button>
      </div>
    </header>

    <div class="game-container">
      <div class="top-panels">
        <!-- Панель персонажа слева -->
        <CharacterPanel
          :characters="characterStore.characters"
          :current-character="character"
          @create-character="showCreateCharacter = true"
          @select-character="selectCharacter"
        />

        <!-- Центральная область с картой -->
        <GameCanvas
          ref="gameCanvasRef"
          :current-location="currentLocation"
          :monsters="monsters"
          :other-players="otherPlayers"
          :player-x="playerX"
          :player-y="playerY"
          :character="character"
          :selected-monster="selectedMonster"
          @monster-click="onMonsterClick"
          @canvas-click="handleCanvasClick"
        />

        <!-- Панель локаций справа -->
        <LocationsPanel
          :locations="locations"
          :current-location="currentLocation"
          @select-location="selectLocation"
        />

        <!-- Боевая панель -->
        <CombatPanel
          v-if="selectedMonster"
          :monster="selectedMonster"
          :combat-log="combatLog"
          @attack="attackMonster"
          @flee="selectedMonster = null"
        />
      </div>

      <!-- Чат внизу под всеми панелями -->
      <ChatPanel
        :messages="messages"
        @send-message="sendMessage"
      />
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

    <!-- Модальное окно настроек -->
    <div v-if="showSettings" class="modal">
      <div class="modal-content settings-modal">
        <h2>Настройки</h2>
        <div class="settings-section">
          <h3>Горячие клавиши</h3>
          <div class="hotkey-list">
            <div class="hotkey-item">
              <span class="hotkey-label">Информация о персонаже:</span>
              <span class="hotkey-key">C</span>
            </div>
            <div class="hotkey-item">
              <span class="hotkey-label">Инвентарь:</span>
              <span class="hotkey-key">I</span>
            </div>
            <div class="hotkey-item">
              <span class="hotkey-label">Закрыть модальные окна:</span>
              <span class="hotkey-key">Escape</span>
            </div>
          </div>
        </div>
        <div class="modal-buttons">
          <button type="button" @click="showSettings = false">Закрыть</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно персонажа -->
    <CharacterModal
      :show="showCharacterModal"
      :character="character"
      @close="showCharacterModal = false"
    />

    <!-- Модальное окно инвентаря -->
    <InventoryModal
      :show="showInventory"
      :inventory-items="inventoryItems"
      @close="showInventory = false"
      @equip-item="equipItem"
      @unequip-item="unequipItem"
      @delete-item="deleteItem"
      @move-item="moveItemToSlot"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCharacterStore } from '../stores/character'
import websocketService from '../services/websocket'
import CharacterPanel from '../components/CharacterPanel.vue'
import CharacterModal from '../components/CharacterModal.vue'
import GameCanvas from '../components/GameCanvas.vue'
import LocationsPanel from '../components/LocationsPanel.vue'
import ChatPanel from '../components/ChatPanel.vue'
import CombatPanel from '../components/CombatPanel.vue'
import InventoryModal from '../components/InventoryModal.vue'

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

const messages = ref([
  { user: 'Система', text: 'Добро пожаловать в TimeZero!' }
])

const gameCanvasRef = ref(null)
const playerX = ref(400)
const playerY = ref(300)
const otherPlayers = ref([])
const monsters = ref([])
const selectedMonster = ref(null)
const combatLog = ref([])
const locations = ref([])
const currentLocation = ref(null)

// Модальные окна
const showSettings = ref(false)
const showCharacterModal = ref(false)
const showInventory = ref(false)
const inventoryItems = ref([])

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
  if (gameCanvasRef.value) {
    gameCanvasRef.value.drawCanvas()
  }
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

const sendMessage = (message) => {
  if (message.trim()) {
    // Отправка через WebSocket
    websocketService.sendChat(message)
  }
}

// Функции инвентаря
const openInventory = async () => {
  await loadInventory()
  showInventory.value = true
}

const loadInventory = async () => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/inventory/characters/${character.value.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      inventoryItems.value = await response.json()
    }
  } catch (error) {
    console.error('Ошибка загрузки инвентаря:', error)
  }
}

const equipItem = async (item) => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/inventory/characters/${character.value.id}/equip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        slot_id: item.id,
        equip: true
      })
    })

    if (response.ok) {
      await loadInventory()
      await characterStore.fetchCharacters()
    }
  } catch (error) {
    console.error('Ошибка экипировки:', error)
  }
}

const unequipItem = async (item) => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/inventory/characters/${character.value.id}/equip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        slot_id: item.id,
        equip: false
      })
    })

    if (response.ok) {
      await loadInventory()
      await characterStore.fetchCharacters()
    }
  } catch (error) {
    console.error('Ошибка снятия экипировки:', error)
  }
}

const moveItemToSlot = async (item, newPosition) => {
  if (!character.value) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/inventory/characters/${character.value.id}/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        slot_id: item.id,
        new_position: newPosition
      })
    })

    if (response.ok) {
      await loadInventory()
    }
  } catch (error) {
    console.error('Ошибка перемещения предмета:', error)
  }
}

const deleteItem = async (item) => {
  if (!character.value || !confirm('Вы уверены, что хотите выбросить этот предмет?')) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:8000/inventory/characters/${character.value.id}/slots/${item.id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.ok) {
      await loadInventory()
      await characterStore.fetchCharacters()
    }
  } catch (error) {
    console.error('Ошибка удаления предмета:', error)
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
      if (character.value && character.value.location_id) {
        currentLocation.value = locations.value.find(loc => loc.id === character.value.location_id) || locations.value[0]
      } else if (locations.value.length > 0) {
        currentLocation.value = locations.value[0]
      }

      if (gameCanvasRef.value) {
        gameCanvasRef.value.drawCanvas()
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки локаций:', error)
  }
}

const selectLocation = async (location) => {
  if (!character.value) return

  currentLocation.value = location
  await teleportToLocation(location)
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
      if (gameCanvasRef.value) {
        gameCanvasRef.value.drawCanvas()
      }
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
      if (gameCanvasRef.value) {
        gameCanvasRef.value.drawCanvas()
      }

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
        if (gameCanvasRef.value) {
          gameCanvasRef.value.drawCanvas()
        }
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

const onMonsterClick = (monster) => {
  selectedMonster.value = monster
  combatLog.value = []
}

const handleCanvasClick = async (event) => {
  if (!character.value) return

  const canvas = gameCanvasRef.value.$refs.canvas
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  // Проверяем клик по локации (приоритет)
  for (const location of locations.value) {
    const dx = x - location.x
    const dy = y - location.y
    const distance = Math.sqrt(dx * dx + dy * dy)

    if (distance < 40) {
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

    if (distance < 30) {
      clickedMonster = monster
      break
    }
  }

  if (clickedMonster) {
    onMonsterClick(clickedMonster)
  }
}

// Обработчик клавиатуры для горячих клавиш
const handleKeyPress = async (event) => {
  // Игнорируем нажатия в полях ввода
  if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
    return
  }

  // C - открыть информацию о персонаже
  if (event.key === 'c' || event.key === 'C' || event.key === 'с' || event.key === 'С') {
    if (character.value) {
      showCharacterModal.value = !showCharacterModal.value
    }
  }

  // I - открыть инвентарь
  if (event.key === 'i' || event.key === 'I' || event.key === 'ш' || event.key === 'Ш') {
    if (character.value) {
      if (!showInventory.value) {
        await loadInventory()
      }
      showInventory.value = !showInventory.value
    }
  }

  // Escape - закрыть все модальные окна
  if (event.key === 'Escape') {
    showSettings.value = false
    showCharacterModal.value = false
    showInventory.value = false
  }
}

onMounted(async () => {
  // Загрузка персонажей пользователя
  await characterStore.fetchCharacters()

  // Добавляем обработчик горячих клавиш
  window.addEventListener('keydown', handleKeyPress)

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
      if (gameCanvasRef.value) {
        gameCanvasRef.value.drawCanvas()
      }
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
      if (gameCanvasRef.value) {
        gameCanvasRef.value.drawCanvas()
      }
    })
  }

  // Загрузка локаций
  await loadLocations()

  // Загрузка монстров для боевой системы
  if (character.value) {
    await loadMonsters()
  }
})

onUnmounted(() => {
  // Удаляем обработчик горячих клавиш
  window.removeEventListener('keydown', handleKeyPress)

  websocketService.disconnect()
})
</script>

<style scoped>
.game-view {
  height: 100vh;
  width: 100vw;
  background-color: #1a1a1a;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.game-header {
  background-color: #252525;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #333;
  flex-shrink: 0;
  height: 50px;
}

.game-header h1 {
  color: #4a9a4a;
  font-size: 20px;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.settings-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.settings-btn:hover {
  background-color: #333;
  color: #4a9a4a;
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
  flex-direction: column;
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

.top-panels {
  display: flex;
  flex: 1;
  overflow: hidden;
  min-height: 0;
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

.settings-modal {
  max-width: 500px;
}

.settings-section {
  margin-bottom: 20px;
}

.settings-section h3 {
  color: #4a9a4a;
  margin-bottom: 15px;
  font-size: 18px;
}

.hotkey-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hotkey-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #1a1a1a;
  border-radius: 6px;
  border: 1px solid #333;
}

.hotkey-label {
  color: #ccc;
  font-size: 14px;
}

.hotkey-key {
  background-color: #333;
  color: #4a9a4a;
  padding: 6px 12px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
  font-weight: bold;
  border: 1px solid #444;
  min-width: 60px;
  text-align: center;
}
</style>
