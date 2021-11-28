from enum import unique
from backend import db
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    usn = db.Column(db.String(80), unique=True)
    type = db.Column(db.String(80))
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    
    

    def __repr__(self):
        return '<User %r>' % self.username