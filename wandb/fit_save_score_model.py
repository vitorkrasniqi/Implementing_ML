from compile_model import *

def fit_model(batch_size, epochs):
    import wandb
    from wandb.keras import WandbCallback
    config = wandb.config
    model.fit(x_train, y_train,
              batch_size=config.batch_size,
              epochs=config.epochs,
              verbose=1,
              validation_data=(x_test, y_test),
              callbacks=[WandbCallback()])

def save_model():
    model.save("my_fitted_model.h5")
    
def scoring():
    global score
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    return score
