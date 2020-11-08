import loading_the_data
from loading_the_data import *

data_load()

import preparing_the_data
from preparing_the_data import format_data_x, normalize, vectorize_y

format_data_x(28, 28)
normalize(255) 
vectorize_y(10)

import developing_the_model
from developing_the_model import develop_model

develop_model(10)

import compile_save_model
from compile_save_model import compile, save_model 

compile()
save_model()

import train_evaluate 
from train_evaluate import model_load, fit_model, scoring

model_load()
fit_model(128, 2) 
scoring()
