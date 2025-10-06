<template>
  <div v-if="show" class="modal" @click.self="$emit('close')">
    <div class="character-info-modal">
      <div class="modal-header">
        <h2>{{ character?.name || 'Персонаж' }}</h2>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <div class="modal-body" v-if="character">
        <!-- Основная информация -->
        <div class="info-section">
          <div class="info-row">
            <span class="label">Пол:</span>
            <span class="value">{{ getGenderLabel(character.gender) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Профессия:</span>
            <span class="value">{{ getProfessionLabel(character.profession) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Уровень:</span>
            <span class="value">{{ character.level }}</span>
          </div>
        </div>

        <!-- Здоровье -->
        <div class="stat-section">
          <h3>Здоровье</h3>
          <div class="hp-bar">
            <div class="bar-fill" :style="{ width: (character.health / character.max_health * 100) + '%' }"></div>
          </div>
          <div class="hp-text">{{ character.health }} / {{ character.max_health }}</div>
        </div>

        <!-- Характеристики -->
        <div class="stat-section">
          <h3>Характеристики</h3>
          <div class="stat-grid">
            <div class="stat-item">
              <span class="stat-icon">💪</span>
              <span class="stat-name">Сила</span>
              <span class="stat-value">{{ character.strength }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🏃</span>
              <span class="stat-name">Ловкость</span>
              <span class="stat-value">{{ character.dexterity }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🧠</span>
              <span class="stat-name">Интеллект</span>
              <span class="stat-value">{{ character.intelligence }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">❤️</span>
              <span class="stat-name">Выносливость</span>
              <span class="stat-value">{{ character.endurance }}</span>
            </div>
          </div>
        </div>

        <!-- Ресурсы -->
        <div class="stat-section">
          <h3>Ресурсы</h3>
          <div class="resource-grid">
            <div class="resource-item">
              <span class="resource-icon">⭐</span>
              <span class="resource-name">Опыт</span>
              <span class="resource-value">{{ character.experience || 0 }}</span>
            </div>
            <div class="resource-item">
              <span class="resource-icon">💰</span>
              <span class="resource-name">Золото</span>
              <span class="resource-value">{{ character.gold }}</span>
            </div>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="action-buttons">
          <button @click="$emit('open-inventory')" class="action-btn inventory">
            🎒 Инвентарь
          </button>
          <button @click="$emit('open-equipment')" class="action-btn equipment">
            ⚔️ Экипировка
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({
  show: Boolean,
  character: Object
})

defineEmits(['close', 'open-inventory', 'open-equipment'])

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
</script>

<style scoped>
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
  z-index: 2000;
}

.character-info-modal {
  background-color: #1a1a1a;
  border-radius: 12px;
  border: 2px solid #4a9a4a;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
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
  color: #4a9a4a;
  margin: 0;
  font-size: 24px;
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
  padding: 25px;
  overflow-y: auto;
  flex: 1;
}

.info-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #333;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 15px;
}

.label {
  color: #888;
  font-weight: 500;
}

.value {
  color: #fff;
  font-weight: bold;
}

.stat-section {
  margin-bottom: 25px;
}

.stat-section h3 {
  color: #4a9a4a;
  font-size: 16px;
  margin: 0 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #333;
}

.hp-bar {
  background-color: #333;
  height: 24px;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.bar-fill {
  background: linear-gradient(90deg, #4a9a4a, #5aaa5a);
  height: 100%;
  transition: width 0.3s;
}

.hp-text {
  text-align: center;
  color: #ccc;
  font-size: 14px;
  font-weight: bold;
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-item {
  background-color: #252525;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #333;
}

.stat-icon {
  font-size: 24px;
}

.stat-name {
  color: #888;
  font-size: 13px;
  flex: 1;
}

.stat-value {
  color: #4a9a4a;
  font-size: 18px;
  font-weight: bold;
}

.resource-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.resource-item {
  background-color: #252525;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #333;
}

.resource-icon {
  font-size: 24px;
}

.resource-name {
  color: #888;
  font-size: 13px;
  flex: 1;
}

.resource-value {
  color: #aa9a6a;
  font-size: 18px;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #333;
}

.action-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.inventory {
  background-color: #5a7a5a;
  color: white;
}

.action-btn.inventory:hover {
  background-color: #6a9a6a;
  transform: translateY(-2px);
}

.action-btn.equipment {
  background-color: #7a6a5a;
  color: white;
}

.action-btn.equipment:hover {
  background-color: #9a8a6a;
  transform: translateY(-2px);
}
</style>
