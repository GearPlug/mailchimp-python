import requests
from requests.auth import HTTPBasicAuth
from requests.auth import AuthBase

user = "gearplug"
apikey = "edc91fe2b71a58a4e057e90abcdbf226-us16"
#
# url = "https://{0}.api.mailchimp.com/3.0/lists/".format("us16")
# auth=HTTPBasicAuth(user, apikey)
#
# r = requests.get(url, params=auth)
# print(r.text)

token="OAuth 568cf681e9fce8af17b08553573a3ec8"

#headers = {'Authorization':token}

#response=requests.get('https://login.mailchimp.com/oauth2/metadata', headers=headers).json()

#print(response["api_endpoint"])

url='https://{0}.api.mailchimp.com/3.0/lists/'.format(apikey.split('-').pop())
r=AuthBase()
headers={'Authorization':token}
#headers={'user': user, 'apikey': apikey}
response=requests.get(url, params=headers)
print("listas")
print(response.json())
