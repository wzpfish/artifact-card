# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import MYSQL_URL
from model import Card 

engine = create_engine(MYSQL_URL, encoding="utf-8")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def get_card(item_def):
    result = session.query(Card).filter(Card.item_def == item_def).first()
    return result

def save_cards(cards):
    if not cards:
        return

    if not engine.dialect.has_table(engine, Card.__tablename__):
        Card.__table__.metadata.create_all(engine)

    for card in cards:
        session.merge(card)
    session.commit()
