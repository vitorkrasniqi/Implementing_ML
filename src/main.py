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

import compile_model
from compile_model import compile

compile()

import fit_save_score_model 
from fit_save_score_model import fit_model, save_model, scoring

fit_model(128, 12) 
save_model()
scoring()

import load_model_predict
from load_model_predict import load_model, predict

load_model()
predict()
