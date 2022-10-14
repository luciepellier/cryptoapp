from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

# from flask_migrate import Migrate
from .config import SECRET_KEY
from .controllers import AddForm, RemoveForm, save_coin, edit_coin
# from .models import Cryptos

# instance flask
# app = Flask(__name__, instance_path="/Users/luciepellier/Documents/Projects/CryptoApp")
app = Flask(__name__)

# Add database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///active_cryptos.db"

# secret key CSRF
app.config['SECRET_KEY'] = SECRET_KEY

# Init DB
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
metadata = MetaData(bind=engine)
db = SQLAlchemy(app)
session = sessionmaker(bind=engine)

with app.app_context():
    db.create_all()
    # Per validar les taules disponibles
    print("Current tables", engine.table_names())

@app.route("/")	
def homepage():
    # get Cryptos
    return render_template("home.html", title="Crypto Tracker")

@app.route("/ajouter", methods=["GET","POST"])	
def add_crypto():
    # name = None
    # quantity = None
    # cost = None
    message = ""
    form = AddForm()

    # Quan sigui un POST gestiona el save
    if request.method == "POST":
        result = engine.execute("SELECT * FROM cryptos")
        print(result.fetchall())

        # TODO: validate Form
        # assert form.quantity > 0, "asdasdasd"
        print("POST", form.name, form.quantity, form.cost)
        print (form.validate())
        save_coin(form.name, form.quantity, form.cost)
        message = f"Votre crypto {form.name.data} a été ajoutée !"
           
        form.name.data = ""
        form.quantity.data = ""
        form.cost.data = ""
        # return redirect(url_for('add_crypto'))

    return render_template("add.html", title="Ajouter", form = form, message=message)

@app.route("/supprimer", methods=["GET","POST"])	
def remove_crypto():
    message = ""
    form = RemoveForm()

    # Quan sigui un POST gestiona el save
    if request.method == "POST":
        result = engine.execute("SELECT * FROM cryptos")
        print(result.fetchall())

        # TODO: validate Form
        # assert form.quantity > 0, "asdasdasd"
        print("POST", form.name, form.quantity, form.cost)
        print (form.validate())
        edit_coin(form.name, form.quantity, form.cost)
        message = f"Votre crypto {form.name.data} a été retirée !"

        # if form.validate():
        #     print("POST")
        #     crypto = Cryptos.query.filter_by(name=form.name.data).first()
        #     crypto = Cryptos(name=form.name.data, quantity=form.quantity.data, cost=form.cost.data)
        #     db.session.add(crypto)
        #     db.session.commit()
           
        form.name.data = ""
        form.quantity.data = ""
        form.cost.data = ""
        # return redirect(url_for('remove_crypto'))

    return render_template("remove.html", title="Supprimer", form=form, message=message)

@app.route("/solde")	
def graph():
    return render_template("graph.html", title="Solde")

if __name__ == "__main__":
    app.run(debug=True)