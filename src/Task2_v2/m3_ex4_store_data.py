
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from psycopg2 import OperationalError, errorcodes, errors
import sys
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib
from matplotlib import pyplot
import pandas as pd 
import sqlalchemy





connection = psycopg2.connect(user = "admin",
                                  password = "password1234",
                                  host = "localhost",
                                  port = "5432",
                                  database = "milestone_3")


connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
cu = connection.cursor()
print ( connection.get_dsn_parameters(),"\n")


# %%

num_classes = 10
input_shape = (28, 28, 1)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")


# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

print("y_train shape:", y_train.shape)
print(y_train.shape[0], "train samples")
print(y_test.shape[0], "test samples")



y_train_df = y_train[0:50]
y_train_df =  y_train_df.astype(np.int64)
y_train_df =  y_train_df.astype(np.str)
y_train_df = y_train_df.tolist()
y_train_df = pd.DataFrame(y_train_df ) 
y_train_df.columns = ['y_train_0', 'y_train_1', 'y_train_2', 'y_train_3', 'y_train_4', 'y_train_5', 'y_train_6', 'y_train_7', 'y_train_8', 'y_train_9']
y_train_df['ID_'] = y_train_df.index



y_test_df = y_test[0:50]
y_test_df =  y_test_df.astype(np.int64)
y_test_df =  y_test_df.astype(np.str)
y_test_df = y_test_df.tolist()
y_test_df = pd.DataFrame(y_test_df ) 
y_test_df.columns = ['y_test_0', 'y_test_1', 'y_test_2', 'y_test_3', 'y_test_4', 'y_test_5', 'y_test_6', 'y_test_7', 'y_test_8', 'y_test_9']
y_test_df['ID_'] = y_test_df.index



x_train_df = x_train[0:5]
x_train_df =  x_train_df.astype(np.int64)
x_train_df =  x_train_df.astype(np.str)
x_train_df = x_train_df.tolist()
x_train_df = pd.DataFrame(x_train_df ) 
x_train_df.columns = [ 'x_train_0', 'x_train_1', 'x_train_2', 'x_train_3', 'x_train_4', 'x_train_5', 'x_train_6', 'x_train_7', 'x_train_8', 'x_train_9', 'x_train_10', 'x_train_11', 'x_train_12', 'x_train_13', 'x_train_14', 'x_train_15', 'x_train_16', 'x_train_17', 'x_train_18', 'x_train_19', 'x_train_20', 'x_train_21', 'x_train_22', 'x_train_23', 'x_train_24', 'x_train_25', 'x_train_26', 'x_train_27']
x_train_df['ID_'] = x_train_df.index




x_test_df = x_test[0:2]
x_test_df =  x_test_df.astype(np.int64)
x_test_df =  x_test_df.astype(np.str)
x_test_df = x_test_df.tolist()
x_test_df = pd.DataFrame(x_test_df ) 
x_test_df.columns = [ 'x_test_0', 'x_test_1', 'x_test_2', 'x_test_3', 'x_test_4', 'x_test_5', 'x_test_6', 'x_test_7', 'x_test_8', 'x_test_9', 'x_test_10', 'x_test_11', 'x_test_12', 'x_test_13', 'x_test_14', 'x_test_15', 'x_test_16', 'x_test_17', 'x_test_18', 'x_test_19', 'x_test_20', 'x_test_21', 'x_test_22', 'x_test_23', 'x_test_24', 'x_test_25', 'x_test_26', 'x_test_27']
x_test_df['ID_'] = x_test_df.index


# %%


engine = sqlalchemy.create_engine('postgresql://admin:password1234@localhost:5432/milestone_3')
 
y_train_df.to_sql('y_train_df',engine, if_exists ='replace')
y_test_df.to_sql('y_test_df',engine,   if_exists ='replace')

x_train_df.to_sql('x_train_df',engine,   if_exists ='replace')
x_test_df.to_sql('x_test_df',engine,   if_exists ='replace')




# %%


y_train_df = '''
SELECT     y_train_1  from y_train_df
limit 2
;

'''


y_test_df = '''
SELECT     y_test_1  from y_test_df
limit 2
;

'''

x_train_df = '''
SELECT    x_train_1  from x_train_df
limit 2
;

'''



x_test_df = '''
SELECT   *  from x_test_df
limit 2
;

'''




cu.execute(y_train_df )
cu.execute(y_test_df )
cu.execute(x_train_df )
cu.execute(x_test_df )

rows = cu.fetchall()
print(rows )


# %%






engine = sqlalchemy.create_engine('postgresql://admin:password1234@localhost:5432/milestone_3')
 
y_train_df.to_sql('y_train_df',engine, if_exists ='replace')
y_test_df.to_sql('y_test_df',engine,   if_exists ='replace')

x_train_df.to_sql('x_train_df',engine,   if_exists ='replace')
x_test_df.to_sql('x_test_df',engine,   if_exists ='replace')




# %%


y_train_df = '''
SELECT     y_train_1  from y_train_df
limit 2
;

'''


y_test_df = '''
SELECT     y_test_1  from y_test_df
limit 2
;

'''

x_train_df = '''
SELECT    x_train_1  from x_train_df
limit 2
;

'''



x_test_df = '''
SELECT   *  from x_test_df
limit 2
;

'''




cu.execute(y_train_df )
cu.execute(y_test_df )
cu.execute(x_train_df )
cu.execute(x_test_df )

rows = cu.fetchall()
print(rows )


# %%



