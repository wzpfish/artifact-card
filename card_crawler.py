# coding: utf-8
import requests
import logging

from util import retry_session
from model import Card
import db

def get_crawl_url(setid):
    assert setid in ["00", "01"]

    url = f"https://playartifact.com/cardset/{setid}/"
    r = retry_session().get(url)
    if r.status_code != requests.codes.ok:
        logging.error(f"failed to get url {url}")
        return
    result = r.json()
    crawl_url = result["cdn_root"] + result["url"]
    return crawl_url


def extract_card_color(item):
    colors = ["blue", "red", "black", "green"]
    for color in colors:
        if f"is_{color}" in item:
            return color
    return None


def crawl():
    url = get_crawl_url("01")    
    print(url)
    r = retry_session().get(url)
    if r.status_code != requests.codes.ok:
        logging.error(f"failed to get url {url}")
        return
    
    result = r.json()
    card_list = result["card_set"]["card_list"]
    cards = []
    for item in card_list:
        card = Card(card_id=item.get("card_id"),
                card_type=item.get("card_type"),
                card_name=item.get("card_name", {}).get("schinese"),
                rarity=item.get("rarity"),
                color=extract_card_color(item),
                item_def=item.get("item_def"),
                price=None
                )
        cards.append(card)
    return cards


def run():
    cards = crawl()
    logging.info(f"crawl cards successfully, count={len(cards)}")
    db.save_cards(cards)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
            format="[%(levelname)s] [%(asctime)s] [%(module)s] %(message)s")
    run()
