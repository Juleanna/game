from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routes import auth, characters, websocket, movement, combat, locations, inventory

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TimeZero API", version="1.0.0")

# CORS для Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(auth.router)
app.include_router(characters.router)
app.include_router(websocket.router)
app.include_router(movement.router)
app.include_router(combat.router)
app.include_router(locations.router)
app.include_router(inventory.router)


@app.get("/")
async def root():
    return {
        "message": "TimeZero API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
