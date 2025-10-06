<template>
  <div v-if="monster" class="combat-panel">
    <h3>Бой: {{ monster.name }}</h3>
    <div class="monster-stats">
      <div class="stat-bar">
        <span>HP: {{ monster.health }}/{{ monster.max_health }}</span>
        <div class="bar">
          <div class="bar-fill monster-hp" :style="{ width: (monster.health / monster.max_health * 100) + '%' }"></div>
        </div>
      </div>
      <p>Уровень: {{ monster.level }}</p>
    </div>
    <div class="combat-actions">
      <button @click="$emit('attack')" class="attack-btn">⚔️ Атаковать</button>
      <button @click="$emit('flee')" class="flee-btn">🏃 Отступить</button>
    </div>
    <div class="combat-log">
      <div v-for="(log, index) in combatLog" :key="index" class="log-entry" :class="log.type">
        {{ log.message }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  monster: Object,
  combatLog: Array
})

defineEmits(['attack', 'flee'])
</script>

<style scoped>
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

.bar {
  background-color: #333;
  height: 20px;
  border-radius: 10px;
  overflow: hidden;
  margin: 5px 0;
}

.bar-fill {
  height: 100%;
  transition: width 0.3s;
}

.monster-hp {
  background: linear-gradient(90deg, #aa4444, #cc5555);
}

.monster-stats p {
  color: #aaaaaa;
  margin: 5px 0;
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

.attack-btn {
  background-color: #aa4444;
  color: white;
}

.attack-btn:hover {
  background-color: #cc5555;
  transform: scale(1.05);
}

.flee-btn {
  background-color: #555555;
  color: white;
}

.flee-btn:hover {
  background-color: #666666;
}

.combat-log {
  max-height: 200px;
  overflow-y: auto;
  background-color: #1a1a1a;
  border-radius: 6px;
  padding: 12px;
}

.log-entry {
  padding: 6px 0;
  border-bottom: 1px solid #333;
  font-size: 0.95em;
}

.log-entry:last-child {
  border-bottom: none;
}

.log-entry.damage {
  color: #ff6666;
}

.log-entry.success {
  color: #66ff66;
}

.log-entry.info {
  color: #6666ff;
}

.log-entry.warning {
  color: #ffaa44;
}

.log-entry.death {
  color: #ff4444;
  font-weight: bold;
}
</style>
