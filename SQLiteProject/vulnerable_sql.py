import sqlite3

#Probes DB for vulnerablilities and attempts to extract all users
def get_user_credentials(username, db = 'test.db'):
    try: 
        print(f"SQLite3: Attempting to connect to {db} ...") #Debug  
        db_connection = sqlite3.connect(db) #attempt to connect to db
        print(f"SQLite3: Established connection to {db}! ") #Debug
        

        print(f"\nSQLite3: Initializing cursor ...") #Debug
        db_cursor = db_connection.cursor() #creates cursor
        print(f"SQLite3: Cursor initialized!") #Debug

        #check for vulnerable query in db
        probe_query1 = f"select * from users where username ='{username}'"
        #probe_query2 = f"SELECT * FROM users WHERE username = ?"

        print(f"\nExecuting Query: {probe_query1}") #DEBUG

        db_cursor.execute(probe_query1)

        #if successful, collects all user data
        probe_result = db_cursor.fetchall() #returns list of tuples or an empty list
        if len(probe_result) > 0:
            print(f"Extraction Successful!\n")

        #close connection
        db_connection.close()
        return probe_result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        #close connection
        if db_connection:
            db_connection.close()


#test SQL injection
inj_prompt1 = "'OR '1' = '1" #statement is true, should return all users!
print(f"\nTesting inj_prompt 1 with malicious imput: {inj_prompt1}")
print(get_user_credentials(inj_prompt1))

#test normal input
normal_input = "alice"
print(f"\nTesting inj_prompt1 with normal input: {normal_input}")
print (get_user_credentials(normal_input))