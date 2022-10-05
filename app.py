from flask import Flask, render_template
from models import models

crypto_app = Flask(__name__)

# cryptocurrencies_list = [
#     {"cryptocurrency": "Bitcoin", "value": 0.123},
#     {"cryptocurrency": "Ethereum", "value": 1.879},
#     {"cryptocurrency": "Ripple", "value": 1.234}
# ]

cryptos = models.Cryptos 

@crypto_app.route("/")	
def homepage():
    return render_template("home.html", title="CryptoApp")

@crypto_app.route("/ajouter")	
def add():
    return render_template("add.html", title="Ajouter", cryptos = cryptos)

@crypto_app.route("/supprimer")	
def remove():
    return render_template("remove.html", title="Supprimer", cryptos = cryptos)

@crypto_app.route("/solde")	
def graph():
    return render_template("graph.html", title="Solde")

if __name__ == "__main__":
    crypto_app.run(debug=True)