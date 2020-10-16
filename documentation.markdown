# Running the mnist_cnn.py Code
## Installing Keras
### Pip
To install the Keras package, pip is needed. If you don't have pip, don't worry, we got you.

If you are working on a machine where you have the privileges to use sudo commands, do this:
```sh
$  sudo apt-get install -y python3-pip
```
If you work on a machine without these rights, you can set up a virtual environment, where pip is always installed, like this:
```sh
$ virtualenv name #where name = name of your virtual machine

$ source name/bin/activate
```
### Setuptools
In the next step, we update setuptools:
```sh
$ pip3 install --upgrade setuptools
# if this does not work, try using pip instead of pip3
```
### Tensorflow
Now we install tensorflow, which is the last step before installing keras:
```sh
$ pip3 install tensorflow
```
If you want to make sure it installed properly, do this and you can see which version was installed:
```sh
$ pip3 show tensorflow
```
### Keras
To install keras, we use the same command:
```sh
$ pip3 install keras
```
And same as before, if you want to check that the installation was successful, use:
```sh
$ pip3 show keras
```
Congrats! You installed all packages needed to run the code!

## Running the File
Now all that is left is to run the file, using one simple command:
```sh
$ python3 mnist_cnn.py
```
## Done!
That's all!

If you used the virtual environment, just use the command deactivate to exit it.
```sh
$ deactivate
```
