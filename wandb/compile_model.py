from developing_the_model import *

def compile(learning_rate):
    import wandb
    config = wandb.config
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(config.learning_rate),
                  metrics=['accuracy'])
