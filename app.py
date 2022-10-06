from flask import Flask, render_template
# from flask_migrate import Migrate
from config import SECRET_KEY
from controllers.controllers import AddCrypto

# instance flask
crypto_app = Flask(__name__)

# Add database
crypto_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite3:///active_cryptos.db"

# secret key CSRF
crypto_app.config['SECRET_KEY'] = SECRET_KEY

@crypto_app.route("/")	
def homepage():
    return render_template("home.html", title="CryptoApp")

@crypto_app.route("/ajouter", methods=["GET","POST"])	
def name():
    name = None
    form = AddCrypto()
    # validate form with the first data entry
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("add.html", title="Ajouter", name = name, form = form)

@crypto_app.route("/supprimer")	
def remove():
    return render_template("remove.html", title="Supprimer")

@crypto_app.route("/solde")	
def graph():
    return render_template("graph.html", title="Solde")

if __name__ == "__main__":
    crypto_app.run(debug=True)