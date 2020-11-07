from loading_the_data import *

def format_data_x(img_rows, img_cols):
    global x_train
    global x_test
    global input_shape
    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)
            
format_data_x(28, 28)

def normalize(num):
    global x_train
    global x_test
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= num
    x_test /= num
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

normalize(255)

def vectorize_y(num_classes):
    global y_train
    global y_test
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
vectorize_y(10)

