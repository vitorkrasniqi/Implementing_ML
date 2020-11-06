from loading_the_data import *

num_classes = 10

img_rows, img_cols = 28, 28

def format_data_x(train, test, img_rows, img_cols):
    if K.image_data_format() == 'channels_first':
        train = train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        test = test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)
        
format_data_x(x_train, x_test, 28, 28)

def normalize_x(train, test):
    train = train.astype('float32')
    test = test.astype('float32')
    train /= 255
    test /= 255
    print('x_train shape:', train.shape)
    print(train.shape[0], 'train samples')
    print(test.shape[0], 'test samples')

normalize_x(x_train, x_test)

def vectorize_y(train, test, num_classes):
    train = keras.utils.to_categorical(train, num_classes)
    test = keras.utils.to_categorical(test, num_classes)
    
vectorize_y(y_train, y_test, 10)

