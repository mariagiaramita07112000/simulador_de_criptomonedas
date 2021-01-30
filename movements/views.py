from movements import app
from flask import render_template, request , redirect, url_for
from movements.forms import MovementForm
import csv 
import sqlite3
from datetime import datetime , date
import coinmarketcapapi
import requests

@app.route("/")
def listaIngresos():
    form= MovementForm()
    conn= sqlite3.connect("movements/data/basededatos.db")
    c= conn.cursor()

    c.execute("SELECT date, time , from_currency, from_quantity, to_currency, to_quantity, PU FROM movimientos;") or []
    ingresos= c.fetchall()

    conn.close()

    '''# llamo a mi fichero csv 
    fIngresos= open("movements/data/basededatos.csv ", "r")
    # leo linea a linea mi fichero 
    csvReader= csv.reader(fIngresos, delimiter="," , quotechar='"')
    ingresos= list(csvReader) '''
    return render_template("movements.html", datos=ingresos , form=form)  

@app.route('/compra.html', methods=['GET','POST'])
def compraNueva():
    form= MovementForm(csrf_enabled=False)
    to_quantity = 0
    PU = 0
    print(form.validate_on_submit())
    
    if request.method== 'POST' and form.validate_on_submit():

        today= date.today()
        today_2= "{}/{}/{}".format(today.day, today.month , today.year)
        now = datetime.now()
        time= "{}:{}:{}".format(now.hour, now.minute, now.second)
        
        amount= request.form.get("from_quantity")
        symbol= request.form.get("from_currency")
        convert= request.form.get("to_currency")

        apikey= '8cf2c866-52c9-47d1-a4f9-d06a347da773'
        url_api="https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
        respuesta= requests.get(url_api.format(amount, symbol , convert, apikey))
        if respuesta.status_code == 200:
            datos= respuesta.json()
            cantidad_2= datos['data'] ['quote'] [convert] ['price']
            to_quantity = cantidad_2
            PU = (float(cantidad_2) / float(amount))
        else:
            print(respuesta.json()['status'])

        if request.form.get('submit2') is not None:
            fIngresos= open("movements/data/basededatos.csv" , "w+" , newline="")
            csvWriter = csv.writer(fIngresos, delimiter="," , quotechar='"')
            csvWriter.writerow([request.form.get("Fecha") , request.form.get("Hora"), request.form.get("convert_From"), request.form.get("Q"), request.form.get("convert_To"), request.form.get("Q2"), request.form.get("PU")])
            conn= sqlite3.connect('movements/data/basededatos.db')
            c= conn.cursor()

            c.execute('INSERT INTO movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity, "PU") VALUES (?,?,?,?,?,?,?);', 
            (
                today_2,
                time,
                request.form.get('from_currency'),
                float(request.form.get('from_quantity')),
                request.form.get('to_currency'),
                float(request.form.get('to_quantity')),
                float(request.form.get("PU"))

            ))
    
            conn.commit()
            conn.close()
            return redirect(url_for("listaIngresos"))

    return render_template("compra.html", form=form, PU=PU, to_quantity=to_quantity)




@app.route("/status.html", methods=["GET"])
def status():
    ingresos=0

    form= MovementForm()
    conn= sqlite3.connect("movements/data/basededatos.db")
    c= conn.cursor()


    c.execute('SELECT SUM(from_quantity) AS total , from_currency FROM movimientos WHERE from_currency="EUR"')
    from_eur_quantity= c.fetchone()[0]

    c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos GROUP BY to_currency;")
    to_currencies= c.fetchall()

    c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos GROUP BY from_currency")  
    from_currencies= c.fetchall()

    result_currencies = []

    for to_currency in to_currencies:
        result_currency = []
        is_coincidence = False
        print(to_currency[0])
        for from_currency in from_currencies:
            if to_currency[1] == from_currency[1]:
                is_coincidence = True
                result_currency.append(to_currency[0] - from_currency[0])
                result_currency.append(to_currency[1])
                result_currencies.append(result_currency)
        if is_coincidence == False: 
            result_currency.append(to_currency[0])
            result_currency.append(to_currency[1])
            result_currencies.append(result_currency)
            

    print(result_currencies)


    conn.close()
    suma = 0

    for result_currency in result_currencies:
        apikey= '8cf2c866-52c9-47d1-a4f9-d06a347da773'
        url_api="https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
        respuesta= requests.get(url_api.format(result_currency[0], result_currency[1] ,"EUR", apikey))
        if respuesta.status_code == 200:
            datos= respuesta.json()
            suma += float(datos['data']['quote']['EUR']['price'])
            print(datos['data'] ['quote'] ['EUR'] ['price'])
    print(suma)


    return render_template("status.html" , valor_invertido= from_eur_quantity, valor_actual=suma)




