# coding: utf-8
import requests
from config import NOWAPI_APP_KEY, NOWAPI_SIGN

url_schema = "http://api.k780.com/?app=finance.rate&scur=USD&tcur=CNY&appkey={}&sign={}&format=json"

def get_usd_cny_rate():
    url = url_schema.format(NOWAPI_APP_KEY, NOWAPI_SIGN) 
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        result = r.json()
        if "result" in result and "rate" in result["result"]:
            return float(result["result"]["rate"])
    return 6.9
