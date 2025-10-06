<template>
  <aside class="character-panel">
    <h2>Персонажи</h2>
    <div v-if="characters.length === 0" class="no-character">
      <p>У вас нет персонажей</p>
      <button @click="$emit('create-character')">Создать персонажа</button>
    </div>
    <div v-else>
      <div class="character-list">
        <div
          v-for="char in characters"
          :key="char.id"
          :class="['character-item', { active: currentCharacter && currentCharacter.id === char.id }]"
          @click="$emit('select-character', char)"
        >
          <div class="char-name">{{ char.name }}</div>
          <div class="char-level">Ур. {{ char.level }}</div>
        </div>
      </div>
      <button v-if="characters.length < 3" @click="$emit('create-character')" class="create-btn">
        + Создать персонажа
      </button>

    </div>
  </aside>
</template>

<script setup>
defineProps({
  characters: Array,
  currentCharacter: Object
})

defineEmits(['create-character', 'select-character'])
</script>

<style scoped>
.character-panel {
  width: 240px;
  min-width: 200px;
  background-color: #252525;
  border-right: 1px solid #333;
  padding: 15px;
  overflow-y: auto;
  flex-shrink: 0;
}

.character-panel h2 {
  color: #4a9a4a;
  margin-bottom: 15px;
  font-size: 18px;
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
  border-radius: 6px;
  padding: 10px;
  margin-bottom: 8px;
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

</style>
