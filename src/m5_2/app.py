from flask import Flask, request, jsonify
import numpy as np
from tensorflow import keras

app = Flask(__name__)

id2class = {0: "0",
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",}
           
model = keras.models.load_model("my_fitted_model.h5")
@app.route('/predict', methods=['POST'])

def predict():
    parameters = request.get_json(force=True)
    im = np.array(parameters['image'])
    im = im.astype("float32")/255
    im = np.expand_dims(im, -1)[None]
    out = id2class[np.argmax(model.predict(im))]
    return out
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')

