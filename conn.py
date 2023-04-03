import sqlite3
import csv

# Establishing a connection to the database
conn = sqlite3.connect('db.sqlite3')

# Creating a cursor object using the connection
cur = conn.cursor()

# Executing the query
cur.execute("select python,web,dbms,ml,dsa,student_id,username from student_tag_score LEFT JOIN  auth_user on student_tag_score.student_id=auth_user.id;")
#cur.execute("SELECT username, score, student_id FROM auth_user JOIN student_stuexam_db ON student_stuexam_db.student_id = auth_user.id")

# Fetching all the rows returned by the query
rows = cur.fetchall()

# Opening a CSV file to write the data
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username', 'score', 'student_id'])
    writer.writerows(rows)

# Closing the database connection
cur.close()
conn.close()
