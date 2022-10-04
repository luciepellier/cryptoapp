from flask import Flask, render_template
crypto_app = Flask(__name__)
message = "Contrôle tes gains et transactions depuis ta CryptoApp"

cryptocurrencies_list = [
    {"cryptocurrency": "Bitcoin", "value": 0.123},
    {"cryptocurrency": "Ethereum", "value": 1.879},
    {"cryptocurrency": "Ripple", "value": 1.234}
]

@crypto_app.route('/')	
def home():
    return render_template('home.html', title="CryptoApp", message=message, hello=True, cryptocurrencies = cryptocurrencies_list)

@crypto_app.route('/ajouter')	
def add():
    return render_template('add.html', title="Ajouter", message=message)

@crypto_app.route('/supprimer')	
def remove():
    return render_template('remove.html', title="Supprimer", message=message)

@crypto_app.route('/solde')	
def graph():
    return render_template('graph.html', title="Solde", message=message)

if __name__ == "__main__":
    crypto_app.run(debug=True)