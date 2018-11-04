import requests
import urllib

# https://yugiohprices.docs.apiary.io/#reference/checking-card-prices/check-price-for-cards-print-tag/check-price-for-card's-print-tag
# this api's data seems way off, probably can't use this even for rough estimates
url = "http://yugiohprices.com/api"
def get_prices_by_name(name):
    # TODO: how do we handle spaces? -> penguin%20soldier
    u = url + "/get_card_prices/%s" % urllib.parse.quote(name)
    print(u)
    r = requests.get(u)
    # returns a list of all card tags of this name
    return r

def get_data_by_tag(tag):
    u = url + "/price_for_print_tag/%s" % tag
    print(u)
    r = requests.get(u)
    return r


elf = get_data_by_tag("YS11-EN035")
print(elf.status_code)
print(elf.json())
elves = get_prices_by_name("Seven Tools of the Bandit")
print(elves.status_code)
print(elves.json())