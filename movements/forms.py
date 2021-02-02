from movements import app
from flask_wtf import FlaskForm
from wtforms import IntegerField,DateField, TimeField,SelectField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import sqlite3
from flask import render_template

symbol_cripto=["EUR","EOS","XRP", "BCH", "ADA", "ETH","XLM","BTC", "USDT","LTC","BNB","TRX","BSV"]
messages=[]

def validate_currencies(form, field):
    if form.data['from_currency'] == form.data['to_currency']:
        raise ValidationError('Las monedas deben ser distintas')

def validate_quantity(form,field):
    try:
        conn= sqlite3.connect("movements/data/basededatos.db")
        c= conn.cursor()

    except Exception as e:
        print(f"no se ha podido conectar con la base de datos{str(e)}")
        messages.append("error al conectar la api")
        return render_template("errores.html", messages=messages)
    
    try:
        c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos WHERE to_currency='"+form.data['from_currency']+"' GROUP BY to_currency;")
        from_currency1=c.fetchone()
        if from_currency1 is not None:
            from_currency1= from_currency1[0]
        else:
            from_currency1=0
            print(from_currency1)
    except Exception as e:
        print(f"no se ha podido obtener el to_currency de esta moneda{str(e)}")
        messages.append("error al obtener el to de esta moneda")
        return render_template("errores.html", messages=messages)

    try:
        c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos WHERE from_currency='"+form.data['from_currency']+"' GROUP BY from_currency;")
        from_currency2=c.fetchone()
        if from_currency2 is not None:
            from_currency2=from_currency2[0]
        else:
            from_currency2=0
    except Exception as e:
        print(f"no se ha podido obtener el from_currency de la moneda {str(e)}")
        messages.append("no se ha podido obtener el from de esta moneda ")
        return render_template("errores.html", messages=messages)
    
    try:
        result=float(from_currency1) - float(from_currency2)
    except Exception as e: 
        print(f"hay datos erroneos y no se ha podido realizar la operacion {str(e)}")
        messages.append("se han introducido datos erroneos y no se ha podido realizar la operacion , por favor revise los datos antes de continuar")
        return render_template("errores.html", messages=messages)

    print(result)
    print(form.data["from_quantity"])
    if float(form.data['from_quantity']) > result and form.data['from_currency'] != 'EUR':
        print(form.data['from_quantity'])
        raise ValidationError('no tienes suficiente saldo')



class MovementForm(FlaskForm):

    id= IntegerField("id")
    date=  DateField("date")
    time= TimeField("time")
    from_currency= SelectField("From" , validators=[DataRequired('seleccciona la moneda'), validate_currencies], choices=[])
    from_quantity=  FloatField("Q" , validators=[DataRequired("solo numeros y las comas deben ser respresentadas con puntos"), validate_quantity])
    to_currency= SelectField("To", validators=[DataRequired('selecciona una opcion'), validate_currencies], choices=symbol_cripto)
    to_quantity= FloatField("Q2" )
    PU= FloatField("PU")
    submit= SubmitField("Aceptar")
    submit2= SubmitField("OK")
    
