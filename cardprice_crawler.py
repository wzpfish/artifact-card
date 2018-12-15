# coding: utf-8
import logging
import requests

from finance import get_usd_cny_rate
import db
from util import retry_session

url_schema = "https://steamcommunity.com/market/search/render/?\
query=&start={}&count={}&search_descriptions=0&sort_column=popular\
&sort_dir=desc&appid=583950&norender=1"

usd_cny_rate = get_usd_cny_rate()

def crawl(start, pagesize):
    url = url_schema.format(start, pagesize)

    r = retry_session().get(url)
    if r.status_code != requests.codes.ok:
        logging.error(f"failed to get result for start={start} pagesize={pagesize}")
        return
    
    cards = []
    result = r.json()
    total_count = result["total_count"]

    for item in result["results"]:
        usd_price = item["sell_price"]
        cny_price = usd_price / 100 * usd_cny_rate
        cny_price = round(cny_price, 2)
        item_def = int(item["hash_name"])

        card = db.get_card(item_def)
        if card:
            card.price = cny_price
            cards.append(card)
    return total_count, cards


def run():
    start = 0
    pagesize = 50
    total_count = 1
    while start < total_count:
        total_count, cards = crawl(start, pagesize)
        logging.info(f"crawl start={start}, pagesize={pagesize} successfully.")
        db.save_cards(cards)
        start += pagesize
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
            format="[%(levelname)s] [%(asctime)s] [%(module)s] %(message)s")
    run()
