#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "═══════════════════════════════════════════════════════════"
echo "  🎮 TimeZero - Постапокалиптическая MMORPG"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python не найден! Установите Python 3.11+ и попробуйте снова.${NC}"
    exit 1
fi

# Проверка Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js не найден! Установите Node.js и попробуйте снова.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python найден:${NC}"
python3 --version
echo -e "${GREEN}✅ Node.js найден:${NC}"
node --version
echo ""

# Создание виртуального окружения
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}📦 Создание виртуального окружения для backend...${NC}"
    cd backend
    python3 -m venv venv
    cd ..
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
    echo ""
fi

# Установка зависимостей backend
if [ ! -d "backend/venv/lib" ]; then
    echo -e "${YELLOW}📦 Установка зависимостей backend...${NC}"
    cd backend
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo -e "${GREEN}✅ Зависимости backend установлены${NC}"
    echo ""
fi

# Установка зависимостей frontend
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Установка зависимостей frontend...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✅ Зависимости frontend установлены${NC}"
    echo ""
fi

# Проверка базы данных
if [ ! -f "database/timezero.db" ]; then
    echo -e "${YELLOW}🌱 База данных не найдена. Запуск seed скрипта...${NC}"
    cd backend
    source venv/bin/activate
    python seed_data.py
    cd ..
    echo -e "${GREEN}✅ База данных заполнена${NC}"
    echo ""
else
    echo -e "${GREEN}✅ База данных найдена${NC}"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"
echo "  🚀 Запуск серверов..."
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}📌 Backend будет доступен на: http://localhost:8000${NC}"
echo -e "${BLUE}📌 Frontend будет доступен на: http://localhost:5173${NC}"
echo -e "${BLUE}📌 API документация: http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}⚠️  Для остановки серверов нажмите Ctrl+C${NC}"
echo ""

# Функция для очистки процессов при выходе
cleanup() {
    echo ""
    echo "🛑 Остановка серверов..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Запуск backend
cd backend
source venv/bin/activate
echo "🔧 Backend сервер запускается..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Ожидание запуска backend
sleep 3

# Запуск frontend
cd frontend
echo "🎨 Frontend сервер запускается..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ Серверы запущены!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🌐 Откройте браузер и перейдите на http://localhost:5173"
echo ""
echo "📝 Полезные команды:"
echo "   - Регистрация: создайте новый аккаунт"
echo "   - Создание персонажа: выберите профессию из 14 доступных"
echo "   - Начните игру в Новой Москве!"
echo ""
echo "🎮 Приятной игры!"
echo ""

# Ожидание завершения
wait
