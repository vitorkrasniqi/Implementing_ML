import requests
import json

from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

idx = 321
im = x_test[idx].tolist()
data = {'image': im}
URL ='http://127.0.0.1:5000/predict'

result = requests.post(URL, json.dumps(data))
print(f"Prediction = {result.text}")

