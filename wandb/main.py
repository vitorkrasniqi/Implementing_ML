from __future__ import print_function

import wandb 
from wandb.keras import WandbCallback

run = wandb.init(project='our-wandb',
           config={
              "learning_rate": 0.005,
              "epochs": 12,
              "batch_size": 128,
              "loss": "categorical_crossentropy",
              "architecture": "CNN",
              "dataset": "MNIST"
           })
config = wandb.config

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

compile(0.005)

import fit_save_score_model 
from fit_save_score_model import fit_model, save_model, scoring

fit_model(128, 12) 
save_model()
score = scoring()

wandb.log({'Test loss': score[0], 'Test accuracy': score[1]})

run.join()

