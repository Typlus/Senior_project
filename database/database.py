
import sqlite3

DB_NAME = "detections.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            species TEXT
        )
    """)
    conn.commit()
    conn.close()

# this is for testing if the table is corretly made
```
#def test_database():
#    conn = get_connection()
 #   cursor = conn.cursor()

 #   cursor.execute(""" INSERT INTO detections (filename, species) VALUES (?,?)""",("dolphin001.wav", "Dolphin"))
##   conn.commit()

#    cursor.execute("SELECT * FROM detections")
 #   results = cursor.fetchall()

 #   print(results)

#    conn.close()

if __name__ == "__main__":
    create_tables()
    test_database()
  
