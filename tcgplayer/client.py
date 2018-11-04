from .tcgplayer_exception import TCGplayerException
import requests

url = "https://api.tcgplayer.com"
token_path = "/token"
version_path = "/v1.17.0/"
class TCGplayerClient(object):

    def __init__(self,public_key,private_key):
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
                # two week tokens at time of writing
                self.token_expires_date = token_response[".expires"]
            except KeyError:
                raise TCGplayerException("Error: TCG has changed the keys for accessing a bearer token.")
        
        self.headers = {
            "Accept": "application/json",
            "Authorization": "bearer %s" % self.bearer_token
        }


    def get_categories(self):
        r = requests.get(url + version_path + "/catalog/categories", headers=self.headers)
        print(r.status_code)
        print(r.json())