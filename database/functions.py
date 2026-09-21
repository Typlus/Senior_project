import database
 # this can be expanded to have more or less inputed values (will mark with a +/- for spots that this can be done)   
def get_all_results(): # get all avalible results from table 
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detections")
   
    results = cursor.fetchall()

    conn.close()
    return results

print(get_all_results())

def get_result_by_id(detection_id): # get one result from the table. detection_id will be set by streamlit by user input/click
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM detections where id =?",(detection_id,))

    result = cursor.fetchone()

    conn.close()
    if result:
        return {
            "id": result[0],
            "species": result[1],
            "filename": result[2],
            "confidence": result[3]
        }
        

    return None

def add_result(filename,species): # (+/-) add data from model to table. to add more passed data put the traits wanted in order of the table in database 
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute( """INSERT INTO detections (filename,species) VALUES (?,?)""",(filename,species)) # (+/-) same as passed values, add more ? to VALUES and put the added traits after species

    conn.commit()
    conn.close()

    
def delete_result(detection_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute (" DELETE FROM detections where id =?",(detection_id,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted # will be used for streamlit to diplay message if table was deleted or not 



def results_by_filter(Q1,Q2):
    conn = database.get_connection()
    cursor = conn.cursor() 
    if not Q1:
         cursor.execute("""
            SELECT * FROM detections
            WHERE confidence >= ?
        """, (Q2,))
    else:
        placeholders = ",".join("?" for _ in Q1)
        query = f"""SELECT * FROM detections where species IN ({placeholders}) AND confidence >= ?"""

        cursor.execute(query,(*Q1,Q2))

    results = cursor.fetchall()
    conn.close()

    return results

def add_demo_data():
    conn = database.get_connection()
    cursor = conn.cursor()

    demo_data = [
        ("Dolphin", "dolphin001.wav", 95),
        ("Dolphin", "dolphin002.wav", 82),
        ("Dolphin", "dolphin003.wav", 67),
        ("Whale", "whale001.wav", 91),
        ("Whale", "whale002.wav", 76),
        ("Whale", "whale003.wav", 54),
        ("Fish", "fish001.wav", 88),
        ("Fish", "fish002.wav", 72),
        ("Fish", "fish003.wav", 43),
        ("Otter", "otter001.wav", 96),
        ("Otter", "otter002.wav", 81),
        ("Otter", "otter003.wav", 62),
        ("Dolphin", "dolphin004.wav", 74),
        ("Whale", "whale004.wav", 69),
        ("Fish", "fish004.wav", 97)
    ]

    cursor.executemany("""
        INSERT INTO detections (species, filename, Confidence)
        VALUES (?, ?, ?)
    """, demo_data)

    conn.commit()
    conn.close()



def clear_database():
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM detections")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='detections'")

    conn.commit()
    conn.close()
