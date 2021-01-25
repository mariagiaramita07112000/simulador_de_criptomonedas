from flask_wtf import FlaskForm
from wtforms import IntegerField,DateField, TimeField,SelectField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

symbol_cripto=["EUR","EOS","XRP", "BCH", "ADA", "ETH","XLM","BTN", "USDT","LTC","BNB","TRX","BSV"]

class MovementForm(FlaskForm):
    id= IntegerField("id")
    date=  DateField("date")
    time= TimeField("time")
    from_currency= SelectField("From" , validators=[DataRequired('seleccciona la moneda') ], choices=symbol_cripto)
    from_quantity=  FloatField("Q" , validators=[DataRequired("solo numeros")])
    to_currency= SelectField("To", validators=[DataRequired('selecciona una opcion') ], choices=symbol_cripto )
    to_quantity= FloatField("Q2", validators=[Length(max =8)])
    PU= FloatField("PU")
    submit= SubmitField("Aceptar")
    submit2= SubmitField("OK")
    
