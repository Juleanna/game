@echo off
chcp 65001 > nul
title TimeZero Game

echo 🎮 TimeZero - Запуск серверов...
echo.

:: Запуск backend
start "Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"

:: Ожидание 3 секунды
timeout /t 3 /nobreak > nul

:: Запуск frontend
start "Frontend" cmd /k "cd frontend && npm run dev"

echo ✅ Серверы запускаются!
echo 🌐 Откройте http://localhost:5173 в браузере
echo.
pause
