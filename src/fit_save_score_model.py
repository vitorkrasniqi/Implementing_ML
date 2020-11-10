from compile_model import *

def fit_model(batch_size, epochs):
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test))

def save_model():
    model.save("my_fitted_model.h5")
    
def scoring():
    global score
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
