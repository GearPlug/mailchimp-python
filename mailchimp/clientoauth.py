from requests.auth import AuthBase
import requests

token = "568cf681e9fce8af17b08553573a3ec8"


class ClientOauth(AuthBase):

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'OAuth ' + self.access_token
        return r

    def get_metadata(self):
        try:
            r = requests.get('https://login.mailchimp.com/oauth2/metadata', auth=self)
            return r.json()
        except requests.exceptions.RequestException as e:
            raise e

    def get_base_url(self):
        return self.get_metadata()['api_endpoint']

