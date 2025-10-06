"""
Add tilemap field to locations table
"""
import sqlite3
import json
from pathlib import Path

db_path = Path(__file__).parent.parent / "database" / "timezero.db"

# Типы тайлов
TILE_GRASS = 0      # Трава
TILE_ROAD = 1       # Дорога
TILE_BUILDING = 2   # Здание
TILE_WATER = 3      # Вода
TILE_WASTELAND = 4  # Пустошь
TILE_RADIATION = 5  # Радиация

def generate_tilemap(location_type, radiation_level):
    """Генерация тайлмапа 20x15 в зависимости от типа локации"""
    width, height = 20, 15
    tilemap = []

    if location_type == "city":
        # Город - больше зданий и дорог
        for y in range(height):
            row = []
            for x in range(width):
                if x % 5 == 0 or y % 4 == 0:
                    row.append(TILE_ROAD)
                elif (x + y) % 3 == 0:
                    row.append(TILE_BUILDING)
                else:
                    row.append(TILE_GRASS)
            tilemap.append(row)

    elif location_type == "wasteland":
        # Пустошь - пустыня с радиацией
        for y in range(height):
            row = []
            for x in range(width):
                if radiation_level > 5 and (x + y) % 4 == 0:
                    row.append(TILE_RADIATION)
                else:
                    row.append(TILE_WASTELAND)
            tilemap.append(row)

    elif location_type == "industrial":
        # Промзона - здания и пустошь
        for y in range(height):
            row = []
            for x in range(width):
                if (x % 4 == 0 and y % 3 == 0):
                    row.append(TILE_BUILDING)
                elif (x + y) % 5 == 0:
                    row.append(TILE_ROAD)
                else:
                    row.append(TILE_WASTELAND)
            tilemap.append(row)

    else:
        # По умолчанию - смешанная местность
        for y in range(height):
            row = []
            for x in range(width):
                if (x + y) % 6 == 0:
                    row.append(TILE_WATER)
                elif (x % 3 == 0):
                    row.append(TILE_ROAD)
                else:
                    row.append(TILE_GRASS)
            tilemap.append(row)

    return tilemap

def migrate():
    """Add tilemap field and generate maps for existing locations"""
    print("Starting tilemap migration...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if tilemap column exists
        cursor.execute("PRAGMA table_info(locations)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'tilemap' not in columns:
            # Add tilemap column
            cursor.execute("""
                ALTER TABLE locations
                ADD COLUMN tilemap TEXT DEFAULT '[]'
            """)
            print("Column 'tilemap' added successfully")

        # Generate tilemaps for existing locations
        cursor.execute("SELECT id, name, radiation_level, is_city FROM locations")
        locations = cursor.fetchall()

        for loc_id, name, radiation_level, is_city in locations:
            # Determine location type
            if is_city:
                loc_type = "city"
            elif "завод" in name.lower() or "метро" in name.lower():
                loc_type = "industrial"
            elif "пустошь" in name.lower():
                loc_type = "wasteland"
            else:
                loc_type = "default"

            # Generate tilemap
            tilemap = generate_tilemap(loc_type, radiation_level)
            tilemap_json = json.dumps(tilemap)

            # Update location
            cursor.execute(
                "UPDATE locations SET tilemap = ? WHERE id = ?",
                (tilemap_json, loc_id)
            )
            print(f"Generated tilemap for: {name}")

        conn.commit()
        print("Tilemap migration completed successfully!")

    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
