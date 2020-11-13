# Milestone 3: Report
## Task 1)
### Installing docker-compose
To install docker compose, we followed the guide on docker docs and used the following code:
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
After executing those commands, we test if the installation was successful by checking the version of docker-compose, like this:
```sh
docker-compose --version
```
As an output, we get: docker-compose version 1.27.4 and build, meaning that the installation was successful.

### composetest
To get more familiar with the process of creating a multi-docker container application, we decided to follow the tutorial [here](https://docs.docker.com/compose/gettingstarted/). 

First, we created an app.py with the following content:
```sh
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```
Then we create requirements.txt consisting of:
```sh
flask
redis
```
In the next step, we create the following dockerfile:
```sh
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```
As a last step before building our test, we create a docker-compose.yml file containing this:
```sh
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
```
Note: the `volumes` and `environment` parts were added after testing the application without them, as represented on the linked page. 

The next step was to build it, sing command:
```sh
docker-compose up
```
At this point, when we paste http://localhost:5000/ into our browser, we see: Hello World! I have been seen N times and with each reload, we get N+1 times. So it works.

But since we already have the code as a volume, we can now change the text that we want to display, f.e. to Hello from Docker! When we make this change in the app.py file, we get the following message in the terminal: 
```sh
web_1    |  * Detected change in '/code/app.py', reloading
```
Now when we reload the page in our browser, we can see the following text: Hello from Docker! I have been seen 7 times.

### Questions
Q: Which services are being used for the application (described in the link above)? How do they relate to the host names in terms of computer networks?

Q: What ports are being used (within the application and in the docker-compose file)?

Q: How does the host machine (e.g. your computer) communicate with the application inside the Docker container. Which ports are exposed from the application to the host machine?

Q: What is localhost, why is it useful in the domain of web applications?

## Task 2)
### Questions
Q: What is PostgreSQL? Is it SQL or no-SQL and why?

A: PostgreSQL (also known as Postgres) is a relational database management system. The difference between SQL and no-SQL is that SQL databases are relational, use structured query language and have a predefined schema. NoSQL are non-relational and have dynamic schemas for unstructured data. Postgres is therefore SQL. 

Q: If you stpped and deleted the Docker container running the database and restarted it, would your joke still be in the database? Why or why not?

A: In our case, the data would persist because they are stored in a volume (defined in the docker-compose file below) and a Docker volume is not deleted when the container is deleted.

### Running a PostgreSQL Server
With this task, we had several problems and were not able to run the server while following many guides. We then decided to run both PostgreSQL and PGADMIN with the help of a docker-compose file and that finally worked for us. First, we make a new directory for this project and change into that directory, like so:
```sh
mkdir -p ~/Desktop/docker/pgdev
cd ~/Desktop/docker/pgdev
```
As a next step, we create a new docker-compose file with the command `> docker-compose.yaml`. We put the following into the file:
```sh
version: "3.7"

services:
    db:
        image: postgres:12.4
        restart: always
        environment:
            POSTGRES_DB: postgres
            POSTGRES_USER: admin
            POSTGRES_PASSWORD: secret
            PGDATA: /var/lib/postgresql/data
        volumes:
            - db-data:/var/lib/postgresql/data
        ports:
            - "5432:5432"
 
    pgadmin:
        image: dpage/pgadmin4:4.18
        restart: always
        environment:
            PGADMIN_DEFAULT_EMAIL: welovedatasciencealltheway@tryingtolearnit.though
            PGADMIN_DEFAULT_PASSWORD: password1234
            PGADMIN_LISTEN_PORT: 80
        ports:
            - "8080:80"
        volumes:
            - pgadmin-data:/var/lib/pgadmin
        links:
            - "db:pgsql-server"
volumes:
    db-data:
    pgadmin-data:
```
With this file, we start the services:
```sh
docker-compose up -d
```
After the command is executed, we can chceck that everything worked and that the correct ports are exposed with the `docker-compose ps` command. To this, we get the following output: 
 Name |Command   |State   |Ports  
--|---|---|--
pgdev_db_1|docker-entrypoint.sh postgres|Up |0.0.0.0:5432->5432/tcp
pgdev_pgadmin_1| /entrypoint.sh  |Up |  443/tcp, 0.0.0.0:8080->80/tcp

This means that to run the database, our system is using the port 5432 and 8080 (= host port) to run the PGadmin and the ports are redirected in the container to ports 5432 and 80, respectively.

Now we can already open our browser, paste http://localhost:8080 and see our PGADMIN login page. 

After we login, we select to create a new server. We named the server Database Test and inputed our password. For the Host name/address information, we needed an IP address of the container on which the database is running. We use the command `docker ps -a` and look at the container named pgdev_db_1. From this row, we need the container ID, which we use in the command `docker inspect container_ID`.

At the end of the output, we see the IP address and write it in the Host name/address box. Then we can save and the server is created.

### ms3_jokes database
So far, we did not manage to create a database called ms3_jokes with a python script, so we decided to do it in PGadmin for now and try to figure it out later.

Creating a database there is really easy, we just click on databases and choose to create a database. We name the database ms3_jokes and the database is created. In schemas of that database, we can see that there are no tables in the database.

To create a table, we open the Query Tool and use the following notation:
```sh
CREATE TABLE jokes(ID numeric, joke TEXT)
```
After this, we refresh the tables and see that there is, indeed, a new table called jokes with 2 columns: id and joke. Now all we have to do is insert our favorite joke with the following:
```sh
INSERT INTO jokes(ID, joke) VALUES ('1', 'I have a joke about a data miner, but you probably will not dig it.')
```
After this command is executed, we refresh the table and can view the data, which now holds our joke with ID number 1.

### Python solution
While solving the second task with a python script, we use the docker-compose file that can be seen above. Over the course of this project, we have learned that with docker-compose files, the structure must be written very precisely and it is important to save this code in the correct format.

When we have this, we start the database by executing the following command in the terminal:
```sh
docker-compose up
```
We have also written a Python script, where we start by importing the package psycopg2, which is recommended for communication with databases:
```sh
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
```
Here we could have saved port, because the standard is always 5432.
```sh
connection = psycopg2.connect(user = "admin",
                              password = "secret",
                              host = "localhost",
                              port = "5432",
                              database = "postgres")
```
We have created this to bypass SQL injection.
```sh
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cu = connection.cursor()
print(connection.get_dsn_parameters(), "\n")

name_Database = "ms3_jokes";
sqlCreateDatabase = "create database" + name_Database + ";"
cu.execure(sqlCreateDatabase);

use_data_base = ""
\connect ms3_jokes
'''
show_database = '''

SELECT current_database();
'''
create_table_query = '''CREATE TABLE jokes
    (ID INT PRIMARY KEY NOT NULL,
    JOKE TEXT NOT NULL); '''

load_data_into_table_query = '''
    INSERT INTO jokes (ID, joke) VALUES('1', 'I have a joke about a data miner, but you probably will not dig it.');
    '''

select_data_query = '''
    Select * from jokes;
    '''
cu.execute(use_data_base)
cu.execute(show_database)
cu.execute(create_table_query)
cu.execute(load_data_into_table_query)
cu.execute(select_data_query)

print("Table created successfully in PostgreSQL")

rows = cu.fetchall()
for r in rows:
    print(f"ID {r[0]} joke {r[1]}")

connection.commit()
connection.close()
```
With `connection.commit` we wrote directly in the database and with `connection.close` we close the connection.

After that we logged into the terminal to see if our Python script was successful. So we logged via terminal with the database using the psql client. 

First we had to load the psql language into the terminal by typing the following:
```sh
sudo docker-compose run db bash
```
IMPORTANT at this point: we have to run db here, because we defined the connection in YALM as db.

Now we could register in the data bank container:
```sh
root@93b723a30a4a:/# psql --host=db --username=admin --dbname=postgres

Password for user admin:
psql (12.4 (Debian 12.4-1.pgdg100+1))
Type "help" for help.
```
Now logged into the created database:
```sh
ms3_jokes=#`
```
Now we want to list all created databases with the following command:
```sh
ms3_jokes=# \l
```
List of databases
 Name |Owner   |Encoding   |Collate   | Ctype  | Access privileges 
--|---|---|---|---|--
ms3_jokes | admin  |UTF8   |en_US.utf8   |en_US.utf8   |  
postgres |admin   |UTF8   |en_US.utf8   | en_US.utf8  |  
template0 |admin   |UTF8   |en_US.utf8   | en_US.utf8  | =c/admin   admin=CTc/admin 
template1 |admin   |UTF8   |en_US.utf8   | en_US.utf8  | =c/admin   admin=CTc/admin 

If we want to list all created tables:
```sh
ms3_jokes=# \d
```
Now we want to check our joke:
```sh
ms3_jokes=# select * from jokes;
```
 id | joke 
--|--
1  | I have a joke about a data miner, but you probably will not dig it. 

## Task 3) 
### Impedance Mismatch

### Our Data Set

### Task 2) With Our Data

## Task 4) 
### Our docker-compose.yml File

### Our Database Structure
