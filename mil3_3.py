#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.models import load_model

def data_load():
    global x_train
    global y_train
    global x_test
    global y_test
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
data_load()

import numpy as np
import tensorflow as tf
import matplotlib
from matplotlib import pyplot

mnist_db = x_train # we will use this to select a sample for the database

mnist_db.ndim #check number of dimensions
np.shape(mnist_db) #print out the dimensions

pyplot.imshow(mnist_db[27973]) #example of a plot/picture

num_pixels = 784 # the number of pixels is 28*28=784

mnist_db = mnist_db/255
mnist_db = mnist_db.reshape(mnist_db.shape[0],
                            num_pixels)

print(mnist_db.shape) #just because I'm obsessive and want to triple check

sample_db = x_train1[321]
print(sample_db)
pyplot.imshow(mnist_train_images[321])

db_final = sample_db.tostring()  #we put this in the database
print(db_final)

#for when we load it back to python from the database
back_check = np.fromstring(db_final)

