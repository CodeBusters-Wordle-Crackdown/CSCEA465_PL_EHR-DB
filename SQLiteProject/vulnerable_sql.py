import sqlite3

#Probes DB for vulnerablilities and attempts to extract all users
def get_user_credentials(username, db = 'test.db'):
    print(f"SQLite3: Attempting to connect to {db} ...") #Debug  
    db_connection = sqlite3.connect(db) #attempt to connect to db
    print(f"SQLite3: Established connection to {db}! ") #Debug

    print(f"SQLite3: Initializing cursor ...") #Debug
    db_cursor = db_connection.cursor() #creates cursor
    print(f"SQLite3: Cursor initialized!") #Debug

    #check for vulnerable query in db
    probe_query = f"select * from users where username ='{username}'"
    print(f"Executing Query: {probe_query}") #DEBUG

    db_cursor.execute(probe_query)

    #if successful, collects all user data
    probe_result = db_cursor.fetchall() #returns list of tuples or an empty list

    #close connection
    db_connection.close()


#test SQL injection
inj_prompt1 = "'OR '1' = '1" #statement is true, should return all users!
print(get_user_credentials(inj_prompt1))