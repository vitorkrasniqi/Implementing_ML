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

Q: If you stpped and deleted the Docker container running the database and restarted it, would your joke still be in the database? Why or why not?

### Running a PostgreSQL Server

## Task 3) 
### Impedance Mismatch

### Our Data Set

### Task 2) With Our Data

## Task 4) 
### Our docker-compose.yml File

### Our Database Structure
