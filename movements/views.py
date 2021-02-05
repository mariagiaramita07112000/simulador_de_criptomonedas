from movements import app
from flask import render_template, request , redirect, url_for
from movements.forms import MovementForm
from config import *
from config_template import *
import csv 
import sqlite3
from datetime import datetime , date
import coinmarketcapapi
import requests

messages=[]


def get_currencies():
    to_currencies=[]
    from_currencies=[]

    try:
        conn= sqlite3.connect("movements/data/basededatos.db")
        c= conn.cursor()

    except Exception as e:
        print(f"error al conectar con la base de datos {type(e).__name__} - {e} ")
        messages.append(" error al conectar con la base de datos")
        return render_template("errores.html", messages=messages)

    try:
        c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos GROUP BY to_currency;")
        to_currencies= c.fetchall()
        print(to_currencies)

    except Exception as e:
        print(f"error al obtener la suma de q {type(e).__name__} - {e} ")
        messages.append(" error al obtener la suma de to")
        return render_template("errores.html", messages=messages)

    try:
        c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos GROUP BY from_currency")  
        from_currencies= c.fetchall()

    except Exception as e:
        print(f"error al conectar con la base de datos {type(e).__name__} - {e} ")
        messages.append(" error al conectar con la base de datos")
        return  render_template("errores.html", messages=messages)

    try:
        result_currencies = []
        for to_currency in to_currencies:
            is_coincidence = False
            for from_currency in from_currencies:
                if to_currency[1] == from_currency[1]:
                    is_coincidence = True
                    if (to_currency[0] - from_currency[0]) > 0:
                        result_currencies.append(to_currency[1])
            if is_coincidence == False: 
                result_currencies.append(to_currency[1])

        result_currencies.append('EUR')

        conn.commit()
        conn.close()
        return result_currencies

    except Exception as e:
        print(f"error al añadir las currencies, verifique los datos {type(e).__name__} - {e} ")
        messages.append(" error al añadir los datos ")
        return  render_template("errores.html", messages=messages)


def connection():
    succes=True
    c=[]

    conn= sqlite3.connect("movements/data/basededatos.db")
    c=conn.cursor()

    return c

def make_query(query, params=[]):
    c=[]

    c=connection()
    c.execute(query, params)

    return c 

@app.route("/")
def listaIngresos():
    form= MovementForm()
    
    
    try:
        result = make_query("SELECT date, time , from_currency, from_quantity, to_currency, to_quantity, PU FROM movimientos;") or []
        print(result)
        ingresos= result.fetchall()
        result.close()
    except Exception as e:
        print(f"no ha podido realizar la consulta a la base de datos {type(e).__name__} - {e}")
        messages.append("lo siento, no se hemos podido conectar con la base de datos")
        return render_template("errores.html", datos=[] , form=form, messages=messages) 


    return render_template("movements.html", datos=ingresos , form=form, messages=messages)  

@app.route('/compra.html', methods=['GET','POST'])
def compraNueva():
    form= MovementForm(csrf_enabled=False)
    form.from_currency.choices = get_currencies()
    to_quantity = 0
    PU = 0
    
    
    print(form.validate_on_submit())
    
    if request.method== 'POST' and form.validate_on_submit():
        try:
            today= date.today()
            today_2= "{}/{}/{}".format(today.day, today.month , today.year)
            now = datetime.now()
            time= "{}:{}:{}".format(now.hour, now.minute, now.second)
        except Exception as e:
            print(f"no se ha podido obtener la fecha y la hora actual {type(e).__name__} - {e}")
            messages.append("se ha producido un error al obtener la hora y fecha")
            return render_template("errores.html", messages=messages)
        
        amount= request.form.get("from_quantity")
        symbol= request.form.get("from_currency")
        convert= request.form.get("to_currency")

        try:
            url_api="https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

            respuesta= requests.get(url_api.format(amount, symbol , convert, apikey))
            if respuesta.status_code == 200:
                datos= respuesta.json()
                cantidad_2= datos['data'] ['quote'] [convert] ['price']
                to_quantity = cantidad_2
                PU = (float(cantidad_2) / float(amount))
            elif respuesta.status_code == 401:
                print("apikey invalida")
                messages.append("No se ha podido enviar la solicitud a la api, debido a que ha introducido una apikey invalida")
                return render_template("errores.html", messages=messages)

            else:
                print("se ha producido un error  ", respuesta.status_code)
                messages.append("se ha producido un error en la consulta verifique por favor los datos")
                return render_template("errores.html", messages=messages)

        except Exception as e :
        
            print(f"no hemos podido conectar con la api{type(e).__name__} - {e} ")
            messages.append("No se ha podido enviar la solicitud a la api, por favor comuniquese con el administrador")
            return render_template("errores.html", messages=messages)

        try:
            if request.form.get('submit2') is not None:
                fIngresos= open("movements/data/basededatos.csv" , "w+" , newline="")
                csvWriter = csv.writer(fIngresos, delimiter="," , quotechar='"')
                csvWriter.writerow([request.form.get("Fecha") , request.form.get("Hora"), request.form.get("convert_From"), request.form.get("Q"), request.form.get("convert_To"), request.form.get("Q2"), request.form.get("PU")])
                conn= sqlite3.connect("movements/data/basededatos.db")
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
        except Exception as e:
            print(f"error en la base de datos {type(e).__name__} - {e} ")
            messages.append("error al conectar con la base de datos ")
            return render_template("errores.html", messages=messages)
    


    return render_template("compra.html", form=form, PU=PU, to_quantity=to_quantity)




@app.route("/status.html", methods=["GET"])
def status():
    form= MovementForm()
    ingresos=0
    try:
        
        conn= sqlite3.connect("movements/data/basededatos.db")
        c= conn.cursor()
    except Exception as e:
        print(f"error al conectar con la base de datos {type(e).__name__} - {e} ")
        messages.append(" error al conectar con la base de datos")
        return render_template("errores.html", messages=messages)

    try:
        c.execute('SELECT SUM(from_quantity) AS total , from_currency FROM movimientos WHERE from_currency="EUR"')
        from_eur_quantity= c.fetchone()[0]

    except Exception as e:
        print(f"error de consulta {type(e).__name__} - {e} ")
        messages.append(" no se ha podido obtener el valor en EUR, por favor verifique los datos")
        return render_template("errores.html", messages=messages)

    try:
        c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos GROUP BY to_currency;")
        to_currencies= c.fetchall()

    except Exception as e:
        print(f"error de consulta {type(e).__name__} - {e} ")
        messages.append(" no se ha podido obtener la suma total , por favor verifique los datos")
        return render_template("errores.html", messages=messages)

    try:
        c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos GROUP BY from_currency")  
        from_currencies= c.fetchall()
    
        result_currencies = []
    except Exception as e:
        print(f"error en la base de datos {type(e).__name__} - {e} ")
        messages.append("error al conectar con la base de datos, verifique los datos introducidos ")
        return render_template("errores.html", messages=messages)

    try:
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
    except Exception as e:
        print(f"error al obtener el resultado {type(e).__name__} - {e} ")
        messages.append("error al obtener el resultado ")
        return render_template("errores.html", messages=messages)


    print(result_currencies)
    conn.close()
    
    try:
        suma = 0

        for result_currency in result_currencies:
            url_api="https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
            respuesta= requests.get(url_api.format(result_currency[0], result_currency[1] ,"EUR", apikey))
            if respuesta.status_code == 200:
                datos= respuesta.json()
                suma += float(datos['data']['quote']['EUR']['price'])
                print(datos['data'] ['quote'] ['EUR'] ['price'])
        print(suma)

    except Exception as e:
        print(f"error de respuesta en la api {type(e).__name__} - {e} ")
        messages.append("se ha producido un error de respuesta en la api , por favor verifique los datos introducidos ")
        return render_template("errores.html", messages=messages)


    return render_template("status.html" , valor_invertido= from_eur_quantity, valor_actual=suma)




