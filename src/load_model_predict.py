from fit_save_score_model import *

def model_load():
    global model
    model = load_model("my_fitted_model.h5")

def predict(x):
    global pred
    pred = model.predict_classes(x, verbose = 1)
    return pred
