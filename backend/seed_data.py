"""
Скрипт для заполнения базы данных начальными данными
Запуск: python seed_data.py
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.location import Location
from app.models.monster import Monster
from app.models.npc import NPC, NPCType
from app.models.item import Item, ItemType, ItemRarity


def create_locations(db: Session):
    """Создание начальных локаций"""
    print("📍 Создание локаций...")

    locations = [
        Location(
            id=1,
            name="Новая Москва",
            x=400,
            y=300,
            radiation_level=0,
            is_safe_zone=True,
            is_city=True,
        ),
        Location(
            id=2,
            name="Заброшенный завод",
            x=600,
            y=200,
            radiation_level=3,
            is_safe_zone=False,
            is_city=False,
        ),
        Location(
            id=3,
            name="Радиоактивная пустошь",
            x=700,
            y=400,
            radiation_level=8,
            is_safe_zone=False,
            is_city=False,
        ),
        Location(
            id=4,
            name="Торговый форпост",
            x=300,
            y=150,
            radiation_level=1,
            is_safe_zone=True,
            is_city=True,
        ),
        Location(
            id=5,
            name="Старое метро",
            x=500,
            y=500,
            radiation_level=5,
            is_safe_zone=False,
            is_city=False,
        ),
    ]

    for location in locations:
        existing = db.query(Location).filter(Location.id == location.id).first()
        if not existing:
            db.add(location)

    db.commit()
    print(f"✅ Создано {len(locations)} локаций")


def create_monsters(db: Session):
    """Создание начальных монстров"""
    print("👹 Создание монстров...")

    monsters = [
        # Новая Москва - безопасная зона (мелкие монстры)
        Monster(
            name="Мутировавшая крыса",
            level=1,
            location_id=1,
            health=30,
            max_health=30,
            damage=5,
            defense=2,
            experience_reward=20,
            gold_reward=5,
            x=420,
            y=320,
            is_aggressive=0,
        ),
        Monster(
            name="Бродячая собака",
            level=2,
            location_id=1,
            health=50,
            max_health=50,
            damage=8,
            defense=3,
            experience_reward=30,
            gold_reward=8,
            x=380,
            y=280,
            is_aggressive=0,
        ),

        # Заброшенный завод - средний уровень
        Monster(
            name="Мутант-рабочий",
            level=5,
            location_id=2,
            health=120,
            max_health=120,
            damage=15,
            defense=8,
            experience_reward=100,
            gold_reward=25,
            x=620,
            y=220,
            is_aggressive=1,
        ),
        Monster(
            name="Ржавый андроид",
            level=6,
            location_id=2,
            health=150,
            max_health=150,
            damage=18,
            defense=12,
            experience_reward=120,
            gold_reward=30,
            x=580,
            y=180,
            is_aggressive=1,
        ),
        Monster(
            name="Химический зомби",
            level=7,
            location_id=2,
            health=180,
            max_health=180,
            damage=20,
            defense=10,
            experience_reward=140,
            gold_reward=35,
            x=640,
            y=240,
            is_aggressive=1,
        ),

        # Радиоактивная пустошь - высокий уровень
        Monster(
            name="Радиоактивный мутант",
            level=10,
            location_id=3,
            health=300,
            max_health=300,
            damage=35,
            defense=20,
            experience_reward=250,
            gold_reward=60,
            x=720,
            y=420,
            is_aggressive=1,
        ),
        Monster(
            name="Гигантский скорпион",
            level=12,
            location_id=3,
            health=400,
            max_health=400,
            damage=45,
            defense=25,
            experience_reward=300,
            gold_reward=80,
            x=680,
            y=380,
            is_aggressive=1,
        ),

        # Старое метро - средний-высокий уровень
        Monster(
            name="Подземный хищник",
            level=8,
            location_id=5,
            health=200,
            max_health=200,
            damage=25,
            defense=15,
            experience_reward=160,
            gold_reward=40,
            x=520,
            y=480,
            is_aggressive=1,
        ),
        Monster(
            name="Туннельный демон",
            level=9,
            location_id=5,
            health=250,
            max_health=250,
            damage=30,
            defense=18,
            experience_reward=200,
            gold_reward=50,
            x=480,
            y=520,
            is_aggressive=1,
        ),
    ]

    for monster in monsters:
        db.add(monster)

    db.commit()
    print(f"✅ Создано {len(monsters)} монстров")


def create_npcs(db: Session):
    """Создание NPC"""
    print("🧙 Создание NPC...")

    npcs = [
        NPC(
            name="Торговец Иван",
            npc_type=NPCType.TRADER,
            location_id=1,
            level=5,
            health=200,
            max_health=200,
            is_trader=True,
            gold=5000,
            dialogue="Приветствую, странник! У меня есть всё необходимое для выживания.",
        ),
        NPC(
            name="Старейшина Михаил",
            npc_type=NPCType.QUEST_GIVER,
            location_id=1,
            level=10,
            health=300,
            max_health=300,
            is_trader=False,
            gold=100,
            dialogue="У меня есть важное задание для храброго путника...",
        ),
        NPC(
            name="Страж Алексей",
            npc_type=NPCType.GUARD,
            location_id=1,
            level=8,
            health=350,
            max_health=350,
            is_trader=False,
            gold=50,
            dialogue="Я охраняю этот город от мутантов. Будь осторожен за его пределами!",
        ),
        NPC(
            name="Торговец оружием Петр",
            npc_type=NPCType.TRADER,
            location_id=4,
            level=6,
            health=180,
            max_health=180,
            is_trader=True,
            gold=10000,
            dialogue="Лучшее оружие в пустоши! Не пожалеешь!",
        ),
        NPC(
            name="Механик Сергей",
            npc_type=NPCType.TRADER,
            location_id=2,
            level=7,
            health=150,
            max_health=150,
            is_trader=True,
            gold=3000,
            dialogue="Могу починить любую технику. За разумную цену, конечно.",
        ),
    ]

    for npc in npcs:
        db.add(npc)

    db.commit()
    print(f"✅ Создано {len(npcs)} NPC")


def create_items(db: Session):
    """Создание предметов"""
    print("⚔️ Создание предметов...")

    items = [
        # Оружие
        Item(
            name="Ржавый нож",
            description="Старый нож, покрытый ржавчиной",
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.COMMON,
            weight=0.5,
            value=10,
            damage=5,
            required_level=1,
        ),
        Item(
            name="Охотничий нож",
            description="Острый нож для охоты",
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.UNCOMMON,
            weight=0.7,
            value=50,
            damage=12,
            required_level=3,
        ),
        Item(
            name="Пистолет Макарова",
            description="Надёжное оружие времён СССР",
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.RARE,
            weight=1.0,
            value=200,
            damage=25,
            required_level=5,
            required_dexterity=15,
        ),
        Item(
            name="Автомат Калашникова",
            description="Легендарное оружие",
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.EPIC,
            weight=3.5,
            value=800,
            damage=45,
            required_level=10,
            required_strength=20,
        ),
        Item(
            name="Плазменная винтовка",
            description="Экспериментальное энергетическое оружие",
            item_type=ItemType.WEAPON,
            rarity=ItemRarity.LEGENDARY,
            weight=4.0,
            value=3000,
            damage=80,
            required_level=20,
            required_intelligence=25,
        ),

        # Броня
        Item(
            name="Кожаная куртка",
            description="Простая защита от ветра",
            item_type=ItemType.ARMOR,
            rarity=ItemRarity.COMMON,
            weight=2.0,
            value=20,
            defense=3,
            required_level=1,
        ),
        Item(
            name="Бронежилет",
            description="Защита от пуль и осколков",
            item_type=ItemType.ARMOR,
            rarity=ItemRarity.UNCOMMON,
            weight=8.0,
            value=150,
            defense=15,
            required_level=5,
        ),
        Item(
            name="Силовая броня",
            description="Продвинутая боевая экипировка",
            item_type=ItemType.ARMOR,
            rarity=ItemRarity.EPIC,
            weight=25.0,
            value=2000,
            defense=40,
            required_level=15,
            required_endurance=30,
        ),

        # Расходники
        Item(
            name="Аптечка",
            description="Восстанавливает 50 HP",
            item_type=ItemType.CONSUMABLE,
            rarity=ItemRarity.COMMON,
            weight=0.5,
            value=25,
            health_restore=50,
            max_stack=10,
        ),
        Item(
            name="Большая аптечка",
            description="Восстанавливает 150 HP",
            item_type=ItemType.CONSUMABLE,
            rarity=ItemRarity.UNCOMMON,
            weight=1.0,
            value=75,
            health_restore=150,
            max_stack=5,
        ),
        Item(
            name="Стимпак",
            description="Полностью восстанавливает здоровье",
            item_type=ItemType.CONSUMABLE,
            rarity=ItemRarity.RARE,
            weight=0.3,
            value=200,
            health_restore=500,
            max_stack=3,
        ),

        # Ресурсы
        Item(
            name="Металлолом",
            description="Годится для крафта",
            item_type=ItemType.RESOURCE,
            rarity=ItemRarity.COMMON,
            weight=2.0,
            value=5,
            max_stack=50,
        ),
        Item(
            name="Электронные компоненты",
            description="Ценные детали для ремонта",
            item_type=ItemType.RESOURCE,
            rarity=ItemRarity.UNCOMMON,
            weight=0.5,
            value=30,
            max_stack=20,
        ),
    ]

    for item in items:
        existing = db.query(Item).filter(Item.name == item.name).first()
        if not existing:
            db.add(item)

    db.commit()
    print(f"✅ Создано {len(items)} предметов")


def seed_database():
    """Главная функция заполнения БД"""
    print("=" * 50)
    print("🌱 Начало заполнения базы данных")
    print("=" * 50)

    # Создание таблиц
    Base.metadata.create_all(bind=engine)

    # Создание сессии
    db = SessionLocal()

    try:
        create_locations(db)
        create_monsters(db)
        create_npcs(db)
        create_items(db)

        print("=" * 50)
        print("✅ База данных успешно заполнена!")
        print("=" * 50)
        print("\n📊 Статистика:")
        print(f"  Локаций: {db.query(Location).count()}")
        print(f"  Монстров: {db.query(Monster).count()}")
        print(f"  NPC: {db.query(NPC).count()}")
        print(f"  Предметов: {db.query(Item).count()}")
        print("\n🎮 Теперь можно запускать игру!")

    except Exception as e:
        print(f"❌ Ошибка при заполнении БД: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
