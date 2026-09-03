import test
 # this can be expanded to have more or less inputed values (will mark with a +/- for spots that this can be done)   
def get_all_results(): # get all avalible results from table 
    conn = test.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM detections")
   
    results = cursor.fetchall()

    conn.close()
    return results

print(get_all_results())

def get_result_by_id(detection_id): # get one result from the table. detection_id will be set by streamlit by user input/click
    conn = test.get_connection()
    cursor = conn.cursor()

    cursor.execute( "SELECT * FROM detections where id =?",(detection_id,))

    result = cursor.fetchone()

    conn.close()
    return result

def add_result(filename,species): # (+/-) add data from model to table. to add more passed data put the traits wanted in order of the table in database 
    conn = test.get_connection()
    cursor = conn.cursor()

    cursor.execute( """INSERT INTO detections (filename,species) VALUES (?,?)""",(filename,species)) # (+/-) same as passed values, add more ? to VALUES and put the added traits after species

    conn.commit()
    conn.close()

    
def delete_result(detection_id):
    conn = test.get_connection()
    cursor = conn.cursor()

    cursor.execute (" DELETE FROM detections where id =?",(detection_id,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted # will be used for streamlit to diplay message if table was deleted or not 



def results_by_filter():
    conn = test.get_connection()
    cursor = conn.cursor()
    
