# Milestone 5: Report

## Task 1)
### Questions
Q: How can you train a predictive model? How could you manage experiments, and create reports/visualizations while training your model?

A: When training a predictive model, we split our data into train and test set. We train the model on the train set with labels, which the algorithm learns to predict. Then we feed the test data without labels into the model and we let the model predict the labels. As a last step, we compare the predicted labels with the actual values to evaluate the performance of the model.

We can write report on our project and visualize the performance and other selected metrics with Weights and Biases, where we can see graphical representations of our different runs of the code, as we did in Milestone 4.

Q: How can you improve collaboration in a team?

A: The main tool in collaborating on the project has been GitHub and WhatsApp. One thing we would have to improve in the future would be to let each other know how far we have come in the task. Sometimes it is quite complicated to see what was actually done in the project, because when we are still figuring out parts of the assignment, the individual branches can get messy.

Q: How would you assess and ensure the quality of your code?

A: To make sure our code is of good quality, we followed the following guidelines:

- use the PEP8 style guide of Python code
- divide the code into snippets that are related
- define our own functions
- test the functions and modules individually
- when the whole code works on one machine, test it on the other machine as well

Q: How can you provide data to the model at inference time and save its predictions to analyze the model's performance in a real-world scenario?

A: The inference data could be provided by a REST API like in our example and we could have a database, which already stores the train and test data and to which we would save the predictions as well. Therefore we could measure the performance on the extended data points.

Q: How can you  improve on the model iteratively and deploy it to customers in a web application? How could you structure your product as a microservice architecture?

A: When preparing the model, we can use gradient descent to find values of parameters that minimize the loss function of a model (can be seen in the compile() function). We can also do hyperparameter tuning and tune f.e. number of epochs, batch size and learning rate. Both methods are approaches of machine learning iteration. Finally, we would deploy the model with best results to the customer.

Microservice architecture is basically about splitting a big, complex system into smaller sub-systems based on their function. Each of the sub-systems can be deployed individually. In the project, we have been using this architecture almost from the start. We have several containers - f.e. one that takes care of PostgreSQL, one where we run our Python code - and then we connect them to the web application, where they work together to bring the predictions to customers.

### Example
Describe the process step by step with the example of an E-mail spam detector. Assume you want to provide a service where customers can send their E-mails to (f.e. a web page where you can upload E-mail text). The service responds with either "Spam" or "No Spam". Which tools would you use for each step in the process until the response ends up at the customers'screens? Also describe what metrics you might use to find out whether your model works (f.e. would you focus on Precision or Recall? Etc).

First, we would have to decide which kind of model we want to build for this service. Since we are talking about sequence/text data, recurrent neural network would be our choice. Because we have different length of input and output in this sequence-to-vector model, we would have to use an encoder-decoder architecture for the model and we should explore the possibility of including an attention layer to avoid problems with longer messages.

We have to collect/find a dataset with spam and no spam emails with labels. We can store the data in a database like PostgreSQL. Then we train the model, optimize and tune it and evaluate the performance on test data. When we are happy with the result, we save the trained model. For the compiling of the model, we would use Keras. To evaluate the performance of the model, we could make use of Weights and Biases again.

Then we prepare an app.py script, where we initialize the flask app, load the model and specify where we want to run the app. We would have two docker containers - the Flask app and the database.

Once we run the app, we would get new inputs from customers and return predictions, which we can then store in the database to extend our dataset.

We would focus on recall, as it tells us how many of spam emails the model correctly classifies. We expect that most of the inputs would be spam, because people would most probably only check emails they find suspicious. Therefore it would be useful to know how many of the spam emails the model classifies correctly.

## Task 2)
### Solution 1 - Incomplete

In task 2, we have two different approaches. The first one is not finished due to a problem we were not able to solve. The files for this can be seen in a separate folder m5_2 in our src folder. The repository will be messy after this milestone, but we will clean it up for the final deliverable. 

The first file we made was the app.py file where we write the flask app. The file looks like this:

```sh
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
```
I had several problems with this file, which was my own fault, because I had a typo or a missing bracket a few times. We use the host = '0.0.0.0' because the app runs in docker. 

Next up, we have the dockerfile to make our first (and unfortunately last) container. The dockerfile has the follwoing contents:
```sh
FROM ubuntu:20.04

RUN apt update -y
RUN apt install -y python3-pip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]

```
Lastly, we prepared a python script that uses the requests library. It looks like this:
```sh
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
```
The last file in the folder is the requirements file. 

With these files, we used the `docker build -t test .` command to build our docker image. Then we looked at the image using `docker images` and copied the image id, so that we could run the container. We ran it with the command `docker run -d -p 5000:5000 <image_id>`. After crashing 12 times because of some minor mistakes in the code, we got the container running. Finally, we ran the request script using `python3 req.py`. We are using the test data point with index 321 and in the terminal, we get a prediction of 7 (that is not correct, but I don't blame the model, the 2 in the image is weirdly written). 

However, when I input http://127.0.0.1:5000/predict in my browser, it says that the method is not allowed and for http://127.0.0.1:5000 it says that the requested url was not found on the server. I was not sure how to solve this problem so I did not proceed with this solution further.

### Solution 2
The second solution can be seen in a separate folder as well, specifically in the milestone5 folder in src. We also have an app.py script, which looks like this:
```sh
from flask import Flask, render_template, request, make_response
from functools import wraps, update_wrapper
from PIL import Image
from predictor import Predictor

import numpy as np
import torch

# Initialize the predictor object.
predictor = Predictor()

# Initialize Flask app.
app = Flask(__name__)

# Base endpoint to perform prediction.
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        prediction = predictor.predict(request)
        return render_template('index.html', prediction=prediction)
    else:
        return render_template('index.html', prediction=None)
		
if __name__ == '__main__':
   app.run()
```
We use the render_template function to display a web page we have prepared in advance, usually dynamic. Here, by “dynamic,” we mean a page that we can send variables to via parameters sent through the render_template function. These dynamic pages are called templates and can even incorporate Python scripting in between chunks of HTML and even Javascript. Do not confuse render_template with a similar function, redirect, which sends the user to a different sub application.

As you can see, we reference index.html in this script. We used that to create a web page in advance so it would look more professional. The html file containt the following: 
```sh
<!DOCTYPE html>
<html>
   <head>
      <!-- STYLESHEET -->
      <link rel="stylesheet" type="text/css" href="./static/css/main.css">
      <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

      <!-- JAVSCRIPT -->
      <script src="./static/js/main.js"></script>
   </head>
   <body>
      <div class="content">
         <h1 class="title"> Data Science Toolkits and Architectures: Implementing MNIST </h1>
         <form id="form" action = "http://localhost:5000/" method = "POST" 
               enctype = "multipart/form-data">
         <div class="image-box center">
            {% if prediction == None %}
            <!-- Show upload buttons if there is no prediction results yet. -->
               <img id="upload-img" class="center" 
                    src="./static/img/upload.png" width="100">
               <label for="file-upload" class="center custom-button">
                  <i class="fa fa-upload"></i> upload your image
                  <input type="file" id="file-upload" name="image" onchange=submit() />
               </label> 
            {% else %}
            <!-- Show prediction results. -->
               <p class="result"> Clearly and without ifs and buts, the image corresponds to the number <b>{{ prediction }}</b> </p>
            {% endif %}
         </div>
            {% if prediction != None %}
            <!-- Show upload button for follow up predictions. -->
               <label for="file-upload" class="center custom-button">
                  <i class="fa fa-upload"></i> upload another image
                  <input type="file" id="file-upload" name="image" onchange=submit() />
               </label>
            {% endif %}
         </form>  
      </div>
   </body>
</html>
```


