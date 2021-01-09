from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class InfoModel(db.Model):
    __tablename__ = 'output'
 
    id = db.Column(db.Integer, primary_key = True)
    output = db.Column(db.Integer())
 
    def __init__(self,output ):
        self.output  = output 
      
 
    def __repr__(self):
        return f"{self.output }"