import requests

url = "http://api.tcgplayer.com/catalog/categories"

response = requests.request("GET", url)

print(response.text)
