from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

# from flask_migrate import Migrate
from .config import SECRET_KEY
from .controllers import AddForm, RemoveForm, save_new_coin
# from .models import Cryptos

# instance flask
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
    return render_template("home.html", title="Crypto Tracker")

@app.route("/ajouter", methods=["GET","POST"])	
def add_crypto():
    name = None
    quantity = None
    cost = None
    form = AddForm()

    # Quan sigui un POST gestiona el save
    if request.method == "POST":
        result = engine.execute("SELECT * FROM cryptos")
        print(result.fetchall())

        # TODO: validate Form
        print("POST", form.name, form.quantity, form.cost)
        print (form.validate())
        save_new_coin(form.name, form.quantity, form.cost)
        
        # if form.validate():
        #     print("POST")
        #     crypto = Cryptos.query.filter_by(name=form.name.data).first()
        #     crypto = Cryptos(name=form.name.data, quantity=form.quantity.data, cost=form.cost.data)
        #     db.session.add(crypto)
        #     db.session.commit()
        
    name = form.name.data
    form.name.data = ""
    form.quantity.data = ""
    form.cost.data = ""
    flash("Crypto added successfully!")

    # my_cryptos = Cryptos.query.order_by(Cryptos.date_added)

    return render_template("add.html", title="Ajouter", form = form, 
    name=name, 
    quantity=quantity, 
    cost=cost
    #, my_cryptos=my_cryptos
    )

@app.route("/supprimer")	
def remove_crypto():
    return render_template("remove.html", title="Supprimer")

@app.route("/solde")	
def graph():
    return render_template("graph.html", title="Solde")

if __name__ == "__main__":
    app.run(debug=True)