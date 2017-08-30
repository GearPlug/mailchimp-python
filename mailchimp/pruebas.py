usuario="gearplug"
api_key="edc91fe2b71a58a4e057e90abcdbf226-us16"

client_id="716279204376"
client_secret="6f6dc2ffaf5f309c1929654dd4cb74b32187baf98a099d8328"
import requests
from requests.auth import HTTPBasicAuth
import webbrowser

authorize_uri="https://login.mailchimp.com/oauth2/authorize?client_id=716279204376&redirect_uri=http://127.0.0.1:8000&response_type=code"
#r=requests.post(authorize_uri)
#m=webbrowser.open(authorize_uri)
access_token_uri="https://login.mailchimp.com/oauth2/token"
encode_url="http://127.0.0.1:8000"
code="dc78635cbfe12fa2d65910c72c2b6cef"
data={"grant_type":"authorization_code", "client_id":client_id,"client_secret":client_secret, "redirect_uri":encode_url,"code":code}
r=requests.post(access_token_uri,data)
print(r.text)
token="568cf681e9fce8af17b08553573a3ec8"

# r = requests.get(url, auth=self.auth)
class Client(object):
#     def __init__(self, mc_client):
    def __init__(self, user=None, secret=None, access_token=None):

        if access_token:
            pass
        elif user and secret:
            self.auth = HTTPBasicAuth(user, secret)
            pass
        else:
            print("error")

    def _get(self):
        pass
    def _post(self):
        pass


class MailchimpOAuth(requests.auth.AuthBase):

    def __init__(self, access_token):
        self._access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'OAuth ' + self._access_token
        return r

    def get_metadata(self):
        try:
            r = requests.get('https://login.mailchimp.com/oauth2/metadata', auth=self)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            return r.json()

    def get_base_url(self):
        return self.get_metadata()['api_endpoint']