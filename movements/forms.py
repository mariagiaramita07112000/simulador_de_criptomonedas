from flask_wtf import FlaskForm
from wtforms import IntegerField,DateField, TimeField,SelectField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import sqlite3

to_currencies=[]
from_currencies=[]


conn= sqlite3.connect("movements/data/basededatos.db")
c= conn.cursor()

c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos GROUP BY to_currency;")
to_currencies= c.fetchall()
c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos GROUP BY from_currency")  
from_currencies= c.fetchall()

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

symbol_cripto=["EUR","EOS","XRP", "BCH", "ADA", "ETH","XLM","BTC", "USDT","LTC","BNB","TRX","BSV"]

def validate_currencies(form, field):
    if form.data['from_currency'] == form.data['to_currency']:
        raise ValidationError('Las monedas deben ser distintas')

def validate_quantity(form,field):
    
    conn= sqlite3.connect("movements/data/basededatos.db")
    c= conn.cursor()

    c.execute("SELECT SUM(to_quantity) AS total, to_currency FROM movimientos WHERE to_currency='"+form.data['from_currency']+"' GROUP BY to_currency;")
    from_currency1=c.fetchone()[0]
    print(from_currency1)
    c.execute("SELECT SUM(from_quantity) AS total, from_currency FROM movimientos WHERE from_currency='"+form.data['from_currency']+"' GROUP BY from_currency;")
    from_currency2=c.fetchone()[0]

    result=float(from_currency1) - float(from_currency2)
    print(result)
    print(form.data["from_quantity"])
    if float(form.data['from_quantity']) > result:
        print(form.data['from_quantity'])
        raise ValidationError('no tienes suficiente saldo')

class MovementForm(FlaskForm):

    id= IntegerField("id")
    date=  DateField("date")
    time= TimeField("time")
    from_currency= SelectField("From" , validators=[DataRequired('seleccciona la moneda'), validate_currencies], choices=result_currencies)
    from_quantity=  FloatField("Q" , validators=[DataRequired("solo numeros"), validate_quantity])
    to_currency= SelectField("To", validators=[DataRequired('selecciona una opcion'), validate_currencies], choices=symbol_cripto)
    to_quantity= FloatField("Q2")
    PU= FloatField("PU")
    submit= SubmitField("Aceptar")
    submit2= SubmitField("OK")
    
