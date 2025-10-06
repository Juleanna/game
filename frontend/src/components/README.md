# Компоненты игры TimeZero

## Структура компонентов

### CharacterPanel.vue
**Описание**: Панель персонажей слева
- Список всех персонажей пользователя (до 3-х)
- Информация о текущем персонаже (статы, здоровье, опыт, золото)
- Кнопка создания персонажа
- Кнопка открытия инвентаря

**Props**:
- `characters` (Array) - список персонажей
- `currentCharacter` (Object) - текущий персонаж

**Events**:
- `create-character` - создание нового персонажа
- `select-character` - выбор персонажа
- `open-inventory` - открытие инвентаря

---

### GameCanvas.vue
**Описание**: Основная игровая область с canvas
- Отрисовка Tilemap карт локаций
- Отрисовка монстров
- Отрисовка других игроков
- Отрисовка текущего игрока

**Props**:
- `currentLocation` (Object) - текущая локация
- `monsters` (Array) - список монстров
- `otherPlayers` (Array) - другие игроки
- `playerX`, `playerY` (Number) - координаты игрока
- `character` (Object) - текущий персонаж
- `selectedMonster` (Object) - выбранный монстр

**Events**:
- `canvas-click` - клик по canvas
- `monster-click` - клик по монстру
- `location-click` - клик по локации

**Methods**:
- `drawCanvas()` - перерисовка canvas (exposed)

---

### LocationsPanel.vue
**Описание**: Панель локаций справа
- Список всех доступных локаций
- Отображение текущей локации
- Иконки и статусы локаций (безопасность, радиация)

**Props**:
- `locations` (Array) - список локаций
- `currentLocation` (Object) - текущая локация

**Events**:
- `select-location` - выбор локации

---

### ChatPanel.vue
**Описание**: Панель чата внизу
- История сообщений
- Поле ввода сообщения
- Отправка сообщений

**Props**:
- `messages` (Array) - список сообщений

**Events**:
- `send-message` - отправка сообщения

---

### CombatPanel.vue
**Описание**: Модальная панель боя (центр экрана)
- Информация о монстре (здоровье, уровень)
- Кнопки действий (атаковать, отступить)
- Лог боя

**Props**:
- `monster` (Object) - монстр в бою
- `combatLog` (Array) - лог боевых действий

**Events**:
- `attack` - атаковать
- `flee` - отступить

---

### InventoryModal.vue
**Описание**: Модальное окно инвентаря
- Слоты экипировки (5 слотов)
- Сетка инвентаря (40 слотов)
- Drag & Drop для перемещения предметов
- Тултип с информацией о предмете
- Действия: экипировать, снять, выбросить

**Props**:
- `show` (Boolean) - показывать/скрывать
- `inventoryItems` (Array) - предметы в инвентаре

**Events**:
- `close` - закрыть инвентарь
- `equip-item` - экипировать предмет
- `unequip-item` - снять предмет
- `delete-item` - удалить предмет
- `move-item` - переместить предмет

---

## Использование

```vue
<template>
  <div class="game-view">
    <CharacterPanel
      :characters="characters"
      :currentCharacter="currentCharacter"
      @create-character="showCreateModal = true"
      @select-character="selectCharacter"
      @open-inventory="showInventory = true"
    />

    <GameCanvas
      :currentLocation="currentLocation"
      :monsters="monsters"
      :otherPlayers="otherPlayers"
      :playerX="playerX"
      :playerY="playerY"
      :character="currentCharacter"
      :selectedMonster="selectedMonster"
      @monster-click="onMonsterClick"
      @canvas-click="onCanvasClick"
    />

    <LocationsPanel
      :locations="locations"
      :currentLocation="currentLocation"
      @select-location="selectLocation"
    />

    <ChatPanel
      :messages="messages"
      @send-message="sendChatMessage"
    />

    <CombatPanel
      :monster="selectedMonster"
      :combatLog="combatLog"
      @attack="attackMonster"
      @flee="selectedMonster = null"
    />

    <InventoryModal
      :show="showInventory"
      :inventoryItems="inventoryItems"
      @close="showInventory = false"
      @equip-item="equipItem"
      @unequip-item="unequipItem"
      @delete-item="deleteItem"
      @move-item="moveItem"
    />
  </div>
</template>
```

## Преимущества разделения

1. **Модульность** - каждый компонент отвечает за одну функцию
2. **Переиспользование** - компоненты можно использовать в других частях приложения
3. **Тестирование** - легче тестировать отдельные компоненты
4. **Читаемость** - код проще понять и поддерживать
5. **Производительность** - компоненты обновляются независимо
