import os
from datetime import datetime
import json
import requests

# ripped almost directly from yugioh-scanner project
class TCGplayerClient(object):

    def valid_token(self, expires_date):
        present = datetime.now()
        # Example: Sat, 12 Jan 2019 01:49:36 GMT
        date = expires_date.split(",")[1]
        #'  12 Jan 2019 01:49:36 GMT'
        ed = datetime.strptime(date," %d %b %Y %H:%M:%S %Z")
        return present < ed

    def __init__(self, public_key, private_key):
        self.url = "https://api.tcgplayer.com"
        self.token_path = "/token"
        self.version_path = "/v1.17.0/"
        # TODO: find a place to store bearer token in lambda: Dynamo?
        token_file = os.path.expanduser("~/.tcgplayer")
        have_bt = False

        try:
            with open(token_file) as f:
                # if it exists
                lines = f.read().splitlines()
                if len(lines) != 2:
                    # just pass
                    raise FileNotFoundError()
                expires_date = lines[0]
                token = lines[1]

                if self.valid_token(expires_date):
                    have_bt = True
                
        except FileNotFoundError:
            pass

        if have_bt:
            print("Using an existing bearer token")
            self.bearer_token = token
        else:
            self.public_key = public_key
            self.private_key = private_key
            # get bearer token
            token_data = {
                "grant_type": "client_credentials",
                "client_id": public_key,
                "client_secret": private_key
            }
            r = requests.get(url + token_path, data=token_data)
            if r.status_code != requests.codes.ok:
                raise ValueError("Token request failed, %d" %r.status_code)  
            else:
                token_response = r.json()
                try:
                    self.bearer_token = token_response["access_token"]
                    # two week tokens at time of writing
                    self.token_expires_date = token_response[".expires"]
                    # save the bearer token
                    lines = [self.token_expires_date, self.bearer_token]
                    with open(token_file, "w") as f:
                        f.seek(0)
                        for l in lines:
                            f.write(l + "\n")
                        f.truncate()
                except KeyError:
                    raise ValueError("Error: TCG has changed the keys for accessing a bearer token.")
        
        self.headers = {
            "Accept": "application/json",
            "Authorization": "bearer %s" % self.bearer_token
        }

    def _get(self, path, params=None):
        r = requests.get(self.url+self.version_path+path, params=params, headers=self.headers)
        if r.status_code != requests.codes.ok:
            print(r)
            raise ValueError("GET not ok, %d"%r.status_code)
        else:
            return r.json()["results"]

    def _post(self, path, body=None):
        r = requests.post(self.url+self.version_path+path, json=body, headers=self.headers)
        if r.status_code != requests.codes.ok:
            print(r)
            raise ValueError("POST not ok, %d"%r.status_code)
        else:
            return r.json()["results"]

    def search_by_number(self, query):
        # returns a list of product ids that matched
        body = {
            "filters": [
                {"name": "Number", "values": [query]}
            ]
        }
        return self._post("/catalog/categories/2/search", body=body)

    def get_product_details(self, product_ids):
        comma_list = ",".join(map(str, product_ids))
        return self._get("/catalog/products/%s"%comma_list)

    def get_product_pricing(self, product_ids):
        if not product_ids:
            return None
        comma_list = ",".join(map(str,product_ids))
        return self._get("/pricing/product/%s"%comma_list)


def main(event, context):
    try:
        number = event["queryStringParameters"]["number"]
    except KeyError:
        return {
            "statusCode": 404,
            "body": "Need 'number' parameter"
        }

    public_key = os.environ["public_key"]
    private_key = os.environ["private_key"]
    try:
        # TODO: we might run into timeouts
        client = TCGplayerClient(public_key, private_key)

        # search, get list of product ids
        results = client.search_by_number(number)
        if not results:
            return {
                "statusCode": 501,
                "body": "Failed getting search results"
            }
        
        names = {}
        # get details for the product ids
        details = client.get_product_details(results)
        prices = client.get_product_pricing(results)

        # cleanout empty prices
        prices = [x for x in prices if x["marketPrice"] is not None]

        # map the product id to the name
        for d in details:
            names[d["productId"]] = d["name"]

        # prices are by product id, add relevant details to the price object
        for p in prices:
            p["name"] = names[p["productId"]]
            p["cardNumber"] = number
            del p["directLowPrice"]

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET, OPTIONS",
            },
            "body": json.dumps(prices)
        }
    except Exception as e:
        print("Failed getting API client")
        print(e)
        return {
            "statusCode": 500
        }


if __name__ == "__main__":
    import sys
    event = {
        "queryStringParameters": {
            "number": sys.argv[1]
        }
    }
    print(main(event, ""))
