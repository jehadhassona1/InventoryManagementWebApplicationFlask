from app import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50),nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50),nullable=False)


class ProductMovement(db.Model):
    id = db.Column(db.Integer ,primary_key=True)
    fromLocation = db.Column(db.Integer)
    toLocation = db.Column(db.Integer)
    productId = db.Column(db.Integer , nullable=False)
    quantity = db.Column(db.Integer)



