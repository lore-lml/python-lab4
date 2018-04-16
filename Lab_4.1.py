import mysql.connector

query = "SELECT * FROM task_list"
conn = mysql.connector.connect(user='root', password='asdf12345',
                              host='localhost',
                              database='tasks')
cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchall()
for element in result:
    print(str(element[0]) + " " + element[1])
cursor.close()
conn.close()
