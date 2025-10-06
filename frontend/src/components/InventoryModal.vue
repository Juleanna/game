<template>
  <div v-if="show" class="modal inventory-modal">
    <div class="inventory-container">
      <div class="inventory-header">
        <h2>Инвентарь</h2>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <div class="inventory-content">
        <!-- Инвентарь - только сетка -->
        <div class="inventory-grid-container">
          <h3>Предметы ({{ inventoryItems.filter(i => !i.is_equipped).length }}/40)</h3>
          <div class="inventory-grid">
            <div
              v-for="index in 40"
              :key="index"
              :class="['inventory-slot']"
              @drop="onDrop($event, index - 1, false)"
              @dragover.prevent
              @dragenter.prevent
            >
              <div v-if="getItemAtSlot(index - 1)"
                   class="item-card"
                   draggable="true"
                   @dragstart="onDragStart($event, getItemAtSlot(index - 1))"
                   @click="showItemTooltip(getItemAtSlot(index - 1))">
                <div class="item-icon" :class="getRarityClass(getItemAtSlot(index - 1))">
                  {{ getItemIcon(getItemAtSlot(index - 1).item.item_type) }}
                </div>
                <div class="item-quantity" v-if="getItemAtSlot(index - 1).quantity > 1">
                  {{ getItemAtSlot(index - 1).quantity }}
                </div>
              </div>
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
          <p class="item-value">Цена: {{ selectedItem.item.value }} золота</p>
          <div class="tooltip-actions">
            <button v-if="!selectedItem.is_equipped" @click="$emit('equip-item', selectedItem)" class="equip-btn">
              Экипировать
            </button>
            <button v-else @click="$emit('unequip-item', selectedItem)" class="unequip-btn">
              Снять
            </button>
            <button @click="$emit('delete-item', selectedItem)" class="delete-btn">
              Выбросить
            </button>
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
  inventoryItems: Array
})

const emit = defineEmits(['close', 'equip-item', 'unequip-item', 'delete-item', 'move-item'])

const selectedItem = ref(null)
const draggedItem = ref(null)

const getItemAtSlot = (position) => {
  return props.inventoryItems.find(item => item.slot_position === position && !item.is_equipped)
}

const getItemIcon = (itemType) => {
  const icons = {
    'weapon': '⚔️',
    'armor': '🛡️',
    'helmet': '⛑️',
    'boots': '👢',
    'gloves': '🧤',
    'consumable': '🧪',
    'quest': '📜'
  }
  return icons[itemType] || '📦'
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

const onDrop = (event, target, isEquipmentSlot) => {
  event.preventDefault()

  if (!draggedItem.value) return

  if (isEquipmentSlot) {
    // Экипировка предмета
    if (draggedItem.value.item.item_type === target) {
      emit('equip-item', draggedItem.value)
    }
  } else {
    // Перемещение в инвентаре
    emit('move-item', draggedItem.value, target)
  }

  draggedItem.value = null
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.inventory-container {
  background-color: #1a1a1a;
  border-radius: 12px;
  width: 70%;
  max-width: 700px;
  max-height: 70vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.inventory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background-color: #252525;
  border-bottom: 2px solid #333;
}

.inventory-header h2 {
  color: #4a9a4a;
  margin: 0;
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

.inventory-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.item-card {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: grab;
}

.item-card:active {
  cursor: grabbing;
}

.item-card.equipped {
  border-left: 3px solid #4a9a4a;
  padding-left: 9px;
}

.item-icon {
  font-size: 32px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #333;
  border-radius: 6px;
  border: 2px solid #444;
}

.item-name {
  color: #fff;
  font-weight: bold;
  font-size: 14px;
  flex: 1;
}

.rarity-common .item-icon { border-color: #888; }
.rarity-uncommon .item-icon { border-color: #4a9a4a; }
.rarity-rare .item-icon { border-color: #4a6a9a; }
.rarity-epic .item-icon { border-color: #9a4a9a; }
.rarity-legendary .item-icon { border-color: #aa7a3a; }

.inventory-grid-container {
  flex: 1;
}

.inventory-grid-container h3 {
  color: #4a9a4a;
  margin: 0 0 20px 0;
}

.inventory-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 6px;
}

.inventory-slot {
  aspect-ratio: 1;
  background-color: #252525;
  border: 2px solid #333;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.2s;
}

.inventory-slot:hover {
  border-color: #4a9a4a;
  background-color: #2a2a2a;
}

.inventory-slot .item-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.inventory-slot .item-icon {
  width: 40px;
  height: 40px;
  font-size: 24px;
}

.item-quantity {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background-color: #000;
  color: #fff;
  font-size: 11px;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 3px;
}

.item-tooltip {
  position: absolute;
  right: 30px;
  top: 50%;
  transform: translateY(-50%);
  width: 300px;
  background-color: #1a1a1a;
  border: 2px solid #4a9a4a;
  border-radius: 8px;
  overflow: hidden;
  z-index: 1000;
}

.tooltip-header {
  padding: 12px 15px;
  font-weight: bold;
  font-size: 16px;
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
  font-size: 13px;
  margin: 0 0 10px 0;
}

.item-description {
  color: #ccc;
  font-size: 13px;
  margin: 0 0 15px 0;
  font-style: italic;
}

.item-stats {
  margin: 15px 0;
}

.item-stats p {
  color: #6aaa6a;
  font-size: 13px;
  margin: 5px 0;
}

.item-level {
  color: #aa6a6a;
  font-size: 13px;
  margin: 10px 0 5px 0;
}

.item-value {
  color: #aa9a6a;
  font-size: 13px;
  margin: 5px 0;
}

.tooltip-actions {
  display: flex;
  gap: 8px;
  margin-top: 15px;
}

.tooltip-actions button {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  transition: all 0.2s;
}

.equip-btn {
  background-color: #4a9a4a;
  color: white;
}

.equip-btn:hover {
  background-color: #5aaa5a;
}

.unequip-btn {
  background-color: #9a6a4a;
  color: white;
}

.unequip-btn:hover {
  background-color: #aa7a5a;
}

.delete-btn {
  background-color: #9a4a4a;
  color: white;
}

.delete-btn:hover {
  background-color: #aa5a5a;
}
</style>
