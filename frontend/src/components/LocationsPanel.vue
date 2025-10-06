<template>
  <aside class="locations-panel">
    <h3>Локации</h3>
    <div class="locations-list">
      <div
        v-for="loc in locations"
        :key="loc.id"
        :class="['location-item', { active: currentLocation && currentLocation.id === loc.id }]"
        @click="$emit('select-location', loc)"
      >
        <div class="loc-icon" :class="{ 'safe': loc.is_safe_zone, 'danger': !loc.is_safe_zone }">
          {{ loc.is_city ? '🏙️' : '🗺️' }}
        </div>
        <div class="loc-details">
          <div class="loc-name">{{ loc.name }}</div>
          <div class="loc-stats">
            <span v-if="loc.is_safe_zone" class="safe-tag">Безопасно</span>
            <span v-if="loc.radiation_level > 0" class="rad-tag">☢️ {{ loc.radiation_level }}</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  locations: Array,
  currentLocation: Object
})

defineEmits(['select-location'])
</script>

<style scoped>
.locations-panel {
  width: 280px;
  background-color: #252525;
  border-left: 1px solid #333;
  padding: 20px;
  overflow-y: auto;
}

.locations-panel h3 {
  color: #4a9a4a;
  margin: 0 0 15px 0;
  font-size: 18px;
}

.locations-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.location-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.location-item:hover {
  border-color: #4a9a4a;
  transform: translateX(3px);
}

.location-item.active {
  border-color: #4a9a4a;
  background-color: #2a3a2a;
}

.loc-icon {
  font-size: 28px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #333;
}

.loc-icon.safe {
  background-color: #3a5a3a;
}

.loc-icon.danger {
  background-color: #5a3a3a;
}

.loc-details {
  flex: 1;
}

.loc-name {
  color: #fff;
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 4px;
}

.loc-stats {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.safe-tag {
  background-color: #3a5a3a;
  color: #6aaa6a;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.rad-tag {
  background-color: #5a3a3a;
  color: #ff6666;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}
</style>
