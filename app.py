from flask import Flask, render_template
# from flask_migrate import Migrate
from .config import SECRET_KEY
from .controllers.controllers import AddCrypto

# instance flask
app = Flask(__name__)

# Add database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite3:///active_cryptos.db"

# secret key CSRF
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")	
def homepage():
    return render_template("home.html", title="Crypto Tracker")

@app.route("/ajouter", methods=["GET","POST"])	
def name():
    name = None
    form = AddCrypto()
    # validate form with the first data entry
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("add.html", title="Ajouter", name = name, form = form)

@app.route("/supprimer")	
def remove():
    return render_template("remove.html", title="Supprimer")

@app.route("/solde")	
def graph():
    return render_template("graph.html", title="Solde")

if __name__ == "__main__":
    app.run(debug=True)