from .tcgplayer_exception import TCGplayerException
import requests

url = "https://api.tcgplayer.com"
token_path = "/token"
version_path = "/v1.17.0/"

class TCGplayerClient(object):
    """
    Yugioh Category details:
    {
    'categoryId': 2,
    'name': 'YuGiOh', 
    'modifiedOn': '2018-11-02T17:42:59.407', 
    'displayName': 'YuGiOh', 
    'seoCategoryName': 'YuGiOh', 
    'sealedLabel': 'Sealed Products', 
    'nonSealedLabel': 'Single Cards', 
    'conditionGuideUrl': 'https://store.tcgplayer.com/help/yugiohconditions', 
    'isScannable': True, 
    'popularity': 1058057
    }

    YuGiOh Search Manifest: see manifest.json
    """
    def __init__(self,public_key,private_key, bt=None):
        if bt:
            self.bearer_token = bt
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
            token_response = r.json()
            if r.status_code != requests.codes.ok:
                raise TCGplayerException(token_response)
            else:
                try:
                    self.bearer_token = token_response["access_token"]
                    print(self.bearer_token)
                    # two week tokens at time of writing
                    self.token_expires_date = token_response[".expires"]
                except KeyError:
                    raise TCGplayerException("Error: TCG has changed the keys for accessing a bearer token.")
        
        self.headers = {
            "Accept": "application/json",
            "Authorization": "bearer %s" % self.bearer_token
        }


    def _get(self, path, data=None):
        r = requests.get(url+version_path+path, data=data, headers=self.headers)
        if r.status_code != requests.codes.ok or not r.json()["success"]:
            raise TCGplayerException(r.json())
        else:
            return r.json()["results"]


    def _post(self, path, body=None):
        r = requests.post(url+version_path+path, json=body, headers=self.headers)
        if r.status_code != requests.codes.ok or not r.json()["success"]:
            raise TCGplayerException(r.json())
        else:
            return r.json()["results"]


    def get_categories(self):
        querystring = {
            "limit": 100,
            "sortOrder": "categoryId"
        }
        return self._get("/catalog/categories?limit=100&sortOrder=categoryId")

    def get_yugioh_category_details(self):
        # doesn't need to be a list for 1 item
        return self._get("/catalog/categories/2")[0]
    
    def get_yugioh_search_manifest(self):
        # doesn't need to be a list for 1 item
        return self._get("/catalog/categories/2/search/manifest")[0]

    def search(self):
        # returns a list of product ids that matched
        body = {
            "filters": [
                #{"name": "Number", "values": ["SDY-001"]}
                {"name": "ProductName", "values": ["Mystical ELf"]}
            ]
        }
        return self._post("/catalog/categories/2/search", body=body)
    
    def get_product_details(self, product_ids):
        comma_list = ",".join(map(str, product_ids))
        return self._get("/catalog/products/%s"%comma_list)

    def get_product_pricing(self, product_ids):
        comma_list = ",".join(map(str,product_ids))
        return self._get("/pricing/product/%s"%comma_list)

    def get_market_price_and_range_by_sku(self,sku):
        # returns a results list, but only ever returns one item
        data = self._get("/pricing/marketprices/%s"%sku)[0]
        return data["price"], data["lowestRange"], data["highestRange"]
