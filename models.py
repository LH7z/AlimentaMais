from datetime import date
from database import db
from flask_login import UserMixin

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="disponível")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reserved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"<Food {self.name}>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80),nullable=True)
    foods = db.relationship('Food', backref='owner', foreign_keys='Food.user_id', lazy=True)
    reserves = db.relationship('Food', foreign_keys='Food.reserved_by', backref='reserver', lazy=True)
