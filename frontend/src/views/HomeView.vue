<template>
  <div class="home">
    <div class="hero">
      <h1>TimeZero</h1>
      <p class="subtitle">Постапокалиптическая MMORPG</p>
      <p class="description">
        Добро пожаловать в мир после ядерной войны. Выживайте в радиоактивной пустоши,
        сражайтесь с мутантами, исследуйте разрушенные города и создайте своего уникального персонажа.
      </p>
      <div class="buttons">
        <router-link to="/register">
          <button class="btn-primary">Начать игру</button>
        </router-link>
        <router-link to="/login">
          <button class="btn-secondary">Войти</button>
        </router-link>
      </div>
    </div>

    <div class="features">
      <div class="feature">
        <h3>14 Профессий</h3>
        <p>Выберите свой путь: от наёмника до псионика</p>
      </div>
      <div class="feature">
        <h3>Огромный мир</h3>
        <p>Тысячи локаций для исследования</p>
      </div>
      <div class="feature">
        <h3>PvP и PvE</h3>
        <p>Сражайтесь с монстрами и другими игроками</p>
      </div>
      <div class="feature">
        <h3>Система фракций</h3>
        <p>Присоединяйтесь к одной из враждующих сторон</p>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
}

.hero {
  text-align: center;
  padding: 100px 20px 60px;
}

h1 {
  font-size: 72px;
  color: #4a9a4a;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.subtitle {
  font-size: 24px;
  color: #888;
  margin-bottom: 30px;
}

.description {
  max-width: 600px;
  margin: 0 auto 40px;
  font-size: 16px;
  line-height: 1.6;
  color: #ccc;
}

.buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn-primary {
  background-color: #4a9a4a;
  padding: 15px 40px;
  font-size: 18px;
}

.btn-primary:hover {
  background-color: #5aaa5a;
}

.btn-secondary {
  background-color: #555;
  padding: 15px 40px;
  font-size: 18px;
}

.btn-secondary:hover {
  background-color: #666;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.feature {
  background-color: #252525;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #333;
}

.feature h3 {
  color: #4a9a4a;
  margin-bottom: 10px;
  font-size: 20px;
}

.feature p {
  color: #aaa;
  font-size: 14px;
}
</style>
