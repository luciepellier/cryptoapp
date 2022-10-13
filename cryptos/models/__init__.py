from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Float, DateTime, create_engine
from ..app import db

Base = declarative_base()

# Create a Cryptos Base
class Cryptos(Base):
    __tablename__ = "cryptos"
    name = Column(String(55), primary_key=True, nullable=False)
    quantity = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

# method to represent the class object as a string
def __repr__(self):
    return "<Name %r>" % self.name

# _________________________________________

# # Enter DB initial coins inversion
# cryptos = [
#     Cryptos(name = "Bitcoin", quantity=0.0051, cost=100.50),
#     Cryptos(name = "Ethereum", quantity=0.22, cost=300.00),
#     Cryptos(name = "XRP", quantity=0.22, cost=300.00)
# ]

# engine = sessionmaker(bind=create_engine("sqlite:///active_cryptos.db"))


# def add_cryptos():
#     with engine() as session:
#         for crypto in cryptos:
#             session.add(cryptos)
#         session.commit()

# add_cryptos()

# with engine() as session:
#     session.add(Cryptos)

