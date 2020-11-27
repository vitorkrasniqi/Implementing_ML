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
