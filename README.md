# Data Science Toolkits and Architectures

Data science is on everyone's lips and is highly regarded. The training and learning of data science skills is taught by many universities and online course providers with the help of cleaned data, where only the ML algorithm has to be trained. 

In contrast, this module is about properly implementing and putting into production a machine learning/deep learning algorithm using software tools. The understanding of data-driven software and typical life cycle of machine learning projects is promoted in this project, in which this project was developed in five different milestones. 


## Milestone 1 

In this milestone, we first had to create a Git repository so that we can work together as a team, because we have already received data and code for this project.The dataset assigned to our group (accessible [here](http://yann.lecun.com/exdb/mnist/)) is the MNIST database, which is a subset of a larger database MNIST that consists of Special Database 3 (SD-3) and Special Database 1 (SD-1).

The MNIST training set consists of 30 000 patterns from SD-3 and 30 000 patterns from SD-1 and it contains examples from approximately 250 writers. The test set consists of 60 000 patterns as well, however, only a subset of this test set is available on the site. This subset is of 10 000 test images, 5 000 from each database. There are 4 files available on the website: * training set images (60 000 patterns) * test set images (10 000 patterns) * training set labels * test set labels. 

The data is stored in the IDX file format for vectors and multidimensional matrices of various numerical types. The machine learning algorithm used on this dataset solves a classification problem, because our goal is to predict a categorical output/value. We classify each image into one of ten possible categories depending on which number is written in the image (0-9).

Also, the correct packages had to be downloaded in the correct version so that the required packages could run. All code was described in detail by us.


## Milestone 2

The second milestone started by thinking about what we don't want to show to the world using .gitignore. This .gitignore file we have then also adjusted over longer time with the help of version-control. We also adapted the code so that our code could load the data on its own, fit it to a neural network, and save and load .h5 files using Keras so that the fitted model could also execute the predictions.

The structure of the code was not sufficient for us, so we divided the code into several modules, taking into account the PEP8 standard. We divided the scripts by functionality, so that we have scripts for loading packages, model creation and prediction. (More scripts have been created).

Later, in a virtual environment, we downloaded all the packages needed to run the code so that we could agree as a team on the right packages and versions. At the same time we created a requirements file so that we could quickly download the required packages in other environments (virtual env or local).

Finally, we took the first step towards Docker by installing Docker and creating a simple Dockerfile based on Python 3.8.3 that runs our script and downloads the required packages from our defined requirements file. Using Docker-build we then created our first images and then got our Docker running and could see our code running.


## Milestone 3

This step is about working with relational databases so that we can store the input and output of our neural network. However, the transfer is to be done with the help of Docker, where we can access the database with the help of the host IP address and the defined port. 

Thus, at the beginning we have dealt with PostgreSQL and Docker Compose (We already know that in this project we will create several Dockerfiles and need Docker Compose , since we also want to start several containers in the same time and connect them with the help of a network. ), since we have as a goal to create a multi-container Docker software.

We got into this by first creating a database and database users using a docker-compose file.  Then later we created a table using Python and stored a bad joke there. 

In a further step, we stored the input and output data of our deep learning model into a relational database by working with PostgreSQL and Docker Compose. For this we used libraries like pandas, sqlalchemy and psycopg2. 

## Milestone 4

In the fourth milestone, we had to instrument our code with Weights and Biases so that we could see how selected metrics behave when we change some parameters in our code. We began by changing our code base - we had to specify the wandb project in our main script, import wandb into individual snippets of the code and implement wandb into our compile and fit_model functions.

We checked that the code does what we need it to do in Spyder and once everything was correct there, we moved on to running it in a container. For this, we created a dockerfile and an entrypoint script and ran them together using the docker build command. Once we were done, we ran our code a few times to see the different runs on Weights and Biases (can be seen [here](https://wandb.ai/michaelahavl/our-wandb?workspace=user-michaelahavl)). Due to the demanding computation, we only tested different values of batch size and epochs.

For the last task, we prepared a Jupyter Notebook and looked at our dataset more thoroughly and this time from a practical point of view, unlike the more theoretical overview we prepared in the first milestone.
