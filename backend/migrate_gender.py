"""
Migracija dlja dobavlenija polja gender v tablicu characters
"""
import sqlite3
from pathlib import Path

# Put' k baze dannyh
db_path = Path(__file__).parent.parent / "database" / "timezero.db"

def migrate():
    """Dobavlenie polja gender v tablicu characters"""
    print("Nachalo migracii bazy dannyh...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Proveryaem, sushhestvuet li uzhe kolonka gender
        cursor.execute("PRAGMA table_info(characters)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'gender' in columns:
            print("Kolonka 'gender' uzhe sushhestvuet")
        else:
            # Dobavljaem kolonku gender
            cursor.execute("""
                ALTER TABLE characters
                ADD COLUMN gender TEXT DEFAULT 'male'
            """)
            print("Kolonka 'gender' uspeshno dobavlena")

        conn.commit()
        print("Migracija zavershena uspeshno!")

    except Exception as e:
        print(f"Oshibka migracii: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
