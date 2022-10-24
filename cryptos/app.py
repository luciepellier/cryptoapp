from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import os

# from flask_migrate import Migrate
from .config import SECRET_KEY
from .controllers import AddForm, RemoveForm, save_coin, edit_coin, get_coin_change 

# data visualization
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64

# instance flask
# app = Flask(__name__, instance_path="/Users/luciepellier/Documents/Projects/CryptoApp")
app = Flask(__name__)

# Add database
# Review if CRYPTOS_DATABASE_URI is setted, or fallback to default DB
DATABASE_URI = os.getenv("CRYPTOS_DATABASE_URI", "sqlite:///active_cryptos.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

# secret key CSRF
app.config['SECRET_KEY'] = SECRET_KEY

# Init DB
engine = create_engine(DATABASE_URI)
metadata = MetaData(bind=engine)
db = SQLAlchemy(app)
session = sessionmaker(bind=engine)

with app.app_context():
    db.create_all()
    # Validate available tables
    #print("Current tables", engine.table_names())

@app.route("/", methods=["GET"])	
def homepage():
    result = engine.execute("SELECT SUM (quantity * cost) FROM cryptos")
    for i in result:
        profit = "%.2f" % round((sum(i)), 2)
        btc = "%.2f" % round(get_coin_change("BTC"), 2)
        eth = "%.2f" % round(get_coin_change("ETH"), 2)
        xrp = "%.2f" % round(get_coin_change("XRP"), 2)
    return render_template("home.html", title="Crypto Tracker", profit=profit, 
    btc=btc, eth=eth, xrp=xrp)

@app.route("/ajouter", methods=["GET","POST"])	
def add_crypto():
    message = ""
    form = AddForm()
    # when POST manage save in DB
    if request.method == "POST":
        try:
            assert form.quantity.data > 0, "La quantité doit être supérieure à zéro"
            assert form.cost.data > 0, "Le prix doit être supérieur à zéro"
            # result = engine.execute("SELECT * FROM cryptos")
            # print(form.validate())
            # print(result.fetchall())
            # print("POST", form.name, form.quantity, form.cost)
            save_coin(form.name, form.quantity, form.cost)
            message = f"Votre crypto {form.name.data} a été ajoutée !"   
        except Exception as e:
            message = f"Réviser l'erreur suivante: '{e}'"

        form.name.data = ""
        form.quantity.data = ""
        form.cost.data = ""
    return render_template("add.html", form = form, message = message)

@app.route("/supprimer", methods=["GET","POST"])	
def remove_crypto():
    message = ""
    form = RemoveForm()
    # when POST manage save in DB
    if request.method == "POST":
        try:
            assert form.quantity.data > 0, "La quantité doit être supérieure à zéro"
            assert form.cost.data > 0, "Le prix doit être supérieur à zéro"
            #result = engine.execute("SELECT * FROM cryptos")
            #print(result.fetchall())
            #print("POST", form.name, form.quantity, form.cost)
            #print (form.validate())
            edit_coin(form.name, form.quantity, form.cost)
            message = f"Votre crypto {form.name.data} a été retirée !"
        except Exception as e:
            message = f"Réviser l'erreur suivante: '{e}'"

        form.name.data = ""
        form.quantity.data = ""
        form.cost.data = ""
    return render_template("remove.html", form=form, message=message)

@app.route("/solde", methods=["GET"])	
def profit_chart():
    conn = engine.connect()
    # Create Dataframe Pandas
    historic = pd.read_sql_query("SELECT DATE(date_added) as Date, quantity, cost, (quantity * cost) as Total_Investissements_Jour FROM cryptos", conn)
    historic_df = pd.DataFrame(historic)
    # Group dates per day and cumsum 
    totals_per_day = historic_df.groupby(['Date']).sum().cumsum()
    # Save and display the Pandas Plot
    buff = BytesIO()
    figure = totals_per_day[["Total_Investissements_Jour"]].plot(kind="bar").get_figure()
    plt.xlabel("Date")
    plt.ylabel("Solde Total en €")
    plt.style.use("dark_background")
    plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})
    figure.savefig(buff, format="png", transparent=True)
    data = base64.b64encode(buff.getbuffer()).decode("ascii")
    figure_base64 = f'data:image/png;base64,{data}'

    return render_template("graph.html", figure=figure_base64)

if __name__ == "__main__":
    app.run(debug=True)


