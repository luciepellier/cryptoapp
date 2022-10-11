from ..app import db, metadata
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialize db

# conn = sqlite3.connect('active_cryptos.db')

# # print("Opened database successfully")

# # create a cursor
# c = conn.cursor()

# Create a Crypto db model
class Cryptos(db.Model):
    name = db.Column(db.String(55), primary_key=True, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# conn.commit()

# conn.close()

# print("Closed database successfully")

# method to represent the class object as a string
def __repr__(self):
    return "<Name %r>" % self.name