import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



connection = psycopg2.connect(user = "admin",
                                  password = "secret",
                                  host = "localhost",
                                  port = "5432",
                                  database = "ms3_jokes")


connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
cu = connection.cursor()
print ( connection.get_dsn_parameters(),"\n")



name_Database = "ms3_jokes";
sqlCreateDatabase = "create database "+name_Database+";"
cu.execute(sqlCreateDatabase);



use_data_base = '''
\connect ms3_jokes

'''

show_database = '''
SELECT current_database();

'''

create_table_query = '''CREATE TABLE jokes
          (ID INT PRIMARY KEY     NOT NULL,
          JOKE          TEXT    NOT NULL); '''
                   
                   
load_data_into_table_query = '''
INSERT INTO jokes (ID, joke) VALUES ('1', 'I have a joke about a data miner, but you probably will not dig it.');
'''
select_data_query = '''
Select * from jokes;
'''

cu.execute(  use_data_base )
cu.execute( show_database )

cu.execute(create_table_query)
cu.execute(  load_data_into_table_query )
cu.execute(  select_data_query  )

print("Table created successfully in PostgreSQL ")

rows = cu.fetchall()
for r in rows:
    print(f"ID {r[0]} joke {r[1]} ")


connection.commit()
connection.close()






