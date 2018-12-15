# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Card(Base):
    __tablename__ = "card"
    
    card_id = Column(Integer, primary_key=True)
    card_type = Column(String(64))
    card_name = Column(String(256))
    rarity = Column(String(64))
    color = Column(String(64))
    item_def = Column(Integer)
    price = Column(Float)

    def __repr__(self):
        return f"<Card(name={self.card_name})>"
