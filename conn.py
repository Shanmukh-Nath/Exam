import sqlite3 as sq
import pandas as pd

conn = sq.connect('db.sqlite3')
print(conn)

cur = conn.cursor()

q = pd.read_csv('questions_question_db.csv')

q.to_sql('questions_question_db',conn,if_exists='replace',index=False)

