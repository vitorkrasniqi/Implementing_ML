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

In the second approach, we just converted the images into pickle files and converted them into csv, which we used to load into a database (the .py files are also stored in our repository). 

### Our Data Set
Our dataset can be accesed on this [link](http://yann.lecun.com/exdb/mnist/). The data can be downloaded as 4 separate compressed files of the .gz format. Once you decompress the data, images are in a idx3-ubyte format and the labels are in idx1-ubyte. The IDX file format is actually meant for vectors and multidimensional matrices of several numeric types, which worked out great for us in the end, because we could use that directly. Usually we prefer to load the data to python with the mnist.load_data function, which is really straightforward and returns the data in arrays of uint8, images with dimensions (60000 or 10000, 28, 28) and labels as (60000 or 10000, ).

In a database, it would make sense to define a table for images, where the individual images would be stored with their labels and connect the labels to a prediction table, where it would have a variable of predicted value and actual value as well, so that we could easily compare. The predictions and actual labels would be stored as a numeric value and the image as an array. 

The label value would make it easy to just choose images of a specific value that you want to see.

## Task 4) 
### Our docker-compose.yml File

Unfortunately, while finishing up the task, Vitor has some error and is unable to push files onto github and if I pull them, I don't see them as well of course. 
I myself have a different problem today, which is that I am not able to run any web application that worked f.e. 2 days ago and my docker containers act like everything is okay.

23:49 we are still trying to solve it.

### Our Database Structure

data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAaQAAAB8CAYAAAAmVsTDAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAABpKADAAQAAAABAAAAfAAAAAB3sxr/AAAcKklEQVR4Ae2dB5QURdeGS8UAZkXMiuJREUSMiCIqZhSzghgO6FEwogjmLIo5S1AwH8UIoiBGFEQw54goYgLFDIgY+q/nnr/mmx12h9ndCd3Ne8/pnZmO1U/V9u2quvXWIpE3JxMBERABERCBChNYtMLX1+VFQAREQAREwAjIIakgiIAIiIAIxIKAHFIsskGJEAEREAERkENSGRABERABEYgFATmkWGSDEiECIiACIiCHpDIgAiIgAiIQCwJySLHIBiVCBERABERADkllQAREQAREIBYE5JBikQ1KhAiIgAiIgBySyoAIiIAIiEAsCMghxSIblAgREAEREAE5JJUBERABERCBWBCQQ4pFNigRIiACIiACckgqAyIgAiIgArEgIIcUi2xQIkRABERABOSQVAZEQAREQARiQUAOKRbZoESIgAiIgAjIIakMiIAIiIAIxIKAHFIsskGJEAEREAERkENSGRABERABEYgFATmkWGSDEiECIiACIiCHpDIgAiIgAiIQCwJySLHIBiVCBERABERADkllQAREQAREIBYE5JBikQ1KhAiIgAiIgBySyoAIiIAIiEAsCMghxSIblAgREAEREAE5JJUBERABERCBWBCQQ4pFNigRIiACIiACckgqAyIgAiIgArEgIIdUxGyYNGmSW2SRRdyMGTOKeFadSgREQAQWDgJySEXM5yiKing2nUoEREAEFi4Cckglyu+XX37Z7bHHHu7MM890a6+9tuvYsaN79tln3TbbbOPWWGMNd95552Wu/OCDD7q2bdu61Vdf3R188MHuq6++sm1//fWXO/nkk916663n9t13X3f22We7G264wbb99NNPrkuXLnau7bbbzs4dTnjRRRe5DTfc0K577rnnOjnKQEafIiACcSYgh1Si3Pntt9/cM8884z788EN32WWXuXfeecftvvvu7sADD3SnnHKKrZs6daoLTof1jz76qPvhhx/c5ZdfbqkaOnSoreM3TumKK65wn3zyiW3r3Lmz+/zzz93AgQPdbrvt5vbZZx/3xRdfuPHjx7tbb73V3X777e6SSy5xN910k5swYUKJ7lKnFQEREIHiEWhQvFPpTLkEFl10UTds2DC3zDLLuDFjxrgpU6a4s846y/3333/mLCZPnuyWXnppq/V07drVTZ8+3Wo2OC9s1KhRjtrOYYcdZsuLL75o63FEzz//vHvllVesZrXffvu5Rx55xI0cOdKttNJKbs6cObYcccQRrlWrVm7VVVe14/RHBERABOJMQDWkEuZO48aNzRlxiYYNG7rWrVvb1XBUDRo0cP/8849bdtll3ZtvvulWXHFFt+6667qnnnrK9mHbCy+84Jo3b26/+bPtttvadxwSRlMd52L56KOPLJji8MMPt9oSTXyrrLKKGzx4sJ3bDtAfERABEYgxATmkEmYOTifbiMDLteHDh5vTGD16tNVqevfubbtw7GKLLea+/PLLzCHUoLAVVljBPj/44AP3+++/2/Laa6+5448/3tEMeN1111lt6+abb7ZaE01/MhEQARGIOwE5pArnEP0+a621lttqq62s/+juu+92//77r6WKQAecybRp09zTTz+dqT21bNnSrbzyym7IkCHmtAg3b9++vfv000/dww8/7Giqw6gtNW3a1P3555/2W39EQAREIM4E5JBKkDvV1YS4TO56fh911FEW2ICD2WijjVyHDh2s+e3GG290AwYMsP6fDTbYwB1zzDHWH7TEEktYMyCOioWmPqL5jj76aAtu4Hz0Ta255pqOJkMi7NgmEwEREIG4E1jEP7A0eKbCuUQWULtp1qyZW3zxxd0vv/zillxySffSSy9ZdB21nKWWWspCx+kb6tmzp6WY4AWOI1x8tdVWy9zF3Llz3WeffWa1KByTTAREQASSQEAOKca5dPXVV7tBgwa54447zvqGHnroIff666+79ddfP8apVtJEIF4E/v77bwsiym2hiFcqlRojQA2pXOYvSG1MixgUvQyUqwzrOqUhcNddd1UpE75pOurUqVM0bty4el/QtzxEfghF9OSTT0Z+CETe873//vuR74e1fQrZP+/JtLHWBMreh+RTaP0a+hSHYpWB3HdL3ogZoyVLDgHKwvLLL+++++47W959911HPvbo0aNoN9GmTRuHKko+o5mclgmskP3znUvbak+g7A6p9knUESJQOAEeYvS5LejBU/gZtWe5CDDMgf5Qlo033tgUTT7+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

## Optional Project Riddles
- What is an SQL Injection Attack?
    - SQL injection, also known as SQLI, is a common attack vector that uses malicious SQL code for backend database manipulation to access information that was not intended to be displayed. Websites are the most frequent targets of SQL injections. There are three types of SQL injections and they are classified according to the methods they use to access backend data and their damage potential:

        - In-band SQLi (Classic)
        - Inferential SQLi (Blind)
        - Out-of-band SQLi.
        - Data can be deleted, extracted and manipulated. Therefore it can cause huge real-world problems.
  
- How can you protect yourself?
    - Input validation (a.k.a. sanitization): it is a best practice of writing code that can identify illegitimate user inputs.
    - Web application firewall (WAF): it is commonly employed to filter out SQLI, as well as other online threats
    - Signature recognition, IP reputation: Whenever a web application firewall encounters a suspicious, but not outright malicious input may cross-verify it with IP data before deciding to block the request. It only blocks the input if the IP itself has a bad reputational history.
    
- What is a Decompression Bomb?
    - A decompression bomb is a malicious file that unpacks to an enormous amount of data - thus "flooding" the unpacking engine. That leads to crashing or rendering useless the program or system reading it. It is often employed to disable antivirus software, in order to create an opening for more traditional viruses. It is also called ‘zip of death’ or a zip bomb.
