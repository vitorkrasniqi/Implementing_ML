import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



connection = psycopg2.connect(user = "admin",
                                  password = "secret",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")


connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
cu = connection.cursor()
print ( connection.get_dsn_parameters(),"\n")




create_table_query = '''
CREATE store_digits(
   col1 TEXT     NOT NULL,
   col2 TEXT    NOT NULL);
'''

create_table_query = '''
COPY store_digits FROM 'resources/Old_files/Data/output.csv' WITH (FORMAT csv);
'''

connection.commit()
connection.close()






