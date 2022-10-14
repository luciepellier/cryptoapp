from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, BigInteger, String, Float, DateTime, create_engine
from ..app import db

Base = declarative_base()

# Create a Cryptos Base
class Cryptos(Base):
    __tablename__ = "cryptos"
    id = Column(BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True, nullable=False)
    name = Column(String(55), nullable=False)
    quantity = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)

    # method to represent the class object as a string
    def __repr__(self):
        return f"<Crypto {self.name}>"

    # property that displays total Profit 
    @property
    def profit(self):
        return self.quantity * self.cost
