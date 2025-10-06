<template>
  <div v-if="show" class="modal character-modal">
    <div class="character-container">
      <div class="character-header">
        <h2>Информация о персонаже</h2>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <div v-if="character" class="character-content">
        <div class="character-main">
          <h3>{{ character.name }}</h3>
          <div class="character-details">
            <p><strong>Пол:</strong> {{ getGenderLabel(character.gender) }}</p>
            <p><strong>Профессия:</strong> {{ getProfessionLabel(character.profession) }}</p>
            <p><strong>Уровень:</strong> {{ character.level }}</p>
          </div>

          <div class="stats">
            <h4>Здоровье</h4>
            <div class="stat">
              <div class="bar">
                <div class="bar-fill health" :style="{ width: (character.health / character.max_health * 100) + '%' }"></div>
              </div>
              <span>{{ character.health }} / {{ character.max_health }}</span>
            </div>

            <h4>Характеристики</h4>
            <div class="stat-grid">
              <div class="stat-item">
                <span class="stat-icon">💪</span>
                <span class="stat-label">Сила:</span>
                <span class="stat-value">{{ character.strength }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-icon">🏃</span>
                <span class="stat-label">Ловкость:</span>
                <span class="stat-value">{{ character.dexterity }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-icon">🧠</span>
                <span class="stat-label">Интеллект:</span>
                <span class="stat-value">{{ character.intelligence }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-icon">❤️</span>
                <span class="stat-label">Выносливость:</span>
                <span class="stat-value">{{ character.endurance }}</span>
              </div>
            </div>

            <h4>Ресурсы</h4>
            <div class="resources">
              <div class="resource-item">
                <span class="resource-icon">⭐</span>
                <span class="resource-label">Опыт:</span>
                <span class="resource-value">{{ character.experience }}</span>
              </div>
              <div class="resource-item">
                <span class="resource-icon">💰</span>
                <span class="resource-label">Золото:</span>
                <span class="resource-value">{{ character.gold }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-character">
        <p>Персонаж не выбран</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  character: Object
})

defineEmits(['close'])

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
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.character-container {
  background-color: #1a1a1a;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.character-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background-color: #252525;
  border-bottom: 2px solid #333;
}

.character-header h2 {
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

.character-content {
  padding: 30px;
  overflow-y: auto;
  flex: 1;
}

.character-main h3 {
  color: #4a9a4a;
  font-size: 24px;
  margin: 0 0 20px 0;
}

.character-details {
  background-color: #252525;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.character-details p {
  color: #ccc;
  margin: 10px 0;
  font-size: 15px;
}

.character-details strong {
  color: #4a9a4a;
  margin-right: 10px;
}

.stats h4 {
  color: #4a9a4a;
  margin: 25px 0 15px 0;
  font-size: 18px;
}

.stat {
  margin-bottom: 10px;
}

.stat span {
  color: #ccc;
  font-size: 14px;
  display: block;
  margin-top: 5px;
}

.bar {
  background-color: #333;
  height: 24px;
  border-radius: 12px;
  overflow: hidden;
  margin: 8px 0;
}

.bar-fill {
  height: 100%;
  transition: width 0.3s;
}

.bar-fill.health {
  background: linear-gradient(90deg, #4a9a4a, #6aaa6a);
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background-color: #252525;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-icon {
  font-size: 20px;
}

.stat-label {
  color: #888;
  font-size: 14px;
  flex: 1;
}

.stat-value {
  color: #4a9a4a;
  font-weight: bold;
  font-size: 16px;
}

.resources {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.resource-item {
  background-color: #252525;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.resource-icon {
  font-size: 20px;
}

.resource-label {
  color: #888;
  font-size: 14px;
  flex: 1;
}

.resource-value {
  color: #aa9a6a;
  font-weight: bold;
  font-size: 16px;
}

.no-character {
  padding: 40px;
  text-align: center;
  color: #888;
}
</style>
