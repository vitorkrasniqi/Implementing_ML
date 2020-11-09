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
## Gitignore
Before we mention what we would like to "hide" with .gitignore, let us briefly mention the greatest thing we have learned from this task.
We have noticed that .gitignore allows you to hide files very specifically and according to certain characteristics. 

Then we changed this over a longer period of time and noticed that .gitignore has no effect on the git repository. For example, we tried to hide new files afterwards, but they were still visible on github.
We spent a lot of time trying to figure out why these files were still visible. The main reason was that we did not empty the cache.

So all we had to do was run this command:
```sh
git rm -rf --cached
```
We have ignored the following files for the following reason:

mnist_cnn.py -  The original code, we wanted to keep this as the original. But nobody has to see this.

resources/Old_files/ - Folder that has the following files: 
  - Data/ = There we manually downloaded and saved data. We ignored this at the first milestone. We do not want the public to see this data.
  - Milestone_1 = Files from the Milestone_1, which are no longer used

Command_For_Git - Since we are both still Linux beginners, we have created a file with the most important command lines. We will have a look at this file to get along with the terminal.

src/__pycache__/ - When we run a program in Python, the interpreter first compiles it into bytecode (this is an oversimplification) and saves it in the __pycache__ folder. If we look there, we find in the folder of our project a number of files that have the names of the .py files in common, only their extensions are either .pyc or .pyo. These are byte-code compiled or optimised byte-code compiled versions of the files of our programme.

*.h5 - The trained model from our code, it is unnecessarily big and we do not need to store it.

## Questions
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

Q: How can you assess the quality of a python package on PyPI?

A: We can check the GitHub statistics, where we see the stars, forks and open issues. Good indicator of quality is the stars statistics - the more stars the package has, the better it is.

## Code Funcionality

Our assigned code already has a lot of the funcionality, but we had to add two funcionalities. 

We had to load an additional library first:
```sh
from keras.models import load_model
```
With this library it is very easy to save a model as .h5 file and load this model. 

Accordingly, we only had to write the following code to adapt the code:
```sh
model.save("my_model.h5")
model = load_model("my_model.h5")
```

## Splitting The Code 
Main idea for our code split: one file is only to load all the data and packages.

Second step is to prepare our data : here we do data processing, flatten the data, normalize (we did this at once, because this is the step required to develop the model).

Step 3 is just developing the model! Without running it.

Then one module to compile and save, because with big data this can be time consuming (I Guess).

The last part ist to load data, fit the model and evaluate things!

## Pip Requirements File
To prepare the pip requirements file, we first set up a virtual environment where we install all packages needed to run the code (I did it based on our documentation file). We then use the pip freeze command to create a text file with the package requirements to run the code, like this:
```sh
virtualenv milestone_2
source milestone_2/bin/activate
pip install --upgrade setuptools
pip install tensorflow
pip install keras
pip freeze > requirements.txt
```
Now we have a pip requirements file. I use the command `deactivate` to deactivate the virtual environment and that's it!

### Hashes

I got the hashes for the two required packages by using f.e. `hashin Keras==2.4.3` and it added the hash into a requirements.txt file that I prepared for this task.

Package  |  Hash
--|--
Keras==2.4.3   |  hash=sha256:05e2faf6885f7899482a7d18fc00ba9655fe2c9296a35ad96949a07a9c27d1bb
tensorflow==2.3.1   |  hash=sha256:1f72edee9d2e8861edbb9e082608fd21de7113580b3fdaa4e194b472c2e196d0

## Dockerize The Code
### Install Docker
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

#to be able to run docker as a non-root user, I have to do this:
sudo usermod -aG docker parallels #parallels is my username since I am using parallels to run linux
newgrp docker

docker run hello-world
#now it works YAAAYY
```
### Dockerfile
Our simple docker file simply described:

From the docker hub we only wanted to download Python, therefore we used Python3.8.3 as the base image!
```sh
FROM python:3.8.3
```
Now we want to create a folder where we can copy our code.
```sh
WORKDIR /home/vitor/Deeplearning
```
With dot we copy everything from our local folder to our created folder which we created with WORKDIR.
```sh
COPY . /home/vitor/Deeplearning
```
With Run we install all defined Python packages so that the requirements for the Python script are fulfilled.
```sh
RUN pip install -r resources/requirements.txt
```
Now we act as if we were in the terminal. We run the Python script with the following command!
```sh
CMD python src/main.py
```
### Creating Image
With Docker Build we create the image.
With the tag option we give this image a name! The dot says here again that everything must come from the local again!

We use the command:
```sh
sudo docker build --tag run_it .
```
Now we can see that the docker file is running and the requirements are installed!

Small control, with `sudo docker images` we can see that we have created it. 

With `sudo docker ps` we can see which images are currently running. With `sudo ps -a` we can see all running docker images.

An example of old dockerimage:

CONTAINER ID  | IMAGE  | COMMAND  | CREATED  | STATUS  |PORTS   |NAMES  
--|---|---|---|---|---|--
bafdc95d3bbd  | hi  | "/bin/sh -c 'python ..."  | 30 hours ago  |Exited (1) 30 hours ago   |   | upbeat_tereshkova 

At Names we can see that Docker does stand-up commedy on the side and distributes funny names himself. For this reason it is important to create a name yourself while running! (So that Docker does not make fun of us :( )

Now we want to run this docker and see if our code works! Now we make the docker work and give it a name!
```sh
sudo docker run --name running_it -d run_it
```
Output: 76b719d27502c3e290d6c9b4ae878f99b6891e55eee9504b3a90315e558c2aed

With this command we can then see how our code is running:
```sh
sudo docker logs running_it
```
We can run old images with the following command:
```sh
sudo Docker start name
```
We stop them with the following command:
```sh
sudo docker stop name
```
Sidenote: using `sudo usermod -aG docker user` we can get out of using sudo with every command, like in the instance above while installing docker. 
