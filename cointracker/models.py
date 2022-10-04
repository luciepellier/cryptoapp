from orm import Model

class Crypto(Model):
    name = str
    quantity = float
    value = float