# TimeZero - Постапокалиптическая MMORPG

Браузерная многопользовательская игра в стиле TimeZero с постапокалиптическим миром.

> 🚀 **Быстрый старт:** Запустите `start.bat` (Windows) или `./start.sh` (Linux/Mac)
>
> 📖 **Новичкам:** Читайте [QUICKSTART.md](QUICKSTART.md)

## Технологии

### Backend
- Python 3.11+
- FastAPI (REST API + WebSocket)
- SQLAlchemy (ORM)
- SQLite/PostgreSQL
- JWT аутентификация

### Frontend
- Vue 3 + Vite
- Pinia (state management)
- Canvas API для игровой карты
- WebSocket клиент

## Структура проекта

```
.
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── models/   # Модели базы данных
│   │   ├── routes/   # API endpoints
│   │   ├── core/     # Конфигурация, безопасность
│   │   └── services/ # Бизнес-логика
│   └── main.py
├── frontend/         # Vue 3 frontend
│   └── src/
│       ├── components/
│       ├── views/
│       ├── stores/
│       └── services/
└── database/         # Файлы БД
```

## 🚀 Быстрый запуск

### Автоматический запуск (рекомендуется)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

Скрипт автоматически:
- Проверит наличие Python и Node.js
- Создаст виртуальное окружение
- Установит все зависимости
- Заполнит базу данных (если пуста)
- Запустит backend и frontend серверы

### Ручной запуск

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python seed_data.py  # Заполнение БД (первый раз)
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### После запуска

Откройте браузер: **http://localhost:5173**

- Backend API: http://localhost:8000
- API документация: http://localhost:8000/docs

## Игровые механики

- 14 профессий персонажей
- Система боя (PvE и PvP)
- Карта мира с локациями
- Система предметов (оружие, броня)
- Квесты
- Фракции
- Чат и взаимодействие игроков
