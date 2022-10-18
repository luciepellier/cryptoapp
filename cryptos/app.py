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
    # Per validar les taules disponibles
    print("Current tables", engine.table_names())

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

    return render_template("add.html", title="Ajouter", form = form, message = message)

@app.route("/supprimer", methods=["GET","POST"])	
def remove_crypto():
    message = ""
    form = RemoveForm()

    # when POST manage save in DB
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


@app.route("/solde", methods=["GET"])	
def profit_chart():
    # Create Dataframe Pandas profit
    conn = engine.connect()

    historic = pd.read_sql_query("SELECT DATE(date_added) as date, quantity, cost, (quantity * cost) as amount FROM cryptos", conn)
    historic_df = pd.DataFrame(historic)

    totals_per_day = historic_df.groupby(['date']).sum().cumsum()

    buff = BytesIO()
    figure = totals_per_day[["amount"]].plot().get_figure()
    figure.savefig(buff, format="png", transparent=True)
    data = base64.b64encode(buff.getbuffer()).decode("ascii")
    figure_base64 = f'data:image/png;base64,{data}'

    return render_template("graph.html", title="Solde", figure=figure_base64)


    # for row in historic_df.iterrows():
    #     # print (row)
    #     print (row[2])
    #     # print (f"SELECT DATE(date_added) as date, SUM(quantity), SUM(cost), SUM((quantity * cost)) as amount FROM cryptos WHERE DATE(date_added) <= DATE({row['date']}) GROUP BY date")
    #     totals_per_day = pd.read_sql_query(f"SELECT DATE(date_added) as date, SUM(quantity), SUM(cost), SUM((quantity * cost)) as amount FROM cryptos WHERE DATE(date_added) <= DATE({row['date_added']}) GROUP BY date", conn)
    #     totals_df = pd.DataFrame(totals_per_day)
    #     print (totals_df)


    # x = [dt.datetime.strptime(d,'%Y-%m-%d %H:%M%S.%X').date() for d in dates]
    #y = pd.read_sql_query("SELECT (quantity * cost) FROM cryptos", conn)
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    #plt.plot(x,y)
    #plt.gcf().autofmt_xdate()
    # Generate the figure **without using pyplot**.

    # import pudb; pu.db    

if __name__ == "__main__":
    app.run(debug=True)