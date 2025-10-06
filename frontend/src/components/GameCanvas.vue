<template>
  <div class="game-canvas-container">
    <div class="location-info-top">
      <h3 v-if="currentLocation">{{ currentLocation.name }}</h3>
      <p v-if="currentLocation && currentLocation.radiation_level > 0" class="radiation-warning">
        ☢️ Радиация: {{ currentLocation.radiation_level }}
      </p>
    </div>
    <canvas ref="canvas" width="800" height="600" @click="handleClick"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  currentLocation: Object,
  monsters: Array,
  otherPlayers: Array,
  playerX: Number,
  playerY: Number,
  character: Object,
  selectedMonster: Object
})

const emit = defineEmits(['canvas-click', 'monster-click', 'location-click'])

const canvas = ref(null)

const getTileColor = (tileType) => {
  const colors = {
    0: '#5a8a5a', // Grass
    1: '#666666', // Road
    2: '#8a6a4a', // Building
    3: '#4a6a8a', // Water
    4: '#8a7a5a', // Wasteland
    5: '#aa4444'  // Radiation
  }
  return colors[tileType] || '#333333'
}

const drawCanvas = () => {
  const canvasEl = canvas.value
  if (!canvasEl) return

  const ctx = canvasEl.getContext('2d')

  // Очистка canvas
  ctx.fillStyle = '#1a1a1a'
  ctx.fillRect(0, 0, canvasEl.width, canvasEl.height)

  // Отрисовка Tilemap текущей локации
  if (props.currentLocation && props.currentLocation.tilemap) {
    try {
      const tilemap = JSON.parse(props.currentLocation.tilemap)
      const tileWidth = canvasEl.width / 20
      const tileHeight = canvasEl.height / 15

      for (let y = 0; y < tilemap.length; y++) {
        for (let x = 0; x < tilemap[y].length; x++) {
          const tileType = tilemap[y][x]
          ctx.fillStyle = getTileColor(tileType)
          ctx.fillRect(x * tileWidth, y * tileHeight, tileWidth, tileHeight)

          ctx.strokeStyle = '#00000033'
          ctx.lineWidth = 0.5
          ctx.strokeRect(x * tileWidth, y * tileHeight, tileWidth, tileHeight)
        }
      }
    } catch (e) {
      console.error('Ошибка парсинга tilemap:', e)
    }
  }

  // Отрисовка монстров
  props.monsters.forEach(monster => {
    ctx.fillStyle = '#aa4444'
    ctx.fillRect(monster.x - 25, monster.y - 25, 50, 50)

    if (props.selectedMonster && props.selectedMonster.id === monster.id) {
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
  props.otherPlayers.forEach(player => {
    ctx.fillStyle = '#9a4a4a'
    ctx.fillRect(player.x - 25, player.y - 25, 50, 50)
    ctx.fillStyle = '#fff'
    ctx.font = '12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(player.name || 'Игрок', player.x, player.y - 30)
  })

  // Отрисовка текущего игрока
  ctx.fillStyle = '#4a9a4a'
  ctx.fillRect(props.playerX - 25, props.playerY - 25, 50, 50)

  if (props.character) {
    ctx.fillStyle = '#fff'
    ctx.font = 'bold 12px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(props.character.name, props.playerX, props.playerY - 30)
  }
}

const handleClick = (event) => {
  const rect = canvas.value.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  // Проверяем клик по монстру
  for (const monster of props.monsters) {
    const dx = x - monster.x
    const dy = y - monster.y
    const distance = Math.sqrt(dx * dx + dy * dy)

    if (distance < 30) {
      emit('monster-click', monster)
      return
    }
  }

  emit('canvas-click', { x, y })
}

// Перерисовка при изменении данных
watch(() => [props.currentLocation, props.monsters, props.otherPlayers, props.playerX, props.playerY, props.selectedMonster], () => {
  drawCanvas()
}, { deep: true })

onMounted(() => {
  drawCanvas()
})

defineExpose({
  drawCanvas
})
</script>

<style scoped>
.game-canvas-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  padding-bottom: 0;
}

.location-info-top {
  background-color: #252525;
  border: 1px solid #333;
  border-radius: 4px;
  padding: 10px 15px;
  margin-bottom: 10px;
}

.location-info-top h3 {
  color: #4a9a4a;
  margin: 0 0 5px 0;
  font-size: 18px;
}

.location-info-top p {
  margin: 0;
  font-size: 13px;
}

.radiation-warning {
  color: #ff6666 !important;
  font-weight: bold;
}

canvas {
  border: 2px solid #333;
  border-radius: 4px;
  display: block;
  cursor: crosshair;
}
</style>
