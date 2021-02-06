
Bienvenidos a MY CRYPTO !
MY CRYPTO  es una aplicacion en la que podras consultar el cambio de 12 tipos de criptomonedas las cuales son: ["EUR","EOS","XRP", "BCH", "ADA", "ETH","XLM","BTN", "USDT","LTC","BNB","TRX","BSV"] , en la pagina de inicio tendras una lista de todos los movimientos realizados;  al pulsar el boton + te enviara a la pagina de compra donde podras registrar un nuevo movimiento  pulsando FROM para escoger la moneda de la cual quieres cambiar , donde Q sera la cantidad que deseas cambiar, TO la moneda que deseas comprar con la cantidad de monedas FROM , siendo asi PU el precio unitario , luego tendras una pagina de estatus donde valor invertido sera la cantidad total de euros invertidos y valor actual sera (total de euros invertidos + saldo de euros invertidos + valor de euros de nuestras cryptos )



PASOS A SEGUIR PARA USAR LA APLICACION:

# instalacion

paso 1:

Tendras tambien que crear tu entorno virtual (venv)

paso 2 : 

para instalar las dependencias ejecutar
```
pip install -r requirements.txt

´´´
paso 3 :

Deberas crearte tu propia apikey en coinmarketcap  e introducirla en el fichero config_template.py de la siguiente manera:
apikey:"aqui dentro tu api"

https://coinmarketcap.com/api/

paso 4: 
deberas crearte tu propia base de datos en sqlite le pondras por nombre basededatos.db crearas la tabla con los datos indicados en la carpeta migrations , fichero intial.sql en CREATE TABLE donde estan registradas las sentencias que debes tener en tu tabla. 

para eso debes :
desde el directorio data desde el directorio /data ejecutar
sqlite3 <nombre_bd>.db
Desde la consola de sqlite3 
ejecutar
.read migrations/initial.sql
Comprobar que se han creado las tablas
.tables
Salir
.q


deberas crearte un fichero llamado .env en el cual tendras los siguientes datos :
FLASK_APP=run.py
FLASK_ENV=development
