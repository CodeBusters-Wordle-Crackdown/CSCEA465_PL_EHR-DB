import sqlite3

#Probes DB for vulnerablilities and attempts to extract all users
def get_user_credentials(username):
    db_connection = sqlite3.connect('test.db')
    db_cursor = db_connection.cursor()

    #check for vulnerable query in db
    probe_query = f"select * from users where username ='{username}'"
    db_cursor.execute(probe_query)

    #if successful, collects all user data
    probe_result = db_cursor.fetchall()

    #close connection
    db_connection.close()


#test SQL injection
inj_prompt1 = "'OR '1' = '1" #statement is true, should return all users!
print(get_user_credentials(inj_prompt1))