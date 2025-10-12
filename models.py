from datetime import date
from database import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="disponível")

    def __repr__(self):
        return f"<Food {self.name}>"
