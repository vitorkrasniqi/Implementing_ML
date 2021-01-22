from flask import Flask, render_template, request, make_response
from functools import wraps, update_wrapper
from PIL import Image
from predictor import Predictor
from flask_sqlalchemy import SQLAlchemy

import numpy as np
import torch



# Initialize the predictor object.
predictor = Predictor()

# Initialize Flask app.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:password1234@localhost:5432/milestone_3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class output(db.Model):
    __tablename__ = 'output'
 
    id = db.Column(db.Integer, primary_key = True)
    output = db.Column(db.Integer())
 
    def __init__(self,output ):
        self.output  = output 
      
 
    def __repr__(self):
        return f"{self.output }"



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




