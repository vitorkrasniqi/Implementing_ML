import numpy as np
import idx2numpy
import matplotlib.pyplot as plt
import pandas as pd 





imagefile  = 'resources/Old_files/Data/t10k-images-idx3-ubyte'


X_train = idx2numpy.convert_from_file('resources/Old_files/Data/train-images-idx3-ubyte')
Y_train = idx2numpy.convert_from_file('resources/Old_files/Data/train-labels-idx1-ubyte')

X_test = idx2numpy.convert_from_file('resources/Old_files/Data/t10k-images-idx3-ubyte')
Y_test = idx2numpy.convert_from_file('resources/Old_files/Data/t10k-labels-idx1-ubyte')

print(X_test.ndim ) #check number of dimensions)
print(np.shape(X_test)) #print out the dimensions



print("X_Train",X_train.shape)
print("Y_Train",X_train.shape)

print("X_Test",X_test.shape)
print("Y_Test",X_test.shape)


np.set_printoptions(linewidth=np.nan)
print(X_train[22])


X_train = X_train.reshape(X_train.shape[0], -1) # flattens X_train to 50,000 * (1*28*28) : Basically keeps the first dimension intact and flattens all other dimensions
X_train = X_train.astype('float32')
X_train /= 255
