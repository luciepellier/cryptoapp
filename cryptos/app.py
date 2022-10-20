from sqlite3 import connect
import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

# from flask_migrate import Migrate
from .config import SECRET_KEY
from .controllers import AddForm, RemoveForm, save_coin, edit_coin, coin_id_dict, get_coin_name, get_coin_change 

# data visualization
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import base64

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

    # when POST manage save in DB and validate form with method validate()
    if request.method == "POST":
        result = engine.execute("SELECT * FROM cryptos")
        print(result.fetchall())
        print("POST", form.name, form.quantity, form.cost)
        print (form.validate())
        save_coin(form.name, form.quantity, form.cost)
        message = f"Votre crypto {form.name.data} a été ajoutée !"          
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
        result = engine.execute("SELECT * FROM cryptos")
        print(result.fetchall())
        print("POST", form.name, form.quantity, form.cost)
        print (form.validate())
        edit_coin(form.name, form.quantity, form.cost)
        message = f"Votre crypto {form.name.data} a été retirée !"
        form.name.data = ""
        form.quantity.data = ""
        form.cost.data = ""

    return render_template("remove.html", form=form, message=message)

@app.route("/solde", methods=["GET"])	
def profit_chart():
    conn = engine.connect()
    # Create Dataframe Pandas
    historic = pd.read_sql_query("SELECT DATE(date_added) as date, quantity, cost, (quantity * cost) as amount FROM cryptos", conn)
    historic_df = pd.DataFrame(historic)
    # Group dates per day and cumsum 
    totals_per_day = historic_df.groupby(['date']).sum().cumsum()
    # Save and display the plot
    buff = BytesIO()
    figure = totals_per_day[["amount"]].plot().get_figure()
    figure.savefig(buff, format="png", transparent=False)
    data = base64.b64encode(buff.getbuffer()).decode("ascii")
    figure_base64 = f'data:image/png;base64,{data}'

    return render_template("graph.html", figure=figure_base64)

if __name__ == "__main__":
    app.run(debug=True)


# @app.route("/supprimer", methods=["GET","DELETE"])	
# def remove_crypto():
#     message = ""
#     form = RemoveForm()
# 
#     if request.method == "DELETE":
#         result = engine.execute("SELECT * FROM cryptos")
#         print(result.fetchall())
#         print("DELETE", form.name, form.quantity)
#         print (form.validate())
#         delete_coin(form.name, form.quantity)
#         message = f"Votre crypto {form.name.data} a été supprimée !"
#         form.name.data = ""
#         form.quantity.data = ""
# 
#     return render_template("remove.html", form=form, message=message)
