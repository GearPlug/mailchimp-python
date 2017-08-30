
class Prueba:

    def __init__(self,token):
        self._token=token

    def __call__(self,r):
        print("calable")

    def hola(self):
        print("hola")

p=Prueba("12")
print(p.hola())
print(p._token)
print(p("m"))