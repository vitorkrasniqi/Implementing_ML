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
