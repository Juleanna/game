"""
Delete temporary locations from database
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / "database" / "timezero.db"

def cleanup():
    """Delete all temporary 'Position X,Y' locations"""
    print("Cleaning up temporary locations...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Find temporary locations
        cursor.execute("SELECT id, name FROM locations WHERE name LIKE 'Position %'")
        temp_locations = cursor.fetchall()

        if temp_locations:
            print(f"Found {len(temp_locations)} temporary locations:")
            for loc_id, name in temp_locations:
                print(f"  - {name}")

            # Delete them
            cursor.execute("DELETE FROM locations WHERE name LIKE 'Position %'")
            conn.commit()
            print(f"Deleted {len(temp_locations)} temporary locations!")
        else:
            print("No temporary locations found.")

        # Show remaining locations
        cursor.execute("SELECT id, name FROM locations ORDER BY id")
        locations = cursor.fetchall()
        print(f"\nRemaining locations ({len(locations)}):")
        for loc_id, name in locations:
            print(f"  {loc_id}: {name}")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    cleanup()
