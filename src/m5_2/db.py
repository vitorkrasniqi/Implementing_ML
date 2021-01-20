from req import idx, result
import psycopg2
from psycopg2 import sql

index = idx
pred = result.text
print(index, pred)

connection = psycopg2.connect(host="localhost",
                              database="mnist",
                              user="postgres",
                              password="MH2021",
                              port="5432")
    
cursor = connection.cursor()


sql = '''INSERT INTO predictions (id, prediction) VALUES (%s, %s);'''
cursor.execute(sql, (index, pred))

connection.commit()
cursor.close()
connection.close()

