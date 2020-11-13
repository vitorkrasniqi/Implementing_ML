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

### Questions for composetest
Q: Which services are being used for the application (described in the link above)? How do they relate to the host names in terms of computer networks?

A: The services used in the composetest are defined in the docker-compose file. The two services are web and redis. We can see that both of the services are up when we use the command `docker-compose ps`, which gives the following table as an output:

Name  | Command  |State   | Ports 
--|---|---|--
composetest_redis_1  | docker-entrypoint.sh redis ...  |Up   | 6379/tcp
composetest_web_1  |flask run   |Up   | 0.0.0.0:5000->5000/tcp 

Q: What ports are being used (within the application and in the docker-compose file)?

A: As can be also seen in the table above, the ports that are being used are 6379 where we run redis and 5000 used in the docker-compose. 5000 is used on the host machine as well as in the container.

Q: How does the host machine (e.g. your computer) communicate with the application inside the Docker container. Which ports are exposed from the application to the host machine?

A: How our machine communicates with the application is also apparent from the table. We see that the host machine identified by 0.0.0.0. communicates through the port 5000 with the server, which uses also port 5000. 

SIDENOTE: This does not have to be the case. For example, in Task 2, we can see that pgadmin has the following port information: 0.0.0.0:8080->80/tcp, which meand that the host machine is using the port 8080 to communicate and is being redirected in the container to port 80.

Q: What is localhost, why is it useful in the domain of web applications?

A: Localhost refers to the computer/system that is currently used. In the project, we use localhost whenever we have a running web application like PGADMIN. We connect to it through our brower by writing for example: http://localhost:5000/ where 5000 is the port that is being used on the host machine. We can also use 127.0.0.1 instead of localhost.

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
This is a tale of a great adventure that we took, exploring many different ways to transform data for many hours only to find out that our initial data can be loaded into PostgreSQL directly. Am I crying while writing this? Maybe.

Our first solution can be seen in the mil3_3 python file, where we transformed the data by reducing it from an array of 3 dimensions (60000, 28, 28) to an array of dimensions (60000, 784) - 784 being the number of pixels (28x28) - by using the following commands:
```sh
num_pixels = 784
mnist_db = mnist_db/255
mnist_db = mnist_db.reshape(mnist_db.shape[0],
                            num_pixels)
```
Then we selected a sample of 1 image to test the rest. We wanted to use the 1 row of data and transfer it into a binary string, which we have done by this:
```sh
db_final = sample_db.tostring()
```
Then when we would need to come back from string to an array, we would use the command `np.fromstring(db_final)`.

We also have a way of "drawing" the picture, with the following:
```sh
pyplot.imshow(x_train[27973])
```
Which produces the following plot:

data:image/png;base64,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

I decided to insert the plot as this for 2 reasons: 

1. I came across this "format" today and thought it might be fun for you to decode it (even though it will probably take you like 2 seconds).

2. I don't know how else to put a plot into markdown:)



### Our Data Set
Our dataset can be accesed on this [link](http://yann.lecun.com/exdb/mnist/). The data can be downloaded as 4 separate compressed files of the .gz format. Once you decompress the data, images are in a idx3-ubyte format and the labels are in idx1-ubyte. The IDX file format is actually meant for vectors and multidimensional matrices of several numeric types, which worked out great for us in the end, because we could use that directly. Usually we prefer to load the data to python with the mnist.load_data function, which is really straightforward and returns the data in arrays of uint8, images with dimensions (60000 or 10000, 28, 28) and labels as (60000 or 10000, ).

In a database, it would make sense to define a table for images, where the individual images would be stored with their labels and connect the labels to a prediction table, where it would have a variable of predicted value and actual value as well, so that we could easily compare. The predictions and actual labels would be stored as a numeric value and the image as an array. 

The label value would make it easy to just choose images of a specific value that you want to see.

### Task 2) With Our Data


## Task 4) 
### Our docker-compose.yml File

### Our Database Structure
