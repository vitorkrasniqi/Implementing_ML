# Milestone 2: Report
## Cleaning Our Gir Repository
To clean up our git repository, we created a folder for the documents needed for our first milestone and we will continue to do so with each milestone to keep our main branch organized. We also deleted files that we don't need anymore and which we used at the beginning of our project to make initial pushes.

First we go to the right folder by using cd
```sh
vitor@krasniqi:~/Documents/Python$ cd Implementing_ML
vitor@krasniqi:~/Documents/Python/Implementing_ML
```
We deleted our branch, which is not used anymore:
```sh
Documents/Python/Implementing_ML$ git branch -d "milestone_1"
```
We check if it deleted:
```sh
vitor@krasniqi:~/Documents/Python/Implementing_ML$ git show-branch
```
And now we need to push it by doing this:
```sh
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git push
```
But this did not work, we received this error term:
> error: dst refspec milestone_1 matches more than one

We tried again:
```sh
git push origin :milestone_1
```
BUT IT DID NOT THE DUCK WORK

We tried this:
```sh
git push origin :refs/heads/milestone_1
```
Now it worked:
```sh
- [deleted] milestone_1
```
It seems that we needed to delete also the reference!

Our second wrong decision: We created the braches firt and then we decided which strategy we are following.
```sh
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git checkout -b "milestone_2_3"
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git checkout -b "milestone_2_4"
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git checkout -b "milestone_2_6"
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git add .
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git commit -m 'setting up the branches'
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ git push

#Git Ignore File erstellen:
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ vi .gitignore

# Cleaning the Repository
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ mkdir Milestone_1

# Moving all the files to new folder
(base) vitor@krasniqi:~/Documents/Python/Implementing_ML$ mv file_commentet.py /Milestone_1
```

##Questions
Q: What is a Hash function? What are some of the use cases?

A: The hash function creates a digital fingerprint for the file and it is unique for each file. It is not possible to change the fingerprint without changing the file and the other way around.
In our project, we use it every time we commit something to our repository - the commit function creates a specific ID for that commit, which is our "fingerprint".

Q: What is a Python module, package and script. How do they differ from one another?

A:
- Scripts: Scripts are pieces of code that we can execute and it runs by itself.

- Modules: Files that are intended to be imported. Generally it is a library that needs to be imported by other pieces of code.

- Packages: When we import a package, the object created by python is always of type module, so the distinction is only at the file system level. Only variables and functions in the __init__.py file of the package are visible, not sub-packages or modules. Packages are basically directories that contain multiple modules.

Q: How would you explain a Docker container and volume to a child?

A: For this question, we really can't think of anything more accurate than the example Arthur presented at the lecture. The example presented was that a Docker container is basically a box where you would store your toys and volume is like a hole in the box through which we can take some toys away or put more toys in.

Q: What is your preference concerning the use of Python virtualenv and Docker? When would you use one or the other?

A: Virtualenv only keeps dependencies, whereas a container stores the entire system. Virtualenv uses a shared python interpreter version, which is generally the python version installed on the system. That means that the code could still break when all dependencies are correct due to different versions of python installed on different machines. In a container, we can also install the correct version of python.

As for our preference, we do not have any so far because we do not have enough experience to compare virtualenv and a container, as this is the first time we are working with a container.

Q: What is the Docker build context?

A: Docker build context is a set of files that is located in specified `PATH` or `URL` in the following code:
```sh
docker build [OPTIONS] PATH | URL | -
```
+ Atrhur's remark: the build context should not be unnecessarily large, because in that case the building of our image would take a long time (because docker has to load those files).

Q: How can you asses the quality of a python package on PyPI?

A: We can check the GitHub statistics, where we see the stars, forks and open issues. Good indicator of quality is the stars statistics - the more stars the package has, the better it is.

## Splitting The Code 
Main idea for our code split: one file is only to load all the data and packages.

Second step is to prepare our data : here we do data processing, flatten the data, normalize (we did this at once, because this is the stepped required to develop the model).

Step 3 is just developing the model! Without running it.

Then one module to compile and save, because with big data this can be time consuimg (I Guess).

The last part ist to load data, fit the model and evaluate things!

## Pip Requirements File
To prepare the pip requirements file, we first setup a virtual environment where we install all packages needed to run the code (I did it based on our documentation file). We then use the pip freeze command to create a text file with the package requirements to run the code, like this:
```sh
virtualenv milestone_2
source milestone_2/bin/activate
pip install --upgrade setuptools
pip install tensorflow
pip install keras
pip freeze > requirements.txt
```
Now we have a pip requirements file. I use the command `deactivate` to deactivate the virtual environment and that's it!

## Dockerize The Code
To install Docker, we use the following commands:
```sh
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

#check the status
sudo systemctl status docker

#checking the installation
docker container run hello-world
## DOES NOT WORK! ERROR: docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.35/containers/create: dial unix /var/run/docker.sock: connect: permission denied.See 'docker run --help'.

#to obe able to run docker as a non-root user, I have to do this:
sudo usermod -aG docker parallels #parallels is my username since I am using parallels to run linux
newgrp docker

docker run hello-world
#now it works YAAAYY
```
