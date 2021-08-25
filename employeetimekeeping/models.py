from employeetimekeeping import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(10), unique = True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    activities = db.relationship('Activity', backref='relatedUser', lazy=True)
    
    def __repr__(self):
        return f"Username: {self.name}"

class Activity(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    break_start = db.Column(db.DateTime)
    break_end = db.Column(db.DateTime)
    lunch_start = db.Column(db.DateTime)
    lunch_end = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"shift start: {self.shift_start}, shift end: {self.shift_end}, break start: {self.break_start}, break end: {self.break_end}, lunch start: {self.lunch_start}, lunch end: {self.lunch_end}"
