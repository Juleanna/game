<template>
  <div v-if="show" class="modal" @click.self="$emit('close')">
    <div class="equipment-modal">
      <div class="modal-header">
        <h2>Экипировка {{ character?.name }}</h2>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <div class="modal-body">
        <!-- Визуализация персонажа в центре -->
        <div class="character-display">
          <div class="character-silhouette">
            <div class="gender-icon">
              {{ character?.gender === 'male' ? '👤' : character?.gender === 'female' ? '👩' : '🧑' }}
            </div>
          </div>
        </div>

        <!-- Слоты экипировки вокруг персонажа -->
        <div class="equipment-layout">
          <!-- Шлем (сверху) -->
          <div class="slot-position top">
            <div
              class="equipment-slot helmet"
              @drop="onDrop($event, 'helmet')"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getEquippedItem('helmet')"
                   class="item-card equipped"
                   draggable="true"
                   @dragstart="onDragStart($event, getEquippedItem('helmet'))"
                   @click="showItemTooltip(getEquippedItem('helmet'))">
                <div class="item-icon" :class="getRarityClass(getEquippedItem('helmet'))">
                  ⛑️
                </div>
                <div class="item-label">{{ getEquippedItem('helmet').item.name }}</div>
              </div>
              <div v-else class="empty-slot">
                <span class="slot-icon">⛑️</span>
                <span class="slot-label">Шлем</span>
              </div>
            </div>
          </div>

          <!-- Оружие (слева) -->
          <div class="slot-position left">
            <div
              class="equipment-slot weapon"
              @drop="onDrop($event, 'weapon')"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getEquippedItem('weapon')"
                   class="item-card equipped"
                   draggable="true"
                   @dragstart="onDragStart($event, getEquippedItem('weapon'))"
                   @click="showItemTooltip(getEquippedItem('weapon'))">
                <div class="item-icon" :class="getRarityClass(getEquippedItem('weapon'))">
                  ⚔️
                </div>
                <div class="item-label">{{ getEquippedItem('weapon').item.name }}</div>
              </div>
              <div v-else class="empty-slot">
                <span class="slot-icon">⚔️</span>
                <span class="slot-label">Оружие</span>
              </div>
            </div>
          </div>

          <!-- Броня (справа) -->
          <div class="slot-position right">
            <div
              class="equipment-slot armor"
              @drop="onDrop($event, 'armor')"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getEquippedItem('armor')"
                   class="item-card equipped"
                   draggable="true"
                   @dragstart="onDragStart($event, getEquippedItem('armor'))"
                   @click="showItemTooltip(getEquippedItem('armor'))">
                <div class="item-icon" :class="getRarityClass(getEquippedItem('armor'))">
                  🛡️
                </div>
                <div class="item-label">{{ getEquippedItem('armor').item.name }}</div>
              </div>
              <div v-else class="empty-slot">
                <span class="slot-icon">🛡️</span>
                <span class="slot-label">Броня</span>
              </div>
            </div>
          </div>

          <!-- Перчатки (слева внизу) -->
          <div class="slot-position bottom-left">
            <div
              class="equipment-slot gloves"
              @drop="onDrop($event, 'gloves')"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getEquippedItem('gloves')"
                   class="item-card equipped"
                   draggable="true"
                   @dragstart="onDragStart($event, getEquippedItem('gloves'))"
                   @click="showItemTooltip(getEquippedItem('gloves'))">
                <div class="item-icon" :class="getRarityClass(getEquippedItem('gloves'))">
                  🧤
                </div>
                <div class="item-label">{{ getEquippedItem('gloves').item.name }}</div>
              </div>
              <div v-else class="empty-slot">
                <span class="slot-icon">🧤</span>
                <span class="slot-label">Перчатки</span>
              </div>
            </div>
          </div>

          <!-- Ботинки (справа внизу) -->
          <div class="slot-position bottom-right">
            <div
              class="equipment-slot boots"
              @drop="onDrop($event, 'boots')"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getEquippedItem('boots')"
                   class="item-card equipped"
                   draggable="true"
                   @dragstart="onDragStart($event, getEquippedItem('boots'))"
                   @click="showItemTooltip(getEquippedItem('boots'))">
                <div class="item-icon" :class="getRarityClass(getEquippedItem('boots'))">
                  👢
                </div>
                <div class="item-label">{{ getEquippedItem('boots').item.name }}</div>
              </div>
              <div v-else class="empty-slot">
                <span class="slot-icon">👢</span>
                <span class="slot-label">Ботинки</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Тултип предмета -->
        <div v-if="selectedItem" class="item-tooltip">
          <div class="tooltip-header" :class="getRarityClass(selectedItem)">
            {{ selectedItem.item.name }}
          </div>
          <div class="tooltip-body">
            <p class="item-type">{{ getItemTypeLabel(selectedItem.item.item_type) }}</p>
            <p v-if="selectedItem.item.description" class="item-description">{{ selectedItem.item.description }}</p>
            <div class="item-stats">
              <p v-if="selectedItem.item.damage > 0">⚔️ Урон: +{{ selectedItem.item.damage }}</p>
              <p v-if="selectedItem.item.defense > 0">🛡️ Защита: +{{ selectedItem.item.defense }}</p>
              <p v-if="selectedItem.item.strength_bonus > 0">💪 Сила: +{{ selectedItem.item.strength_bonus }}</p>
              <p v-if="selectedItem.item.dexterity_bonus > 0">🏃 Ловкость: +{{ selectedItem.item.dexterity_bonus }}</p>
              <p v-if="selectedItem.item.intelligence_bonus > 0">🧠 Интеллект: +{{ selectedItem.item.intelligence_bonus }}</p>
              <p v-if="selectedItem.item.endurance_bonus > 0">❤️ Выносливость: +{{ selectedItem.item.endurance_bonus }}</p>
            </div>
            <p class="item-level">Требуется уровень: {{ selectedItem.item.level_required }}</p>
            <div class="tooltip-actions">
              <button @click="$emit('unequip-item', selectedItem)" class="unequip-btn">
                Снять
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: Boolean,
  character: Object,
  inventoryItems: Array
})

const emit = defineEmits(['close', 'equip-item', 'unequip-item'])

const selectedItem = ref(null)
const draggedItem = ref(null)

const getEquippedItem = (itemType) => {
  return props.inventoryItems?.find(item =>
    item.is_equipped && item.item.item_type === itemType
  )
}

const getRarityClass = (item) => {
  if (!item || !item.item) return ''
  return `rarity-${item.item.rarity.toLowerCase()}`
}

const getItemTypeLabel = (type) => {
  const labels = {
    'weapon': 'Оружие',
    'armor': 'Броня',
    'helmet': 'Шлем',
    'boots': 'Ботинки',
    'gloves': 'Перчатки',
    'consumable': 'Расходуемое',
    'quest': 'Квестовый предмет'
  }
  return labels[type] || type
}

const showItemTooltip = (item) => {
  selectedItem.value = item
}

const onDragStart = (event, item) => {
  draggedItem.value = item
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('itemId', item.id)
}

const onDrop = (event, itemType) => {
  event.preventDefault()

  if (!draggedItem.value) return

  // Экипировка предмета
  if (draggedItem.value.item.item_type === itemType) {
    emit('equip-item', draggedItem.value)
  }

  draggedItem.value = null
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2100;
}

.equipment-modal {
  background-color: #1a1a1a;
  border-radius: 12px;
  border: 2px solid #7a6a5a;
  width: 90%;
  max-width: 650px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background-color: #252525;
  border-bottom: 2px solid #333;
}

.modal-header h2 {
  color: #9a8a6a;
  margin: 0;
  font-size: 22px;
}

.close-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #333;
  color: #fff;
}

.modal-body {
  padding: 30px;
  overflow-y: auto;
  flex: 1;
  position: relative;
}

.equipment-layout {
  position: relative;
  width: 100%;
  height: 450px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.character-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
}

.character-silhouette {
  width: 180px;
  height: 250px;
  background: linear-gradient(180deg, #252525, #1a1a1a);
  border: 2px solid #333;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.gender-icon {
  font-size: 100px;
  opacity: 0.3;
}

.slot-position {
  position: absolute;
  z-index: 2;
}

.slot-position.top {
  top: 0;
  left: 50%;
  transform: translateX(-50%);
}

.slot-position.left {
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.slot-position.right {
  top: 50%;
  right: 0;
  transform: translateY(-50%);
}

.slot-position.bottom-left {
  bottom: 20px;
  left: 60px;
}

.slot-position.bottom-right {
  bottom: 20px;
  right: 60px;
}

.equipment-slot {
  background-color: #252525;
  border: 2px solid #444;
  border-radius: 10px;
  padding: 12px;
  min-width: 140px;
  min-height: 90px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.equipment-slot:hover {
  border-color: #9a8a6a;
  background-color: #2a2a2a;
  transform: scale(1.05);
}

.empty-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  opacity: 0.4;
  text-align: center;
}

.slot-icon {
  font-size: 36px;
}

.slot-label {
  color: #888;
  font-size: 12px;
  font-weight: bold;
}

.item-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: grab;
  text-align: center;
}

.item-card:active {
  cursor: grabbing;
}

.item-icon {
  font-size: 40px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #333;
  border-radius: 8px;
  border: 3px solid #444;
  transition: all 0.2s;
}

.item-card:hover .item-icon {
  transform: scale(1.1);
}

.item-label {
  color: #fff;
  font-weight: bold;
  font-size: 13px;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rarity-common .item-icon { border-color: #888; }
.rarity-uncommon .item-icon { border-color: #4a9a4a; }
.rarity-rare .item-icon { border-color: #4a6a9a; }
.rarity-epic .item-icon { border-color: #9a4a9a; }
.rarity-legendary .item-icon { border-color: #aa7a3a; }

.item-tooltip {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 280px;
  background-color: #1a1a1a;
  border: 2px solid #9a8a6a;
  border-radius: 8px;
  overflow: hidden;
  z-index: 1000;
}

.tooltip-header {
  padding: 12px 15px;
  font-weight: bold;
  font-size: 15px;
  border-bottom: 2px solid #333;
}

.tooltip-header.rarity-common { background-color: #3a3a3a; color: #aaa; }
.tooltip-header.rarity-uncommon { background-color: #2a4a2a; color: #6aaa6a; }
.tooltip-header.rarity-rare { background-color: #2a3a5a; color: #6a8aaa; }
.tooltip-header.rarity-epic { background-color: #4a2a5a; color: #aa6aaa; }
.tooltip-header.rarity-legendary { background-color: #5a4a2a; color: #aa9a6a; }

.tooltip-body {
  padding: 15px;
}

.item-type {
  color: #888;
  font-size: 12px;
  margin: 0 0 8px 0;
}

.item-description {
  color: #ccc;
  font-size: 12px;
  margin: 0 0 12px 0;
  font-style: italic;
}

.item-stats {
  margin: 12px 0;
}

.item-stats p {
  color: #6aaa6a;
  font-size: 12px;
  margin: 4px 0;
}

.item-level {
  color: #aa6a6a;
  font-size: 12px;
  margin: 8px 0;
}

.tooltip-actions {
  margin-top: 12px;
}

.unequip-btn {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  background-color: #9a6a4a;
  color: white;
  transition: all 0.2s;
}

.unequip-btn:hover {
  background-color: #aa7a5a;
  transform: translateY(-2px);
}
</style>
