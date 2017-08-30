from client import Client

user = "gearplug"
apikey = "edc91fe2b71a58a4e057e90abcdbf226-us16"
access_token="568cf681e9fce8af17b08553573a3ec8"

if __name__ == '__main__':
    client=Client(access_token=access_token)
    print("token")
    print(client.access_token)




